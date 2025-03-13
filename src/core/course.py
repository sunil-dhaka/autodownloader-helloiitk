"""
Course module for accessing and managing course information.
"""
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from dataclasses import dataclass

from src.core.auth import Authenticator
from src.utils.config import COURSES_URL


@dataclass
class Course:
    """
    Data class to store course information.
    
    Parameters
    ----------
    name : str
        Course name
    instructor : str
        Course instructor name
    course_id : str
        Course identifier used in API calls
    """
    name: str
    instructor: str
    course_id: str


class CourseManager:
    """
    Handles fetching and managing course information.
    
    This class is responsible for retrieving course lists and
    providing course selection functionality.
    """
    
    def __init__(self, auth: Authenticator):
        """
        Initialize with an authenticator.
        
        Parameters
        ----------
        auth : Authenticator
            An authenticated Authenticator instance
        """
        self.auth = auth
        self._courses: List[Course] = []
        
    @property
    def courses(self) -> List[Course]:
        """
        Get list of courses, fetching if needed.
        
        Returns
        -------
        List[Course]
            List of available courses
        """
        if not self._courses:
            self._fetch_courses()
        return self._courses
    
    def _fetch_courses(self) -> None:
        """
        Fetch course information from IITK website.
        """
        if not self.auth.is_authenticated:
            raise ValueError("Authentication required to fetch courses")
        
        response = self.auth.session.get(COURSES_URL)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to fetch courses: HTTP {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        self._courses = []
        
        for course in soup.find_all('span', class_='field-content'):
            if course.h3 and course.a:
                course_item = Course(
                    name=course.h3.text,
                    instructor=course.a.text.strip().split('\n')[1],
                    course_id=course.a['href'].split('/')[-1][:-2]
                )
                self._courses.append(course_item)
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get course by its ID.
        
        Parameters
        ----------
        course_id : str
            The course ID to look for
            
        Returns
        -------
        Optional[Course]
            The course if found, None otherwise
        """
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None