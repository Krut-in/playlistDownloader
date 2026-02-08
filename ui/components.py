"""
UI Components Module
Clean, professional Streamlit UI components
"""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_header():
    """Render clean application header with theme toggle"""
    col1, col2 = st.columns([11, 1])
    
    with col1:
        st.markdown('''
            <div class="app-header">
                <h1 class="app-title">Playlist Downloader</h1>
                <p class="app-subtitle">Download from Spotify & YouTube playlists</p>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        current_mode = st.session_state.get('dark_mode', True)
        toggle_icon = "☀" if current_mode else "🌙"
        
        if st.button(toggle_icon, key="theme_toggle"):
            st.session_state.dark_mode = not current_mode
            st.rerun()


def render_url_input() -> tuple:
    """Render the URL input section with compact layout"""
    col1, col2, col3 = st.columns([5, 2, 2])
    
    with col1:
        url = st.text_input(
            "URL",
            placeholder="Paste a Spotify or YouTube playlist URL",
            label_visibility="collapsed",
            key="url_input"
        )
    
    with col2:
        keyword_options = [
            "None",
            "Lyrics",
            "Official Audio",
            "Visualizer",
            "Live",
            "Acoustic",
            "Instrumental",
            "Remix"
        ]
        keyword = st.selectbox(
            "Search Keyword",
            keyword_options,
            index=0,
            label_visibility="collapsed",
            key="keyword_select"
        )
    
    with col3:
        extract_clicked = st.button("Extract", type="primary", use_container_width=True)
    
    return url, keyword, extract_clicked


def render_playlist_info(playlist_meta: Any, track_count: int, url_type: str):
    """Render compact playlist information"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        image_url = getattr(playlist_meta, 'image_url', '')
        if image_url:
            st.image(image_url, width=64)
    
    with col2:
        name = getattr(playlist_meta, 'name', 'Unknown')
        
        # Badge type based on source
        if 'spotify' in url_type.lower():
            badge_class = "badge-success"
        else:
            badge_class = "badge-error"
        
        type_label = url_type.replace('_', ' ').title()
        st.markdown(f'''
            <div class="playlist-info-header">
                <span class="playlist-name">{name}</span>
                <span class="badge {badge_class}">{type_label}</span>
                <span class="playlist-track-count">{track_count} tracks</span>
            </div>
        ''', unsafe_allow_html=True)


def render_quota_indicator(quota_used: int, daily_limit: int = 10000):
    """Render API quota with color-coded status"""
    percentage = min(100, (quota_used / daily_limit) * 100)
    
    if percentage < 50:
        color = "var(--success)"
        status = "Healthy"
    elif percentage < 80:
        color = "var(--warning)"
        status = "Moderate"
    else:
        color = "var(--error)"
        status = "Critical"
    
    st.markdown(f'''
        <div class="quota-container" role="status" aria-label="API Quota Usage">
            <div class="quota-header">
                <span class="quota-label">API Quota · {status}</span>
                <span class="quota-label">{quota_used:,} / {daily_limit:,}</span>
            </div>
            <div class="quota-bar" role="progressbar" aria-valuenow="{int(percentage)}" aria-valuemin="0" aria-valuemax="100" aria-label="{int(percentage)}% quota used">
                <div class="quota-fill" style="width: {percentage}%; background: {color};"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)


def render_track_table(
    tracks: List[Any],
    youtube_matches: Dict[int, List[Any]],
    selected_match_indices: Dict[int, int],
    selected_tracks: set,
    matching_errors: Dict[int, str]
):
    """Render track list with status indicators"""
    
    # Stats header
    matched_count = sum(1 for i in range(len(tracks)) if i in youtube_matches and youtube_matches[i])
    failed_count = len(matching_errors)
    pending_count = len(tracks) - matched_count - failed_count
    
    st.markdown(f'''
        <div class="stats-header">
            <span class="badge badge-success">{matched_count} Matched</span>
            <span class="badge badge-error">{failed_count} Failed</span>
            <span class="badge badge-muted">{pending_count} Pending</span>
            <span class="stats-count">{len(selected_tracks)} selected</span>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Callback function for select all checkbox
        def on_select_all_change():
            if st.session_state.select_all_checkbox:
                # Select all tracks
                st.session_state.selected_tracks = set(range(len(tracks)))
            else:
                # Deselect all tracks
                st.session_state.selected_tracks = set()
        
        select_all = st.checkbox(
            "Select all",
            value=len(selected_tracks) == len(tracks) and len(tracks) > 0,
            key="select_all_checkbox",
            on_change=on_select_all_change
        )
    
    st.markdown('<div style="margin: var(--space-4) 0;"></div>', unsafe_allow_html=True)
    
    # Track list
    for idx, track in enumerate(tracks):
        matches = youtube_matches.get(idx, [])
        selected_match_idx = selected_match_indices.get(idx, 0)
        error = matching_errors.get(idx, "")
        has_match = len(matches) > 0
        
        # Start track row wrapper
        st.markdown('<div class="track-row">', unsafe_allow_html=True)
        
        cols = st.columns([1, 2, 8, 2, 4])
        
        with cols[0]:
            # Callback function for individual track checkbox
            def on_track_select_change(track_idx=idx):
                if st.session_state[f"track_select_{track_idx}"]:
                    st.session_state.selected_tracks.add(track_idx)
                else:
                    st.session_state.selected_tracks.discard(track_idx)
            
            is_selected = st.checkbox(
                "Select",
                value=idx in selected_tracks,
                key=f"track_select_{idx}",
                label_visibility="collapsed",
                on_change=on_track_select_change,
                args=(idx,)
            )
        
        with cols[1]:
            if has_match and matches[selected_match_idx].thumbnail_url:
                st.image(matches[selected_match_idx].thumbnail_url, width=48)
            else:
                st.markdown('<div class="track-thumbnail-empty">♪</div>', unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown(f'''
                <div class="track-info">
                    <div class="track-name">{track.name}</div>
                    <div class="track-artist">{track.artists}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with cols[3]:
            if has_match:
                st.markdown('<span class="badge badge-success">Matched</span>', unsafe_allow_html=True)
            elif error:
                st.markdown('<span class="badge badge-error">Failed</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-muted">Pending</span>', unsafe_allow_html=True)
        
        with cols[4]:
            if has_match and len(matches) > 1:
                match_options = [f"{i+1}. {m.title[:25]}..." for i, m in enumerate(matches)]
                new_selection = st.selectbox(
                    "Alt",
                    range(len(matches)),
                    index=selected_match_idx,
                    format_func=lambda x: match_options[x] if x < len(match_options) else "",
                    key=f"alt_match_{idx}",
                    label_visibility="collapsed"
                )
                
                if new_selection != selected_match_idx:
                    st.session_state.selected_match_indices[idx] = new_selection
        
        # Close track row wrapper
        st.markdown('</div>', unsafe_allow_html=True)


def render_download_button(selected_count: int) -> bool:
    """Render download button with count"""
    if selected_count > 0:
        label = f"Download {selected_count} Track{'s' if selected_count != 1 else ''}"
    else:
        label = "Select tracks to download"
    
    return st.button(
        label,
        type="primary",
        disabled=selected_count == 0,
        use_container_width=True
    )


def render_download_progress(current: int, total: int, current_track: str, status: str, thumbnail_url: str = None):
    """Render download progress"""
    st.markdown('<h3 class="section-header">Downloading</h3>', unsafe_allow_html=True)
    
    if thumbnail_url:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(thumbnail_url, use_container_width=True)
        
        with col2:
            progress = current / total if total > 0 else 0
            st.progress(progress)
            
            st.markdown(f'''
                <div class="progress-meta">
                    <span class="progress-count">{current} of {total}</span>
                    <span class="progress-percent">{int(progress * 100)}%</span>
                </div>
                <p class="progress-track-name">
                    {current_track[:50]}{"..." if len(current_track) > 50 else ""}
                </p>
            ''', unsafe_allow_html=True)
    else:
        progress = current / total if total > 0 else 0
        st.progress(progress)
        
        st.markdown(f'''
            <div class="progress-meta">
                <span class="progress-count">{current} of {total}</span>
                <span class="progress-percent">{int(progress * 100)}%</span>
            </div>
            <p class="progress-track-name">
                {current_track[:50]}{"..." if len(current_track) > 50 else ""}
            </p>
        ''', unsafe_allow_html=True)


def render_completion_summary(
    success_count: int,
    failed_count: int,
    output_folder: str,
    failed_tracks: List[tuple] = None
):
    """Render completion summary"""
    total = success_count + failed_count
    success_rate = (success_count / total * 100) if total > 0 else 0
    
    # Header message
    if success_rate >= 90:
        st.markdown('''
            <div class="completion-header">
                <h3 class="completion-title" style="color: var(--success);">Download Complete</h3>
                <p class="completion-subtitle">Your music is ready</p>
            </div>
        ''', unsafe_allow_html=True)
    elif success_rate >= 50:
        st.markdown('''
            <div class="completion-header">
                <h3 class="completion-title" style="color: var(--warning);">Partially Complete</h3>
                <p class="completion-subtitle">Some tracks had issues</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="completion-header">
                <h3 class="completion-title" style="color: var(--error);">Issues Encountered</h3>
                <p class="completion-subtitle">Check failed tracks below</p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Stats cards
    st.markdown('<div style="margin: var(--space-6) 0;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
            <div class="stat-card stat-card-success">
                <div class="stat-value" style="color: var(--success);">{success_count}</div>
                <div class="stat-label" style="color: var(--success);">Successful</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="stat-card stat-card-error">
                <div class="stat-value" style="color: var(--error);">{failed_count}</div>
                <div class="stat-label" style="color: var(--error);">Failed</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        rate_color = "var(--success)" if success_rate >= 80 else "var(--warning)" if success_rate >= 50 else "var(--error)"
        st.markdown(f'''
            <div class="stat-card">
                <div class="stat-value" style="color: {rate_color};">{success_rate:.0f}%</div>
                <div class="stat-label" style="color: var(--text-secondary);">Success Rate</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="folder-path-container">
            <span class="folder-path-label">Saved to:</span><br>
            <code class="folder-path">{output_folder}</code>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div style="margin: var(--space-4) 0;"></div>', unsafe_allow_html=True)
    
    # Failed tracks
    if failed_tracks:
        with st.expander(f"View {len(failed_tracks)} failed tracks"):
            for track_name, error in failed_tracks:
                st.markdown(f'''
                    <div class="failed-track-item">
                        <div class="failed-track-name">{track_name}</div>
                        <div class="failed-track-error">{error}</div>
                    </div>
                ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div style="margin-top: var(--space-4);"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Open Folder", use_container_width=True, type="secondary"):
            import subprocess
            subprocess.run(['open', output_folder])
    
    with col2:
        if st.button("Start New", use_container_width=True, type="primary"):
            from .state import reset_session_state
            reset_session_state()
            st.rerun()


def render_status_indicator(status: str) -> str:
    """Return HTML for a colored status indicator"""
    status_map = {
        'pending': ('badge-muted', 'Pending'),
        'matching': ('badge-warning', 'Matching'),
        'downloading': ('badge-warning', 'Downloading'),
        'success': ('badge-success', 'Complete'),
        'failed': ('badge-error', 'Failed'),
    }
    
    class_name, label = status_map.get(status, ('badge-muted', 'Unknown'))
    return f'<span class="badge {class_name}">{label}</span>'
