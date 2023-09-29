from flask import request, jsonify, abort
from bankapp import app, db
from bankapp.user import User
from bankapp.user_details import UserDetails
from bankapp.schemas import UserSchema


@app.route('/')
def home_page():
    return 'This is a bank account app!'


@app.route('/users', methods= ['GET'])
def get_users():
    return User().get_users()


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return User().get_user(user_id)


@app.route('/users', methods=['POST'])
def create_user():
    return User().create_user()


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return User().delete_user(user_id)


@app.route('/users/<int:user_id>/update_details', methods= ['PUT'])
def update_user_details(user_id):
    return UserDetails().update(user_id)


@app.route('/users/<int:user_id>/update_pin', methods= ['PUT'])
def update_user_pin(user_id):
    return UserDetails().update_pin(user_id)


# http://127.0.0.1:5000/users/1/withdraw
@app.route('/users/<int:user_id>/withdraw', methods=['PUT'])
def withdraw(user_id):
    data = request.get_json(force=True)
    amount = data['amount']
    pin = data['pin']
    if amount > 2000:
        abort(400, description='You are not allowed to go over 2000 euro daily limit') 
    else:
        user = User.query.get_or_404(user_id, "User does not exist")
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


# http://127.0.0.1:5000/users/1/deposit
@app.route('/users/<int:user_id>/deposit', methods=['PUT'])
def deposit(user_id):
    data = request.get_json(force=True)
    amount = data['amount']
    pin = data['pin']
    if amount >= 3000:
        abort(400, description='You are not allowed to go over 3000 euro daily limit') 
    else:
        user = User.query.get_or_404(user_id, "User does not exist")
        if pin == user.pin:
            user.balance += amount
            db.session.commit()
            user_schema = UserSchema()
            response = user_schema.dump(user)
            return jsonify(response)
        else:
            abort(400, description="Pin is not correct")


@app.route('/users/<int:user_id>/transfer', methods=['PUT'])
def transfer(user_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    receiver_id = data["receiverId"]
    if amount > 3000:
        abort(400, description='You are not allowed to go over 3000 euro daily limit') 
    else:
        sender = User.query.get_or_404(user_id, "Sender does not exist")
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



