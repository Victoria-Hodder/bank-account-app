from bankapp import db
from .user import User
from flask import request, jsonify, abort


# TODO: Need to specify which account to interact with

class Transactions(User):
    
    def withdraw(self):
        data = request.get_json(force=True)
        amount = data['amount']
        pin = data['pin']
        if amount > 2000:
            abort(400, description='You are not allowed to go over 2000 euro daily limit') 
        else:
            user = User.query.get_or_404(self.user_id, "User does not exist")
            if pin == user.pin: 
                if amount <= user.balance:
                    user.balance -= amount
                    db.session.commit()
                    user_schema = UserSchema()
                    response = user_schema.dump(user)
                    return jsonify(response)       
                else:
                    abort(
                        400,
                        description="You are not allowed to withdraw more money than you have on your account!",
                    )
            else:
                abort(400, description="Pin is not correct")

    def deposit(self):
        data = request.get_json(force=True)
        amount = data['amount']
        pin = data['pin']
        if amount >= 3000:
            abort(400, description='You are not allowed to go over 3000 euro daily limit') 
        else:
            user = User.query.get_or_404(self.user_id, "User does not exist")
            if pin == user.pin:
                user.balance += amount
                db.session.commit()
                user_schema = UserSchema()
                response = user_schema.dump(user)
                return jsonify(response)
            else:
                abort(400, description="Pin is not correct")

    def transfer(self):
        data = request.get_json(force=True)
        amount = data["amount"]
        pin_number = data["pin"]
        receiver_id = data["receiverId"]
        if amount > 3000:
            abort(400, description='You are not allowed to go over 3000 euro daily limit') 
        else:
            sender = User.query.get_or_404(self.user_id, "Sender does not exist")
            if pin_number == sender.pin:
                if amount <= sender.balance:
                    receiver = User.query.get_or_404(receiver_id, "Receiver user does not exist")
                    sender.balance -= amount
                    receiver.balance += amount
                    db.session.commit()
                    user_schema = UserSchema()
                    response = user_schema.dump(receiver)
                    return jsonify(response)
                else:
                    abort(400, description='You dont have enought amount of money in your acount!')
            else:
                abort(400, description="Pin is not correct")



from bankapp.schemas import UserSchema
