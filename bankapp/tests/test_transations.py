from bankapp import app, db
import json

from bankapp.models.user_model import UserModel
from bankapp.tests.test_base import TestBase


class TestTransactions(TestBase):
    pass
    def test_withdraw_money_by_user_id(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        mock_request_data = {
            'amount': 20,
            'pin': f'{mock_user.pin}',
            }
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id}/withdraw',data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['balance'], 80)

    def test_deposit_money_by_user_id(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        mock_request_data = {
            'amount': 20,
            'pin': f'{mock_user.pin}',
            }
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id}/deposit',
                                   data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['balance'], 120)

    def test_deposit_money_by_user_id_wrong_pin(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        mock_request_data = {
            'amount': 20,
            'pin': f'{mock_user.pin}',
            }
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id+1}/deposit',
                                   data=json.dumps(mock_request_data))
        self.assertEqual(response.status_code,404)

    def test_deposit_money_by_user_id_suprass_daily_limit(self):
        mock_user = self.create_user()
        mock_account = self.create_current_account()
        mock_request_data = {
            'amount': 3020,
            'pin': f'{mock_user.pin}',
            }
        response = self.client.put(f'/users/{mock_user.id}/accounts/{mock_account.id+1}/deposit',
                                   data=json.dumps(mock_request_data))
        self.assertEqual(response.status_code,400)


    def test_transfer_money_by_user_id(self):
        mock_sender = self.create_user()
        mock_current_account = self.create_current_account()
        mock_receiver = self.create_second_user()
        mock_savings_account = self.create_savings_account()
        mock_request_data = {
            'amount': 20,
            'pin': f'{mock_sender.pin}',
            'destination account': f'{mock_savings_account.id}'
            }
        response = self.client.put(f'/users/{mock_sender.id}/accounts/{mock_current_account.id}/move_my_money',
                                  data=json.dumps(mock_request_data))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['account_type'], mock_savings_account.account_type)
        self.assertEqual(data['balance'], mock_savings_account.balance)
        self.assertEqual(data['id'], mock_savings_account.id)
        self.assertEqual(data['user_id'], mock_receiver.id)
