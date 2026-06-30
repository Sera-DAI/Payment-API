import pytest
from app.models import Payment
from app.extensions import db
from datetime import datetime, timedelta

def test_socket_connection(socket_client):
    """Testa se o cliente de socket consegue estabelecer conexão com sucesso."""
    assert socket_client.is_connected() is True

def test_payment_confirmation_socket_emission(client, socket_client, app):
    """Testa se a confirmação via HTTP emite corretamente o sinal via SocketIO para o cliente."""
    # 1. Cria um pagamento pendente no banco em memória
    with app.app_context():
        payment = Payment(
            value=250.00,
            paid=False,
            bank_payment_id="socket-test-bank-id",
            qr_code="qr_socket_test",
            expiration_date=datetime.now() + timedelta(minutes=30)
        )
        db.session.add(payment)
        db.session.commit()
        payment_id = payment.id

    # 2. Garante que o cliente de testes do SocketIO está conectado
    assert socket_client.is_connected() is True
    
    # Limpa eventos recebidos anteriormente (ex: eventos de conexão)
    socket_client.get_received()

    # 3. Dispara a confirmação do pagamento via chamada HTTP POST
    response = client.post('/payment/pix/confirmation', json={
        "bank_payment_id": "socket-test-bank-id",
        "value": 250.00
    })
    assert response.status_code == 200

    # 4. Verifica se o Socket.IO transmitiu a notificação para o cliente
    received_events = socket_client.get_received()
    
    # Mapeia os nomes dos eventos recebidos
    event_names = [event['name'] for event in received_events]
    expected_event = f'payment-confirmed-{payment_id}'
    
    assert expected_event in event_names
