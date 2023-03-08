import hashlib
from db import get_userdata


def salted_password(password, salt):
    return hashlib.sha512(f"{password}{salt}".encode()).hexdigest()


class UserService:
    valid_roles = ["admin", "editor", "viewer"]

    def get_user(self, name, password):
        user = get_userdata(name)
        salt = "salt"
        username = "username"

        if user:
            salt = user.salt
            username = user.username

        expected_password = salted_password(password, salt)
        if username == name:
            if user.password == expected_password:
                return user

    def is_valid_role(self, role):
        return role in self.valid_roles
