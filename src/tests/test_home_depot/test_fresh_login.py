import pytest
from src.bot.home_depot.logins import FreshLogin

class TestLogin:
    def test_fresh_login(self):
        email = ""
        password = ""
        fres_login = FreshLogin(email=email, password=password, headless=True, quit_driver=True)

    def test_cookie_logout(self):
        ...