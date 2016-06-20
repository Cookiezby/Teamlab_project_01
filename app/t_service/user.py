from app import models, db


class UserService(object):
    @staticmethod
    def get_user_by_name(name):
        user = models.User.query.filter_by(name=name).first()
        if user:
            print user
            return user
        else:
            return None

    @staticmethod
    def get_all_users():
        users = models.User.query.all()
        return users
