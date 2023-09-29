from bankapp import db
from bankapp.models import UserModel
from flask import jsonify, abort, request


class User(UserModel):
    def get_users(self):
        user_schema = UserSchema(many=True)
        users = UserModel.query.all()
        response = user_schema.dump(users)
        return jsonify(response)
    
    def get_user(self, user_id):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        user_schema = UserSchema()
        response = user_schema.dump(user)
        return jsonify(response)
    
    def create_user(self):
        data = request.get_json(force=True)
        new_name = data ['name']
        new_address = data['address']
        new_pin = int(data['pin'])
        new_balance = int(data['balance'])

        if not new_name and new_address and new_balance and new_pin:
            abort(400, description="Bad request!")
        else:
            user = UserModel.query.filter_by(name=new_name).first()
            if user:
                abort(400, description="Oops user already exists")
            else:
                new_user = UserModel(name=new_name, address=new_address, pin=new_pin, balance=new_balance)
                db.session.add(new_user)
                db.session.commit()
                user_schema = UserSchema()
                response = user_schema.dump(new_user)
                return jsonify(response)

    def delete_user(self, user_id):
        user = UserModel.query.get_or_404(user_id, "You do not exist, please try again")
        db.session.delete(user)
        db.session.commit()
        return f"bye bye {user.name}"


from bankapp.schemas import UserSchema
