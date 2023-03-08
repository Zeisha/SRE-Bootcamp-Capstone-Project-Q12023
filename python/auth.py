import jwt
from os import getenv
from userservice import UserService

SECRET_KEY = getenv("JWT_KEY")
user_service = UserService()


class Auth:
    ENCODE_ALGORITHM = "HS256"

    def generate_token(self, username, password):
        user = user_service.get_user(username, password)
        if user:
            return jwt.encode(
                payload={"role": user.role},
                key=SECRET_KEY,
                algorithm=self.ENCODE_ALGORITHM,
            )  # noqa: E501

    def decrypt_token(self, token):
        return jwt.decode(token, SECRET_KEY, algorithms=self.ENCODE_ALGORITHM)

    def is_valid_token(self, token):
        try:
            claim = self.decrypt_token(token)
        except jwt.DecodeError:
            return False

        return self.is_valid_claim(claim)

    def is_valid_claim(self, claim):
        return user_service.is_valid_role(claim["role"])
