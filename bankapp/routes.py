from flask import request, jsonify

from bankapp.models import User
from bankapp import app, db

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


# http://127.0.0.1:5000/withdraw?pin=5594&user_name=John%20Brown&amount=50

@app.route('/withdraw')
def withdraw_money():
    pin_number = request.args.get('pin')
    user_name = request.args.get('user_name')
    amount = int(request.args.get('amount'))

    searchedUser = User.query.filter_by(name=user_name).first()    

    if searchedUser: 

        balance = searchedUser.balance 

        if pin_number == searchedUser.pin:
            
            if amount <= balance:
                searchedUser.balance -= amount
                db.session.commit()
                return 'Withdrew {} EUR. New balance is: {} EUR.'.format(amount, searchedUser.balance)        
            else:
                return 'You are not allowed to withdraw more money than you have on your account!'
        
            if amount <= 2000:
                balance -= amount
                db.session.commit()
                return 'Withdrew {} EUR. New balance is: {} EUR.'.format(amount, searchedUser.balance)
            else:
                return 'You are not allowed to go over 2000 euro daily limit'

        else:
            return pin_error()

    else: 
        return "User does not exist"


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