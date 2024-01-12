from bankapp import app, db
import json

from bankapp.models.account_model import AccountModel
from bankapp.tests.test_base import TestBase

"""
Here I test functionality that applies to both account types (savings 
and current): namely getting all accounts and closing an account.

Why?
- Partly to reflect how the controllers are organised
- Partly because the URL and the expected behaviour does not differ between 
the account types

I nevertheless chose to test getting and opening an individual account 
separately in test_current_account and test_savings_account

Why?
- To test specific accounts can be called
- When opening an account, the URL and expected behaviour differs slightly 
between the two account types
"""


class TestAccounts(TestBase):

    def test_get_accounts(self):
        mock_account = self.create_current_account()
        mock_savings_account = self.create_savings_account()
        response = self.client.get(f'/accounts')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)

        self.assertEqual(data[0]['account_type'], mock_account.account_type)
        self.assertEqual(data[0]['balance'], mock_account.balance)
        self.assertEqual(data[0]['user_id'], mock_account.user_id)

        self.assertEqual(data[1]['account_type'], mock_savings_account.account_type)
        self.assertEqual(data[1]['balance'], mock_savings_account.balance)
        self.assertEqual(data[1]['user_id'], mock_savings_account.user_id)

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
