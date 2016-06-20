from app import db, login_manager
from flask.ext.login import UserMixin
from flask import redirect


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect('/login')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=True)
    password = db.Column(db.String(20), index=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follow_id = db.Column(db.Integer)  # thr current user
    followed_id = db.Column(db.Integer)  # the one be followed


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,unique=True)
    avatar_url = db.Column(db.String(60))
    user_info = db.Column(db.String(200))
