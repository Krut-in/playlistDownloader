"""
Metadata Embedder Module
Embeds ID3 tags and album art into M4A files
"""

import os
from typing import Optional
from mutagen.mp4 import MP4, MP4Cover
from .logger import get_logger

# Initialize logger for this module
logger = get_logger("metadata")

class MetadataEmbedder:
    """Embeds ID3 tags and album art into M4A/MP4 files"""
    
    @staticmethod
    def embed_metadata(
        filepath: str,
        track_name: str,
        artist: str,
        album: str,
        album_art: Optional[bytes] = None,
        youtube_url: Optional[str] = None,
        year: Optional[str] = None
    ) -> bool:
        """
        Embed metadata into an M4A file
        
        Args:
            filepath: Path to the M4A file
            track_name: Track/song name
            artist: Artist name(s)
            album: Album name
            album_art: Album artwork as JPEG bytes
            youtube_url: YouTube source URL (stored in comment)
            year: Release year
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            audio = MP4(filepath)
            
            # Standard MP4/M4A tags
            audio['\xa9nam'] = track_name  # Title
            audio['\xa9ART'] = artist       # Artist
            audio['\xa9alb'] = album        # Album
            
            if year:
                audio['\xa9day'] = year     # Year
            
            if youtube_url:
                audio['\xa9cmt'] = f"Source: {youtube_url}"  # Comment
            
            # Embed album art if provided
            if album_art:
                # Determine image format (JPEG or PNG)
                if album_art[:3] == b'\xff\xd8\xff':
                    # JPEG
                    cover = MP4Cover(album_art, imageformat=MP4Cover.FORMAT_JPEG)
                elif album_art[:8] == b'\x89PNG\r\n\x1a\n':
                    # PNG
                    cover = MP4Cover(album_art, imageformat=MP4Cover.FORMAT_PNG)
                else:
                    # Assume JPEG for unknown formats
                    cover = MP4Cover(album_art, imageformat=MP4Cover.FORMAT_JPEG)
                
                audio['covr'] = [cover]
            
            audio.save()
            return True
            
        except Exception as e:
            logger.error(f"Error embedding metadata: {e}", exc_info=True)
            return False
    
    @staticmethod
    def read_metadata(filepath: str) -> dict:
        """
        Read metadata from an M4A file
        
        Args:
            filepath: Path to the M4A file
            
        Returns:
            Dictionary of metadata tags
        """
        if not os.path.exists(filepath):
            return {}
        
        try:
            audio = MP4(filepath)
            
            return {
                'title': audio.get('\xa9nam', [''])[0],
                'artist': audio.get('\xa9ART', [''])[0],
                'album': audio.get('\xa9alb', [''])[0],
                'year': audio.get('\xa9day', [''])[0],
                'comment': audio.get('\xa9cmt', [''])[0],
                'has_cover': 'covr' in audio
            }
            
        except Exception:
            return {}
