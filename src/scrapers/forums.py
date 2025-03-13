"""
Scraper for forum posts data.
"""
from typing import List, Dict, Any
import pandas as pd
import os

from src.scrapers.base import BaseScraper


class ForumsScraper(BaseScraper):
    """
    Scraper for course forum posts.
    """
    
    def fetch_data(self, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch forum posts data.
        
        Parameters
        ----------
        max_pages : int, optional
            Maximum number of pages to fetch, by default 10
            
        Returns
        -------
        List[Dict[str, Any]]
            List of forum posts
        """
        forums_questions_list = []
        
        for page in range(1, max_pages + 1):
            endpoint = f"forums/fetch/general?pager={page}"
            forums_data = self.make_api_request(endpoint)
            
            if len(forums_data.get('data', [])) > 0:
                for question in forums_data['data']:
                    forums_questions_list.append({
                        'title': question.get('title', ''),
                        'desc': question.get('description', ''),
                        'username': question.get('username', '')
                    })
                    
                print(f"Questions so far: {len(forums_questions_list)} -- page no: {page}")
            else:
                break
                
        return forums_questions_list
        
    def save_to_csv(self, data: List[Dict[str, Any]], output_path: str) -> str:
        """
        Save forum posts data to a CSV file.
        
        Parameters
        ----------
        data : List[Dict[str, Any]]
            List of forum posts
        output_path : str
            Path to save the CSV file
            
        Returns
        -------
        str
            Path to the saved CSV file
        """
        if not data:
            print("No forum data to save.")
            return ""
            
        df = pd.DataFrame(data)
        csv_path = os.path.join(output_path, "forums.csv")
        
        df.to_csv(csv_path, index=False)
        print(f"Forums data saved to {csv_path}")
        
        return csv_path