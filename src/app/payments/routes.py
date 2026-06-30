from flask import jsonify, request, send_file, render_template, url_for
from app.payments.schemas import payments_bp
from datetime import datetime, timedelta
from app.models import Payment
from app.extensions import db
from app.strategies.pix import Pix

@payments_bp.route('/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    
    if 'value' not in data: 
        return jsonify({
            "Message": "Invalid value"
        }), 400
        
    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id'] 
    new_payment.qr_code = data_payment_pix['qr_code_path']
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({
        "Message": "The payment is been created",
        "Payment": new_payment
    })
@payments_bp.route('/pix/confirmation', methods=['POST'])
def pix_confirmation():
    data = request.get_json()
    
    # 1. Verify required payload fields
    if not data or 'bank_payment_id' not in data or 'value' not in data:
        return jsonify({
            "Message": "Invalid payload: 'bank_payment_id' and 'value' are required"
        }), 400
        
    bank_payment_id = data['bank_payment_id']
    value = float(data['value'])
    
    # 2. Retrieve payment by bank_payment_id
    payment = Payment.query.filter_by(bank_payment_id=bank_payment_id).first()
    
    if not payment:
        return jsonify({
            "Message": "Payment transaction not found"
        }), 404
        
    # 3. Validate that the payment amount matches the database
    if payment.value != value:
        return jsonify({
            "Message": "Payment value mismatch"
        }), 400
        
    # 4. Check if the payment has already been completed
    if payment.paid:
        return jsonify({
            "Message": "Payment has already been confirmed"
        }), 200
        
    # 5. Confirm the payment
    payment.paid = True
    db.session.commit()
    
    # 6. Notify the frontend in real time via Socket.IO
    from app.factory import socketio
    socketio.emit(f'payment_status_{payment.id}', {'status': 'confirmed'})
    
    return jsonify({
        "Message": "Payment confirmed successfully",
        "Payment": payment
    })

@payments_bp.route('/pix/qrcode/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/qrcode/{file_name}.png', mimetype='image/png', as_attachment=False)

@payments_bp.route('pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.filter_by(id=payment_id).first()
    payment_information = {
        "host": "http://127.0.0.1:5000", 
        "qrcode_url": url_for('payment.get_image', file_name=payment.qr_code), #type: ignore - fazer a rota caso não tenha valor
        "value": payment.value, #type: ignore - fazer a rota caso não tenha valor
        "payment_id": payment_id,
        "expiration_date": payment.expiration_date #type: ignore - fazer a rota caso não tenha valor
    }
    
    return render_template('payments/checkout.html', **payment_information)