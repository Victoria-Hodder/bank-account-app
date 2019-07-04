from bankapp import ma
from bankapp.models import User

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User