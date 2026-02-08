"""
YouTube Client Module
Handles YouTube search and playlist extraction
"""

import os
import sys
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple
from googleapiclient.discovery import build


@dataclass
class YouTubeMatch:
    """Represents a YouTube video match for a track"""
    video_id: str
    title: str
    channel: str
    thumbnail_url: str
    duration: str
    url: str
    
    @classmethod
    def from_search_result(cls, item: dict) -> 'YouTubeMatch':
        """Create YouTubeMatch from YouTube API search result"""
        video_id = item['id']['videoId']
        snippet = item['snippet']
        
        # Get the best quality thumbnail available
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url', '')
        )
        
        return cls(
            video_id=video_id,
            title=snippet['title'],
            channel=snippet['channelTitle'],
            thumbnail_url=thumbnail_url,
            duration='',  # Duration requires additional API call
            url=f"https://www.youtube.com/watch?v={video_id}"
        )


@dataclass
class YouTubeVideo:
    """Represents a video from a YouTube playlist"""
    url: str
    title: str


class YouTubeClient:
    """Handles YouTube search and playlist extraction"""
    
    # Approximate API quota costs
    SEARCH_COST = 100  # Each search costs ~100 units
    DAILY_QUOTA = 10000  # Default daily quota
    
    def __init__(self, api_key: str = None):
        """
        Initialize YouTube client with API key
        
        Args:
            api_key: YouTube Data API key (uses env var if not provided)
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        
        if not self.api_key:
            raise ValueError("YouTube API key not found. Set YOUTUBE_API_KEY environment variable.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self._quota_used = 0
    
    @property
    def quota_used(self) -> int:
        """Get estimated quota used in this session"""
        return self._quota_used
    
    @property
    def quota_remaining(self) -> int:
        """Get estimated remaining quota"""
        return max(0, self.DAILY_QUOTA - self._quota_used)
    
    def reset_quota_counter(self):
        """Reset the quota counter (call at start of new day)"""
        self._quota_used = 0
    
    def search_track(
        self, 
        song_name: str, 
        artist: str, 
        keyword: str = "Lyrics",
        max_results: int = 3
    ) -> List[YouTubeMatch]:
        """
        Search YouTube for a track and return multiple matches
        
        Args:
            song_name: Name of the song
            artist: Artist name
            keyword: Search keyword (Lyrics, Visualizer, Official Audio, etc.)
            max_results: Number of results to return (default 3 for alternatives)
            
        Returns:
            List of YouTubeMatch objects (up to max_results)
        """
        # Build search query - only append keyword if it's not "None" or empty
        if keyword and keyword.lower() != "none":
            query = f"{song_name} {artist} {keyword}"
        else:
            query = f"{song_name} {artist}"
        
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results,
                videoCategoryId="10"  # Music category
            )
            response = request.execute()
            
            # Track quota usage
            self._quota_used += self.SEARCH_COST
            
            matches = []
            for item in response.get('items', []):
                match = YouTubeMatch.from_search_result(item)
                matches.append(match)
            
            return matches
            
        except Exception as e:
            # Return empty list on error, let caller handle it
            return []
    
    def detect_youtube_playlist(self, url: str) -> bool:
        """
        Check if URL is a YouTube playlist
        
        Args:
            url: URL to check
            
        Returns:
            True if it's a YouTube playlist URL
        """
        url_lower = url.lower()
        return ('youtube.com' in url_lower or 'youtu.be' in url_lower) and 'list=' in url_lower
    
    def extract_playlist(self, playlist_url: str) -> Tuple[List[YouTubeVideo], str]:
        """
        Extract all video URLs from a YouTube playlist using yt-dlp
        
        Args:
            playlist_url: The YouTube playlist URL
            
        Returns:
            Tuple of (list of YouTubeVideo, playlist title)
        """
        try:
            # Use yt-dlp to extract playlist information
            cmd = [
                sys.executable,
                '-m', 'yt_dlp',
                '--flat-playlist',
                '--print', 'url',
                '--print', 'title',
                '--no-warnings',
                playlist_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            output_lines = result.stdout.strip().split('\n')
            
            if not output_lines or output_lines[0] == '':
                return [], "Unknown Playlist"
            
            # Parse alternating url/title lines
            videos = []
            for i in range(0, len(output_lines) - 1, 2):
                url = output_lines[i]
                title = output_lines[i + 1] if i + 1 < len(output_lines) else "Unknown"
                videos.append(YouTubeVideo(url=url, title=title))
            
            # Get playlist title
            title_cmd = [
                sys.executable,
                '-m', 'yt_dlp',
                '--flat-playlist',
                '--print', 'playlist_title',
                '--no-warnings',
                playlist_url
            ]
            
            title_result = subprocess.run(
                title_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            playlist_title = title_result.stdout.strip().split('\n')[0] if title_result.stdout.strip() else "YouTube_Playlist"
            
            return videos, playlist_title
            
        except subprocess.CalledProcessError:
            return [], "Unknown Playlist"
        except Exception:
            return [], "Unknown Playlist"
