
from bankapp import db
from bankapp.models.account_model import AccountModel
from flask import jsonify, abort, request
from bankapp.models.user_model import UserModel

class AccountService:

    # Insert your very own admin pin here
    admin_pin = ''

    def __init__(self, account_id=None):
        self.account_id = account_id

    def get_accounts(self):
        accounts = AccountModel.query.all()
        account_schema = AccountSchema(many=True)
        response = account_schema.dump(accounts)
        return jsonify(response)
    
    def get_user_accounts(self, user_id):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        accounts = AccountModel.query.all()

        user_accounts = [account for account in accounts
                         if account.user_id == user.id]

        account_schema = AccountSchema(many=True)
        response = account_schema.dump(user_accounts)
        return response
    
    def open_account(self, user_id, account_type):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        data = request.get_json(force=True)
        new_balance = data['balance']
        user_pin = data['pin']

        if user_pin == user.pin:
            new_account = AccountModel(account_type=account_type, balance=new_balance, user_id=user_id)
            db.session.add(new_account)
            db.session.commit()
            account_schema = AccountSchema()
            response = account_schema.dump(new_account)
            return jsonify(response)
        else:
            abort(400, description="Pin is not correct. Please try again")
    
    def close_account(self, user_id):
        account = AccountModel.query.get_or_404(self.account_id, "You cannot delete an account which does not exist")
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        db.session.delete(account)
        db.session.commit()
        return f"You successfully deleted your account. Thanks for using V's banking, {user.name}"
    

from bankapp.schemas.account_schema import AccountSchema
