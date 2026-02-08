"""
Centralized logging configuration for the Spotify/YouTube Playlist Downloader.

Provides structured logging with both file and console output for:
- Debugging failed downloads
- Sharing logs for troubleshooting
- Monitoring long-running batch jobs
"""

import logging
import os
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "downloader",
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    log_dir: Optional[str] = None
) -> logging.Logger:
    """
    Set up and return a configured logger instance.
    
    Args:
        name: Logger name (default: 'downloader')
        log_file: Optional custom log filename (default: 'downloader.log')
        level: Logging level (default: INFO)
        log_dir: Optional directory for log files (default: project root)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatter with timestamp
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler - always enabled
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler - for persistent logs
    if log_file is None:
        log_file = "downloader.log"
    
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)
    else:
        # Default to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(project_root, log_file)
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "downloader") -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance (creates with default config if not exists)
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Create default logger instance for easy import
logger = setup_logger()


# Convenience functions for common logging patterns
def log_download_start(track_name: str, artist: str = "") -> None:
    """Log the start of a track download."""
    if artist:
        logger.info(f"Starting download: {track_name} by {artist}")
    else:
        logger.info(f"Starting download: {track_name}")


def log_download_success(track_name: str, file_path: str = "") -> None:
    """Log successful download completion."""
    if file_path:
        logger.info(f"Successfully downloaded: {track_name} -> {file_path}")
    else:
        logger.info(f"Successfully downloaded: {track_name}")


def log_download_error(track_name: str, error: Exception) -> None:
    """Log download failure with exception details."""
    logger.error(f"Failed to download: {track_name}", exc_info=True)


def log_playlist_processing(playlist_name: str, track_count: int) -> None:
    """Log start of playlist processing."""
    logger.info(f"Processing playlist: {playlist_name} ({track_count} tracks)")


def log_youtube_search(query: str, result_url: str = "") -> None:
    """Log YouTube search operation."""
    if result_url:
        logger.debug(f"YouTube search '{query}' -> {result_url}")
    else:
        logger.warning(f"YouTube search failed for: {query}")


def log_api_error(service: str, error: Exception) -> None:
    """Log API-related errors."""
    logger.error(f"{service} API error: {error}", exc_info=True)
