from flask import request, jsonify

from bankapp.models import User
from bankapp import app, db

@app.route('/')
def home_page():
    return 'This is a bank account app!'

# http://127.0.0.1:5000/balance?pin=1234&user_name=John Brown
@app.route('/balance')
def display_balance():
    pin_number = request.args.get('pin') # instead of writing a pin as argument, we use this line of code. why?
    user_name = request.args.get('user_name') # instead of writing a pin as argument, we use this line of code. why?
    searchedUser = User.query.filter_by(name=user_name).first()

    if pin_number == searchedUser.pin:
        return 'This is your current balance: {} EUR'.format(searchedUser.balance)
    else:
        return pin_error()

def pin_error():
    return 'Access denied: incorrect PIN.'

# http://127.0.0.1:5000/withdraw?pin=1234&user=user1&amount=50
@app.route('/withdraw')
def withdraw_money():
    pin_number = request.args.get('pin') # instead of writing a pin as argument, we use this line of code. why?
    user_name = request.args.get('user') # instead of writing a pin as argument, we use this line of code. why?
    amount = request.args.get('amount') # instead of writing a pin as argument, we use this line of code. why?
    amount = int(amount) # why does this have to be transformed into integer?

    balance = users[user_name][1]
    if pin_number == users[user_name][0]:
        if amount <= balance:
            balance = balance - amount
            return 'Withdrew {} EUR. New balance is: {} EUR.'.format(amount, balance)
        else:
            return 'You are not allowed to withdraw more money than you have on your account!'
    else:
        return pin_error()


#    if current_user.is_authenticated:
 #       return redirect(url_for('home'))
  #  form = LoginForm()
   # if form.validate_on_submit():
    #    user = User.query.filter_by(email=form.email.data).first()        
        
        
#return jsonify(d) - where should I put this?
#return jsonify({'restaurants': restaurants})
#return jsonify({'users': user.name})