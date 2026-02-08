#!/usr/bin/env python3
"""
Spotify to YouTube Link Converter

A fully automated application that:
1. Automatically installs required packages if missing
2. Takes Spotify playlist URL as input
3. Exports playlist to CSV with Track Name and Artist Name(s)
4. Searches YouTube for each song using "{song} lyrics" query
5. Adds YouTube links to the dataset
6. Saves results to organized CSV files
7. Automatically downloads all songs to playlist-specific folders
"""

import os
import sys
import subprocess
import importlib
from typing import Optional, Tuple, List

# Package management functions
def install_package(package: str) -> bool:
    """Install a Python package using pip"""
    # Use print here since logger isn't set up yet during package installation
    try:
        print(f"Installing {package}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False

def check_and_install_packages() -> bool:
    """Check if required packages are installed and install missing ones"""
    print("Checking and installing required packages...")
    print("=" * 50)
    
    required_packages = {
        "spotipy": "spotipy",
        "pandas": "pandas", 
        "googleapiclient": "google-api-python-client",
        "tqdm": "tqdm",
        "dotenv": "python-dotenv"
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            importlib.import_module(import_name)
            print(f"{package_name} is already installed")
        except ImportError:
            print(f"{package_name} is missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        success_count = 0
        
        for package in missing_packages:
            if install_package(package):
                success_count += 1
        
        print(f"\nPackage installation summary:")
        print(f"  Successfully installed: {success_count}")
        print(f"  Failed to install: {len(missing_packages) - success_count}")
        
        if success_count < len(missing_packages):
            print("\nSome packages failed to install. Please install them manually:")
            for package in missing_packages:
                print(f"  pip install {package}")
            return False
        
        print("All required packages are now installed!")
        return True
    else:
        print("All required packages are already installed!")
        return True

def check_yt_dlp() -> bool:
    """Check if yt-dlp is installed and install it if missing"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"yt-dlp is installed (version: {result.stdout.strip()})")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp is not installed")
        print("Installing yt-dlp...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'yt-dlp'],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("yt-dlp installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install yt-dlp")
            print("Please install manually: pip install yt-dlp")
            return False

# Import packages after ensuring they're installed
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from googleapiclient.discovery import build
from tqdm import tqdm
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Utility functions
def sanitize_filename(filename: str) -> str:
    """Convert playlist name to a valid folder name"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    filename = filename.strip(' .')
    
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def check_environment() -> bool:
    """Check if all required environment variables are set"""
    required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET', 'YOUTUBE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error("Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.info("Please create a .env file with your API keys:")
        logger.info("1. Copy env_template.txt to .env")
        logger.info("2. Fill in your actual API keys")
        logger.info("3. Never commit .env to version control")
        return False
    
    return True

def detect_url_type(url: str) -> str:
    """Detect whether URL is Spotify or YouTube playlist
    
    Args:
        url: The URL to detect
    
    Returns:
        'spotify' if Spotify playlist/album
        'youtube' if YouTube playlist
        'unknown' if neither
    """
    url_lower = url.lower()
    
    # Check for Spotify URLs
    if 'spotify.com' in url_lower and ('playlist/' in url_lower or 'album/' in url_lower):
        return 'spotify'
    
    # Check for YouTube playlist URLs
    if ('youtube.com' in url_lower or 'youtu.be' in url_lower) and 'list=' in url_lower:
        return 'youtube'
    
    return 'unknown'

def extract_youtube_playlist_videos(playlist_url: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """Extract all video URLs from a YouTube playlist using yt-dlp
    
    Args:
        playlist_url: The YouTube playlist URL
    
    Returns:
        Tuple of (list of video URLs, playlist title) or (None, None) if failed
    """
    try:
        logger.info("Extracting YouTube playlist information...")
        
        # Use yt-dlp to extract playlist information without downloading
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
        
        if not output_lines:
            logger.warning("No videos found in playlist")
            return None, None
        
        # Extract video URLs (every odd line) and titles (every even line)
        video_urls = []
        for i in range(0, len(output_lines), 2):
            if i < len(output_lines):
                video_urls.append(output_lines[i])
        
        # Get playlist title using a separate command
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
        
        logger.info(f"Playlist: {playlist_title}")
        logger.info(f"Total videos: {len(video_urls)}")
        
        return video_urls, playlist_title
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting playlist: {e}", exc_info=True)
        logger.error(f"Error output: {e.stderr}")
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return None, None

# Core functionality functions
def export_spotify_playlist(playlist_url: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Export Spotify playlist or album to DataFrame with Track Name and Artist Name(s)"""
    
    # Check if it's an album or playlist
    if 'album/' in playlist_url:
        # It's an album
        album_id = playlist_url.split('album/')[1].split('?')[0]
        
        try:
            album = sp.album(album_id)
            album_name = album['name']
            logger.info(f"Album: {album_name}")
            logger.info(f"Total tracks: {album['total_tracks']}")
            
            # Extract track information
            track_data = []
            for track in album['tracks']['items']:
                track_info = {
                    'Track Name': track['name'],
                    'Artist Name(s)': ', '.join([artist['name'] for artist in track['artists']])
                }
                track_data.append(track_info)
            
            return pd.DataFrame(track_data), album_name
            
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return None, None
    
    elif 'playlist/' in playlist_url:
        # It's a playlist
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        
        try:
            playlist = sp.playlist(playlist_id)
            playlist_name = playlist['name']
            logger.info(f"Processing playlist: {playlist_name}")
            logger.info(f"Total tracks: {playlist['tracks']['total']}")
            
            tracks = []
            results = sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            
            # Handle playlists with more than 100 songs
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            
            # Extract track information
            track_data = []
            for track in tracks:
                if track['track']:
                    track_info = {
                        'Track Name': track['track']['name'],
                        'Artist Name(s)': ', '.join([artist['name'] for artist in track['track']['artists']])
                    }
                    track_data.append(track_info)
            
            return pd.DataFrame(track_data), playlist_name
            
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return None, None
    else:
        logger.error("Invalid URL format. Please provide a Spotify playlist or album URL.")
        return None, None

def get_youtube_link(song_name: str, artist: Optional[str] = None, keyword: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Search YouTube for song and return first result with video title
    
    Args:
        song_name: Name of the song to search for
        artist: Optional artist name
        keyword: Optional keyword to append to search (e.g., 'Visualizer', 'Lyrics', 'Audio')
    
    Returns:
        Tuple of (YouTube URL, Video Title)
    """
    # Build search query
    query = f"{song_name}"
    if artist:
        query += f" {artist}"
    
    # Add keyword if provided, otherwise default to 'lyrics'
    if keyword:
        query += f" {keyword}"
    else:
        query += " lyrics"

    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1,
            videoCategoryId=10  # Music category
        )
        response = request.execute()

        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_title = response['items'][0]['snippet']['title']
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            return youtube_url, video_title
    except Exception as e:
        logger.error(f"Error searching for '{query}': {e}", exc_info=True)

    return None, None

def create_playlist_folder(playlist_name: str) -> Optional[str]:
    """Create a folder with the playlist name"""
    folder_name = sanitize_filename(playlist_name)
    
    try:
        os.makedirs(folder_name, exist_ok=True)
        logger.info(f"Created folder: {folder_name}")
        return folder_name
    except Exception as e:
        logger.error(f"Failed to create folder: {e}", exc_info=True)
        return None

def download_songs(links: List[str], playlist_folder: str) -> bool:
    """Execute yt-dlp command to download all songs to the playlist folder"""
    if not links or not playlist_folder:
        logger.warning("No YouTube links or playlist folder specified")
        return False
    
    logger.info(f"Starting download of {len(links)} songs...")
    logger.info(f"Downloading to folder: {playlist_folder}")
    logger.info("This may take a while depending on the number of songs...")
    
    # Change to the playlist folder
    original_dir = os.getcwd()
    os.chdir(playlist_folder)
    
    try:
        # Create the yt-dlp command using Python module
        cmd = [
            sys.executable,
            '-m', 'yt_dlp',
            '-f', 'bestaudio[ext=m4a]',
            '--output', '%(title)s.%(ext)s'
        ]
        cmd.extend(links)
        
        logger.info(f"Executing command: {' '.join(cmd[:7])}... [and {len(links)} URLs]")
        logger.debug("=" * 60)
        
        # Execute the download command
        subprocess.run(cmd, check=True)
        
        logger.debug("=" * 60)
        logger.info("Download completed successfully!")
        logger.info(f"Songs downloaded to: {os.path.abspath('.')}")
        
        # List all downloaded files
        downloaded_files = [f for f in os.listdir('.') if f.endswith('.m4a')]
        if downloaded_files:
            logger.info(f"Downloaded {len(downloaded_files)} songs:")
            for file in downloaded_files:
                logger.debug(f"  - {file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed with error: {e}", exc_info=True)
        return False
    except KeyboardInterrupt:
        logger.warning("Download interrupted by user")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

def process_youtube_playlist(playlist_url: str) -> bool:
    """Process a YouTube playlist directly without YouTube search
    
    Args:
        playlist_url: The YouTube playlist URL
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Processing YouTube playlist...")
    
    # Extract video URLs from the YouTube playlist
    video_urls, playlist_name = extract_youtube_playlist_videos(playlist_url)
    
    if not video_urls or not playlist_name:
        logger.error("Failed to extract videos from YouTube playlist.")
        return False
    
    # Create folder for the playlist
    playlist_folder = create_playlist_folder(playlist_name)
    if not playlist_folder:
        logger.error("Failed to create playlist folder")
        return False
    
    logger.info(f"Successfully extracted {len(video_urls)} videos!")
    logger.debug("First few videos:")
    for i, url in enumerate(video_urls[:5], 1):
        logger.debug(f"  {i}. {url}")
    
    if len(video_urls) > 5:
        logger.debug(f"  ... and {len(video_urls) - 5} more")
    
    # Download all videos using the existing download function
    logger.info(f"Total videos to download: {len(video_urls)}")
    logger.info(f"Videos will be downloaded to: {playlist_folder}/")
    
    # Execute the download
    logger.info("Starting automatic download...")
    return download_songs(video_urls, playlist_folder)

def process_playlist(playlist_url: str, search_keyword: Optional[str] = None) -> bool:
    """Main function to process a Spotify playlist
    
    Args:
        playlist_url: The Spotify playlist or album URL
        search_keyword: Optional keyword to append to YouTube searches (e.g., 'Visualizer', 'Lyrics')
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Exporting Spotify playlist...")
    df, playlist_name = export_spotify_playlist(playlist_url)
    
    if df is None or playlist_name is None:
        logger.error("Failed to export playlist. Please check your URL and try again.")
        return False
    
    # Create folder for the playlist
    playlist_folder = create_playlist_folder(playlist_name)
    if not playlist_folder:
        logger.error("Failed to create playlist folder")
        return False
    
    logger.info(f"Successfully exported {len(df)} tracks!")
    
    # Show first few tracks
    logger.debug("First few tracks:")
    logger.debug(df.head().to_string())
    
    # Display search keyword if provided
    if search_keyword:
        logger.info(f"Using custom YouTube search keyword: '{search_keyword}'")
    else:
        logger.info("Using default YouTube search keyword: 'lyrics'")
    
    logger.info("Starting YouTube search...")
    
    # Add progress bar for visual feedback
    tqdm.pandas(desc="Searching YouTube")
    
    # Create YouTube links and video titles
    df[['YouTube Link', 'YouTube Video Title']] = df.progress_apply(
        lambda row: pd.Series(get_youtube_link(row['Track Name'], row['Artist Name(s)'], search_keyword)),
        axis=1
    )
    
    # Check results
    logger.info("Completed searches!")
    logger.debug(df[['Track Name', 'Artist Name(s)', 'YouTube Link', 'YouTube Video Title']].head().to_string())
    
    # Save enhanced CSV file
    final_output = os.path.join(playlist_folder, "spotify_playlist_with_youtube.csv")
    df.to_csv(final_output, index=False)
    logger.info(f"Saved results to {final_output}")
    
    # Show completion message
    success_rate = df['YouTube Link'].notnull().mean()
    logger.info(f"Success rate: {success_rate:.0%}")
    
    # Generate download command and execute
    links = df[df['YouTube Link'].notna()]['YouTube Link'].tolist()
    
    if links:
        command = 'yt-dlp -f "bestaudio[ext=m4a]" --output "%(title)s.%(ext)s" \\\n'
        command += " \\\n".join([f'"{link}"' for link in links])
        
        logger.debug("Download command is ready:")
        logger.debug("\n" + "="*50)
        logger.debug(command)
        logger.debug("="*50)
        logger.info(f"Total songs to download: {len(links)}")
        logger.info(f"Songs will be downloaded to: {playlist_folder}/")
        
        # Automatically execute the download
        logger.info("Starting automatic download...")
        return download_songs(links, playlist_folder)
    else:
        logger.warning("No YouTube links found. Please check your API key and try again.")
        return False

def main():
    """Main application function"""
    logger.info("Spotify/YouTube Playlist Downloader")
    logger.info("=" * 50)
    
    # Check and install required packages
    if not check_and_install_packages():
        logger.error("Failed to install required packages. Please try again.")
        return
    
    # Check environment variables
    if not check_environment():
        return
    
    # Check if yt-dlp is available
    if not check_yt_dlp():
        return
    
    # Get playlist URL from user
    print("\n" + "=" * 70)
    print("Enter your Spotify or YouTube playlist URL")
    print("Format: {URL} [keyword]")
    print("\nSupported URLs:")
    print("  • Spotify Playlist: https://open.spotify.com/playlist/xxx")
    print("  • Spotify Album: https://open.spotify.com/album/xxx")
    print("  • YouTube Playlist: https://youtube.com/playlist?list=xxx")
    print("\nOptional keyword (for Spotify only):")
    print("  • Add 'Visualizer', 'Audio', 'Lyrics', etc. after Spotify URL")
    print("  • Example: https://open.spotify.com/playlist/xxx Visualizer")
    print("=" * 70)
    
    user_input = input("\nInput: ").strip()
    
    if not user_input:
        logger.warning("No URL provided!")
        return
    
    # Parse input: split by space, first part is URL, rest is optional keyword
    parts = user_input.split(None, 1)  # Split into max 2 parts
    playlist_url = parts[0]
    search_keyword = parts[1] if len(parts) > 1 else None
    
    # Detect URL type
    url_type = detect_url_type(playlist_url)
    
    logger.info(f"Detected URL type: {url_type.upper()}")
    logger.info(f"Playlist URL: {playlist_url}")
    
    success = False
    
    if url_type == 'spotify':
        # Spotify workflow: Extract songs -> Search YouTube -> Download
        if search_keyword:
            logger.info(f"Search keyword: {search_keyword}")
        else:
            logger.info("Search keyword: (none - will use default 'lyrics')")
        
        success = process_playlist(playlist_url, search_keyword)
        
    elif url_type == 'youtube':
        # YouTube workflow: Extract videos -> Download directly
        if search_keyword:
            logger.info(f"Note: Search keyword '{search_keyword}' is ignored for YouTube playlists")
        
        success = process_youtube_playlist(playlist_url)
        
    else:
        logger.error("Invalid URL format!")
        logger.info("Please provide either:")
        logger.info("  • A Spotify playlist/album URL")
        logger.info("  • A YouTube playlist URL")
        return
    
    if success:
        logger.info("Process completed successfully!")
    else:
        logger.error("Process failed. Please check the error messages above.")

if __name__ == "__main__":
    # Get API keys from environment variables
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # Setup Spotify authentication
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))
    
    main()
