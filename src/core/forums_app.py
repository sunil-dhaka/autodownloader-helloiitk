"""
Forums application for Hello IITK Auto Downloader.
"""
import os
from typing import Optional, List, Dict, Any

from src.core.application import Application
from src.scrapers.forums import ForumsScraper
from src.utils.filesystem import setup_course_directory
from src.utils.cli import get_folder_name


class ForumsApplication(Application):
    """
    Application class for managing forum posts data.
    
    This class extends the base Application and adds functionality
    for fetching and saving forum posts data.
    """
    
    def __init__(self):
        """Initialize the forums application."""
        super().__init__()
        self.forums_scraper: Optional[ForumsScraper] = None
        self.course_dir: Optional[str] = None
        self.forums_dir: Optional[str] = None
        
    def initialize_scrapers(self) -> bool:
        """
        Initialize scrapers after course selection.
        
        Returns
        -------
        bool
            True if scrapers were successfully initialized
        """
        if not self.selected_course:
            print("No course selected. Please select a course first.")
            return False
            
        try:
            self.forums_scraper = ForumsScraper(self.auth, self.selected_course)
            return True
        except Exception as e:
            print(f"Error initializing scrapers: {str(e)}")
            return False
            
    def setup_directories(self) -> bool:
        """
        Set up directories for forum data.
        
        Returns
        -------
        bool
            True if directories were successfully set up
        """
        try:
            # Prompt for folder name
            folder_name = get_folder_name() or self.selected_course.course_id.upper()
            
            # Set up course directory
            self.course_dir = setup_course_directory(os.getcwd(), folder_name)
            
            return True
        except Exception as e:
            print(f"Error setting up directories: {str(e)}")
            return False
            
    def process_forums(self, max_pages: int = 10) -> bool:
        """
        Process forum data - fetch and save.
        
        Parameters
        ----------
        max_pages : int, optional
            Maximum number of pages to fetch, by default 10
            
        Returns
        -------
        bool
            True if forums were successfully processed
        """
        if not self.forums_scraper or not self.course_dir:
            print("Forums scraper and course directory must be initialized before processing forums.")
            return False
            
        try:
            print(f"Fetching forum data for course {self.selected_course.course_id}...")
            forums_data = self.forums_scraper.fetch_data(max_pages)
            
            if not forums_data:
                print(f"No forum posts found for course {self.selected_course.course_id}.")
                return False
                
            print(f"Found {len(forums_data)} forum posts. Saving to CSV...")
            csv_path = self.forums_scraper.save_to_csv(forums_data, self.course_dir)
            
            if csv_path:
                print(f"Forum data saved to {csv_path}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error processing forum data: {str(e)}")
            return False
            
    def run(self) -> bool:
        """
        Run the forums application workflow.
        
        Returns
        -------
        bool
            True if the application completed successfully
        """
        # Run base application flow (authenticate, initialize course manager, select course)
        if not super().run():
            return False
            
        # Initialize scrapers
        if not self.initialize_scrapers():
            return False
            
        # Set up directories
        if not self.setup_directories():
            return False
            
        # Process forums
        return self.process_forums()