#!/usr/bin/env python
"""
Main entry point for the Hello IITK Forums Scraper.

This script allows users to fetch and save forum posts data from Hello IITK courses.
"""
import sys
from src.core.forums_app import ForumsApplication


def main() -> int:
    """
    Run the Hello IITK Forums Scraper application.
    
    Returns
    -------
    int
        Exit code: 0 for success, 1 for failure
    """
    print("=" * 80)
    print("Hello IITK Forums Scraper".center(80))
    print("=" * 80)
    
    app = ForumsApplication()
    success = app.run()
    
    if success:
        print("\nForum posts scraping completed successfully.")
        return 0
    else:
        print("\nForum posts scraping encountered errors.")
        return 1
    
    
if __name__ == '__main__':
    sys.exit(main())