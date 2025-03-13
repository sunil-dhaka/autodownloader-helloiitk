"""
YouTube video downloader implementation.
"""
import youtube_dl
from typing import Dict, Any, Optional

from src.downloaders.base import Downloader, DownloadItem
from src.utils.config import DEFAULT_YOUTUBE_OPTIONS


class YouTubeDownloader(Downloader):
    """
    Downloader implementation for YouTube videos using youtube-dl.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize with optional custom youtube-dl options.
        
        Parameters
        ----------
        options : Dict[str, Any], optional
            Custom options for youtube-dl, by default None
        """
        self.options = options or DEFAULT_YOUTUBE_OPTIONS
    
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
            True if the URL is a YouTube video
        """
        url_lower = item.file_url.lower()
        return "youtu.be" in url_lower or "youtube.com" in url_lower
    
    def download(self, item: DownloadItem) -> bool:
        """
        Download a YouTube video.
        
        Parameters
        ----------
        item : DownloadItem
            The video details to download
            
        Returns
        -------
        bool
            True if download was successful, False otherwise
        """
        try:
            print(f"Downloading YouTube video... {item.file_name}")
            
            # Create a copy of options and set the output template
            ydl_opts = dict(self.options)
            ydl_opts['outtmpl'] = item.file_name
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([item.file_url])
                
            print(f"Completed downloading {item.file_name}.")
            return True
            
        except Exception as e:
            print(f"Error downloading YouTube video {item.file_name}: {str(e)}")
            return False