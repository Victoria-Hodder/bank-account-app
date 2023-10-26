from bankapp import db


# TODO: id, name, (later) balance, user_id
class AccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    def __repr__(self):
        return f"AccountModel(id={self.id},account name='{self.account_type},balance={self.balance}, user_id={self.user_id}')"
