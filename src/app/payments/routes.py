from flask import jsonify
from app.payments.mold import payments_bp

@payments_bp.route('/pix', methods=['POST'])
def create_payment_pix():
    pass