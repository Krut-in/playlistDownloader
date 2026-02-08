"""
Spotify Client Module
Handles all Spotify API interactions for playlist/album extraction
"""

import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


@dataclass
class TrackInfo:
    """Represents a single track with Spotify metadata"""
    index: int
    name: str
    artists: str
    album: str
    album_art_url: str
    duration_ms: int
    spotify_url: str
    
    @property
    def duration_str(self) -> str:
        """Format duration as mm:ss"""
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"


@dataclass
class PlaylistMeta:
    """Metadata about a Spotify playlist"""
    name: str
    description: str
    owner: str
    total_tracks: int
    image_url: str
    spotify_url: str


@dataclass
class AlbumMeta:
    """Metadata about a Spotify album"""
    name: str
    artists: str
    release_date: str
    total_tracks: int
    image_url: str
    spotify_url: str


class SpotifyClient:
    """Handles all Spotify API interactions"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """
        Initialize Spotify client with credentials
        
        Args:
            client_id: Spotify API client ID (uses env var if not provided)
            client_secret: Spotify API client secret (uses env var if not provided)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify API credentials not found. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
        
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        )
    
    def detect_url_type(self, url: str) -> Optional[str]:
        """
        Detect whether URL is a Spotify playlist or album
        
        Args:
            url: The URL to detect
            
        Returns:
            'playlist', 'album', or None if not a valid Spotify URL
        """
        url_lower = url.lower()
        
        if 'spotify.com' not in url_lower:
            return None
        
        if 'playlist/' in url_lower:
            return 'playlist'
        elif 'album/' in url_lower:
            return 'album'
        
        return None
    
    def extract_playlist(self, url: str) -> Tuple[List[TrackInfo], PlaylistMeta]:
        """
        Extract all tracks from a Spotify playlist
        
        Args:
            url: Spotify playlist URL
            
        Returns:
            Tuple of (list of TrackInfo, PlaylistMeta)
        """
        # Extract playlist ID from URL
        playlist_id = url.split('playlist/')[1].split('?')[0]
        
        # Get playlist metadata
        playlist = self.sp.playlist(playlist_id)
        
        # Get playlist image
        image_url = playlist['images'][0]['url'] if playlist['images'] else ''
        
        meta = PlaylistMeta(
            name=playlist['name'],
            description=playlist.get('description', ''),
            owner=playlist['owner']['display_name'],
            total_tracks=playlist['tracks']['total'],
            image_url=image_url,
            spotify_url=playlist['external_urls']['spotify']
        )
        
        # Get all tracks (handling pagination for large playlists)
        tracks = []
        results = self.sp.playlist_tracks(playlist_id)
        tracks.extend(results['items'])
        
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        
        # Convert to TrackInfo objects
        track_list = []
        for idx, item in enumerate(tracks):
            track = item.get('track')
            if track is None:
                continue
            
            # Get album art (use track's album art, not playlist art)
            album_images = track.get('album', {}).get('images', [])
            track_album_art = album_images[0]['url'] if album_images else image_url
            
            track_info = TrackInfo(
                index=idx,
                name=track['name'],
                artists=', '.join([artist['name'] for artist in track['artists']]),
                album=track['album']['name'],
                album_art_url=track_album_art,
                duration_ms=track['duration_ms'],
                spotify_url=track['external_urls']['spotify']
            )
            track_list.append(track_info)
        
        return track_list, meta
    
    def extract_album(self, url: str) -> Tuple[List[TrackInfo], AlbumMeta]:
        """
        Extract all tracks from a Spotify album
        
        Args:
            url: Spotify album URL
            
        Returns:
            Tuple of (list of TrackInfo, AlbumMeta)
        """
        # Extract album ID from URL
        album_id = url.split('album/')[1].split('?')[0]
        
        # Get album metadata
        album = self.sp.album(album_id)
        
        # Get album image
        image_url = album['images'][0]['url'] if album['images'] else ''
        
        meta = AlbumMeta(
            name=album['name'],
            artists=', '.join([artist['name'] for artist in album['artists']]),
            release_date=album['release_date'],
            total_tracks=album['total_tracks'],
            image_url=image_url,
            spotify_url=album['external_urls']['spotify']
        )
        
        # Get all tracks
        track_list = []
        for idx, track in enumerate(album['tracks']['items']):
            track_info = TrackInfo(
                index=idx,
                name=track['name'],
                artists=', '.join([artist['name'] for artist in track['artists']]),
                album=album['name'],
                album_art_url=image_url,
                duration_ms=track['duration_ms'],
                spotify_url=track['external_urls']['spotify']
            )
            track_list.append(track_info)
        
        return track_list, meta
    
    def get_album_art_bytes(self, image_url: str) -> Optional[bytes]:
        """
        Download album art image as bytes for embedding
        
        Args:
            image_url: URL of the album art
            
        Returns:
            Image data as bytes, or None if failed
        """
        if not image_url:
            return None
        
        try:
            import requests
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception:
            return None
    
    def download_cover_art(self, image_url: str, output_folder: str) -> Optional[str]:
        """
        Download cover art and save to folder as cover.jpg
        
        Args:
            image_url: URL of the cover art (playlist or album image)
            output_folder: Path to the output folder
            
        Returns:
            Path to saved cover.jpg, or None if failed
        """
        if not image_url:
            return None
        
        try:
            import requests
            
            # Download the image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Ensure output folder exists
            os.makedirs(output_folder, exist_ok=True)
            
            # Save as cover.jpg
            cover_path = os.path.join(output_folder, 'cover.jpg')
            with open(cover_path, 'wb') as f:
                f.write(response.content)
            
            return cover_path
            
        except Exception:
            return None
