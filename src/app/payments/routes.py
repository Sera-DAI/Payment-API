from flask import jsonify, request
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

@payments_bp.route('/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return jsonify({
        "Message": "Test complete"
    })