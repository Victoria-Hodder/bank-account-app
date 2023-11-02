from bankapp import db
from bankapp.models.account_model import AccountModel


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    accounts = db.relationship('AccountModel', backref='user_account', lazy='dynamic')

    def __repr__(self):
        return f"UserModel(id={self.id},\n name='{self.name}',\n pin='{self.pin}',\n address='{self.address}),\n accounts={self.accounts}\n"

