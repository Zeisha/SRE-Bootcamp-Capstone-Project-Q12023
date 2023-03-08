import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from networking import get_mask_from_cidr, get_cidr_from_mask  # noqa: E402
import unittest  # noqa: E402


class TestNetworking(unittest.TestCase):
    def test_valid_cidr_to_mask(self):
        self.assertEqual("128.0.0.0", get_mask_from_cidr(1))

    def test_valid_mask_to_cidr(self):
        self.assertEqual(1, get_cidr_from_mask("128.0.0.0"))

    def test_invalid_cidr_to_mask(self):
        self.assertEqual("Invalid cidr provided", get_mask_from_cidr(0))

    def test_invalid_mask_to_cidr(self):
        self.assertEqual(
            "Invalid mask provided", get_cidr_from_mask("0.0.0.0")
        )  # noqa: E501


if __name__ == "__main__":
    unittest.main()
