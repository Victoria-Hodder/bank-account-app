from flask import request, jsonify, abort
#from jsonschema import validate
from bankapp import app, db
from bankapp.models import User, Account
from bankapp.schemas import UserSchema, AccountSchema

user_request_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "pin": {"type": "number"}},
}
account_request_schema = {
    "type": "object",
    "properties": {"balance": {"type": "number"}, "ownerId": {"type": "number"}},
}

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


# http://127.0.0.1:5000/users/1/accounts/1/withdraw

@app.route("/users/<int:user_id>/accounts/<int:account_id>/withdraw", methods=["POST"])
def withdraw(user_id, account_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    if amount > 2000:
        abort(
            400, description="You are not allowed to go over 2000 euro daily limit"
        )
    else:
        user = User.query.get_or_404(user_id, "User does not exist")
        if pin_number == user.pin:
            account = Account.query.get_or_404(account_id, "Account does not exist")
            if amount <= account.balance:
                account.balance -= amount
                db.session.commit()
                account_schema = AccountSchema()
                response = account_schema.dump(account).data
                return jsonify(response)
            else:
                abort(
                    400,
                    description="You are not allowed to withdraw more money than you have on your account!",
                )
        else:
            abort(400, description="Pin is not correct")

# http://127.0.0.1:5000/deposit?pin=5594&user_name=John%20Brown&amount=50
@app.route('/deposit')
def display_deposit():
    pin_number = request.args.get('pin')
    user_name = request.args.get('user_name')
    amount = int(request.args.get('amount'))
    
    searchedUser = User.query.filter_by(name=user_name).first()

    if searchedUser:
        balance = searchedUser.balance 

        if pin_number == searchedUser.pin:
            if amount <= 3000:
                searchedUser.balance += amount
                db.session.commit()
                return 'Deposited {} EUR. New balance is: {} EUR.'.format(amount, searchedUser.balance)        
            else:
                return 'You can not deposit money more than the 3000 Euro daily limit'
        else:
            return pin_error()

    else:
        return 'User does not exist'


# http://127.0.0.1:5000/transfer?pin=3412&sender=Peppa%20Potts&receiver=John%20Brown&amount=50
@app.route('/transfer')
def display_transfer():
    pin_number = request.args.get('pin')
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    amount = int(request.args.get('amount'))
    
    searchedSender = User.query.filter_by(name=sender).first()
    searchedReceiver = User.query.filter_by(name=receiver).first()

    if searchedSender and searchedReceiver:
        senderBalance = searchedSender.balance 
        receiverBalance = searchedReceiver.balance

        if pin_number == searchedSender.pin:
            if amount <= 3000:
                searchedSender.balance -= amount
                searchedReceiver.balance += amount
                db.session.commit()
                return "Your transfer is complete!"
            else:
                return 'You can not transfer money more than the 3000 Euro daily limit'
        else:
            return pin_error()
    else:
        return 'Sender or Receiver does not exist'

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

#ddos attack