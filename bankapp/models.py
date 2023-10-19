from bankapp import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Integer)
    # TODO: rename to account_id
    accounts = db.relationship('AccountModel', backref='user_account', lazy='dynamic')

    def __repr__(self):
        return f"UserModel(name='{self.name}', pin='{self.pin}', balance='{self.balance}', address='{self.address})"


# Add Accounts Model
# id, name, (later) balance, user_id
class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    def __repr__(self):
        return f"AccountModel(id={self.id},account name='{self.account_name},user_id={self.user_id}')"
