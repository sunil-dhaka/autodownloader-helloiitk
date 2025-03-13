#!/usr/bin/env python
"""
Main entry point for the Hello IITK Auto Downloader.

This script allows users to download videos and resources from Hello IITK courses.
"""
import sys
from src.core.downloader_app import DownloaderApplication


def main() -> int:
    """
    Run the Hello IITK Auto Downloader application.
    
    Returns
    -------
    int
        Exit code: 0 for success, 1 for failure
    """
    print("=" * 80)
    print("Hello IITK Auto Downloader".center(80))
    print("=" * 80)
    
    app = DownloaderApplication()
    success = app.run()
    
    if success:
        print("\nDownload process completed successfully.")
        return 0
    else:
        print("\nDownload process encountered errors.")
        return 1
    
    
if __name__ == '__main__':
    sys.exit(main())