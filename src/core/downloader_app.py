"""
Downloader application for Hello IITK Auto Downloader.
"""
import os
from typing import Optional, List, Dict, Any

from src.core.application import Application
from src.scrapers.lectures import LecturesScraper
from src.downloaders.manager import DownloadManager
from src.utils.cli import select_resource_type
from src.utils.filesystem import (
    setup_course_directory, 
    setup_resource_directory, 
    get_existing_files
)


class DownloaderApplication(Application):
    """
    Application class for downloading course resources.
    
    This class extends the base Application and adds functionality
    for selecting and downloading different types of resources.
    """
    
    def __init__(self):
        """Initialize the downloader application."""
        super().__init__()
        self.download_manager = DownloadManager()
        self.lectures_scraper: Optional[LecturesScraper] = None
        self.resource_type: Optional[str] = None
        self.course_dir: Optional[str] = None
        self.resource_dir: Optional[str] = None
        
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
            self.lectures_scraper = LecturesScraper(self.auth, self.selected_course)
            return True
        except Exception as e:
            print(f"Error initializing scrapers: {str(e)}")
            return False
            
    def select_resource_type(self) -> bool:
        """
        Let the user select a resource type.
        
        Returns
        -------
        bool
            True if a resource type was successfully selected
        """
        try:
            self.resource_type = select_resource_type()
            print(f"Selected resource type: {self.resource_type}")
            return True
        except Exception as e:
            print(f"Error during resource type selection: {str(e)}")
            return False
            
    def setup_directories(self) -> bool:
        """
        Set up directories for the selected course and resource type.
        
        Returns
        -------
        bool
            True if directories were successfully set up
        """
        if not self.selected_course or not self.resource_type:
            print("Course and resource type must be selected before setting up directories.")
            return False
            
        try:
            # Set up course directory
            self.course_dir = setup_course_directory(os.getcwd(), self.selected_course.course_id)
            
            # Set up resource directory
            self.resource_dir = setup_resource_directory(self.course_dir, self.resource_type)
            
            return True
        except Exception as e:
            print(f"Error setting up directories: {str(e)}")
            return False
            
    def download_resources(self) -> bool:
        """
        Download resources of the selected type.
        
        Returns
        -------
        bool
            True if resources were successfully downloaded
        """
        if not self.lectures_scraper or not self.resource_type:
            print("Scrapers and resource type must be initialized before downloading.")
            return False
            
        try:
            print(f"Getting {self.resource_type} data...")
            download_items = self.lectures_scraper.get_download_items(self.resource_type)
            
            if not download_items:
                print(f"No {self.resource_type} found for course {self.selected_course.course_id}.")
                return False
                
            print(f"Found {len(download_items)} {self.resource_type} to download.")
            
            # Get existing files to avoid re-downloading
            existing_files = get_existing_files()
            
            # Download the files
            print(f"Downloading {self.resource_type} for {self.selected_course.course_id}. Press `Ctrl+C` to stop.")
            results = self.download_manager.download_items(download_items, existing_files)
            
            # Count successful downloads
            success_count = sum(1 for success in results.values() if success)
            print(f"Successfully downloaded {success_count} out of {len(download_items)} {self.resource_type}.")
            
            return True
        except Exception as e:
            print(f"Error downloading resources: {str(e)}")
            return False
            
    def run(self) -> bool:
        """
        Run the downloader application workflow.
        
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
            
        # Select resource type
        if not self.select_resource_type():
            return False
            
        # Set up directories
        if not self.setup_directories():
            return False
            
        # Download resources
        return self.download_resources()