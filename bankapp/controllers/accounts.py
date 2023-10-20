""" 
Logic for different account types 

Account (parent class)
    --> open_account()
    --> delete_account()

CurrentAccount (child, inherits from Account)
    --> account_type = 'current'
    --> inherit methods from Account (for opening/deleting)
SavingsAccount (child, inherits from Account)
    --> account_type = 'savings'
    --> inherit methods from Account (for opening/deleting)

Where would I put the logic for checking the account type ('current'/'savings')?

"""

from bankapp import db
from bankapp.models.account_model import AccountModel
from flask import jsonify, abort, request
from bankapp.models.user_model import UserModel

class AccountService:

    def __init__(self, account_id=None, user_id=None):
        self.account_id = account_id
        self.user_id = user_id

    def get_accounts(self):
        users = AccountModel.query.all()
        account_schema = AccountSchema(many=True)
        response = account_schema.dump(users)
        return jsonify(response)
    
    # TODO: only a user can open an account
    def open_account(self):
        data = request.get_json(force=True)
        new_account = data ['account name']
        user_id = data['user id']
        # TODO: add pin functionality

        if not new_account:
            abort(400, description="To create a new account, you must give it a name.")
        elif (new_account.lower() != 'current') and (new_account.lower() != 'savings'):
            abort(400, description="There are only two valid account types: savings or current.")
        elif not user_id:
            abort(400, description="Only existing users can create an account")
        else:
            new_account = AccountModel(account_name=new_account, user_id=user_id)
            db.session.add(new_account)
            db.session.commit()
            user_schema = AccountSchema()
            response = user_schema.dump(new_account)
            return jsonify(response)
    
    def close_account(self):
        account = AccountModel.query.get_or_404(self.account_id, "You cannot delete an account which does not exist")
        user = UserModel.query.get_or_404(self.user_id, "You do not exist, please try again")
        db.session.delete(account)
        db.session.commit()
        # TODO: add users name to delete message
        return f"You successfully deleted your account. Thanks for using V's banking, {user.name}"
    

from bankapp.schemas.account_schema import AccountSchema


"""
        user = UserModel.query.get_or_404(self.user_id, "You do not exist, please try again")
        db.session.delete(user)
        db.session.commit()
        return f"bye bye {user.name}"

"""