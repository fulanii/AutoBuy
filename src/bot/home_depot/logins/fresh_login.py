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


class FreshLogin:
    """ 
    A class to login homdepot website with an email and a password

    arg:
        email:str
        password:str
        maximize_window:bool default False (to maximize the selenium window)
        headless: bool set to True to not show the chrome browser (default False)
        detach: bool set to True to not quit the chrome browser (default True)
        quit_diver:bool To auto quit driver (default False)

    Function(s):  
        fresh_login(): login using email and password -> dict
        logout_fresh_login(): logout after a fresh login -> bool
        
   """

    home_page:str = "https://www.homedepot.com/"
    login_page:str = "https://www.homedepot.com/auth/view/signin?redirect=/&ref="
    payment_page:str = "https://www.homedepot.com/myaccount/payments"
    security_page:str = "https://www.homedepot.com/account/ui/security"

    def __init__(self, email:str, password:str, quit_driver:bool = False, maximize_window:bool=False, detach:bool=True, headless:bool=False) -> None:
        self.__email:str = email
        self.__password:str = password
        self.driver_manager = DriverManager(maximize_window=maximize_window, detach=detach, headless=headless)
        self.quit_driver = quit_driver
        self.logout = Logout()


    def fresh_login(self) -> dict:
        """
        Login serialize and save the cookies data

        returns: 
            results:dict = {
                "login_status_check": bool,

                "serialization_check": bool,

                "login_and_serialization_check": bool,

                "status_check_fail_amount": int
            }
        """
        driver = self.driver_manager.initialize_driver()

        try:
            driver.get(self.home_page)
            driver.delete_all_cookies()
            driver.refresh()
            my_account = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.MyAccount a#headerMyAccount")))
            my_account.click()

            # find login btn
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="SPSOSignIn"]/a')))
            login_btn.click()
        except TimeoutException:
            driver.get(self.login_page)

        # find username
        user_box = driver.find_element(By.ID, "username")
        user_box.send_keys(self.__email)

        # click continue
        continue_btn = driver.find_element(
            By.CSS_SELECTOR,
            "form button[id='sign-in-button'][data-automation-id='signIn'] ")
        continue_btn.click()

        try:
            # fill password
            driver.implicitly_wait(5)
            password_field = driver.find_element(
                By.CSS_SELECTOR,
                "input#password-input-field")
            password_field.send_keys(self.__password)
        except NoSuchElementException:
            # this is for the no thx diff ways to login btn shown time to time on password page
            no_thx_btn = driver.find_element(By.XPATH, '//*[@id="EZDrawer__container"]/div/div[4]/button')
            no_thx_btn.click()
            
            # fill password again if page above is shown
            driver.implicitly_wait(5)
            password_field = driver.find_element(
                By.CSS_SELECTOR,
                "input#password-input-field")
            password_field.send_keys(self.__password)

        # click login btn
        final_signin_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "form button[data-automation-id='signInSignInButton']")))
        final_signin_btn.click()

        # check 2fa
        try:
            driver.implicitly_wait(10)
            verify_identy = driver.find_element(
                By.CSS_SELECTOR,
                "p[data-automation-id='signInHeader']").text
            # data-automation-id="signInHeader"

            if verify_identy == "Verify Your Identity":
                verify_2fa_sms_btn = driver.find_element(By.ID, "sms-otp-channel")
                verify_2fa_sms_btn.click()

                send_code_btn = driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-automation-id='forgotPasswordSelectionSendCodeButton']")
                send_code_btn.click()

                enter_code_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "input[id='passCode']")))
                ask_me_code = input("What is the sms code: ")
                enter_code_field.send_keys(ask_me_code)

                verify_code_btn = driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-automation-id='TwoFactorAuthVerifyButton']")
                verify_code_btn.click()
        except NoSuchElementException:
            pass

        return self.__fresh_login_status_check()


    def __fresh_login_status_check(self) -> dict:

        """
        This method check if fresh login and serialization is successful

        returns: 
            results:dict = {
                "login_status_check": bool,
                "serialization_check": bool,
                "login_and_serialization_check": bool,
                "status_check_fail_amount": int
            }

        arg: driver
        """
        driver = self.driver_manager.get_driver()
        
        results:dict = {
            "login_status_check": False,
            "serialization_check": False,
            "login_and_serialization_check": False,
            "status_check_fail_amount": 0
        }

        # check login status 1
        try:
            after_login_acc_btn = driver.find_element(
                By.CSS_SELECTOR,
                "#a#headerMyAccount.MyAccount__button[title='My Account']")
            after_login_acc_btn.click()
        except NoSuchElementException:
            results["status_check_fail_amount"] += 1
            pass
        
        # check if sign out available 2
        try:
            signout = driver.find_element(
                By.CSS_SELECTOR,
                "button#signOut.MyAccount__authSignOut[title='Sign Out']").text
        except NoSuchElementException:
            results["status_check_fail_amount"] += 1
            pass

        # check welcome message 3
        try:
            check_login = driver.find_element(
                By.XPATH,
                '//*[@id="headerMyAccountDropdown"]/div/div/p[1]').text
        except NoSuchElementException as error:
            results["status_check_fail_amount"] += 1
            if results["status_check_fail_amount"] >= 3:
                if self.quit_driver:
                    driver.quit()
                raise LoginCheckStatusFailedException(
                "All login check status failed") from error
            else:
                pass

        if (check_login == "Welcome Back!" or
            "Welcome Back!" in driver.page_source or
            signout == "Sign Out"):

            results["login_status_check"] = True # 1
            
            # get session data serialize and store them
            session_data:dict = driver.get_cookies()
            if SessionManager.serialize_session_data(session_data=session_data):
                results["serialization_check"] = True # 2
                results["login_and_serialization_check"] = True # 3
                if self.quit_driver:
                    driver.quit()
                return results

            results["serialization_check"] = False

        if self.quit_driver:
            driver.quit()
        return results


    def logout_fresh_login(self) -> bool:
        """ A method used to logout after fresh login """
        driver = self.driver_manager.get_driver()

        return self.logout.logout(driver=driver)