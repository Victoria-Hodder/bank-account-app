from bankapp import app, db
import unittest
import json

from bankapp.models.user_model import UserModel
from bankapp.tests.test_base import TestBase


class TestTransactions(TestBase):
    pass



"""
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


"""