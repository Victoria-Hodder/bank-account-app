from bankapp import ma
from bankapp.models import UserModel, AccountModel

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    pin = ma.auto_field()
    balance = ma.auto_field()
    accounts = ma.auto_field()

class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        include_fk = True
