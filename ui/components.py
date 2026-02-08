"""
UI Components Module
Clean, professional Streamlit UI components
"""

import streamlit as st
from typing import List, Dict, Any, Optional


def render_header():
    """Render clean application header"""
    st.markdown('''
        <div class="app-header">
            <h1 class="app-title">Playlist Downloader</h1>
            <p class="app-subtitle">Download from Spotify & YouTube playlists</p>
        </div>
    ''', unsafe_allow_html=True)


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
            st.image(image_url, width=56)
    
    with col2:
        name = getattr(playlist_meta, 'name', 'Unknown')
        
        # Badge type based on source
        if 'spotify' in url_type.lower():
            badge_class = "badge-success"
        else:
            badge_class = "badge-error"
        
        type_label = url_type.replace('_', ' ').title()
        st.markdown(f'''
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <span style="font-weight: 600; font-size: 0.9375rem; color: var(--text-primary);">{name}</span>
                <span class="badge {badge_class}">{type_label}</span>
                <span style="color: var(--text-secondary); font-size: 0.75rem;">{track_count} tracks</span>
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
        <div class="quota-container">
            <div class="quota-header">
                <span class="quota-label">API Quota · {status}</span>
                <span class="quota-label">{quota_used:,} / {daily_limit:,}</span>
            </div>
            <div class="quota-bar">
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
        <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; align-items: center;">
            <span class="badge badge-success">{matched_count} Matched</span>
            <span class="badge badge-error">{failed_count} Failed</span>
            <span class="badge badge-muted">{pending_count} Pending</span>
            <span style="margin-left: auto; color: var(--text-secondary); font-size: 0.8125rem;">
                {len(selected_tracks)} selected
            </span>
        </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        select_all = st.checkbox(
            "Select all",
            value=len(selected_tracks) == len(tracks) and len(tracks) > 0,
            key="select_all_checkbox"
        )
        
        if select_all and len(selected_tracks) != len(tracks):
            st.session_state.selected_tracks = set(range(len(tracks)))
            st.rerun()
        elif not select_all and len(selected_tracks) == len(tracks) and len(tracks) > 0:
            st.session_state.selected_tracks = set()
            st.rerun()
    
    st.markdown("---")
    
    # Track list
    for idx, track in enumerate(tracks):
        matches = youtube_matches.get(idx, [])
        selected_match_idx = selected_match_indices.get(idx, 0)
        error = matching_errors.get(idx, "")
        has_match = len(matches) > 0
        
        cols = st.columns([0.4, 0.8, 3, 1.5, 2])
        
        with cols[0]:
            is_selected = st.checkbox(
                "Select",
                value=idx in selected_tracks,
                key=f"track_select_{idx}",
                label_visibility="collapsed"
            )
            
            if is_selected and idx not in st.session_state.selected_tracks:
                st.session_state.selected_tracks.add(idx)
            elif not is_selected and idx in st.session_state.selected_tracks:
                st.session_state.selected_tracks.discard(idx)
        
        with cols[1]:
            if has_match and matches[selected_match_idx].thumbnail_url:
                st.image(matches[selected_match_idx].thumbnail_url, width=44)
            else:
                st.markdown('''
                    <div style="width: 44px; height: 44px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md);"></div>
                ''', unsafe_allow_html=True)
        
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


def render_download_button(selected_count: int) -> bool:
    """Render download button with count"""
    label = f"Download {selected_count} Tracks" if selected_count > 0 else "Select tracks to download"
    return st.button(
        label,
        type="primary",
        disabled=selected_count == 0
    )


def render_download_progress(current: int, total: int, current_track: str, status: str, thumbnail_url: str = None):
    """Render download progress"""
    st.markdown("#### Downloading")
    
    if thumbnail_url:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(thumbnail_url, use_container_width=True)
        
        with col2:
            progress = current / total if total > 0 else 0
            st.progress(progress)
            
            st.markdown(f'''
                <div style="display: flex; justify-content: space-between; margin-top: 8px; align-items: center;">
                    <span style="color: var(--text-secondary); font-size: 0.8125rem;">{current} of {total}</span>
                    <span style="color: var(--accent); font-weight: 500; font-size: 0.875rem;">{int(progress * 100)}%</span>
                </div>
                <p style="font-size: 0.8125rem; margin-top: 8px; color: var(--text-primary);">
                    {current_track[:50]}{"..." if len(current_track) > 50 else ""}
                </p>
            ''', unsafe_allow_html=True)
    else:
        progress = current / total if total > 0 else 0
        st.progress(progress)
        
        st.markdown(f'''
            <div style="display: flex; justify-content: space-between; margin-top: 8px; align-items: center;">
                <span style="color: var(--text-secondary); font-size: 0.8125rem;">{current} of {total}</span>
                <span style="color: var(--accent); font-weight: 500; font-size: 0.875rem;">{int(progress * 100)}%</span>
            </div>
            <p style="font-size: 0.8125rem; margin-top: 8px; color: var(--text-primary);">
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
            <div style="text-align: center; margin: 16px 0;">
                <h3 style="color: var(--success); margin-bottom: 4px;">Download Complete</h3>
                <p style="color: var(--text-secondary); margin: 0; font-size: 0.875rem;">Your music is ready</p>
            </div>
        ''', unsafe_allow_html=True)
    elif success_rate >= 50:
        st.markdown('''
            <div style="text-align: center; margin: 16px 0;">
                <h3 style="color: var(--warning); margin-bottom: 4px;">Partially Complete</h3>
                <p style="color: var(--text-secondary); margin: 0; font-size: 0.875rem;">Some tracks had issues</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="text-align: center; margin: 16px 0;">
                <h3 style="color: var(--error); margin-bottom: 4px;">Issues Encountered</h3>
                <p style="color: var(--text-secondary); margin: 0; font-size: 0.875rem;">Check failed tracks below</p>
            </div>
        ''', unsafe_allow_html=True)
    
    # Stats cards
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
        <p style="font-size: 0.8125rem; margin-top: 16px; text-align: center;">
            <span style="color: var(--text-muted);">Saved to:</span> 
            <code style="background: var(--surface); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; border: 1px solid var(--border);">
                {output_folder}
            </code>
        </p>
    ''', unsafe_allow_html=True)
    
    # Failed tracks
    if failed_tracks:
        with st.expander(f"View {len(failed_tracks)} failed tracks"):
            for track_name, error in failed_tracks:
                st.markdown(f'''
                    <div style="padding: 12px; background: var(--error-bg); border-left: 2px solid var(--error); border-radius: 0 6px 6px 0; margin-bottom: 8px;">
                        <div style="font-weight: 500; color: var(--text-primary); font-size: 0.875rem;">{track_name}</div>
                        <div style="font-size: 0.75rem; color: var(--error); margin-top: 4px;">{error}</div>
                    </div>
                ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Open Folder"):
            import subprocess
            subprocess.run(['open', output_folder])
    
    with col2:
        if st.button("Start New"):
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
