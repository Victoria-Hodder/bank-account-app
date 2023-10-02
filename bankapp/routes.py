from bankapp import app
from .controllers.user import User
from .controllers.user_details import UserDetails
from .controllers.transactions import Transactions


@app.route('/')
def home_page():
    return 'This is a bank account app!'


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


@app.route('/users/<int:user_id>/update_details', methods= ['PUT'])
def update_user_details(user_id):
    return UserDetails(user_id).update()


@app.route('/users/<int:user_id>/update_pin', methods= ['PUT'])
def update_user_pin(user_id):
    return UserDetails(user_id).update_pin()


@app.route('/users/<int:user_id>/withdraw', methods=['PUT'])
def withdraw(user_id):
    return Transactions(user_id).withdraw()


@app.route('/users/<int:user_id>/deposit', methods=['PUT'])
def deposit(user_id):
    return Transactions(user_id).deposit()


@app.route('/users/<int:user_id>/transfer', methods=['PUT'])
def transfer(user_id):
    return Transactions(user_id).transfer()
