from bankapp import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(40), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Integer)

    def __repr__(self):
        return f"UserModel(name='{self.name}', pin='{self.pin}', balance='{self.balance}', address='{self.address})"


# Add Accounts Model
# id, name, (later) balance, user_id
class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"AccountModel(account name='{self.account_name}')"



"""

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")
"""