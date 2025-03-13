"""
Scraper for lecture videos and resources.
"""
from typing import List, Dict, Any

from src.scrapers.base import BaseScraper
from src.downloaders.base import DownloadItem


class LecturesScraper(BaseScraper):
    """
    Scraper for lecture videos and associated resources.
    """
    
    def fetch_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch lecture data including videos and resources.
        
        Returns
        -------
        Dict[str, List[Dict[str, Any]]]
            Dictionary with keys 'videos' and 'resources' containing lists of items
        """
        data = self.make_api_request("lectures/summary")
        
        videos_list = []
        resources_list = []
        
        if len(data) > 0:
            for i, lec in enumerate(data):
                # Extract video
                if self._has_video(lec):
                    video_item = self._extract_video(i, lec)
                    videos_list.append(video_item)
                    
                # Extract resources
                if 'resources' in lec and len(lec['resources']) > 0:
                    resources_list.extend(lec['resources'])
                    
        return {
            'videos': videos_list,
            'resources': resources_list
        }
    
    def fetch_supplementary_resources(self) -> List[Dict[str, Any]]:
        """
        Fetch supplementary resources data.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of supplementary resources
        """
        supp_data = self.make_api_request("resources")
        
        supp_list = []
        if len(supp_data) > 0:
            for data in supp_data:
                if 'resources' in data:
                    supp_list.extend(data['resources'])
                    
        return supp_list
    
    def _has_video(self, lecture: Dict[str, Any]) -> bool:
        """
        Check if a lecture has a video.
        
        Parameters
        ----------
        lecture : Dict[str, Any]
            Lecture data
            
        Returns
        -------
        bool
            True if the lecture has a video
        """
        return (lecture.get('videoURL') is not None or 
                (lecture.get('videosUploaded') is not None and 
                 len(lecture.get('videosUploaded', [])) > 0))
    
    def _extract_video(self, index: int, lecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract video information from lecture data.
        
        Parameters
        ----------
        index : int
            Lecture index for file naming
        lecture : Dict[str, Any]
            Lecture data
            
        Returns
        -------
        Dict[str, Any]
            Video information
        """
        title = lecture.get('title', 'noTitle')
        file_name = f"{index + 1}_{'-'.join(title.split(' '))}.mp4"
        
        if lecture['videoURL'] is None:
            if len(lecture['videosUploaded']) > 0:
                file_url = lecture['videosUploaded'][-1]['path']
            else:
                return None
        else:
            file_url = lecture['videoURL']
            
        return {
            'fileName': file_name,
            'fileURL': file_url
        }
        
    def get_download_items(self, type_name: str) -> List[DownloadItem]:
        """
        Get download items for the specified content type.
        
        Parameters
        ----------
        type_name : str
            Content type: "Videos", "Resources", or "Supp"
            
        Returns
        -------
        List[DownloadItem]
            List of download items
        """
        if type_name == "Videos":
            data = self.fetch_data()
            items = data['videos']
        elif type_name == "Resources":
            data = self.fetch_data()
            items = data['resources']
        elif type_name == "Supp":
            items = self.fetch_supplementary_resources()
        else:
            raise ValueError(f"Unknown resource type: {type_name}")
            
        return [
            DownloadItem(
                file_name=item['fileName'],
                file_url=item['fileURL']
            )
            for item in items
        ]