"""
Spotify/YouTube Playlist Downloader - Streamlit App
A beautiful web interface for downloading entire music collections
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import core modules
from core.spotify_client import SpotifyClient
from core.youtube_client import YouTubeClient
from core.downloader import AudioDownloader
from core.metadata import MetadataEmbedder

# Import UI modules
from ui.state import init_session_state, reset_session_state, get_download_summary
from ui.theme import apply_theme, render_theme_toggle
from ui.components import (
    render_header,
    render_url_input,
    render_playlist_info,
    render_track_table,
    render_download_button,
    render_download_progress,
    render_completion_summary,
    render_quota_indicator,
)

# Page configuration
st.set_page_config(
    page_title="Playlist Downloader",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)


def init_clients():
    """Initialize API clients"""
    try:
        spotify = SpotifyClient()
        youtube = YouTubeClient()
        return spotify, youtube, None
    except ValueError as e:
        return None, None, str(e)


def sanitize_folder_name(name: str) -> str:
    """Convert string to valid folder name"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    name = name.strip(' .')
    if len(name) > 100:
        name = name[:100]
    return name


def detect_url_type(url: str, spotify: SpotifyClient, youtube: YouTubeClient) -> str:
    """Detect URL type (spotify_playlist, spotify_album, youtube, or unknown)"""
    spotify_type = spotify.detect_url_type(url)
    if spotify_type == 'playlist':
        return 'spotify_playlist'
    elif spotify_type == 'album':
        return 'spotify_album'
    elif youtube.detect_youtube_playlist(url):
        return 'youtube'
    return 'unknown'


def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Apply theme
    apply_theme(st.session_state.get('dark_mode', True))
    
    # Render header with inline theme toggle
    render_header()
    
    # Initialize clients
    spotify, youtube, client_error = init_clients()
    
    if client_error:
        st.error(f"Configuration Error: {client_error}")
        st.info("Please ensure your `.env` file contains valid API credentials.")
        st.code("""
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
YOUTUBE_API_KEY=your_api_key
        """)
        return
    
    # URL Input Section
    url, keyword, extract_clicked = render_url_input()
    
    # Handle extract button click
    if extract_clicked and url:
        url_type = detect_url_type(url, spotify, youtube)
        
        if url_type == 'unknown':
            st.error("Invalid URL. Please enter a valid Spotify or YouTube playlist URL.")
        else:
            # Reset state for new extraction
            reset_session_state()
            
            st.session_state.input_url = url
            st.session_state.url_type = url_type
            st.session_state.selected_keyword = keyword
            
            # Extract tracks
            with st.spinner("Extracting tracks..."):
                try:
                    if url_type == 'spotify_playlist':
                        tracks, meta = spotify.extract_playlist(url)
                    elif url_type == 'spotify_album':
                        tracks, meta = spotify.extract_album(url)
                    elif url_type == 'youtube':
                        videos, playlist_name = youtube.extract_playlist(url)
                        # Convert YouTube videos to a similar format
                        from dataclasses import dataclass
                        
                        @dataclass
                        class YTTrackInfo:
                            index: int
                            name: str
                            artists: str
                            album: str
                            album_art_url: str
                            duration_ms: int
                            spotify_url: str
                        
                        tracks = [
                            YTTrackInfo(
                                index=i,
                                name=v.title,
                                artists="YouTube",
                                album=playlist_name,
                                album_art_url="",
                                duration_ms=0,
                                spotify_url=v.url
                            )
                            for i, v in enumerate(videos)
                        ]
                        
                        # Create a mock meta object
                        class YTMeta:
                            def __init__(self):
                                self.name = playlist_name
                                self.image_url = ""
                        
                        meta = YTMeta()
                    
                    st.session_state.tracks = tracks
                    st.session_state.playlist_meta = meta
                    st.session_state.playlist_name = meta.name
                    
                    # Select all tracks by default
                    st.session_state.selected_tracks = set(range(len(tracks)))
                    
                    # For YouTube playlists, set matches directly (no search needed)
                    if url_type == 'youtube':
                        from core.youtube_client import YouTubeMatch
                        for i, track in enumerate(tracks):
                            match = YouTubeMatch(
                                video_id="",
                                title=track.name,
                                channel="YouTube",
                                thumbnail_url="",
                                duration="",
                                url=track.spotify_url  # For YT, this is the YT URL
                            )
                            st.session_state.youtube_matches[i] = [match]
                            st.session_state.selected_match_indices[i] = 0
                        st.session_state.matching_complete = True
                    
                    st.session_state.step = 'matching' if url_type != 'youtube' else 'review'
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error extracting tracks: {str(e)}")
    
    # Display playlist info if tracks are loaded
    if st.session_state.get('tracks') and st.session_state.get('playlist_meta'):
        render_playlist_info(
            st.session_state.playlist_meta,
            len(st.session_state.tracks),
            st.session_state.url_type
        )
        
        # YouTube matching step (for Spotify URLs)
        if st.session_state.step == 'matching' and st.session_state.url_type.startswith('spotify'):
            
            # Show quota indicator
            render_quota_indicator(
                st.session_state.api_quota_used,
                10000
            )
            
            if st.button("Find YouTube Matches", use_container_width=True, type="primary"):
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                tracks = st.session_state.tracks
                keyword = st.session_state.selected_keyword
                
                for idx, track in enumerate(tracks):
                    status_text.text(f"Searching: {track.name} - {track.artists}")
                    
                    try:
                        matches = youtube.search_track(
                            track.name,
                            track.artists,
                            keyword,
                            max_results=3
                        )
                        
                        if matches:
                            st.session_state.youtube_matches[idx] = matches
                            st.session_state.selected_match_indices[idx] = 0
                        else:
                            st.session_state.matching_errors[idx] = "No matches found"
                        
                        st.session_state.api_quota_used = youtube.quota_used
                        
                    except Exception as e:
                        st.session_state.matching_errors[idx] = str(e)[:50]
                    
                    progress_bar.progress((idx + 1) / len(tracks))
                
                st.session_state.matching_complete = True
                st.session_state.step = 'review'
                status_text.empty()
                st.rerun()
        
        # Review and download step
        if st.session_state.step == 'review' and st.session_state.matching_complete:
            
            # Show quota indicator
            if st.session_state.url_type.startswith('spotify'):
                render_quota_indicator(
                    st.session_state.api_quota_used,
                    10000
                )
            
            # Track table with selection
            render_track_table(
                st.session_state.tracks,
                st.session_state.youtube_matches,
                st.session_state.selected_match_indices,
                st.session_state.selected_tracks,
                st.session_state.matching_errors
            )
            
            # Download button
            if render_download_button(len(st.session_state.selected_tracks)):
                st.session_state.step = 'downloading'
                st.session_state.downloading = True
                st.rerun()
        
        # Downloading step
        if st.session_state.step == 'downloading':
            
            # Create output folder
            folder_name = sanitize_folder_name(st.session_state.playlist_name)
            output_folder = os.path.join(os.getcwd(), folder_name)
            st.session_state.output_folder = output_folder
            
            downloader = AudioDownloader(output_folder)
            embedder = MetadataEmbedder()
            
            # Download cover art for Spotify sources
            if st.session_state.url_type.startswith('spotify'):
                cover_url = getattr(st.session_state.playlist_meta, 'image_url', '')
                if cover_url:
                    spotify.download_cover_art(cover_url, output_folder)
            
            selected_indices = sorted(st.session_state.selected_tracks)
            total = len(selected_indices)
            
            progress_bar = st.progress(0)
            status_container = st.empty()
            
            for i, track_idx in enumerate(selected_indices):
                track = st.session_state.tracks[track_idx]
                matches = st.session_state.youtube_matches.get(track_idx, [])
                match_idx = st.session_state.selected_match_indices.get(track_idx, 0)
                
                if not matches:
                    st.session_state.download_status[track_idx] = 'failed'
                    st.session_state.download_errors[track_idx] = 'No YouTube match'
                    continue
                
                selected_match = matches[match_idx]
                
                with status_container.container():
                    render_download_progress(
                        i + 1,
                        total,
                        f"{track.name} - {track.artists}",
                        f"Downloading from YouTube...",
                        thumbnail_url=selected_match.thumbnail_url
                    )
                
                # Download the track
                st.session_state.download_status[track_idx] = 'downloading'
                
                result = downloader.download_track(selected_match.url)
                
                if result.success and result.filepath:
                    st.session_state.download_status[track_idx] = 'success'
                    st.session_state.download_results[track_idx] = result
                    
                    # Embed metadata (only for Spotify sources)
                    if st.session_state.url_type.startswith('spotify'):
                        album_art = spotify.get_album_art_bytes(track.album_art_url)
                        
                        embedder.embed_metadata(
                            filepath=result.filepath,
                            track_name=track.name,
                            artist=track.artists,
                            album=track.album,
                            album_art=album_art,
                            youtube_url=selected_match.url
                        )
                else:
                    st.session_state.download_status[track_idx] = 'failed'
                    st.session_state.download_errors[track_idx] = result.error or 'Unknown error'
                
                progress_bar.progress((i + 1) / total)
            
            st.session_state.downloading = False
            st.session_state.completed = True
            st.session_state.step = 'completed'
            st.rerun()
        
        # Completion step
        if st.session_state.step == 'completed':
            summary = get_download_summary()
            
            # Collect failed tracks info
            failed_tracks = []
            for idx, status in st.session_state.download_status.items():
                if status == 'failed':
                    track = st.session_state.tracks[idx]
                    error = st.session_state.download_errors.get(idx, 'Unknown error')
                    failed_tracks.append((f"{track.name} - {track.artists}", error))
            
            render_completion_summary(
                success_count=summary['success'],
                failed_count=summary['failed'],
                output_folder=st.session_state.output_folder,
                failed_tracks=failed_tracks
            )


if __name__ == "__main__":
    main()
