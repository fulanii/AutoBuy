""" imports """
import os
import time
from bot.home_depot.logins import FreshLogin, CookiesLogin, Logout
from config.get_credential import secrets

def main():
    EMAIL:str = secrets["email"]
    PASSWORD:str = secrets["password"]


    fresh_login_homedepot = FreshLogin(email=EMAIL, password=PASSWORD, quit_driver=True)
    cookie_login_homedepot = CookiesLogin()
    logout_homedepot = Logout()


    # login:bool = False
    # while not login: # while false, execute code bellow
    #     cookie_result = cookie_login_homedepot.login_with_cookies()
    #     if cookie_result  == True:
    #         print("login with cookies success")
    #         login = True
    #     else:
    #         fresh_result = fresh_login_homedepot.fresh_login()
    #         if fresh_result["login_and_serialization_check"] ==  True:
    #             print("Fresh login success")
    #             login == True
    #         else:
    #             login == False
    #             print("Cookies & Fresh login failed")


    if cookie_login_homedepot.login_with_cookies()  == True:
        print("login with cookies success")

    # print(cookie_login_homedepot.logout_with_cookies())



if __name__ =="__main__":
    main()