class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # store hashed passwords
        self.role = role
