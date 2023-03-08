import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import Auth  # noqa: E402
from userservice import salted_password  # noqa: E402
from model import User  # noqa: E402


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = Auth()

        self.test_params = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI",  # noqa: E501
        }

    def test_generate_token(self):
        with patch("auth.user_service.get_user") as mock:
            username, password, role, salt = (
                "admin",
                "secret",
                "admin",
                "salt1234",
            )  # noqa: E501
            mock.return_value = User(
                username=username,
                password=salted_password(password, salt),
                role=role,
                salt=salt,
            )

            token = self.auth.generate_token(username, password)

            mock.assert_called_once_with(username, password)
            self.assertEqual(self.test_params["token"], token)

    def test_decrypt_token(self):
        self.assertEqual(
            "admin", self.auth.decrypt_token(self.test_params["token"])["role"]
        )

    def test_is_valid_token(self):
        self.assertTrue(self.auth.is_valid_token(self.test_params["token"]))

    def test_is_valid_claim_not_true(self):
        self.assertFalse(
            self.auth.is_valid_claim({"username": "xyz", "role": "Superuser"})
        )


if __name__ == "__main__":
    unittest.main()
