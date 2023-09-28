from bankapp import db
from flask import jsonify

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    pin = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Integer)

    def __repr__(self):
        return f"User(name='{self.name}', pin='{self.pin}', balance='{self.balance}')"

    def get_users():
        user_schema = UserSchema(many=True)
        users = User.query.all()
        response = user_schema.dump(users)
        return jsonify(response)
    
    def get_user(user_id):
        user = User.query.get_or_404(user_id, "You do not exist, please try again")
        user_schema = UserSchema()
        response = user_schema.dump(user)
        return jsonify(response)


from bankapp.schemas import UserSchema
