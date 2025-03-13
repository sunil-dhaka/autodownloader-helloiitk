"""
Configuration settings and constants for the Hello IITK downloader application.
"""
from typing import Dict, Any

# API URLs
BASE_URL = "https://hello.iitk.ac.in"
LOGIN_URL = f"{BASE_URL}/user/login"
COURSES_URL = f"{BASE_URL}/index.php/courses"

# Default options for PDF conversion
DEFAULT_PDF_OPTIONS: Dict[str, Any] = {
    'page-size': 'Letter',
    'margin-top': '0.01in',
    'margin-right': '0.75in',
    'margin-bottom': '0.01in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'javascript-delay': '5000'  # give time to render JavaScript
}

# Default CSS file path
CSS_FILE = "main.css"

# File naming
QUIZ_TITLE_PREFIX = ""
ASSIGNMENT_TITLE_PREFIX = ""

# YouTube download options
DEFAULT_YOUTUBE_OPTIONS: Dict[str, Any] = {
    'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
    'vcodec': 'avc1.4d401e'
}