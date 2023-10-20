from bankapp import ma
from bankapp.models.user_model import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    pin = ma.auto_field()
    balance = ma.auto_field()
    accounts = ma.auto_field()
