from app import app, login_manager
from app.user import User
from flask.ext.wtf import Form, TextField, PasswordField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        filtered_list = [user for user in app.config['ADMINS'] if user.name == self.username.data]
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
    filtered_list = [user for user in app.config['ADMINS'] if user.get_id() == userid]
    return filtered_list[0] if filtered_list else None