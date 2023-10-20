from bankapp import app
from .controllers.user import User
from .controllers.user_details import UserService
from .controllers.transactions import Transactions
from .controllers.accounts import AccountService


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
@app.route('/accounts', methods= ['GET'])
def get_accounts():
    return AccountService().get_accounts()

@app.route('/users/<int:user_id>/accounts', methods= ['GET'])
def get_user_accounts(user_id):
    return AccountService().get_user_accounts(user_id)

@app.route('/users/<int:user_id>/accounts/open_account', methods= ['POST'])
def open_account(user_id):
    return AccountService().open_account(user_id)

@app.route('/users/<int:user_id>/accounts/<int:account_id>/close_account', methods= ['DELETE'])
def close_account(account_id, user_id):
    return AccountService(account_id, user_id).close_account()
