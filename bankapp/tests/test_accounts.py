from bankapp import app, db
import json

from bankapp.models.account_model import AccountModel
from bankapp.tests.test_base import TestBase


# Currently primarily "current" account type is being tested
# Eventually this file could be split according to the account types (current, savings)

class TestAccounts(TestBase):

    def test_get_accounts(self):
        mock_account = self.create_current_account()
        response = self.client.get(f'/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_account.user_id)

    def test_get_current_account(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.get(f'/users/{mock_user.id}/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_user.id)

    def test_open_account(self):
        mock_user = self.create_user()
        mock_request_data = {
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

    def test_open_account_wrong_pin(self):
        mock_user = self.create_user()
        mock_request_data = {
            'balance': 2000,
            'pin': '6677'
        }
        response = self.client.post(f'/users/{mock_user.id}/accounts/current/open_account', 
                                    data=json.dumps(mock_request_data))
        self.assertEqual(response.status_code,400)

    def test_close_account(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.delete(f'/users/{mock_user.id}/accounts/{mock_account.id}/close_account')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data, "You successfully deleted your account. " +
                               f"Thanks for using V's banking, {mock_user.name}")
        account = db.session.get(AccountModel, mock_account.id)
        self.assertIsNone(account)

    def test_close_account_does_not_exist(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        response = self.client.delete(f'/users/{mock_user.id}/accounts/{mock_account.id+1}/close_account')
        self.assertEqual(response.status_code,404)

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

    def test_add_interest(self):
        mock_user = self.create_second_user()
        mock_account = self.create_savings_account()
        print(mock_user)
        print(mock_account)
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id}/add_interest',
                                   data=json.dumps(self.test_admin_pin))
        print(response.text)
        data = json.loads(response.get_data(as_text=True))
        print(data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['balance'], round(mock_account.balance))
