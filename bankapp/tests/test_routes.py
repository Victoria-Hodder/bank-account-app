from bankapp import app, db
from bankapp.models.user_model import User
import unittest
import json


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING']=True
        app.config['DEBUG']=False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.drop_all()
        db.create_all()
        self.app = app.test_client()
        self.assertEqual(app.debug,False)

    def tearDown(self):
        pass
    
    def create_user_by_param(self, name, pin, balance):
        user = User(name=name,pin=pin,balance=balance)
        db.session.add(user)
        db.session.commit()
        return user
    
    def create_user(self):
        user=User(name='Test User', pin='1234', balance=1000)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self,id):
        return User.query.filter_by(id=id).first()

    def test_create_user(self):
        mock_request_data = {
            'name': 'Test User',
            'pin': '1234',
            'balance': 1000
        }
        response = self.app.post('/users', data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['pin'], '1234')
        self.assertEqual(data['balance'], 1000)


    def test_get_users(self):
        mock_user = self.create_user()
        response = self.app.get('/users')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['name'], mock_user.name)
        self.assertEqual(data[0]['pin'], mock_user.pin)
        self.assertEqual(data[0]['balance'], mock_user.balance)

    def test_get_user(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.id}')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], mock_user.name)
        self.assertEqual(data['pin'], mock_user.pin)
        self.assertEqual(data['balance'], mock_user.balance)


    def test_get_users_by_id_404(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.id+1}')
        self.assertEqual(response.status_code,404)

    def test_update_user(self):
        mock_user = self.create_user()
        mock_update_data = {
            'name': "Guinea Pig",
            'balance': 100,
            'pin': "1244"
            }
        response = self.app.put(f'/users/{mock_user.id}', data=json.dumps(mock_update_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], 'Guinea Pig')
        self.assertEqual(data['pin'], '1244')
        self.assertEqual(data['balance'], 100)
    
    def test_delete_user(self):
        mock_user = self.create_user()        
        response = self.app.delete(f'/users/{mock_user.id}')        
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code,204)
        self.assertEqual(data,"")
        #Did it delete from DB too?
        user = self.get_user_by_id(mock_user.id)
        self.assertIsNone(user)
    
    def test_delete_users_by_id_404(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.id+1}')
        self.assertEqual(response.status_code,404)


    def test_withdraw_money_by_user_id(self):
        mock_user = self.create_user()
        mock_request_data = {
            'amount': 20,
            'pin': '1234',
            }
        response = self.app.patch(f'/users/{mock_user.id}/withdraw',data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['pin'], '1234')
        self.assertEqual(data['balance'], 980)

    def test_delete_users_by_id_404(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.id+1}')
        self.assertEqual(response.status_code,404)

    def test_deposit_money_by_user_id(self):
        mock_user = self.create_user()
        mock_request_data = {
            'amount': 20,
            'pin': '1234',
            }
        response = self.app.patch(f'/users/{mock_user.id}/deposit',data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['pin'], '1234')
        self.assertEqual(data['balance'], 1020)
    
    def test_deposit_money_by_user_id_wrong_pin(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.pin+"1"}')
        self.assertEqual(response.status_code,404)

    def test_deposit_money_by_user_id_suprass_daily_limit(self):
        mock_user = self.create_user()
        response = self.app.get(f'/users/{mock_user.balance+3200}')
        self.assertEqual(response.status_code,404)

    def test_transfer_money_by_user_id(self):
        mock_sender = self.create_user()
        mock_receiver = self.create_user_by_param(name="Test Receiver",pin='1235',balance=500)
        mock_request_data = {
            'amount': 20,
            'pin': '1234',
            'receiverId': 2
            }
        response = self.app.patch(f'/users/{mock_sender.id}/transfer',data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], "Test Receiver")
        self.assertEqual(data['pin'], '1235')
        self.assertEqual(data['balance'], 520)