"""
Theme Module
Clean, professional CSS theme with restrained design
"""

import streamlit as st


def get_theme_css(dark_mode: bool = True) -> str:
    """Generate clean, professional CSS theme"""
    
    if dark_mode:
        colors = {
            # Solid backgrounds - no gradients
            'bg': '#0f0f0f',
            'surface': '#1a1a1a',
            'surface_elevated': '#222222',
            'border': '#2a2a2a',
            'border_hover': '#3a3a3a',
            
            # Text hierarchy
            'text_primary': '#fafafa',
            'text_secondary': '#a0a0a0',
            'text_muted': '#666666',
            
            # Single accent - Spotify green
            'accent': '#1DB954',
            'accent_hover': '#1ed760',
            'accent_subtle': 'rgba(29, 185, 84, 0.1)',
            
            # Status colors
            'success': '#22c55e',
            'success_bg': 'rgba(34, 197, 94, 0.1)',
            'success_border': 'rgba(34, 197, 94, 0.2)',
            'warning': '#f59e0b',
            'warning_bg': 'rgba(245, 158, 11, 0.1)',
            'warning_border': 'rgba(245, 158, 11, 0.2)',
            'error': '#ef4444',
            'error_bg': 'rgba(239, 68, 68, 0.1)',
            'error_border': 'rgba(239, 68, 68, 0.2)',
        }
    else:
        colors = {
            'bg': '#fafafa',
            'surface': '#ffffff',
            'surface_elevated': '#ffffff',
            'border': '#e5e5e5',
            'border_hover': '#d4d4d4',
            
            'text_primary': '#171717',
            'text_secondary': '#525252',
            'text_muted': '#a3a3a3',
            
            'accent': '#1DB954',
            'accent_hover': '#17a348',
            'accent_subtle': 'rgba(29, 185, 84, 0.08)',
            
            'success': '#16a34a',
            'success_bg': 'rgba(22, 163, 74, 0.08)',
            'success_border': 'rgba(22, 163, 74, 0.15)',
            'warning': '#d97706',
            'warning_bg': 'rgba(217, 119, 6, 0.08)',
            'warning_border': 'rgba(217, 119, 6, 0.15)',
            'error': '#dc2626',
            'error_bg': 'rgba(220, 38, 38, 0.08)',
            'error_border': 'rgba(220, 38, 38, 0.15)',
        }
    
    css = f"""
    <style>
        /* ========================================
           IMPORTS & VARIABLES
           ======================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        :root {{
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            
            /* Colors */
            --bg: {colors['bg']};
            --surface: {colors['surface']};
            --surface-elevated: {colors['surface_elevated']};
            --border: {colors['border']};
            --border-hover: {colors['border_hover']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --text-muted: {colors['text_muted']};
            --accent: {colors['accent']};
            --accent-hover: {colors['accent_hover']};
            --accent-subtle: {colors['accent_subtle']};
            --success: {colors['success']};
            --success-bg: {colors['success_bg']};
            --success-border: {colors['success_border']};
            --warning: {colors['warning']};
            --warning-bg: {colors['warning_bg']};
            --warning-border: {colors['warning_border']};
            --error: {colors['error']};
            --error-bg: {colors['error_bg']};
            --error-border: {colors['error_border']};
            
            /* Spacing - 4px grid */
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 12px;
            --space-4: 16px;
            --space-5: 20px;
            --space-6: 24px;
            --space-8: 32px;
            
            /* Radius - restrained */
            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 8px;
        }}
        
        /* ========================================
           GLOBAL & BACKGROUND
           ======================================== */
        .stApp {{
            background: var(--bg) !important;
            font-family: var(--font-sans);
            min-height: 100vh;
        }}
        
        /* Hide Streamlit chrome */
        #MainMenu, footer, header {{ 
            visibility: hidden !important; 
            height: 0 !important;
        }}
        header[data-testid="stHeader"] {{ 
            display: none !important; 
        }}
        
        /* ========================================
           LAYOUT
           ======================================== */
        .stApp > header,
        header[data-testid="stHeader"],
        [data-testid="stHeader"] {{
            display: none !important;
            height: 0 !important;
        }}
        
        .stApp,
        .stApp > div,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"] {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}
        
        .main,
        section.main,
        section[data-testid="stMain"] {{
            padding-top: 0 !important;
        }}
        
        /* Main content container */
        section.main > div.block-container,
        section[data-testid="stMain"] > div,
        .block-container,
        [data-testid="stMainBlockContainer"] {{
            max-width: 720px !important;
            padding: var(--space-4) var(--space-6) var(--space-6) !important;
            margin: 0 auto;
        }}
        
        [data-testid="stVerticalBlock"] {{
            gap: var(--space-3) !important;
        }}
        
        /* ========================================
           TYPOGRAPHY
           ======================================== */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em;
            line-height: 1.25;
        }}
        
        p, span, label {{ 
            color: var(--text-primary); 
            line-height: 1.5; 
        }}
        
        /* Header */
        .app-header {{
            text-align: left;
            padding: var(--space-4) 0 var(--space-5);
            border-bottom: 1px solid var(--border);
            margin-bottom: var(--space-4);
        }}
        
        .app-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0 0 var(--space-1) 0;
            letter-spacing: -0.02em;
        }}
        
        .app-subtitle {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            font-weight: 400;
            margin: 0;
        }}
        
        .section-label {{
            font-size: 0.6875rem;
            font-weight: 500;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--space-2);
        }}
        
        /* ========================================
           INPUTS
           ======================================== */
        .stTextInput > div > div > input {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
            padding: 10px 12px !important;
            font-size: 0.875rem !important;
            transition: border-color 0.15s ease !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--accent) !important;
            box-shadow: none !important;
            outline: none !important;
        }}
        
        .stTextInput > div > div > input::placeholder {{
            color: var(--text-muted) !important;
        }}
        
        /* Select boxes */
        .stSelectbox > div > div {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            transition: border-color 0.15s ease !important;
        }}
        
        .stSelectbox > div > div:hover {{
            border-color: var(--border-hover) !important;
        }}
        
        .stSelectbox > div > div > div {{
            color: var(--text-primary) !important;
        }}
        
        /* Dropdown menus */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"] {{
            background: var(--surface-elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }}
        
        [data-baseweb="popover"] li,
        [data-baseweb="menu"] li,
        [role="option"] {{
            color: var(--text-primary) !important;
            background: transparent !important;
        }}
        
        [data-baseweb="popover"] li:hover,
        [data-baseweb="menu"] li:hover,
        [role="option"]:hover {{
            background: var(--accent-subtle) !important;
        }}
        
        li[aria-selected="true"],
        [role="option"][aria-selected="true"] {{
            background: var(--accent-subtle) !important;
            color: var(--accent) !important;
        }}
        
        /* ========================================
           BUTTONS
           ======================================== */
        .stButton > button {{
            background: var(--accent) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: background 0.15s ease !important;
            min-height: 36px !important;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-hover) !important;
        }}
        
        .stButton > button:active {{
            opacity: 0.9 !important;
        }}
        
        .stButton > button:disabled {{
            background: var(--border) !important;
            color: var(--text-muted) !important;
            cursor: not-allowed !important;
        }}
        
        /* Secondary buttons */
        button[data-testid="baseButton-secondary"] {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }}
        
        button[data-testid="baseButton-secondary"]:hover {{
            background: var(--surface-elevated) !important;
            border-color: var(--border-hover) !important;
        }}
        
        /* ========================================
           CHECKBOXES
           ======================================== */
        .stCheckbox > label {{
            color: var(--text-primary) !important;
            cursor: pointer !important;
        }}
        
        /* ========================================
           PROGRESS BAR
           ======================================== */
        .stProgress > div > div {{
            background: var(--border) !important;
            border-radius: 100px;
            height: 6px !important;
        }}
        
        .stProgress > div > div > div {{
            background: var(--accent) !important;
            border-radius: 100px;
        }}
        
        /* ========================================
           BADGES
           ======================================== */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 3px 8px;
            border-radius: var(--radius-sm);
            font-size: 0.6875rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }}
        
        .badge-success {{
            background: var(--success-bg);
            color: var(--success);
            border: 1px solid var(--success-border);
        }}
        
        .badge-warning {{
            background: var(--warning-bg);
            color: var(--warning);
            border: 1px solid var(--warning-border);
        }}
        
        .badge-error {{
            background: var(--error-bg);
            color: var(--error);
            border: 1px solid var(--error-border);
        }}
        
        .badge-muted {{
            background: var(--surface);
            color: var(--text-secondary);
            border: 1px solid var(--border);
        }}
        
        /* ========================================
           METRICS
           ======================================== */
        [data-testid="stMetricValue"] {{
            color: var(--text-primary) !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: var(--text-secondary) !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}
        
        /* ========================================
           IMAGES
           ======================================== */
        .stImage img {{
            border-radius: var(--radius-md);
        }}
        
        /* ========================================
           DIVIDERS
           ======================================== */
        hr {{
            border: none !important;
            height: 1px !important;
            background: var(--border) !important;
            margin: var(--space-4) 0 !important;
        }}
        
        /* ========================================
           EXPANDER
           ======================================== */
        .streamlit-expanderHeader {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            color: var(--text-primary) !important;
        }}
        
        /* ========================================
           TRACK INFO
           ======================================== */
        .track-info {{ 
            flex: 1; 
            min-width: 0; 
        }}
        
        .track-name {{
            font-weight: 500;
            font-size: 0.875rem;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .track-artist {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* ========================================
           QUOTA BAR
           ======================================== */
        .quota-container {{ 
            margin-bottom: var(--space-4); 
        }}
        
        .quota-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: var(--space-1);
        }}
        
        .quota-label {{
            font-size: 0.6875rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        
        .quota-bar {{
            height: 4px;
            background: var(--border);
            border-radius: 100px;
            overflow: hidden;
        }}
        
        .quota-fill {{
            height: 100%;
            border-radius: 100px;
            transition: width 0.2s ease;
        }}
        
        /* ========================================
           SCROLLBAR
           ======================================== */
        ::-webkit-scrollbar {{ 
            width: 8px; 
            height: 8px; 
        }}
        ::-webkit-scrollbar-track {{ 
            background: transparent; 
        }}
        ::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 100px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--border-hover);
        }}
        
        /* ========================================
           UTILITY CLASSES
           ======================================== */
        .text-muted {{ color: var(--text-muted) !important; }}
        .text-secondary {{ color: var(--text-secondary) !important; }}
        .text-success {{ color: var(--success) !important; }}
        .text-error {{ color: var(--error) !important; }}
        .text-sm {{ font-size: 0.8125rem !important; }}
        .text-xs {{ font-size: 0.75rem !important; }}
        
        /* ========================================
           STAT CARDS
           ======================================== */
        .stat-card {{
            text-align: center;
            padding: var(--space-4);
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
        }}
        
        .stat-card-success {{
            border-color: var(--success-border);
        }}
        
        .stat-card-error {{
            border-color: var(--error-border);
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 600;
            line-height: 1.2;
        }}
        
        .stat-label {{
            font-size: 0.6875rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: var(--space-1);
        }}
    </style>
    """
    
    return css


def apply_theme(dark_mode: bool = True):
    """Apply the clean, professional theme"""
    st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)


def render_theme_toggle():
    """Render the theme toggle"""
    col1, col2 = st.columns([12, 1])
    
    with col2:
        current_mode = st.session_state.get('dark_mode', True)
        toggle_icon = "◐" if current_mode else "◑"
        
        if st.button(toggle_icon, key="theme_toggle", help="Toggle theme"):
            st.session_state.dark_mode = not current_mode
            st.rerun()
