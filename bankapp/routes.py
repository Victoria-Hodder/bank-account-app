from bankapp import app
from .controllers.user import User
from .controllers.user_details import UserService
from .controllers.transactions import Transactions
from .controllers.accounts import Accounts


@app.route('/')
def home_page():
    return 'This is a bank account app!'


# Routes associated with USERS
@app.route('/users', methods= ['GET'])
def get_users():
    return User().get_users()


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return User(user_id).get_user()


@app.route('/users', methods=['POST'])
def create_user():
    return User().create_user()


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return User(user_id).delete_user()


# Routes associated with USERS SERVICE
@app.route('/users/<int:user_id>/update_details', methods= ['PUT'])
def update_user_details(user_id):
    return UserService(user_id).update()


@app.route('/users/<int:user_id>/update_pin', methods= ['PUT'])
def update_user_pin(user_id):
    return UserService(user_id).update_pin()


# Routes associated with TRANSACTIONS
# TODO: Need to specify which account to interact with
# e.g. users/1/accounts/2/withdraw
@app.route('/users/<int:user_id>/withdraw', methods=['PUT'])
def withdraw(user_id):
    return Transactions(user_id).withdraw()


@app.route('/users/<int:user_id>/deposit', methods=['PUT'])
def deposit(user_id):
    return Transactions(user_id).deposit()


@app.route('/users/<int:user_id>/transfer', methods=['PUT'])
def transfer(user_id):
    return Transactions(user_id).transfer()

# Routes associated with ACCOUNTS
@app.route('/accounts/', methods= ['GET'])
def accounts():
    return "List of accounts"

@app.route('/accounts/open_account', methods= ['POST'])
def open_account():
    return Accounts.open_account()


@app.route('/accounts/close_account', methods= ['DELETE'])
def close_account():
    return Accounts.close_account()


"""
Accounts:
Example routes:
/user/<int:user_id>/accounts --> list accounts attached to a user
/user/<int:user_id>/accounts/<int:account_id> --> details of specific account attached to a user


"""