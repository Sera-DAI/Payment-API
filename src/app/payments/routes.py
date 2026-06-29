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
@payments_bp.route('/pix/confirmation', methods=['P OST'])
def pix_confirmation():
    return jsonify({
        "Message": "Payment has been created."
    })

@payments_bp.route('/pix/qrcode/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/qrcode/{file_name}.png', mimetype='image/png', as_attachment=False)

@payments_bp.route('pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.filter_by(id=payment_id).first()
    payment_information = {
        "qrcode_url": url_for('payment.get_image', file_name=payment.qr_code), #type: ignore - fazer a rota caso não tenha valor
        "value": payment.value, #type: ignore - fazer a rota caso não tenha valor
        "payment_id": payment_id,
        "expiration_date": payment.expiration_date #type: ignore - fazer a rota caso não tenha valor
    }
    
    return render_template('payments/checkout.html', **payment_information)