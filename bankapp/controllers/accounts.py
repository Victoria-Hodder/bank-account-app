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
from bankapp.models import AccountModel
from flask import jsonify, abort, request

class AccountService:

    def __init__(self, account_id=None):
        self.account_id = account_id

    def get_accounts(self):
        users = AccountModel.query.all()
        account_schema = AccountSchema(many=True)
        response = account_schema.dump(users)
        return jsonify(response)
    
    def open_account(self):
        data = request.get_json(force=True)
        new_account = data ['account name']

        if not new_account:
            abort(400, description="To create a new account, you must give it a name.")
        else:
            new_account = AccountModel(account_name=new_account)
            db.session.add(new_account)
            db.session.commit()
            user_schema = AccountSchema()
            response = user_schema.dump(new_account)
            return jsonify(response)
    
    def close_account(self):
        account = AccountModel.query.get_or_404(self.account_id, "You cannot delete an account which does not exist")
        db.session.delete(account)
        db.session.commit()
        return f"You successfully deleted your account. Thanks for using V's banking"
    

from bankapp.schemas import AccountSchema
