import configparser
import os

file = configparser.ConfigParser()
file_path = os.path.join(os.path.dirname(__file__), 'secrets.ini')
file.read(file_path)  

email = file.get('Credentials', 'email')
password = file.get('Credentials', 'password')

def secrets() -> dict:
    """returns username and password"""
    return {"email": email, "password": password}




# This how to write credentials to ini file
# config = configparser.ConfigParser()
# config['Credentials'] = {
#     'email': 'new_email@example.com',
#     'password': 'new_password'
# }

# with open('credentials.ini', 'w') as configfile:
#     config.write(configfile)
