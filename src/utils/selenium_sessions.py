""" imports """
import os
import pickle
import time
from datetime import datetime
from .custom_exceptions.exceptions import DeserializationFailedException
from .custom_exceptions.exceptions import SerializationFailedException


class SessionManager:
    """ 
    A class to serialize and deserialize login cookies data

    Functions:  
        serialize_session_data(session_data:dict) -> bool
        
        deserialize_session_data() -> dict
    """

    file_path: str = os.path.join(os.path.dirname(__file__), 'session_data.pkl')


    @staticmethod
    def serialize_session_data(session_data:dict) -> bool:
        """
        Serialize the session data and save it to a file.

        Args:
            session_data:dict The session data to be serialized.

        Returns:
            bool: True if the session data is serialized and saved successfully, 
            raise SerializationFailedException otherwise.
        """

        try:
            with open(SessionManager.file_path, 'wb') as file:
                pickle.dump(session_data, file)
            return True
        except Exception as error:
            raise SerializationFailedException("Serialization failed")from error


    @staticmethod
    def deserialize_session_data() -> dict:
        """
        Deserialize the session data from a file.

        Returns:
            dict: The deserialized session data as a dictionary, or raise a 
            DeserializationFailedException if an error occurs during deserialization.
        """

        try:
            with open(SessionManager.file_path, 'rb') as file:
                data = pickle.load(file)
            return data
        except Exception as error:
            raise DeserializationFailedException("Deserialization failed") from error

    @staticmethod
    def check_session_cookies_exp() -> dict:
        """
        Deserialize and check if the session data are expired.
        
        returns: dict: {
            "expired_cookies": expired_ones,

            "cookies_with_no_expiration": no_expiration_date,

            "valid_cookies": valid_cookies
        }

        """

        # deserrialize and load the cookies data
        cookies:dict = SessionManager.deserialize_session_data()

        expired_ones = []
        valid_cookies:list = []
        no_expiration_date:list = []
        current_time = int(time.time())

        # Check each cookie's expiry and add to the appropiate dict
        for cookie in cookies:
            try:
                expiration = cookie["expiry"]

                if current_time > expiration:
                    cookie["expiry"] = datetime.fromtimestamp(
                        expiration).strftime("%Y-%m-%d %H:%M:%S")
                    expired_ones.append(cookie)
                else:
                    cookie["expiry"] = datetime.fromtimestamp(
                        expiration).strftime("%Y-%m-%d %H:%M:%S")
                    valid_cookies.append(cookie)
            except KeyError:
                no_expiration_date.append(cookie)

        return {"expired_cookies": expired_ones,
                "cookies_with_no_expiration": no_expiration_date,
                "valid_cookies":valid_cookies
                }
