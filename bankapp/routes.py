from flask import request, jsonify, abort
from bankapp import app, db
from bankapp.models import User
from bankapp.schemas import UserSchema

@app.route('/')
def home_page():
    return 'This is a bank account app!'

# http://127.0.0.1:5000/balance?pin=5594&user_name=John%20Brown
@app.route('/balance')
def display_balance():
    pin_number = request.args.get('pin')
    user_name = request.args.get('user_name')
    searchedUser = User.query.filter_by(name=user_name).first()

    if searchedUser: 
        if pin_number == searchedUser.pin:
            return 'This is your current balance: {} EUR'.format(searchedUser.balance)
        else:
            return pin_error()
    else:
        return "User does not exist"


def pin_error():
    return 'Access denied: incorrect PIN.'


# http://127.0.0.1:5000/users/1/withdraw

@app.route('/users/<int:user_id>/withdraw', methods=['PATCH'])
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
                response = user_schema.dump(user).data
                return jsonify(response)       
            else:
                abort(
                    400,
                    description="You are not allowed to withdraw more money than you have on your account!",
                )
        else:
            abort(400, description="Pin is not correct")


@app.route('/users/<int:user_id>/deposit', methods=['PATCH'])
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
            response = user_schema.dump(user).data
            return jsonify(response)   
        else:
            abort(400, description="Pin is not correct")


@app.route('/users/<int:user_id>/transfer', methods=['PATCH'])
def transfer(user_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    receiver_id = data["receiverId"]
    if amount >= 3000:
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
                response = user_schema.dump(receiver).data
                return jsonify(response)
            else:
                abort(400, description='You dont have enought amount of money in your acount!')
        else:
            abort(400, description="Pin is not correct")

@app.route('/users', methods= ['GET'])
def get_users():
    user_schema = UserSchema(many=True)
    users = User.query.all()
    response = user_schema.dump(users).data
    return jsonify(response)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    new_name = data ['name']
    new_pin = int(data['pin'])
    new_balance = int(data['balance'])

    if not new_name and new_balance and new_pin:
        abort(400, description="Bad request!")
    else:
        # check user exists
        user = User.query.filter_by(name=new_name).first()
        if user:
            abort(400, description="Oops user already exists")
        else:
            new_user = User(name=new_name, pin=new_pin, balance=new_balance)
            db.session.add(new_user)
            db.session.commit()
            #we use Marshmallow library to serialize
            user_schema = UserSchema()
            response = user_schema.dump(new_user).data
            return jsonify(response)

@app.route('/users/<int:user_id>', methods=['GET']) #GET is default
def get_user(user_id):
    user = User.query.get_or_404(user_id, "You do not exist, please try again")
    user_schema = UserSchema()
    response = user_schema.dump(user).data
    return jsonify(response)

#update resource details
#PUT /users {'name' = 'James'}
@app.route('/users/<int:user_id>', methods= ['PUT'])
def update_user(user_id):
    data = request.get_json()
    new_name = data['name']
    new_pin = data['pin']
    new_balance = data['balance']
    user = User.query.get_or_404(user_id)
    user.name = new_name
    user.pin = new_pin
    user.balance = new_balance
    db.session.commit()
    user_schema = UserSchema()
    response = user_schema.dump(user).data
    return jsonify(response)


#delete resource which I selected
#DELETE /users/1
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id, "You do not exist, please try again")
    db.session.delete(user)
    db.session.commit()
    return '', 204
