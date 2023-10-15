""" imports """
from .logout import Logout

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from utils. driver_manager import DriverManager
from utils.selenium_sessions import SessionManager
from utils.custom_exceptions.exceptions import LoginCheckStatusFailedException
from utils.custom_exceptions.exceptions import SerializationFailedException
from utils.custom_exceptions.exceptions import CookiesLoginStatusFailed


class CookiesLogin():
    """ 
    A class to login HomeDepot using the saved cookies

    arg:
        maximize_window:bool default False (to maximize the selenium window)
        headless: bool set to True to not show the chrome browser (default False)
        detach: bool set to True to not quit the chrome browser (default True)
        quit_diver:bool To auto quit driver (default False)
    
    Function(s):  
        login_with_cookies(): login with saved cookies -> bool
        logout_with_cookies(): logout after a cookie login -> bool
    """

    home_page:str = "https://www.homedepot.com/"
    login_page:str = "https://www.homedepot.com/auth/view/signin?redirect=/&ref="
    payment_page:str = "https://www.homedepot.com/myaccount/payments"
    security_page:str = "https://www.homedepot.com/account/ui/security"

    def __init__(self, quit_driver:bool = False, maximize_window:bool=False, detach:bool=True, headless:bool=False) -> None:
        self.driver_manager = DriverManager(maximize_window=maximize_window, detach=detach, headless=headless)
        self.quit_driver = quit_driver
        self.logout = Logout()

    def login_with_cookies(self) -> bool:
        """
        Login using saved cookies data

        returns:
            bool: True if login  is successfully, False if login fails.
        
        exception:
            raise:  
                   LoginCheckStatusFailedException if login status couldn't be verified.
                   LoginFailedException if logins failed.
        """

        status_check_fail_amount:int = 0
        cookies_data:dict = SessionManager.deserialize_session_data()
        driver = self.driver_manager.initialize_driver()

        driver.get(self.home_page)

        for cookie in cookies_data:
            driver.add_cookie(cookie)
        driver.refresh()

        # check login status 1
        try:
            driver.implicitly_wait(5)
            after_login_acc_btn = driver.find_element(
                By.CSS_SELECTOR,
                "a#headerMyAccount.MyAccount__button[title='My Account']")
            after_login_acc_btn.click()
        except NoSuchElementException:
            status_check_fail_amount += 1
            pass

        # check if sign out available 2
        try:
            signout = driver.find_element(
                By.CSS_SELECTOR,
                "button#signOut.MyAccount__authSignOut[title='Sign Out']").text
        except NoSuchElementException:
            status_check_fail_amount += 1
            pass

        # check welcome message 3
        try:
            welcome_msg = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/div/div[2]/div[1]/div/h3/span').text
        except NoSuchElementException as error:
            status_check_fail_amount += 1
            if self.quit_driver:
                driver.quit()
            raise LoginCheckStatusFailedException(
                "Login status check failed") from error

        if  (welcome_msg == "Welcome Back!" or
                "Welcome Back!" in driver.page_source or
                signout == "Sign Out"): 
            return self.__login_cookies_expiration_check()
        if self.quit_driver:
            if self.quit_driver:
                driver.quit()
        raise LoginCheckStatusFailedException(
            "Login status check failed") 


    def __login_cookies_expiration_check(self) -> bool:
        """
        After login with cookies is successful, this method check if the cookies are not expired.
        
        returns: True if cookies are not expired and re-login/re-auth not require
                 False otherwise
        """

        driver = self.driver_manager.get_driver()

        ## check first critical page (payments)
        try:
            driver.get(self.payment_page)
            WebDriverWait(driver, 10).until(
            EC.url_to_be(
            "https://www.homedepot.com/auth/view/signin?redirect=/myaccount/payments"))

            signin_header = driver.find_element(
                By.CSS_SELECTOR,
                "p[data-automation-id='signInHeader']").text
            security_text = driver.find_element(
                By.CLASS_NAME,
                "u__bold.u__medium").text

            if (signin_header == "Sign In or Create an Account" or
                security_text == "For your security, please sign in again."):
                pass # passing here coz i'll need to check a 2nd critical page

        except TimeoutException: # means (cookies not expired nd login not prompted for)
            pass # passing here coz i'll need to check a 2nd critical page
        except NoSuchElementException as error:
            pass


        ## check second critical page (security)
        try:
            driver.get(self.security_page)
            WebDriverWait(driver, 10).until(
                EC.url_to_be(
                "https://www.homedepot.com/auth/view/signin"))

            signin_header = driver.find_element(
                By.CSS_SELECTOR,
                "p[data-automation-id='signInHeader']").text
            security_text = driver.find_element(
                By.CLASS_NAME,
                "u__bold.u__medium").text

            if (signin_header == "Sign In or Create an Account" or
                security_text == "For your security, please sign in again."):
                if self.quit_driver:
                    driver.quit()
            return False # False: meaning cookies expire and re-login/re-auth necessary

        except TimeoutException: # means (cookies not expired nd login not prompted for)
            driver.get(self.home_page)
            return True
        except NoSuchElementException as error:
            if self.quit_driver:
                driver.quit()
            raise CookiesLoginStatusFailed(
                "Login with cookies expiration status check fails") from error


    def logout_with_cookies(self):
        """  A method used to logout after a cookie login """
        driver = self.driver_manager.get_driver()

        return self.logout.logout(driver=driver)