from app import app, login_manager
from flask.ext.wtf import Form, TextField, PasswordField, validators

class User:
    def __init__(self, name, password, id):
        self.name = name
        self.password = password
        self.id = id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymouse(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_password(self, password):
        return self.password == password

user_list = [User("jacob", "Acrobats1!", 15423923532),
            User("jessica", "Acrobats2!", 323101244324),
            User("miriam", "Acrobats3!", 92323895983)]

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        filtered_list = [user for user in user_list if user.name == self.username.data]
        user = filtered_list[0] if filtered_list else None
        if user is None:
            self.username.errors.append('Incorred username or password')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Incorred username or password')
            return False

        self.user = user
        return True

@login_manager.user_loader
def load_user(userid):
    filtered_list = [user for user in user_list if user.get_id() == userid]
    return filtered_list[0] if filtered_list else None