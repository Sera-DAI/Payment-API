from flask import jsonify, request
from app.payments.mold import payments_bp
from datetime import datetime, timedelta
from app.models import Payment
from app.extensions import db

@payments_bp.route('/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    
    if 'value' not in data: 
        return jsonify({
            "Message": "Invalid value"
        }), 400
        
    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
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