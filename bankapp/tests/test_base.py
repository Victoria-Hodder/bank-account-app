import os
import unittest
from dotenv import load_dotenv

from bankapp import app, db
from bankapp.models.user_model import UserModel
from bankapp.models.account_model import AccountModel


# Run in this way
# python3 -m unittest bankapp/tests/*.py

class TestBase(unittest.TestCase):
        
    load_dotenv()
    ADMIN_PIN = os.getenv('ADMIN_PIN')
    test_admin_pin = {
        "admin pin": ADMIN_PIN
    }
        
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
        db.session.commit()
    
    # Mock data
    def create_user(self):
        user=UserModel(name='Bob cat', address='12 Edward Place',pin='1234')
        db.session.add(user)
        db.session.commit()
        return user
    
    def create_second_user(self):
        user=UserModel(name='Katrin Schmidt', address='10 Frankfurter Allee',pin='8765')
        db.session.add(user)
        db.session.commit()
        return user
    
    def create_current_account(self):
        account=AccountModel(account_type='current', balance=100, user_id=1)
        db.session.add(account)
        db.session.commit()
        return account
    
    def create_savings_account(self):
        account=AccountModel(account_type='savings', balance=200, user_id=2)
        db.session.add(account)
        db.session.commit()
        return account
    