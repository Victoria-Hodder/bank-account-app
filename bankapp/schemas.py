from bankapp import ma
from bankapp.models import User, Account

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account