#!/usr/bin/env python
"""
Main entry point for the Hello IITK Quiz & Assignment Scraper.

This script allows users to fetch, format, and convert quiz and assignment data
from Hello IITK courses.
"""
import sys
from src.core.quiz_app import QuizApplication


def main() -> int:
    """
    Run the Hello IITK Quiz & Assignment Scraper application.
    
    Returns
    -------
    int
        Exit code: 0 for success, 1 for failure
    """
    print("=" * 80)
    print("Hello IITK Quiz & Assignment Scraper".center(80))
    print("=" * 80)
    
    app = QuizApplication()
    success = app.run()
    
    if success:
        print("\nQuiz and assignment processing completed successfully.")
        return 0
    else:
        print("\nQuiz and assignment processing encountered errors.")
        return 1
    
    
if __name__ == '__main__':
    sys.exit(main())