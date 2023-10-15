"""imports"""

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


class Logout:
    """ 
    A class used to Logout out of HomeDepot
    """

    home_page:str = "https://www.homedepot.com/"
    login_page:str = "https://www.homedepot.com/auth/view/signin?redirect=/&ref="
    payment_page:str = "https://www.homedepot.com/myaccount/payments"
    security_page:str = "https://www.homedepot.com/account/ui/security"

    def __init__(self, quit_driver:bool = False) -> None:
        self.quit_driver = quit_driver


    def logout(self, driver) -> bool:
        """
        This function check to see if still login and then logout 

        returns:
            bool: True if logout is successfully, False if logout fails.
        
        """

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

        except NoSuchElementException:
            pass
        except TimeoutException: # not logout 1
            pass


        ## check second critical page (security)
        try:
            driver.get(Logout.security_page)
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
                return True # already sign out (prob expired cookies)

        except NoSuchElementException:
            return False # some went wrong or already sgin out from expired cookies
        except TimeoutException: # not logout 2
            pass

        try:
            driver.get(self.home_page)
            
            after_login_acc_btn = driver.find_element(
                By.XPATH, '//*[@id="headerMyAccount"]')
            after_login_acc_btn.click()
            
            logout_btn = driver.find_element(By.XPATH, '//*[@id="signOut"]')
            logout_btn.click()
            return True
        
        except:
            return False # some went wrong or already sgin out from expired cookies
