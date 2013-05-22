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
