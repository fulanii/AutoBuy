import pytest
from bot.home_depot.logins import FreshLogin
from config.get_credential import secrets

class TestFreshLogin:

    def test_fresh_login(self):
        creds = secrets()
        email = creds["email"]
        password = creds["password"]

        
        fresh_login = FreshLogin(email=email, password=password, headless=True, quit_driver=True)
        result =  fresh_login.fresh_login()

        assert type(result) == dict
        assert result["login_status_check"] == True
        assert result["serialization_check"] == True
        assert result["login_and_serialization_check"] == True
        assert result["status_check_fail_amount"] <= 3


    def test_fresh_logout(self):
        creds = secrets()
        email = creds["email"]
        password = creds["password"]

        fresh_login = FreshLogin(email=email, password=password, headless=True, quit_driver=True)
        fresh_login_result =  fresh_login.fresh_login()

        assert fresh_login_result["login_and_serialization_check"] == True
        assert fresh_login.logout_fresh_login() == True