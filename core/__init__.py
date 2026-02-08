# Core module exports
from .spotify_client import SpotifyClient
from .youtube_client import YouTubeClient, YouTubeMatch
from .downloader import AudioDownloader, DownloadResult
from .metadata import MetadataEmbedder
from .logger import (
    setup_logger,
    get_logger,
    logger,
    log_download_start,
    log_download_success,
    log_download_error,
    log_playlist_processing,
    log_youtube_search,
    log_api_error,
)

__all__ = [
    'SpotifyClient',
    'YouTubeClient', 
    'YouTubeMatch',
    'AudioDownloader',
    'DownloadResult',
    'MetadataEmbedder',
    'setup_logger',
    'get_logger',
    'logger',
    'log_download_start',
    'log_download_success',
    'log_download_error',
    'log_playlist_processing',
    'log_youtube_search',
    'log_api_error',
]
