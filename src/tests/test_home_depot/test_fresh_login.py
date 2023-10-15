import pytest
from bot.home_depot.logins import FreshLogin
from config.get_credential import secrets

class TestFreshLogin:
    email = secrets()["email"]
    password = secrets()["password"]

    def test_fresh_login(self):
        fresh_login = FreshLogin(email=TestFreshLogin.email, password=TestFreshLogin.password, headless=False, quit_driver=True)

        result =  fresh_login.fresh_login()

        assert type(result) == dict
        assert result["login_status_check"] == True
        assert result["serialization_check"] == True
        assert result["login_and_serialization_check"] == True
        assert result["status_check_fail_amount"] <= 3


    def test_fresh_logout(self):
        fresh_login = FreshLogin(email=TestFreshLogin.email, password=TestFreshLogin.password, headless=False, quit_driver=True)

        fresh_login_result =  fresh_login.fresh_login()
        assert fresh_login_result["login_and_serialization_check"] == True
        assert fresh_login.logout_fresh_login() == True