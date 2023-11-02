from flask import abort, jsonify, request
from bankapp import db
from bankapp.models.account_model import AccountModel
from bankapp.models.user_model import UserModel
from .accounts import AccountService


class Savings(AccountService):
    def __init__(self, account_id=None):
        super().__init__(account_id)

    def add_interest(self, user_id):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        account = AccountModel.query.get_or_404(self.account_id, "You cannot select an account which does not exist")
        if user_id == account.user_id:
            if account.account_type == 'savings':
                account.balance = account.balance * 1.10
                db.session.commit()
                account_schema = AccountSchema()
                response = account_schema.dump(account)
                return jsonify(response)
            else:
                return abort(400, description="You can only add interest to a savings account")
        else:
            return abort(400, description="user id and account id must match")
        

from bankapp.schemas.account_schema import AccountSchema
