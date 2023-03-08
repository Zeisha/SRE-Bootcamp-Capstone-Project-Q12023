import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import User  # noqa: E402
import userservice  # noqa: E402


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = userservice.UserService()

    def test_get_user_fail(self):
        with patch("userservice.get_userdata") as mock_user:
            username, password, role, salt = (
                "admin",
                "secret",
                "admin",
                "salt1234",
            )  # noqa: E501
            mock_user.return_value = User(
                username=username,
                password=userservice.salted_password(password, salt),
                role=role,
                salt=salt,
            )
            user = self.user_service.get_user("admin", "wrong_password")
        self.assertEqual(None, user)

    def test_is_valid_role(self):
        self.assertTrue(self.user_service.is_valid_role("admin"))


if __name__ == "__main__":
    unittest.main()
