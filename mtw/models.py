from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from mtw import db, login_manager, app
from flask_login import UserMixin


# Deals with user sessions. Grabs the user id to authenticate the user is logged in.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    ''' Main User Class '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    movies = db.relationship('Movie', backref='owner')


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


class Movie(db.Model):
    ''' Movie Class for all movies in the users list '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    year_released = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f"Movie('Title: {self.title}, Year: {self.year_released}, Added: {self.date_added}')"
