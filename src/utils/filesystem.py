"""
File system utility functions for directory and file operations.
"""
import os
from typing import List, Optional


def ensure_directory_exists(path: str) -> str:
    """
    Ensure that a directory exists, creating it if needed.
    
    Parameters
    ----------
    path : str
        Path to the directory
        
    Returns
    -------
    str
        The absolute path to the directory
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    elif not os.path.isdir(abs_path):
        raise NotADirectoryError(f"{abs_path} exists but is not a directory")
    
    return abs_path


def change_to_directory(path: str) -> str:
    """
    Change the current working directory, creating it if needed.
    
    Parameters
    ----------
    path : str
        Path to the directory
        
    Returns
    -------
    str
        The absolute path to the directory
    """
    abs_path = ensure_directory_exists(path)
    os.chdir(abs_path)
    return abs_path


def get_existing_files(path: Optional[str] = None, 
                       extension: Optional[str] = None) -> List[str]:
    """
    Get a list of existing files in a directory, optionally filtered by extension.
    
    Parameters
    ----------
    path : str, optional
        Path to the directory, defaults to current directory
    extension : str, optional
        File extension to filter by (e.g., ".mp4"), defaults to None
        
    Returns
    -------
    List[str]
        List of file names in the directory that are not empty
    """
    directory = path if path is not None else os.getcwd()
    
    files = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            if extension is None or file_name.endswith(extension):
                files.append(file_name)
    
    return files


def setup_course_directory(base_dir: str, course_id: str) -> str:
    """
    Set up and navigate to a course directory.
    
    Parameters
    ----------
    base_dir : str
        Base directory for all courses
    course_id : str
        Course ID used for the directory name
        
    Returns
    -------
    str
        The absolute path to the course directory
    """
    course_dir = os.path.join(base_dir, course_id.upper())
    return change_to_directory(course_dir)


def setup_resource_directory(course_dir: str, resource_type: str) -> str:
    """
    Set up and navigate to a resource directory within a course directory.
    
    Parameters
    ----------
    course_dir : str
        Course directory path
    resource_type : str
        Type of resource (e.g., "Videos", "Resources")
        
    Returns
    -------
    str
        The absolute path to the resource directory
    """
    resource_dir = os.path.join(course_dir, resource_type)
    return change_to_directory(resource_dir)