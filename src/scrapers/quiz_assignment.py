"""
Scraper for quiz and assignment data.
"""
from typing import List, Dict, Any, Optional
import json
import os

from src.scrapers.base import BaseScraper


class QuizAssignmentScraper(BaseScraper):
    """
    Scraper for quiz and assignment data.
    """
    
    def fetch_quizzes(self) -> List[Dict[str, Any]]:
        """
        Fetch all quizzes for the course.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of quiz summary data
        """
        data = self.make_api_request("quiz/summary")
        return data if isinstance(data, list) else []
        
    def fetch_quiz_details(self, quiz_id: str) -> Dict[str, Any]:
        """
        Fetch details for a specific quiz.
        
        Parameters
        ----------
        quiz_id : str
            Quiz ID
            
        Returns
        -------
        Dict[str, Any]
            Quiz details
        """
        return self.make_api_request(f"quiz/{quiz_id}")
        
    def fetch_assignments(self) -> List[Dict[str, Any]]:
        """
        Fetch all assignments for the course.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of assignment summary data
        """
        data = self.make_api_request("assignments/summary")
        return data if isinstance(data, list) else []
        
    def fetch_assignment_details(self, assignment_id: str) -> Dict[str, Any]:
        """
        Fetch details for a specific assignment.
        
        Parameters
        ----------
        assignment_id : str
            Assignment ID
            
        Returns
        -------
        Dict[str, Any]
            Assignment details
        """
        return self.make_api_request(f"assignments/{assignment_id}")
        
    def fetch_assignment_submissions(self, assignment_id: str) -> Dict[str, Any]:
        """
        Fetch submissions for a specific assignment.
        
        Parameters
        ----------
        assignment_id : str
            Assignment ID
            
        Returns
        -------
        Dict[str, Any]
            Assignment submission details
        """
        return self.make_api_request(f"assignments/submissions/{assignment_id}")
    
    def save_quiz_data(self, output_dir: str) -> None:
        """
        Fetch and save all quiz data.
        
        Parameters
        ----------
        output_dir : str
            Directory to save quiz data
        """
        quizzes = self.fetch_quizzes()
        
        if not quizzes:
            print(f"No quizzes found for course {self.course.course_id}.")
            self.save_data_to_file(
                {"response": f"No Quiz data Found for course {self.course.course_id}"}, 
                os.path.join(output_dir, "quizzes-summary.json")
            )
            return
            
        print(f"Total Quizzes Found -- {len(quizzes)}")
        self.save_data_to_file(quizzes, os.path.join(output_dir, "quizzes-summary.json"))
        
        for quiz in quizzes:
            qid = quiz.get('qid')
            if qid is not None:
                quiz_data = self.fetch_quiz_details(qid)
                quiz_title = self._format_title(quiz_data.get('quiz', {}).get('title', 'No-Title'))
                
                # Save quiz data
                self.save_data_to_file(
                    quiz_data, 
                    os.path.join(output_dir, f"{quiz_title}.json")
                )
                
    def save_assignment_data(self, output_dir: str) -> None:
        """
        Fetch and save all assignment data.
        
        Parameters
        ----------
        output_dir : str
            Directory to save assignment data
        """
        assignments = self.fetch_assignments()
        
        if not assignments:
            print(f"No assignments found for course {self.course.course_id}.")
            self.save_data_to_file(
                {"response": f"No assignment data Found for course {self.course.course_id}"}, 
                os.path.join(output_dir, "assignments-summary.json")
            )
            return
            
        print(f"Total Assignments Found -- {len(assignments)}")
        self.save_data_to_file(assignments, os.path.join(output_dir, "assignments-summary.json"))
        
        for assignment in assignments:
            aid = assignment.get('aid')
            if aid is not None:
                # Fetch and save assignment details
                assignment_data = self.fetch_assignment_details(aid)
                assignment_title = self._format_title(assignment.get('title', 'No-Title'))
                
                self.save_data_to_file(
                    assignment_data, 
                    os.path.join(output_dir, f"{assignment_title}.json")
                )
                
                # Fetch and save submission details
                submission_data = self.fetch_assignment_submissions(aid)
                self.save_data_to_file(
                    submission_data, 
                    os.path.join(output_dir, f"{assignment_title}_submission.json")
                )
                
                print(f"Dumped {assignment_title} files")
                
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