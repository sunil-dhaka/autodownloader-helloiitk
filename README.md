# Hello IITK Auto Downloader

A modular application that automates resources (videos, PDFs, quizzes, assignments, forums) downloading and processing from the Hello IITK website.

## Features

- **Resource Downloader**: Download lecture videos, supplementary materials, and other resources
- **Quiz & Assignment Processor**: Convert quizzes and assignments to HTML and PDF formats
- **Forums Scraper**: Extract forum posts data and save as CSV
- **Smart Downloads**: Only downloads files that haven't been downloaded before
- **YouTube Integration**: Handles both direct video URLs and YouTube embedded videos
- **PDF Conversion**: Converts quizzes to well-formatted PDFs with proper LaTeX rendering

## Project Structure

The project has been refactored following SOLID principles and organized into modules:

```
.
├── download.py             # Entry point for resource downloader
├── quiz_scraper.py         # Entry point for quiz & assignment scraper
├── forums_scraper.py       # Entry point for forums scraper
├── README.md               # This documentation
├── requirements.txt        # Dependencies
├── main.css                # Styling for HTML output
└── src/                    # Source code directory
    ├── core/               # Core application components
    │   ├── application.py  # Base application class
    │   ├── auth.py         # Authentication module
    │   ├── course.py       # Course management
    │   ├── downloader_app.py # Downloader application
    │   ├── forums_app.py   # Forums application
    │   └── quiz_app.py     # Quiz application
    ├── converters/         # Data format converters
    │   ├── html_formatter.py # HTML generation
    │   └── pdf_converter.py # PDF conversion
    ├── downloaders/        # Download components
    │   ├── base.py         # Base downloader interface
    │   ├── manager.py      # Download manager
    │   └── youtube.py      # YouTube downloader
    ├── scrapers/           # Data scrapers
    │   ├── base.py         # Base scraper class
    │   ├── forums.py       # Forums scraper
    │   ├── lectures.py     # Lecture resources scraper
    │   └── quiz_assignment.py # Quiz & assignment scraper
    └── utils/              # Utility functions
        ├── cli.py          # Command line interface utilities
        ├── config.py       # Configuration settings
        └── filesystem.py   # File and directory utilities
```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/autodownloader-helloiitk.git
   cd autodownloader-helloiitk
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Make the scripts executable (optional):
   ```sh
   chmod +x download.py quiz_scraper.py forums_scraper.py
   ```

## Usage

### Download Resources (Videos, PDFs, etc.)

```sh
python download.py
```

Follow the prompts to:
1. Enter your Hello IITK credentials
2. Select a course
3. Choose the resource type (Videos, Resources, Supplementary)

### Process Quizzes & Assignments

```sh
python quiz_scraper.py
```

This will:
1. Fetch all quizzes and assignments for the selected course
2. Convert quizzes to HTML and PDF format with proper LaTeX rendering
3. Save assignment details in JSON format

### Scrape Forum Posts

```sh
python forums_scraper.py
```

This will:
1. Fetch forum posts for the selected course
2. Save the data as a CSV file

## Design Principles

The application has been refactored following these principles:

- **Single Responsibility**: Each class has one job and does it well
- **Open/Closed**: The system is open for extension but closed for modification
- **Liskov Substitution**: Derived classes can be substituted for their base classes
- **Interface Segregation**: Smaller, focused interfaces for specific tasks
- **Dependency Inversion**: High-level modules don't depend on low-level modules

## System Requirements

- Python 3.6+
- wkhtmltopdf (for PDF generation)

## License

MIT License