from dataclasses import dataclass
import uuid
import qrcode 

@dataclass
class Pix:
    def create_payment(self):
        bank_payment_id = str(uuid.uuid4())
        hash_payment = f'hash_payment_{str(uuid.uuid4())}'
        img = qrcode.make(hash_payment)
        img.save(f'src/app/static/img/qrcode/qr_code_payment_{bank_payment_id}.png') # type: ignore
        
        return {
            "bank_payment_id": bank_payment_id,
            "qr_code_path": f"qr_code_payment_{bank_payment_id}"
        }