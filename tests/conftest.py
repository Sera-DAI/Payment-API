import os
import sys
import pytest

# Adiciona o diretório 'src' ao PATH do Python para permitir a importação do pacote 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app.factory import create_app, socketio
from app.extensions import db

@pytest.fixture
def app():
    """Configura o aplicativo Flask em modo de testes usando banco de dados SQLite em memória."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key'
    }
    
    # Inicializa o app com a configuração de testes
    app = create_app(test_config)
    
    # Cria o contexto do app e inicializa as tabelas no banco de dados SQLite
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Retorna um cliente HTTP de teste do Flask para testar endpoints REST."""
    return app.test_client()

@pytest.fixture
def socket_client(app):
    """Retorna um cliente de teste do Flask-SocketIO para testar eventos WebSocket."""
    return socketio.test_client(app)
