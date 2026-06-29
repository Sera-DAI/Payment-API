from dotenv import load_dotenv
from app.factory import create_app, socketio

load_dotenv()
app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)