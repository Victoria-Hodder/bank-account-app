from bankapp import app, db
import unittest
import json

from bankapp.models.user_model import UserModel


# Run in this way
# python3 -m unittest bankapp/tests/*.py


class TestRoutes(unittest.TestCase):
        
        def setUp(self):
            app.config['TESTING']=True
            app.config['DEBUG']=False
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
            # I don't know why this works but it does
            app.app_context().push()
            db.drop_all()
            db.create_all()
            self.client = app.test_client()
            self.assertEqual(app.debug,False)


        def tearDown(self):
            pass
        
        def create_user_by_param(self, name, address, pin):
            user = UserModel(name=name,address=address,pin=pin)
            db.session.add(user)
            db.session.commit()
            return user
        

        def create_user(self):
            user=UserModel(name='Test User', address='12 Edward Place',pin='1234')
            db.session.add(user)
            db.session.commit()
            return user



        def test_create_user(self):
            mock_request_data = {
                'name': 'Test User',
                'address': '12 Edward place',
                'pin': '1234'
            }
            response = self.client.post('/users', data=json.dumps(mock_request_data))
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code,200)
            self.assertEqual(data['name'], 'Test User')
            self.assertEqual(data['address'], '12 Edward place')
            self.assertEqual(data['pin'], '1234')


        def test_get_user(self):
            mock_user = self.create_user()
            response = self.client.get(f'/users/{mock_user.id}')
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code,200)
            self.assertEqual(data['name'], mock_user.name)
            self.assertEqual(data['address'], mock_user.address)
            self.assertEqual(data['pin'], mock_user.pin)


if __name__ == '__main__':
    unittest.main()   
