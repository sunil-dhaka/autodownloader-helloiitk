"""
Authentication module for Hello IITK.
"""
import requests
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from src.utils.config import LOGIN_URL

@dataclass
class Credentials:
    """
    Data class to store user credentials.
    
    Parameters
    ----------
    username : str
        Hello IITK username
    password : str
        Hello IITK password
    """
    username: str
    password: str


class AuthenticationError(Exception):
    """Exception raised for authentication failures."""
    pass


class Authenticator:
    """
    Handles user authentication with Hello IITK platform.
    
    This class is responsible for initiating a session, logging in,
    and maintaining authentication tokens.
    """
    
    def __init__(self):
        """Initialize the authenticator with a new session."""
        self.session = requests.Session()
        self.cookies: Dict[str, str] = {}
        self._is_authenticated = False
        
    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return self._is_authenticated and 'uid' in self.cookies and 'token' in self.cookies
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        if not self.is_authenticated:
            return {}
        return {
            'uid': self.cookies['uid'],
            'token': self.cookies['token']
        }
    
    def login(self, credentials: Credentials) -> bool:
        """
        Log in to Hello IITK using the provided credentials.
        
        Parameters
        ----------
        credentials : Credentials
            User credentials for login
            
        Returns
        -------
        bool
            True if login was successful
            
        Raises
        ------
        AuthenticationError
            If login fails
        """
        login_details = {
            'name': credentials.username,
            'pass': credentials.password,
            'form_id': 'user_login_form',
            'op': 'SIGN+IN'
        }
        
        response = self.session.post(LOGIN_URL, data=login_details)
        self.cookies = self.session.cookies.get_dict()
        
        if 'uid' in self.cookies and 'token' in self.cookies:
            self._is_authenticated = True
            return True
        else:
            self.session.cookies.clear()
            self._is_authenticated = False
            raise AuthenticationError("Login failed. Please check your credentials.")
        
    def logout(self) -> None:
        """Log out and clear session data."""
        self.session.cookies.clear()
        self.cookies = {}
        self._is_authenticated = False


def get_credentials_from_user() -> Credentials:
    """
    Prompt user for login credentials.
    
    Returns
    -------
    Credentials
        User credentials from command line input
    """
    print('Enter your hello iitk username:')
    username = input('username: ')
    print('Enter your hello iitk password:')
    password = input('password: ')
    return Credentials(username=username, password=password)