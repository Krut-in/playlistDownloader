"""
Session State Management
Handles all Streamlit session state with proper initialization
"""

import streamlit as st
from typing import Dict, List, Set, Any
from dataclasses import dataclass, field


@dataclass
class AppState:
    """Defines all session state fields with defaults"""
    
    # URL & Input State
    input_url: str = ""
    url_type: str = ""  # 'spotify_playlist' | 'spotify_album' | 'youtube'
    selected_keyword: str = "Lyrics"
    
    # Track Data State
    tracks: List[Any] = field(default_factory=list)  # List[TrackInfo]
    playlist_name: str = ""
    playlist_meta: Any = None  # PlaylistMeta or AlbumMeta
    
    # YouTube Matching State
    youtube_matches: Dict[int, List[Any]] = field(default_factory=dict)  # track_index -> List[YouTubeMatch]
    selected_match_indices: Dict[int, int] = field(default_factory=dict)  # track_index -> match_index
    matching_complete: bool = False
    matching_errors: Dict[int, str] = field(default_factory=dict)
    
    # Selection State (all selected by default)
    selected_tracks: Set[int] = field(default_factory=set)
    
    # Download State
    download_status: Dict[int, str] = field(default_factory=dict)  # 'pending'|'downloading'|'success'|'failed'
    download_errors: Dict[int, str] = field(default_factory=dict)
    download_results: Dict[int, Any] = field(default_factory=dict)  # track_index -> DownloadResult
    downloading: bool = False
    completed: bool = False
    
    # UI State
    dark_mode: bool = True
    api_quota_used: int = 0
    
    # Workflow State
    step: str = "input"  # 'input' | 'matching' | 'review' | 'downloading' | 'completed'


def init_session_state():
    """Initialize all session state variables with defaults"""
    defaults = {
        # URL & Input
        'input_url': "",
        'url_type': "",
        'selected_keyword': "Lyrics",
        
        # Track Data
        'tracks': [],
        'playlist_name': "",
        'playlist_meta': None,
        
        # YouTube Matching
        'youtube_matches': {},
        'selected_match_indices': {},
        'matching_complete': False,
        'matching_errors': {},
        
        # Selection
        'selected_tracks': set(),
        
        # Download
        'download_status': {},
        'download_errors': {},
        'download_results': {},
        'downloading': False,
        'completed': False,
        
        # UI
        'dark_mode': True,
        'api_quota_used': 0,
        
        # Workflow
        'step': 'input',
        
        # Output folder
        'output_folder': '',
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    """Reset session state for new playlist processing"""
    keys_to_reset = [
        'tracks', 'playlist_name', 'playlist_meta',
        'youtube_matches', 'selected_match_indices', 'matching_complete', 'matching_errors',
        'selected_tracks',
        'download_status', 'download_errors', 'download_results', 'downloading', 'completed',
        'step', 'output_folder'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            if isinstance(st.session_state[key], dict):
                st.session_state[key] = {}
            elif isinstance(st.session_state[key], list):
                st.session_state[key] = []
            elif isinstance(st.session_state[key], set):
                st.session_state[key] = set()
            elif isinstance(st.session_state[key], bool):
                st.session_state[key] = False
            else:
                st.session_state[key] = ""
    
    st.session_state['step'] = 'input'


def get_selected_tracks_count() -> int:
    """Get count of selected tracks"""
    return len(st.session_state.get('selected_tracks', set()))


def get_download_summary() -> Dict[str, int]:
    """Get summary of download statuses"""
    statuses = st.session_state.get('download_status', {})
    return {
        'success': sum(1 for s in statuses.values() if s == 'success'),
        'failed': sum(1 for s in statuses.values() if s == 'failed'),
        'pending': sum(1 for s in statuses.values() if s == 'pending'),
        'total': len(statuses)
    }
