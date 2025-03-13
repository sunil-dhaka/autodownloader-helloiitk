"""
Quiz and Assignment application for Hello IITK Auto Downloader.
"""
import os
from typing import Optional, List, Dict, Any

from src.core.application import Application
from src.scrapers.quiz_assignment import QuizAssignmentScraper
from src.converters.html_formatter import HtmlFormatter
from src.converters.pdf_converter import PdfConverter
from src.utils.filesystem import setup_course_directory


class QuizApplication(Application):
    """
    Application class for managing quiz and assignment data.
    
    This class extends the base Application and adds functionality
    for fetching, converting, and saving quiz and assignment data.
    """
    
    def __init__(self):
        """Initialize the quiz application."""
        super().__init__()
        self.quiz_scraper: Optional[QuizAssignmentScraper] = None
        self.pdf_converter = PdfConverter()
        self.course_dir: Optional[str] = None
        self.quizzes_dir: Optional[str] = None
        
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
            self.quiz_scraper = QuizAssignmentScraper(self.auth, self.selected_course)
            return True
        except Exception as e:
            print(f"Error initializing scrapers: {str(e)}")
            return False
            
    def setup_directories(self) -> bool:
        """
        Set up directories for quizzes and assignments.
        
        Returns
        -------
        bool
            True if directories were successfully set up
        """
        try:
            # Set up course directory
            self.course_dir = setup_course_directory(os.getcwd(), self.selected_course.course_id)
            
            # Set up quiz directory
            self.quizzes_dir = os.path.join(self.course_dir, "Quizzes")
            os.makedirs(self.quizzes_dir, exist_ok=True)
            os.chdir(self.quizzes_dir)
            
            return True
        except Exception as e:
            print(f"Error setting up directories: {str(e)}")
            return False
            
    def process_quizzes(self) -> bool:
        """
        Process quiz data - fetch, convert to HTML and PDF.
        
        Returns
        -------
        bool
            True if quizzes were successfully processed
        """
        if not self.quiz_scraper:
            print("Quiz scraper must be initialized before processing quizzes.")
            return False
            
        try:
            print("Fetching quiz data...")
            quizzes = self.quiz_scraper.fetch_quizzes()
            
            if not quizzes:
                print(f"No quizzes found for course {self.selected_course.course_id}.")
                self.quiz_scraper.save_data_to_file(
                    {"response": f"No Quiz data Found for course {self.selected_course.course_id}"}, 
                    os.path.join(self.quizzes_dir, "quizzes-summary.json")
                )
                return True
                
            print(f"Found {len(quizzes)} quizzes. Processing...")
            self.quiz_scraper.save_data_to_file(quizzes, "quizzes-summary.json")
            
            for quiz in quizzes:
                qid = quiz.get('qid')
                if qid:
                    # Fetch quiz details
                    quiz_data = self.quiz_scraper.fetch_quiz_details(qid)
                    
                    # Get title for the quiz
                    quiz_title = self._format_title(quiz_data.get('quiz', {}).get('title', 'No-Title'))
                    
                    # Save JSON data
                    self.quiz_scraper.save_data_to_file(quiz_data, f"{quiz_title}.json")
                    
                    # Convert to HTML
                    html_content = HtmlFormatter.format_quiz_to_html(quiz_data)
                    
                    # Save HTML file
                    html_file = f"{quiz_title}.html"
                    with open(html_file, 'w') as f:
                        f.write(html_content)
                    
                    # Convert to PDF
                    try:
                        self.pdf_converter.convert_html_file(html_file)
                        print(f"Successfully created {quiz_title}.pdf")
                    except Exception as pdf_err:
                        print(f"Error converting quiz to PDF: {str(pdf_err)}")
            
            return True
        except Exception as e:
            print(f"Error processing quizzes: {str(e)}")
            return False
            
    def process_assignments(self) -> bool:
        """
        Process assignment data - fetch and save.
        
        Returns
        -------
        bool
            True if assignments were successfully processed
        """
        if not self.quiz_scraper:
            print("Quiz scraper must be initialized before processing assignments.")
            return False
            
        try:
            print("Fetching assignment data...")
            assignments = self.quiz_scraper.fetch_assignments()
            
            if not assignments:
                print(f"No assignments found for course {self.selected_course.course_id}.")
                self.quiz_scraper.save_data_to_file(
                    {"response": f"No assignment data Found for course {self.selected_course.course_id}"}, 
                    "assignments-summary.json"
                )
                return True
                
            print(f"Found {len(assignments)} assignments. Processing...")
            self.quiz_scraper.save_data_to_file(assignments, "assignments-summary.json")
            
            # Process each assignment
            self.quiz_scraper.save_assignment_data(self.quizzes_dir)
            
            return True
        except Exception as e:
            print(f"Error processing assignments: {str(e)}")
            return False
            
    def _format_title(self, title: str) -> str:
        """
        Format a title for use in filenames.
        
        Parameters
        ----------
        title : str
            Original title
            
        Returns
        -------
        str
            Formatted title
        """
        return "-".join(title.lower().split())
            
    def run(self) -> bool:
        """
        Run the quiz application workflow.
        
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
            
        # Process quizzes
        quiz_success = self.process_quizzes()
        
        # Process assignments
        assignment_success = self.process_assignments()
        
        return quiz_success or assignment_success