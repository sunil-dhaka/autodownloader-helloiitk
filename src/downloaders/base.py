"""
Base downloader classes and interfaces.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import requests
from tqdm import tqdm


@dataclass
class DownloadItem:
    """
    Data class representing a file to be downloaded.
    
    Parameters
    ----------
    file_name : str
        Name to save the file as
    file_url : str
        URL to download the file from
    """
    file_name: str
    file_url: str


class Downloader(ABC):
    """
    Abstract base class for file downloaders.
    
    This class defines the interface all downloaders must implement.
    """
    
    @abstractmethod
    def download(self, item: DownloadItem) -> bool:
        """
        Download a file.
        
        Parameters
        ----------
        item : DownloadItem
            The file details to download
            
        Returns
        -------
        bool
            True if download was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def can_handle(self, item: DownloadItem) -> bool:
        """
        Check if this downloader can handle the given item.
        
        Parameters
        ----------
        item : DownloadItem
            The item to check
            
        Returns
        -------
        bool
            True if this downloader can handle the item
        """
        pass


class HttpDownloader(Downloader):
    """
    Downloader implementation for HTTP downloads using requests library.
    """
    
    def can_handle(self, item: DownloadItem) -> bool:
        """
        Check if this downloader can handle the given item.
        
        This downloader handles all HTTP/HTTPS URLs that are not YouTube videos.
        
        Parameters
        ----------
        item : DownloadItem
            The item to check
            
        Returns
        -------
        bool
            True if this downloader can handle the item
        """
        url_lower = item.file_url.lower()
        return (url_lower.startswith("http") and 
                "youtube.com" not in url_lower and 
                "youtu.be" not in url_lower)
    
    def download(self, item: DownloadItem) -> bool:
        """
        Download a file via HTTP/HTTPS.
        
        Parameters
        ----------
        item : DownloadItem
            The file to download
            
        Returns
        -------
        bool
            True if download was successful, False otherwise
        """
        try:
            response = requests.get(item.file_url, stream=True)
            
            if response.status_code != 200:
                print(f"Failed to download {item.file_name}: HTTP {response.status_code}")
                return False
                
            total_size = int(response.headers.get('Content-Length', 0))
            
            with open(item.file_name, 'wb') as file:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=item.file_name,
                    ascii=True
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))
                            
            print(f"Completed downloading {item.file_name}.")
            return True
            
        except Exception as e:
            print(f"Error downloading {item.file_name}: {str(e)}")
            return False