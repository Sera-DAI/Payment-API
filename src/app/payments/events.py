from app.factory import socketio 
from flask_socketio import disconnect

@socketio.on('connect')
def handle_connect():
    print("[SERVER]: Connection succeded")
    
@socketio.on('confirm_receipt_on_server')
def handle_confirm_receipt(data):
    payment_id = data.get('payment_id')
    status = data.get('status')
    print(f"[SERVER]: Client confirmed receipt of payment #{payment_id} with status: {status}")
    print("[SERVER]: Client desconnected")
    disconnect()