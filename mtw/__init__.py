from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


# Main App object
app = Flask(__name__)

# Import config variables and secret stuff
app.config.from_object('config.Config')

# Database Object
db = SQLAlchemy(app)

# Bcrypt Object for Password Hashing etc
bcrypt = Bcrypt(app)

# Login Manager Object - to deal with session tokens
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Mail object to send password reset emails
mail = Mail(app)


from mtw.models import User
from mtw import views
