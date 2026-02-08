"""
Audio Downloader Module
Handles yt-dlp downloads with progress callbacks
"""

import os
import sys
import subprocess
import re
from dataclasses import dataclass
from typing import Callable, Optional, List
from datetime import datetime


@dataclass
class DownloadResult:
    """Result of a single download operation"""
    success: bool
    filepath: Optional[str]
    error: Optional[str]
    duration_seconds: float
    filesize_bytes: int = 0


class AudioDownloader:
    """Handles yt-dlp downloads with progress tracking"""
    
    def __init__(self, output_dir: str):
        """
        Initialize downloader with output directory
        
        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Convert string to a valid filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        filename = filename.strip(' .')
        if len(filename) > 100:
            filename = filename[:100]
        return filename
    
    @staticmethod
    def check_yt_dlp() -> bool:
        """Check if yt-dlp is available"""
        try:
            subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '--version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def download_track(
        self, 
        url: str, 
        custom_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> DownloadResult:
        """
        Download a single track from YouTube
        
        Args:
            url: YouTube video URL
            custom_filename: Optional custom filename (without extension)
            progress_callback: Optional callback(status_text, progress_percent)
            
        Returns:
            DownloadResult with success status and file path
        """
        start_time = datetime.now()
        
        # Build output template
        if custom_filename:
            output_template = os.path.join(
                self.output_dir, 
                f"{self.sanitize_filename(custom_filename)}.%(ext)s"
            )
        else:
            output_template = os.path.join(
                self.output_dir,
                "%(title)s.%(ext)s"
            )
        
        cmd = [
            sys.executable,
            '-m', 'yt_dlp',
            # Format fallback chain: try m4a first, then any audio, then best overall
            '-f', 'bestaudio[ext=m4a]/bestaudio/best',
            # Post-process to m4a format if source isn't m4a
            '-x', '--audio-format', 'm4a',
            '--output', output_template,
            '--no-warnings',
            '--progress',
            url
        ]
        
        try:
            # Run download with progress capture
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            output_lines = []
            filepath = None
            
            for line in process.stdout:
                output_lines.append(line)
                
                # Parse progress
                if progress_callback and '%' in line:
                    match = re.search(r'(\d+\.?\d*)%', line)
                    if match:
                        percent = float(match.group(1))
                        progress_callback(line.strip(), percent)
                
                # Capture output filepath
                if '[download] Destination:' in line:
                    filepath = line.split('Destination:')[1].strip()
                elif 'has already been downloaded' in line:
                    # Extract filepath from "already downloaded" message
                    match = re.search(r'\[download\] (.+) has already been downloaded', line)
                    if match:
                        filepath = match.group(1)
            
            process.wait()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            if process.returncode == 0:
                # Try to find the downloaded file if filepath wasn't captured
                if not filepath:
                    m4a_files = [f for f in os.listdir(self.output_dir) if f.endswith('.m4a')]
                    if m4a_files:
                        # Get the most recently modified file
                        latest = max(
                            m4a_files,
                            key=lambda f: os.path.getmtime(os.path.join(self.output_dir, f))
                        )
                        filepath = os.path.join(self.output_dir, latest)
                
                filesize = os.path.getsize(filepath) if filepath and os.path.exists(filepath) else 0
                
                return DownloadResult(
                    success=True,
                    filepath=filepath,
                    error=None,
                    duration_seconds=duration,
                    filesize_bytes=filesize
                )
            else:
                error_output = ''.join(output_lines[-5:])  # Last 5 lines for error context
                return DownloadResult(
                    success=False,
                    filepath=None,
                    error=f"Download failed: {error_output}",
                    duration_seconds=duration
                )
                
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return DownloadResult(
                success=False,
                filepath=None,
                error=str(e),
                duration_seconds=duration
            )
    
    def download_batch(
        self,
        urls: List[str],
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[DownloadResult]:
        """
        Download multiple tracks sequentially
        
        Args:
            urls: List of YouTube URLs to download
            progress_callback: Optional callback(current_index, total, status_text)
            
        Returns:
            List of DownloadResult for each URL
        """
        results = []
        total = len(urls)
        
        for idx, url in enumerate(urls):
            if progress_callback:
                progress_callback(idx, total, f"Downloading {idx + 1}/{total}")
            
            result = self.download_track(url)
            results.append(result)
        
        return results
