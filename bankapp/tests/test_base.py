from bankapp import app, db
import unittest

from bankapp.models.user_model import UserModel


# Run in this way
# python3 -m unittest bankapp/tests/*.py

class TestBase(unittest.TestCase):
        
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
            pass
        
        # Mock data
        def create_user(self):
            user=UserModel(name='Bob cat', address='12 Edward Place',pin='1234')
            db.session.add(user)
            db.session.commit()
            return user
        