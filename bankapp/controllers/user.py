from bankapp import db
from bankapp.models.user_model import UserModel
from flask import jsonify, abort, request


class User:
    
    def __init__(self, user_id=None):
        self.user_id = user_id

    def get_users(self):
        user_schema = UserSchema(many=True)
        users = UserModel.query.all()
        response = user_schema.dump(users)
        return jsonify(response)
    
    def get_user(self):
        user = UserModel.query.get_or_404(self.user_id, "You do not exist, please try again")
        user_schema = UserSchema()
        response = user_schema.dump(user)
        return jsonify(response)
    
    def create_user(self):
        data = request.get_json(force=True)
        new_name = data ['name']
        new_address = data['address']
        new_pin = int(data['pin'])

        if not new_name and new_address and new_pin:
            abort(400, description="Something is missing. Please ensure you fill out all fields.")
        else:
            user = UserModel.query.filter_by(name=new_name).first()
            if user:
                abort(400, description="Oops user already exists")
            else:
                new_user = UserModel(name=new_name, address=new_address, pin=new_pin)
                db.session.add(new_user)
                db.session.commit()
                user_schema = UserSchema()
                response = user_schema.dump(new_user)
                return jsonify(response)

    def delete_user(self):
        user = UserModel.query.get_or_404(self.user_id, "You do not exist, please try again")
        db.session.delete(user)
        db.session.commit()
        return f"bye bye {user.name}"


from bankapp.schemas.user_schema import UserSchema
