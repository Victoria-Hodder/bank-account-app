from bankapp import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Integer)

    def __repr__(self):
        return f"UserModel(name='{self.name}', pin='{self.pin}', balance='{self.balance}', address='{self.address})"
