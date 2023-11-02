from flask import jsonify
from bankapp import db
from bankapp.models.account_model import AccountModel
from bankapp.models.user_model import UserModel
from .accounts import AccountService


class Current(AccountService):
    def __init__(self, account_id):
        super().__init__(account_id)

    def apply_charge(self, user_id):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        account = AccountModel.query.get_or_404(self.account_id, "You cannot select an account which does not exist")
        if user_id == account.user_id:
            account.balance = account.balance - 5
            db.session.commit()
            account_schema = AccountSchema()
            response = account_schema.dump(account)
            return jsonify(response)
        else:
            return f"user id and account id must match"

from bankapp.schemas.account_schema import AccountSchema
