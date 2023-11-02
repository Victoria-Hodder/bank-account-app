from bankapp import db
from bankapp.models.account_model import AccountModel
from .user import User
from flask import request, jsonify, abort


# TODO: play with inheriting from AccountService (instead of User)
class Transactions(User):
    
    def withdraw(self, account_id):
        data = request.get_json(force=True)
        amount = data['amount']
        pin = data['pin']
        if amount > 2000:
            abort(400, description='You are not allowed to go over 2000 euro daily limit') 
        else:
            user = User.query.get_or_404(self.user_id, "User does not exist")
            account = AccountModel.query.get_or_404(account_id, "Account does not exist")
            if pin == user.pin: 
                if amount <= account.balance:
                    account.balance -= amount
                    db.session.commit()
                    account_schema = AccountSchema()
                    response = account_schema.dump(account)
                    return jsonify(response)       
                else:
                    abort(
                        400,
                        description="You are not allowed to withdraw more money than you have on your account!",
                    )
            else:
                abort(400, description="Pin is not correct")

    def deposit(self, account_id):
        data = request.get_json(force=True)
        amount = data['amount']
        pin = data['pin']
        if amount >= 3000:
            abort(400, description='You are not allowed to go over 3000 euro daily limit') 
        else:
            user = User.query.get_or_404(self.user_id, "User does not exist")
            account = AccountModel.query.get_or_404(account_id, "Account does not exist")
            if pin == user.pin:
                account.balance += amount
                db.session.commit()
                account_schema = AccountSchema()
                response = account_schema.dump(account)
                return jsonify(response)
            else:
                abort(400, description="Pin is not correct")

    def transfer(self, account_id):
        data = request.get_json(force=True)
        amount = data["amount"]
        pin = data["pin"]
        destination_acc_id = data["destination account"]
        # Amount check
        if amount > 3000:
            abort(400, description='You are not allowed to go over 3000 euro daily limit') 
        # pin check
        else:
            user = User.query.get_or_404(self.user_id, "User does not exist")
            account = AccountModel.query.get_or_404(account_id, "Source account does not exist")
            destination_acc = AccountModel.query.get_or_404(destination_acc_id, "Destination account does not exist")
            if pin == user.pin:
                if account != destination_acc:
                    account.balance -= amount
                    destination_acc.balance += amount
                    db.session.commit()
                    account_schema = AccountSchema()
                    response = account_schema.dump(destination_acc)
                    return jsonify(response)
                else:
                    abort(400, description="Destination account must differ from source account")
            else:
                abort(400, description="Pin is not correct")
                

from bankapp.schemas.account_schema import AccountSchema
