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
            'text_muted': '#737373',
            
            'accent': '#1DB954',
            'accent_hover': '#17a348',
            'accent_subtle': 'rgba(29, 185, 84, 0.08)',
            
            'success': '#16a34a',
            'success_bg': 'rgba(22, 163, 74, 0.08)',
            'success_border': 'rgba(22, 163, 74, 0.2)',
            'warning': '#d97706',
            'warning_bg': 'rgba(217, 119, 6, 0.08)',
            'warning_border': 'rgba(217, 119, 6, 0.2)',
            'error': '#dc2626',
            'error_bg': 'rgba(220, 38, 38, 0.08)',
            'error_border': 'rgba(220, 38, 38, 0.2)',
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
            padding: 0 0 var(--space-4) 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: var(--space-6);
        }}
        
        .app-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0 0 var(--space-1) 0;
            letter-spacing: -0.02em;
        }}
        
        .app-subtitle {{
            font-size: 0.875rem;
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
            padding: 12px 16px !important;
            font-size: 0.875rem !important;
            transition: border-color 0.15s ease !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-subtle) !important;
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
            transition: all 0.15s ease !important;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-subtle) !important;
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
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24) !important;
        }}
        
        [data-baseweb="popover"] li,
        [data-baseweb="menu"] li,
        [role="option"] {{
            color: var(--text-primary) !important;
            background: transparent !important;
            padding: var(--space-2) var(--space-3) !important;
            transition: background 0.15s ease !important;
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
            padding: 12px 24px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: background 0.15s ease !important;
            min-height: 40px !important;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-hover) !important;
        }}
        
        .stButton > button:focus {{
            box-shadow: 0 0 0 3px var(--accent-subtle) !important;
            outline: none !important;
        }}
        
        .stButton > button:active {{
            opacity: 0.9 !important;
        }}
        
        .stButton > button:disabled {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-muted) !important;
            cursor: not-allowed !important;
            opacity: 0.6 !important;
        }}
        
        /* Secondary buttons */
        button[data-testid="baseButton-secondary"] {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
            padding: 12px 24px !important;
            min-height: 40px !important;
        }}
        
        button[data-testid="baseButton-secondary"]:hover {{
            background: var(--surface-elevated) !important;
            border-color: var(--border-hover) !important;
        }}
        
        button[data-testid="baseButton-secondary"]:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-subtle) !important;
        }}
        
        /* Theme toggle - inline with header */
        [data-testid="column"]:last-child:has(button[key="theme_toggle"]) {{
            display: flex !important;
            align-items: flex-start !important;
            justify-content: flex-end !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        button[key="theme_toggle"],
        .stButton > button[kind="secondary"] {{
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            min-height: 32px !important;
            max-width: 32px !important;
            max-height: 32px !important;
            padding: 0 !important;
            background: transparent !important;
            border: 1px solid var(--border) !important;
            border-radius: 6px !important;
            color: var(--text-secondary) !important;
            font-size: 0.875rem !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
        }}
        
        button[key="theme_toggle"]:hover,
        .stButton > button[kind="secondary"]:hover {{
            background: var(--surface) !important;
            border-color: var(--border-hover) !important;
            color: var(--text-primary) !important;
            box-shadow: none !important;
        }}
        
        button[key="theme_toggle"]:focus,
        .stButton > button[kind="secondary"]:focus {{
            border-color: var(--border-hover) !important;
            box-shadow: none !important;
            outline: none !important;
        }}
        
        /* ========================================
           CHECKBOXES
           ======================================== */
        .stCheckbox > label {{
            color: var(--text-primary) !important;
            cursor: pointer !important;
        }}
        
        .stCheckbox input[type="checkbox"] {{
            accent-color: var(--accent) !important;
            cursor: pointer !important;
        }}
        
        .stCheckbox input[type="checkbox"]:focus {{
            outline: 2px solid var(--accent) !important;
            outline-offset: 2px !important;
        }}
        
        /* ========================================
           PROGRESS BAR
           ======================================== */
        .stProgress > div > div {{
            background: var(--border) !important;
            border-radius: 100px;
            height: 8px !important;
        }}
        
        .stProgress > div > div > div {{
            background: var(--accent) !important;
            border-radius: 100px;
            transition: width 0.3s ease;
        }}
        
        /* ========================================
           BADGES
           ======================================== */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: var(--radius-sm);
            font-size: 0.6875rem;
            font-weight: 500;
            letter-spacing: 0.01em;
        }}
        
        .badge-success {{
            background: var(--success-bg);
            color: var(--success);
            border: 1px solid var(--success-border);
            font-weight: 600;
        }}
        
        .badge-warning {{
            background: var(--warning-bg);
            color: var(--warning);
            border: 1px solid var(--warning-border);
            font-weight: 600;
        }}
        
        .badge-error {{
            background: var(--error-bg);
            color: var(--error);
            border: 1px solid var(--error-border);
            font-weight: 600;
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
            transition: all 0.15s ease !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            border-color: var(--border-hover) !important;
        }}
        
        /* ========================================
           TRACK INFO
           ======================================== */
        .playlist-info-header {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            flex-wrap: wrap;
        }}
        
        .playlist-name {{
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--text-primary);
        }}
        
        .playlist-track-count {{
            color: var(--text-secondary);
            font-size: 0.75rem;
        }}
        
        .track-thumbnail-empty {{
            width: 48px;
            height: 48px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-size: 1.25rem;
        }}
        
        .track-info {{ 
            flex: 1; 
            min-width: 0; 
        }}
        
        .track-name {{
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .track-artist {{
            font-size: 0.8125rem;
            font-weight: 400;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-top: 2px;
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
            transition: width 0.3s ease, background 0.3s ease;
        }}
        
        /* ========================================
           SCROLLBAR
           ======================================== */
        ::-webkit-scrollbar {{ 
            width: 12px; 
            height: 12px; 
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
            transition: border-color 0.15s ease;
        }}
        
        .stat-card:hover {{
            border-color: var(--border-hover);
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
        
        /* ========================================
           TRACK TABLE
           ======================================== */
        .track-row {{
            padding: var(--space-3) 0;
            border-bottom: 1px solid var(--border);
            transition: background 0.15s ease;
        }}
        
        .track-row:hover {{
            background: var(--surface);
        }}
        
        .track-row:last-child {{
            border-bottom: none;
        }}
        
        .stats-header {{
            display: flex;
            gap: var(--space-3);
            margin-bottom: var(--space-4);
            padding: var(--space-3);
            flex-wrap: wrap;
            align-items: center;
            background: var(--surface);
            border-radius: var(--radius-md);
        }}
        
        .stats-count {{
            margin-left: auto;
            color: var(--text-secondary);
            font-size: 0.8125rem;
        }}
        
        /* ========================================
           SECTION HEADERS
           ======================================== */
        .section-header {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: var(--space-4);
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--border);
            letter-spacing: -0.01em;
        }}
        
        /* ========================================
           DOWNLOAD PROGRESS
           ======================================== */
        .download-progress-container {{
            margin: var(--space-4) 0;
        }}
        
        .progress-meta {{
            display: flex;
            justify-content: space-between;
            margin-top: var(--space-2);
            align-items: center;
        }}
        
        .progress-count {{
            color: var(--text-secondary);
            font-size: 0.8125rem;
        }}
        
        .progress-percent {{
            color: var(--accent);
            font-weight: 500;
            font-size: 0.875rem;
        }}
        
        .progress-track-name {{
            font-size: 0.875rem;
            margin-top: var(--space-2);
            color: var(--text-primary);
            font-weight: 500;
        }}
        
        /* ========================================
           COMPLETION SUMMARY
           ======================================== */
        .completion-header {{
            text-align: center;
            margin: var(--space-6) 0 var(--space-4) 0;
        }}
        
        .completion-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: var(--space-2);
            letter-spacing: -0.02em;
        }}
        
        .completion-subtitle {{
            color: var(--text-secondary);
            margin: 0;
            font-size: 0.875rem;
        }}
        
        .folder-path-container {{
            text-align: center;
            margin-top: var(--space-4);
            padding: var(--space-3);
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
        }}
        
        .folder-path-label {{
            color: var(--text-muted);
            font-size: 0.8125rem;
        }}
        
        .folder-path {{
            background: var(--surface);
            padding: var(--space-1) var(--space-3);
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            border: 1px solid var(--border);
            font-family: ui-monospace, 'Cascadia Code', 'SF Mono', Monaco, 'Courier New', monospace;
            color: var(--text-primary);
            word-break: break-all;
        }}
        
        /* ========================================
           FAILED TRACKS
           ======================================== */
        .failed-track-item {{
            padding: var(--space-3);
            background: var(--error-bg);
            border-left: 3px solid var(--error);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            margin-bottom: var(--space-2);
            transition: background 0.15s ease;
        }}
        
        .failed-track-item:hover {{
            background: var(--error-border);
        }}
        
        .failed-track-name {{
            font-weight: 500;
            color: var(--text-primary);
            font-size: 0.875rem;
        }}
        
        .failed-track-error {{
            font-size: 0.75rem;
            color: var(--error);
            margin-top: var(--space-1);
        }}
        
        /* ========================================
           RESPONSIVE
           ======================================== */
        @media (max-width: 768px) {{
            .app-title {{
                font-size: 1.25rem;
            }}
            
            .completion-title {{
                font-size: 1.25rem;
            }}
            
            .stat-value {{
                font-size: 1.25rem;
            }}
            
            [data-testid="column"]:last-child:has(.stButton) {{
                top: 12px !important;
                right: 12px !important;
            }}
            
            .stats-header {{
                padding: var(--space-2);
            }}
        }}
        
        @media (max-width: 480px) {{
            section.main > div.block-container,
            section[data-testid="stMain"] > div,
            .block-container,
            [data-testid="stMainBlockContainer"] {{
                padding: 0 var(--space-4) var(--space-4) !important;
            }}
            
            .app-header {{
                padding: var(--space-3) 0;
                margin-bottom: var(--space-4);
            }}
            
            .stat-card {{
                padding: var(--space-3);
            }}
        }}
    </style>
    """
    
    return css


def apply_theme(dark_mode: bool = True):
    """Apply the clean, professional theme"""
    st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)


def render_theme_toggle():
    """Deprecated - theme toggle now integrated in header"""
    pass
