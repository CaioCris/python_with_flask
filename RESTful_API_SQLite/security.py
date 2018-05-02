from werkzeug.security import safe_str_cmp
from RESTful_API_SQLite.user import User


def authentication_user(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
