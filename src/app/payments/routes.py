from flask import jsonify, request, send_file, render_template, url_for
from app.payments.schemas import payments_bp
from datetime import datetime, timedelta
from app.models import Payment
from app.extensions import db
from app.strategies.pix import Pix
from app.factory import socketio

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
    
    if "bank_payment_id" not in data or "value" not in data:
        return jsonify({
            "Message": "Invalid payment data"
        }), 400
    
    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment:
        return jsonify({
            "Message": "paymeny not found."
        }), 404

    if data.get("value") != payment.value:
        return jsonify({
            "Message": "Invalid payment value"
        }), 400
        
    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')
    return jsonify({
        "Message": "Payment is been confirmed."
    })
@payments_bp.route('/pix/qrcode/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/qrcode/{file_name}.png', mimetype='image/png', as_attachment=False)

@payments_bp.route('pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.filter_by(id=payment_id).first()
    
    if payment.paid: #type:ignore
        payment_information = {
        "value": payment.value, #type: ignore
        "payment_id": payment_id,
        "bank_payment_id": payment.bank_payment_id #type: ignore
    }
        return render_template('payments/confirmed.html', **payment_information)
    payment_information = {
        "payment_id": payment_id,
        "host": "http://127.0.0.1:5000", 
        "qrcode_url": url_for('payment.get_image', file_name=payment.qr_code), #type: ignore
        "value": payment.value, #type: ignore 
        "expiration_date": payment.expiration_date #type: ignore 
    }
    
    return render_template('payments/checkout.html', **payment_information)

# @payments_bp.route('pix/confirmed/<int:payment_id>', methods=['GET'])
# def confirmed_pix_page(payment_id):
#     payment = Payment.query.filter_by(id=payment_id).first()
    
#     if not payment or payment.paid == False:
#         return jsonify({"Message": "Payment transaction not found"}), 404
        
#     payment_information = {
#         "value": payment.value,
#         "payment_id": payment_id,
#         "bank_payment_id": payment.bank_payment_id
#     }
    
#     return render_template('payments/confirmed.html', **payment_information)