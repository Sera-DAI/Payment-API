import os
from flask import Flask
from werkzeug.local import LocalProxy
from app.extensions import db, login_manager
    
def create_app():
    app = Flask(__name__)
    
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('MYSQL_DATABASE')
    secret_key = os.getenv('SECRET_KEY')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.payments.mold import payments_bp
    app.register_blueprint(payments_bp)
    
    with app.app_context():
        from app import models
        db.create_all()
    
    return app