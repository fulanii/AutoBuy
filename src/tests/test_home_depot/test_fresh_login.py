import pytest
from bot.home_depot.logins import FreshLogin
from config.get_credential import secrets

class TestFreshLogin:
    email = secrets()["email"]
    password = secrets()["password"]

    def test_fresh_login(self):
        fres_login = FreshLogin(email=TestFreshLogin.email, password=TestFreshLogin.password, headless=True, quit_driver=True)

        assert 1 == 1

    def test_cookie_logout(self):
        ...