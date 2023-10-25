""" imports """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from .webdriver_path import get_chrome_driver_path


class DriverManager:
    """
    A class to initialize and use the selenium chrome driver
    
    :headless: bool set to True to not show the chrome browser
    :detach: bool set to True to not quit the chrome browser
    """
    def __init__(self, headless:bool, detach:bool, maximize_window:bool):
        self.driver_service = Service(executable_path=get_chrome_driver_path())
        self.driver = None
        self.headless = headless
        self.detach = detach
        self.maximize_window = maximize_window

    def initialize_driver(self):
        """ initialize the chrome driver """
        options = Options()

        # my options
        if self.headless:
            options.add_argument("--headless")
        options.add_experimental_option("detach", self.detach)
        if get_chrome_driver_path() == "/usr/local/bin/chromedriver":
            options.binary_location = "/opt/google/chrome/chrome"
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        # stealth options
        # options.add_argument("start-maximized") #?
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(service=self.driver_service, options=options)
        if self.maximize_window:
            self.driver.maximize_window()
            
        stealth(self.driver, languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,)
        return self.driver

    def get_driver(self):
        """ returns the driver after initializing it """
        if not self.driver:
            self.driver = self.initialize_driver()
        return self.driver

    def recreate_driver(self):
        """ Recreate the driver instance after its quit"""
        if self.driver:
            self.driver.quit()
        self.driver = self.initialize_driver()
        return self.driver
    