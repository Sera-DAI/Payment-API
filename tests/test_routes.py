import json
from unittest.mock import patch
from app.models import Payment
from app.extensions import db
from datetime import datetime, timedelta

def test_create_payment_pix_success(client):
    """Testa a criação de um pagamento Pix com sucesso, simulando a geração do QR Code."""
    mock_response = {
        "bank_payment_id": "test-bank-payment-id",
        "qr_code_path": "qr_code_payment_test"
    }
    
    # Mock para evitar a criação física do arquivo QR Code no disco durante os testes
    with patch('app.strategies.pix.Pix.create_payment', return_value=mock_response):
        response = client.post('/payment/pix', json={"value": 150.00})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["Message"] == "The payment is been created"
        assert data["Payment"]["value"] == 150.00
        assert data["Payment"]["bank_payment_id"] == "test-bank-payment-id"
        assert data["Payment"]["qr_code"] == "qr_code_payment_test"

def test_pix_confirmation_success(client, app):
    """Testa a confirmação de um pagamento Pix com dados corretos."""
    # Insere um pagamento falso no banco em memória
    with app.app_context():
        payment = Payment(
            value=100.00,
            paid=False,
            bank_payment_id="test-bank-id",
            qr_code="qr_test",
            expiration_date=datetime.now() + timedelta(minutes=30)
        )
        db.session.add(payment)
        db.session.commit()
        payment_id = payment.id

    # Envia a requisição de confirmação simulando a chamada do banco
    response = client.post('/payment/pix/confirmation', json={
        "bank_payment_id": "test-bank-id",
        "value": 100.00
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["Message"] == "Payment is been confirmed."
    
    # Verifica se o status do pagamento no banco mudou para pago (paid = True)
    with app.app_context():
        p = db.session.get(Payment, payment_id)
        assert p.paid is True #type: ignore

def test_pix_confirmation_invalid_value(client, app):
    """Testa a confirmação enviando um valor incorreto para o ID do pagamento."""
    with app.app_context():
        payment = Payment(
            value=100.00,
            paid=False,
            bank_payment_id="test-bank-id",
            qr_code="qr_test",
            expiration_date=datetime.now() + timedelta(minutes=30)
        )
        db.session.add(payment)
        db.session.commit()

    # Envia confirmação com valor divergente (50.00 em vez de 100.00)
    response = client.post('/payment/pix/confirmation', json={
        "bank_payment_id": "test-bank-id",
        "value": 50.00
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert data["Message"] == "Invalid payment value"
