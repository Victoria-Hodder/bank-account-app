from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///side.db' #with pg_admin you can access tables
db = SQLAlchemy(app)

from bankapp import routes