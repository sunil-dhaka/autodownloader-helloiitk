"""
Command line interface utilities for user interaction.
"""
from typing import List, Dict, Any, Optional, Union
from PyInquirer import prompt

from src.core.course import Course


def select_from_list(message: str, choices: List[str], name: str = "choice") -> str:
    """
    Present a selection list to the user and return their choice.
    
    Parameters
    ----------
    message : str
        The message to display to the user
    choices : List[str]
        List of options to choose from
    name : str, optional
        Name for the selection field, by default "choice"
        
    Returns
    -------
    str
        The selected choice
    """
    questions = [
        {
            'type': 'list',
            'name': name,
            'message': message,
            'choices': choices
        }
    ]
    
    answer = prompt(questions)
    return answer.get(name)


def select_course(courses: List[Course]) -> str:
    """
    Present a course selection menu to the user.
    
    Parameters
    ----------
    courses : List[Course]
        List of available courses
        
    Returns
    -------
    str
        The selected course ID
    """
    choices = [course.course_id for course in courses]
    return select_from_list("Which course?", choices)


def select_resource_type() -> str:
    """
    Present a resource type selection menu to the user.
    
    Returns
    -------
    str
        The selected resource type
    """
    choices = ["Videos", "Resources", "Supp"]
    return select_from_list("Which type of content to download?", choices)


def get_folder_name() -> str:
    """
    Prompt the user for a folder name.
    
    Returns
    -------
    str
        The folder name entered by the user
    """
    return input("Name of the folder where you want to store the files? ")