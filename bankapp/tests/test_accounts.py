from bankapp import app, db
import unittest
import json

from bankapp.models.user_model import UserModel
from bankapp.tests.test_base import TestBase


class TestAccounts(TestBase):

    def test_get_current_account(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.get(f'/users/{mock_user.id}/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_user.id)

    def test_get_accounts(self):
        mock_account = self.create_current_account()
        response = self.client.get(f'/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_account.user_id)

    # test open account
    def test_open_account(self):
        mock_user = self.create_user()
        mock_request_data = {
            'account_type': 'current',
            'balance': 2000,
            'pin': '1234'
        }
        response = self.client.post(f'/users/{mock_user.id}/accounts/current/open_account', 
                                    data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['account_type'], 'current')
        self.assertEqual(data['balance'], 2000)
        self.assertEqual(data ['user_id'], mock_user.id)

    # test open account wrong pin

    # test close account

    # test close account does not exist

    # test apply charge

    # test add interest
