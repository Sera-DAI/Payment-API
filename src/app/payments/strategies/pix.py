from dataclasses import dataclass

@dataclass
class Pix:
    def create_payment(self):
        return {
            "bank_payment_id": "",
            "qr_code_path": ""
        }