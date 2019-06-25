from bankapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    pin = db.Column(db.String(4), nullable=False) #nullable means there cannot be nothing
    balance = db.Column(db.Integer)

    def __repr__(self):
        return f"User(name='{self.name}', pin='{self.pin}', balance='{self.balance}')"