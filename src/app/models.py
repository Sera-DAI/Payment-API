from app.extensions import db, login_manager
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Payment(db.Model):
    __tablename__ = 'payments'
    id: int = db.Column(db.Integer, primary_key=True)
    value: float = db.Column(db.Float)
    paid: bool = db.Column(db.Boolean, default=False)
    bank_payment_id: str = db.Column(db.String(200), nullable=True)
    qr_code: str = db.Column(db.String(200), nullable=True)
    expiration_date: datetime = db.Column(db.DateTime)
    