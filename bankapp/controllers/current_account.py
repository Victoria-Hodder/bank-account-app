from flask import abort, jsonify, request
from bankapp import db
from bankapp.models.account_model import AccountModel
from bankapp.models.user_model import UserModel
from .accounts import AccountService


class Current(AccountService):
    def __init__(self, account_id=None):
        super().__init__(account_id)

    def open_account(self, user_id):
        # TODO: user method overriding to recycle open_account from AccountServices class

        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        data = request.get_json(force=True)
        new_balance = data['balance']
        user_pin = data['pin']

        if user_pin == user.pin:
            new_account = AccountModel(account_type='current', balance=new_balance, user_id=user_id)
            db.session.add(new_account)
            db.session.commit()
            account_schema = AccountSchema()
            response = account_schema.dump(new_account)
            return jsonify(response)
        else:
            abort(400, description="Pin is not correct. Please try again")


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
