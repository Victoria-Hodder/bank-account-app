from bankapp import app, db
import json

from bankapp.models.account_model import AccountModel
from bankapp.tests.test_base import TestBase


"""
See test_accounts.py for documentation on how testing accounts has been
organised

"""

class TestCurrentAccounts(TestBase):

    def test_get_current_account(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.get(f'/users/{mock_user.id}/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_user.id)

    def test_open_current_account(self):
        mock_user = self.create_user()
        mock_request_data = {
            'balance': 2000,
            'pin': f'{mock_user.pin}'
        }
        response = self.client.post(f'/users/{mock_user.id}/accounts/current/open_account', 
                                    data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['account_type'], 'current')
        self.assertEqual(data['balance'], 2000)
        self.assertEqual(data ['user_id'], mock_user.id)

    def test_open_current_account_wrong_pin(self):
        mock_user = self.create_user()
        mock_request_data = {
            'balance': 2000,
            'pin': '6677'
        }
        response = self.client.post(f'/users/{mock_user.id}/accounts/current/open_account', 
                                    data=json.dumps(mock_request_data))
        self.assertEqual(response.status_code,400)

    def test_apply_charge(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id}/apply_charge',
                                   data=json.dumps(self.test_admin_pin))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['balance'], mock_account.balance)

    def test_apply_charge_wrong_admin_pin(self):
        wrong_pin = {
            "admin pin": 2345
        }
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id}/apply_charge',
                                   data=json.dumps(wrong_pin))
        self.assertEqual(response.status_code,400)
