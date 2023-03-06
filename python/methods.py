import hashlib
import jwt
from os import getenv
from dbconnect import get_userdata

SECRET_KEY = getenv("JWT_KEY")


def salted_password(password, salt):
    return hashlib.sha512((password + salt).encode()).hexdigest()


class Token:
    def generate_token(self, username, password):
        result = get_userdata(username)
        if result.username == username and result.password == salted_password(
            password, result.salt
        ):
            return jwt.encode(payload={"role": result.role}, key=SECRET_KEY)

    def decrypt_token(self, token):
        return jwt.decode(token, SECRET_KEY, algorithms="HS256")


class Restricted:
    def access_data(self, authorization):
        token = authorization.removeprefix("Bearer ")
        try:
            decoded = Token().decrypt_token(token)
        except jwt.DecodeError:
            return "Restricted"

        if "role" in decoded and decoded["role"] in ["editor", "admin"]:
            return True

        return False
