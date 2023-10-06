from bankapp import ma
from bankapp.models import UserModel, AccountModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
 #       include_relationships = True
        load_instance = True


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
#        include_fk = True
        load_instance = True

"""
# User
class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()

# Accounts
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True

"""