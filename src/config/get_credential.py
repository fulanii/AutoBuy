import configparser


config = configparser.ConfigParser()
config.read('secrets.ini')  

email = config.get('Credentials', 'email')
password = config.get('Credentials', 'password')

def secrets() -> dict:
    return {email: password}




# This how to write credentials to ini file
# config = configparser.ConfigParser()
# config['Credentials'] = {
#     'email': 'new_email@example.com',
#     'password': 'new_password'
# }

# with open('credentials.ini', 'w') as configfile:
#     config.write(configfile)
