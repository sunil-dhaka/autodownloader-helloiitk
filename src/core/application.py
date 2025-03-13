"""
Base application coordinator for Hello IITK Auto Downloader.
"""
from typing import Optional, Dict, Any, List

from src.core.auth import Authenticator, Credentials, get_credentials_from_user
from src.core.course import CourseManager, Course
from src.utils.cli import select_course


class Application:
    """
    Base application class that coordinates components and workflow.
    
    This class serves as a central coordinator for the application,
    managing authentication, course selection, and other core functionality.
    """
    
    def __init__(self):
        """Initialize the application components."""
        self.auth = Authenticator()
        self.course_manager: Optional[CourseManager] = None
        self.selected_course: Optional[Course] = None
        
    def authenticate(self, credentials: Optional[Credentials] = None) -> bool:
        """
        Authenticate the user.
        
        Parameters
        ----------
        credentials : Optional[Credentials], optional
            User credentials, if None will prompt user for input, by default None
            
        Returns
        -------
        bool
            True if authentication was successful
        """
        if credentials is None:
            credentials = get_credentials_from_user()
            
        try:
            self.auth.login(credentials)
            print("Successfully logged into the session.")
            return True
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False
    
    def initialize_course_manager(self) -> bool:
        """
        Initialize the course manager after authentication.
        
        Returns
        -------
        bool
            True if the course manager was successfully initialized
        """
        if not self.auth.is_authenticated:
            print("You must authenticate before initializing the course manager.")
            return False
            
        try:
            self.course_manager = CourseManager(self.auth)
            print(f"Found {len(self.course_manager.courses)} courses.")
            return True
        except Exception as e:
            print(f"Error initializing course manager: {str(e)}")
            return False
    
    def select_course(self) -> Optional[Course]:
        """
        Let the user select a course.
        
        Returns
        -------
        Optional[Course]
            The selected course or None if selection failed
        """
        if not self.course_manager or not self.course_manager.courses:
            print("No courses available. Please initialize the course manager first.")
            return None
            
        try:
            course_id = select_course(self.course_manager.courses)
            self.selected_course = self.course_manager.get_course_by_id(course_id)
            
            if self.selected_course:
                print(f"Selected course: {self.selected_course.name}")
                return self.selected_course
            else:
                print(f"Course with ID {course_id} not found.")
                return None
        except Exception as e:
            print(f"Error during course selection: {str(e)}")
            return None
    
    def run(self) -> bool:
        """
        Run the main application flow.
        
        Returns
        -------
        bool
            True if the application completed successfully
        """
        if not self.authenticate():
            return False
            
        if not self.initialize_course_manager():
            return False
            
        if not self.select_course():
            return False
            
        return True