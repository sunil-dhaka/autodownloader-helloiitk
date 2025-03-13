"""
Downloaders package for handling different file download methods.
"""
from src.downloaders.base import Downloader, HttpDownloader, DownloadItem
from src.downloaders.youtube import YouTubeDownloader
from src.downloaders.manager import DownloadManager