import os
from flask import Flask, render_template
from werkzeug.local import LocalProxy
from app.extensions import db
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")
    
def create_app(config_override=None):
    app = Flask(__name__)
    
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('MYSQL_DATABASE')
    secret_key = os.getenv('SECRET_KEY')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key
    
    if config_override:
        app.config.update(config_override)
        
    db.init_app(app)
    socketio.init_app(app)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('payments/404.html'), 404
    
    from app.payments import events
    from app.payments.schemas import payments_bp
    app.register_blueprint(payments_bp)
    
    with app.app_context():
        from app import models
        db.create_all()
    
    return app