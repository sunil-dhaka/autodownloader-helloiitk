"""
Download manager for coordinating multiple downloaders.
"""
from typing import List, Dict, Any, Optional

from src.downloaders.base import Downloader, DownloadItem
from src.downloaders.youtube import YouTubeDownloader
from src.downloaders.base import HttpDownloader


class DownloadManager:
    """
    Manager class that coordinates multiple downloaders.
    
    This class selects the appropriate downloader for each item
    and keeps track of download progress.
    """
    
    def __init__(self):
        """Initialize with default downloaders."""
        self.downloaders: List[Downloader] = [
            YouTubeDownloader(),
            HttpDownloader()
        ]
        
    def add_downloader(self, downloader: Downloader) -> None:
        """
        Add a new downloader to the manager.
        
        Parameters
        ----------
        downloader : Downloader
            The downloader to add
        """
        self.downloaders.append(downloader)
        
    def download_item(self, item: DownloadItem) -> bool:
        """
        Download a single item using an appropriate downloader.
        
        Parameters
        ----------
        item : DownloadItem
            The item to download
            
        Returns
        -------
        bool
            True if download was successful, False otherwise
        """
        for downloader in self.downloaders:
            if downloader.can_handle(item):
                return downloader.download(item)
                
        print(f"No suitable downloader found for {item.file_name}")
        return False
        
    def download_items(self, items: List[DownloadItem],
                      existing_files: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Download multiple items, skipping existing files.
        
        Parameters
        ----------
        items : List[DownloadItem]
            List of items to download
        existing_files : List[str], optional
            List of existing file names to skip, by default None
            
        Returns
        -------
        Dict[str, bool]
            Dictionary of file names and whether they were successfully downloaded
        """
        existing = set(existing_files or [])
        results: Dict[str, bool] = {}
        
        for item in items:
            if item.file_name in existing:
                print(f"Already downloaded... {item.file_name}")
                results[item.file_name] = True
                continue
                
            results[item.file_name] = self.download_item(item)
            
        return results