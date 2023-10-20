from bankapp import ma
from bankapp.models.account_model import AccountModel


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        include_fk = True
