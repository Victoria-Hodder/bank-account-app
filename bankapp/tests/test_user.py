from bankapp import app, db
import unittest
import json

from bankapp.models.user_model import UserModel
from bankapp.tests.test_base import TestBase


class TestUser(TestBase):

        def test_get_users(self):
            mock_user = self.create_user()
            response = self.client.get('/users')
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code,200)
            self.assertEqual(data[0]['name'], mock_user.name)
            self.assertEqual(data[0]['address'], mock_user.address)
            self.assertEqual(data[0]['pin'], mock_user.pin)

        def test_get_user(self):
            mock_user = self.create_user()
            response = self.client.get(f'/users/{mock_user.id}')
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code,200)
            self.assertEqual(data['name'], mock_user.name)
            self.assertEqual(data['address'], mock_user.address)
            self.assertEqual(data['pin'], mock_user.pin)

        def test_get_users_by_id_404(self):
            mock_user = self.create_user()
            response = self.client.get(f'/users/{mock_user.id+1}')
            self.assertEqual(response.status_code,404)
        
        def test_create_user(self):
            mock_request_data = {
                'name': 'Queen Sloth',
                'address': 'Best tree ever',
                'pin': '2345'
            }
            response = self.client.post('/users', data=json.dumps(mock_request_data))
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(response.status_code,200)
            self.assertEqual(data['name'], 'Queen Sloth')
            self.assertEqual(data['address'], 'Best tree ever')
            self.assertEqual(data['pin'], '2345')

        def test_delete_user(self):
            mock_user = self.create_user()        
            response = self.client.delete(f'/users/{mock_user.id}')        
            data = response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertEqual(data, f"bye bye {mock_user.name}")
            # Check to see if user is deleted from DB
            user = db.session.get(UserModel, mock_user.id)
            self.assertIsNone(user)

        def test_delete_users_by_id_404(self):
            mock_user = self.create_user()
            response = self.client.get(f'/users/{mock_user.id+1}')
            self.assertEqual(response.status_code,404)
