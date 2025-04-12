from flask import current_app
from flask_login import UserMixin
from database import select_user_by_id
from shared_resources import login_vendeur

class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password


@login_vendeur.user_loader
def load_user(user_id):
    user_data = select_user_by_id(user_id)
    if user_data:
        user = User(user_data['id'], user_data['username'], user_data['email'], user_data['password'])
        return user
    else:
        return None