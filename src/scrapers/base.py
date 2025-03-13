"""
Base scraper classes and interfaces.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json

from src.core.auth import Authenticator
from src.core.course import Course


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers.
    
    This class provides common functionality for scrapers
    and defines the interface they must implement.
    """
    
    def __init__(self, auth: Authenticator, course: Course):
        """
        Initialize with authenticator and course information.
        
        Parameters
        ----------
        auth : Authenticator
            Authenticated authenticator instance
        course : Course
            Course information
        """
        self.auth = auth
        self.course = course
        
    @property
    def api_base(self) -> str:
        """
        Get the base API URL for this course.
        
        Returns
        -------
        str
            Base API URL with course ID
        """
        # The course ID is used with a '21' suffix in API calls
        return f"https://hello.iitk.ac.in/api/{self.course.course_id}21"
    
    def make_api_request(self, endpoint: str) -> Any:
        """
        Make an API request to the specified endpoint.
        
        Parameters
        ----------
        endpoint : str
            API endpoint to request
            
        Returns
        -------
        Any
            JSON response from the API
            
        Raises
        ------
        ValueError
            If authentication is not valid
        ConnectionError
            If the API request fails
        """
        if not self.auth.is_authenticated:
            raise ValueError("Authentication required for API requests")
        
        url = f"{self.api_base}/{endpoint}"
        response = self.auth.session.get(url, headers=self.auth.headers)
        
        if response.status_code != 200:
            raise ConnectionError(f"API request failed: HTTP {response.status_code}")
            
        return response.json()
    
    @abstractmethod
    def fetch_data(self) -> Any:
        """
        Fetch data from the API.
        
        Returns
        -------
        Any
            The fetched data
        """
        pass
        
    def save_data_to_file(self, data: Any, filename: str) -> None:
        """
        Save data to a JSON file.
        
        Parameters
        ----------
        data : Any
            Data to save
        filename : str
            Name of the file to save to
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)