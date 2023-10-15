"""Exceptions that may happen in all autobuy code."""

class LoginFailedException(Exception):
    """Thrown when login fails"""

class DeserializationFailedException(Exception):
    """Thrown when deserialization fails"""

class SerializationFailedException(Exception):
    """Thrown when serialization fails"""

class LoginCheckStatusFailedException(Exception):
    """Trown when login status check fails"""

class CookiesLoginStatusFailed(Exception):
    """Trown when login with cookies status check fails"""

class CookiesLoginPageUrlStatus(Exception):
    """Trown when login with cookies page url check fails"""
