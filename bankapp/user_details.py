from bankapp import db
from bankapp.user import User
from flask import jsonify, request, abort

class UserDetails(User):

    def update(self):
        data = request.get_json(force=True)
        user = User.query.get_or_404(self.user_id)

        json_keys = []
        
        for key in data.keys():
            json_keys.append(key)

        # TODO: add other fields which can be updated (address, tax nr etc)
        for key in json_keys:
            if key == 'name' and data['name'] != user.name:
                new_name = data['name']
                user.name = new_name
            if key == 'address' and data['address'] != user.address:
                new_address = data['address']
                user.address = new_address

        db.session.commit()
        user_schema = UserSchema()
        response = user_schema.dump(user)
        return jsonify(response)
    

    def update_pin(self):
        data = request.get_json(force=True)
        current_pin = data['pin']
        new_pin = data['new pin']
        user = User.query.get_or_404(self.user_id)
        
        if current_pin == user.pin:
            user.pin = new_pin
            db.session.commit()
            user_schema = UserSchema()
            response = user_schema.dump(user)
            return jsonify(response)
        else:
            abort(400, description="Pin is not correct. You must know your current pin to update it.")
    
    
from bankapp.schemas import UserSchema
