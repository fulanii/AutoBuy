""" imports """
import os

def get_chrome_driver_path() -> str:
    """Returns chrome driver depending on the development enviroment"""

    if 'CI' in os.environ:
        chrome_driver_path = '/usr/local/bin/chromedriver'
    else:
        chrome_driver_path = '/Users/daboii/Documents/Programming/chrome-driver/chromedriver_119'
    return chrome_driver_path
