from bankapp import app, db
import unittest
import json

from bankapp.tests.test_base import TestBase


class TestUserDetails(TestBase):        

    def test_update_user(self):
        mock_user = self.create_user()
        mock_update_data = {
            'name': "Guinea Pig",
            'address': "34 Old Street",
            }
        response = self.client.put(f'/users/{mock_user.id}/update_details', data=json.dumps(mock_update_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['name'], 'Guinea Pig')
        self.assertEqual(data['address'], "34 Old Street")

    def test_update_pin(self):
        mock_user = self.create_user()
        mock_update_data = {
            'pin': '1234',
            'new pin': '4568'            
        }
        response = self.client.put(f'/users/{mock_user.id}/update_pin', data=json.dumps(mock_update_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['pin'], '4568')

    def test_update_pin_wrong_pin(self):
        mock_user = self.create_user()
        mock_update_data = {
            'pin': '9999',
            'new pin': '4568'            
        }
        response = self.client.put(f'/users/{mock_user.id}/update_pin', data=json.dumps(mock_update_data))
        self.assertEqual(response.status_code,400)
