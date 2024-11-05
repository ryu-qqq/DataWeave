import unittest
from unittest.mock import MagicMock
from dataweave.cookie_manager import CookieManager
from dataweave.sync_http_client import SyncHttpClient


class TestCookieManager(unittest.TestCase):
    def setUp(self):
        self.http_client = SyncHttpClient()
        self.cookie_manager = CookieManager(http_client=self.http_client)

    def test_get_cookies(self):
        mock_cookie_1 = MagicMock()
        mock_cookie_1.key = "session_id"
        mock_cookie_1.value = "abc123"
        mock_cookie_1.__getitem__.side_effect = lambda key: {
            "domain": "example.com",
            "path": "/",
            "secure": True
        }.get(key)

        mock_cookie_2 = MagicMock()
        mock_cookie_2.key = "user_pref"
        mock_cookie_2.value = "dark_mode"
        mock_cookie_2.__getitem__.side_effect = lambda key: {
            "domain": "example.com",
            "path": "/",
            "secure": False
        }.get(key)

        mock_response = MagicMock()
        mock_response.cookies = {"session_id": mock_cookie_1, "user_pref": mock_cookie_2}
        self.http_client.get = MagicMock(return_value=mock_response)

        result = self.cookie_manager.get_cookies("https://example.com", {"User-Agent": "TestAgent"})

        self.assertIn("session_id", result)
        self.assertEqual(result["session_id"]["value"], "abc123")
        self.assertEqual(result["session_id"]["domain"], "example.com")
        self.assertTrue(result["session_id"]["secure"])

        self.assertIn("user_pref", result)
        self.assertEqual(result["user_pref"]["value"], "dark_mode")
        self.assertEqual(result["user_pref"]["domain"], "example.com")
        self.assertFalse(result["user_pref"]["secure"])


if __name__ == "__main__":
    unittest.main()



