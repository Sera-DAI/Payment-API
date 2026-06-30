import pytest
from app.models import Payment
from app.extensions import db
from datetime import datetime, timedelta

def test_socket_connection(socket_client):
    assert socket_client.is_connected() is True

def test_payment_confirmation_socket_emission(client, socket_client, app):
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

    assert socket_client.is_connected() is True
    socket_client.get_received()

    response = client.post('/payment/pix/confirmation', json={
        "bank_payment_id": "socket-test-bank-id",
        "value": 250.00
    })
    assert response.status_code == 200

    received_events = socket_client.get_received()
    event_names = [event['name'] for event in received_events]
    expected_event = f'payment-confirmed-{payment_id}'
    assert expected_event in event_names
