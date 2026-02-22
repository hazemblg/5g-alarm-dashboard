import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# PAGE CONFIG - Must be the first Streamlit command
st.set_page_config(
    page_title="DRS - 5G Alarm Management System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# User credentials database
USERS = {
    "admin": {"password": "admin123", "role": "Admin", "email": "admin@orange.tn", "full_name": "Administrator"},
    "hazemblg": {"password": "hazem1234", "role": "Engineer", "email": "hazem.benbelgacem@enetcom.u-sfax.tn", "full_name": "Hazem Ben Belgacem"},
    "operator": {"password": "operator123", "role": "Operator", "email": "operator@orange.tn", "full_name": "Network Operator"}
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'full_name' not in st.session_state:
    st.session_state.full_name = ""

def verify_login(username, password):
    """Verify user credentials"""
    if username in USERS and USERS[username]["password"] == password:
        return True, USERS[username]
    return False, None

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_role = ""
    st.session_state.email = ""
    st.session_state.full_name = ""
    st.rerun()

def show_login_page():
    """Display the login page with custom styling"""

    # Custom CSS for login page
    st.markdown("""
        <style>
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Login page styles */
        .stApp {
            background: linear-gradient(135deg, #0e1117 0%, #1e293b 50%, #0e1117 100%) !important;
        }
        
        .logo-section {
            text-align: center;
            margin-bottom: 35px;
        }
        
        .logo-title {
            font-size: 2.5em;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .logo-subtitle {
            color: #94a3b8;
            font-size: 1em;
            margin-bottom: 4px;
        }
        
        .logo-orange {
            color: #ff9500;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        .demo-credentials {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 25px;
            text-align: center;
            color: #cbd5e1;
        }
        
        .demo-credentials code {
            background: #334155;
            padding: 2px 8px;
            border-radius: 4px;
            color: #fbbf24;
            font-family: 'Courier New', monospace;
        }
        
        /* Streamlit input styling */
        .stTextInput > div > div > input {
            background: #334155 !important;
            border: 2px solid #475569 !important;
            color: #fafafa !important;
            padding: 14px 16px !important;
            border-radius: 10px !important;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: white !important;
            padding: 16px !important;
            border: none !important;
            border-radius: 10px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.6) !important;
        }
        
        .login-footer {
            text-align: center;
            margin-top: 20px;
            color: #64748b;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div class="logo-section">
                <h1 class="logo-title">🚨 DRS Alarms</h1>
                <p class="logo-subtitle">5G Network Monitoring System</p>
                <p class="logo-orange">Orange Tunisia</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center; color: #cbd5e1; margin: 30px 0 20px 0;'>Sign In</h2>", unsafe_allow_html=True)

        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

            submit = st.form_submit_button("Login")

            if submit:
                if username and password:
                    is_valid, user_data = verify_login(username, password)
                    if is_valid:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_role = user_data["role"]
                        st.session_state.email = user_data["email"]
                        st.session_state.full_name = user_data["full_name"]
                        st.success(f"Welcome {user_data['full_name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

        # Demo credentials
        st.markdown("""
            <div class="demo-credentials">
                <p><strong>Demo Credentials:</strong></p>
                <p><strong>Admin:</strong> <code>admin</code> / <code>admin123</code></p>
                <p><strong>Hazem:</strong> <code>hazemblg</code> / <code>hazem1234</code></p>
                <p><strong>Operator:</strong> <code>operator</code> / <code>operator123</code></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="login-footer">
                <p>&copy; 2026 Orange Tunisia - DRS Alarms Dashboard</p>
            </div>
        """, unsafe_allow_html=True)

# Check authentication - show login page if not authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()



# GLOBAL THEME (DARK – PREMIUM) + PWA MOBILE SUPPORT

st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="DRS Alarms">
<meta name="theme-color" content="#3b82f6">

<style>

/* Base Styles */
html, body, [class*="css"] {
    background-color: #0e1117;
    color: #fafafa;
    font-family: 'Segoe UI', sans-serif;
}

/* Mobile Viewport Fix */
@viewport {
    width: device-width;
    zoom: 1.0;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
    padding: 20px;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

.filter-badge {
    display: inline-block;
    background-color: #1e293b;
    color: #38bdf8;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    margin: 2px 2px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.kpi-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

.kpi-title {
    font-size: 14px;
    color: #9ca3af;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
    margin-top: 6px;
}

.block {
    background-color: #111827;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

.dashboard-card {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    margin: 10px;
}

.dashboard-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.dashboard-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.dashboard-title {
    font-size: 20px;
    font-weight: 700;
    color: white;
}

.dashboard-desc {
    font-size: 14px;
    color: #cbd5e1;
    margin-top: 8px;
}

.section-header {
    background: linear-gradient(90deg, #1e293b, #334155);
    padding: 15px;
    border-radius: 10px;
    margin: 20px 0 10px 0;
    border-left: 4px solid #3b82f6;
}

/* Hover effects for circular dashboard cards */
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.dashboard-circle:hover {
    animation: pulse 1.5s ease-in-out infinite;
}

/* Responsive grid */
@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

/* ============================================ */
/* MOBILE RESPONSIVE ENHANCEMENTS */
/* ============================================ */

/* Mobile: Touch-friendly buttons */
button, [data-testid="stButton"] button {
    min-height: 48px !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    transition: all 0.2s ease;
}

button:active {
    transform: scale(0.98);
}

/* Mobile: Larger tap targets */
@media (max-width: 768px) {
    button, [data-testid="stButton"] button {
        min-height: 56px !important;
        font-size: 18px !important;
        margin: 8px 0 !important;
    }
    
    /* Adjust circle size for mobile */
    .dashboard-circle, [style*="width: 180px"] {
        width: 140px !important;
        height: 140px !important;
    }
    
    /* Smaller emoji on mobile */
    [style*="font-size: 72px"] {
        font-size: 56px !important;
    }
    
    /* Adjust metrics for mobile */
    .kpi-card {
        padding: 16px !important;
        margin-bottom: 10px;
    }
    
    .kpi-value {
        font-size: 24px !important;
    }
    
    .kpi-title {
        font-size: 12px !important;
    }
    
    /* Stack columns on mobile */
    [data-testid="column"] {
        min-width: 100% !important;
        margin-bottom: 12px;
    }
    
    /* Sidebar optimization */
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }
    
    /* Better spacing for mobile */
    .block-container {
        padding: 1rem !important;
    }
    
    /* Optimize header for mobile */
    h1 {
        font-size: 32px !important;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-size: 24px !important;
    }
    
    h3 {
        font-size: 20px !important;
    }
    
    /* Charts responsive */
    [data-testid="stPlotlyChart"] {
        width: 100% !important;
        overflow-x: auto;
    }
    
    /* Dataframe scrollable */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}

/* Small mobile devices */
@media (max-width: 480px) {
    /* 2-column grid for metrics */
    [data-testid="column"]:nth-child(n) {
        width: 48% !important;
        display: inline-block;
        margin: 1%;
    }
    
    /* Single column for dashboards */
    .dashboard-circle {
        width: 160px !important;
        height: 160px !important;
        margin: 0 auto 16px auto !important;
    }
    
    /* Adjust quick metrics */
    [style*="height: 140px"] {
        height: 120px !important;
        padding: 12px !important;
    }
    
    [style*="font-size: 32px"] {
        font-size: 24px !important;
    }
    
    [style*="font-size: 28px"] {
        font-size: 22px !important;
    }
}

/* Landscape mode optimization */
@media (max-width: 896px) and (orientation: landscape) {
    .block-container {
        padding: 0.5rem !important;
    }
    
    .kpi-card {
        padding: 12px !important;
    }
    
    section[data-testid="stSidebar"] {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    section[data-testid="stSidebar"]:hover {
        transform: translateX(0);
    }
}

/* Touch gestures - smooth scrolling */
* {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
}

/* Prevent text selection on buttons */
button, [data-testid="stButton"] button {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
}

/* PWA Install Button */
.pwa-install-prompt {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    color: white;
    padding: 12px 24px;
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
    cursor: pointer;
    font-weight: 600;
    display: none;
}

@media (max-width: 768px) {
    .pwa-install-prompt {
        display: block;
    }
}

/* Loading spinner optimization for mobile */
[data-testid="stSpinner"] {
    width: 48px !important;
    height: 48px !important;
}

/* Safe area for notched devices (iPhone X+) */
@supports (padding: max(0px)) {
    body {
        padding-left: max(0px, env(safe-area-inset-left));
        padding-right: max(0px, env(safe-area-inset-right));
        padding-top: max(0px, env(safe-area-inset-top));
        padding-bottom: max(0px, env(safe-area-inset-bottom));
    }
}

</style>

<script>
// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed:', err));
    });
}

// PWA Install Prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Show install button
    const installBtn = document.createElement('div');
    installBtn.className = 'pwa-install-prompt';
    installBtn.innerHTML = 'Installer l\\'app';
    installBtn.onclick = () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
            }
            deferredPrompt = null;
            installBtn.style.display = 'none';
        });
    };
    document.body.appendChild(installBtn);
});

// Mobile optimization - Disable pull-to-refresh
document.body.style.overscrollBehavior = 'none';

// Prevent double-tap zoom on buttons
let lastTouchEnd = 0;
document.addEventListener('touchend', (event) => {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// Optimize for mobile performance
if (/Mobi|Android/i.test(navigator.userAgent)) {
    document.documentElement.style.setProperty('--animation-duration', '0.2s');
    console.log('Mobile device detected - optimizations applied');
}

// Custom Smooth Cursor Effect - Simple Circle
(function() {
    console.log('Cursor script started');
    
    // Skip on mobile devices
    if (window.matchMedia('(max-width: 768px)').matches || 'ontouchstart' in window) {
        console.log('Mobile device detected - cursor disabled');
        return;
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCursor);
    } else {
        initCursor();
    }
    
    function initCursor() {
        console.log('Initializing cursor');
        
        // Create single cursor circle
        const cursor = document.createElement('div');
        cursor.className = 'custom-cursor';
        cursor.style.cssText = `
            position: fixed;
            width: 14px;
            height: 14px;
            background: #ffffff;
            border: 2px solid rgba(0, 0, 0, 0.3);
            border-radius: 50%;
            pointer-events: none;
            z-index: 999999;
            transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            transform: translate(-50%, -50%);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            opacity: 1;
            display: block;
            visibility: visible;
        `;
        document.body.appendChild(cursor);
        
        console.log('Cursor element created:', cursor);
        
        let mouseX = 0, mouseY = 0;
        let cursorX = 0, cursorY = 0;
        
        // Track mouse movement
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });
        
        // Smooth cursor animation with easing
        function animate() {
            // Smooth follow effect
            const speed = 0.2;
            cursorX += (mouseX - cursorX) * speed;
            cursorY += (mouseY - cursorY) * speed;
            
            cursor.style.left = cursorX + 'px';
            cursor.style.top = cursorY + 'px';
            
            requestAnimationFrame(animate);
        }
        
        animate();
        console.log('Animation loop started');
        
        // Hover effect on interactive elements
        const interactiveElements = 'button, a, input, select, textarea, [data-testid="stButton"], .stButton, [role="button"]';
        
        document.addEventListener('mouseover', (e) => {
            if (e.target.closest(interactiveElements)) {
                cursor.classList.add('hover');
            }
        });
        
        document.addEventListener('mouseout', (e) => {
            if (e.target.closest(interactiveElements)) {
                cursor.classList.remove('hover');
            }
        });
        
        // Click effect
        document.addEventListener('mousedown', () => {
            cursor.classList.add('click');
        });
        
        document.addEventListener('mouseup', () => {
            cursor.classList.remove('click');
        });
        
        // Hide cursor when leaving window
        document.addEventListener('mouseleave', () => {
            cursor.style.opacity = '0';
        });
        
        document.addEventListener('mouseenter', () => {
            cursor.style.opacity = '1';
        });
        
        console.log('Smooth white circle cursor fully activated');
    }
})();

// Handle orientation change
window.addEventListener('orientationchange', () => {
    setTimeout(() => {
        window.scrollTo(0, 1);
    }, 100);
});

// Add to home screen detection
window.addEventListener('appinstalled', () => {
    console.log('PWA installed successfully!');
});
</script>

""", unsafe_allow_html=True)


# LOAD DATA

@st.cache_data
def load_data_from_file(file_path):
    """Load data from a specific file path"""
    df = pd.read_excel(file_path, header=5, engine='openpyxl')
    if df.shape[1] > 18:
        df = df.iloc[:, :18]

    # Assign column names
    df.columns = [
        'Root_Alarm', 'Severity', 'Alarm_Name', 'First_Occurrence', 'Last_Occurrence',
        'Duplication_Count', 'Alarm_Type', 'Alarm_Group', 'Location', 'Node',
        'Managed_Object', 'Managed_Object_Instance', 'Agent', 'Manager',
        'Alarm_Sequence_Number', 'Additional_Text', 'Acknowledgement_Status', 'Subnet'
    ]

    # Convert data types
    df['First_Occurrence'] = pd.to_datetime(df['First_Occurrence'], errors='coerce')
    df['Last_Occurrence'] = pd.to_datetime(df['Last_Occurrence'], errors='coerce')
    df['Duplication_Count'] = pd.to_numeric(df['Duplication_Count'], errors='coerce')

    # Drop rows with all NaN values
    df = df.dropna(how='all')

    return df

def load_data():
    """Load data with file uploader if needed (not cached)"""
    import os

    # Try different paths for local and cloud deployment
    possible_paths = [
        "alarms1.xlsx",  # Same folder (for Streamlit Cloud)
        r"C:\Users\t14\Downloads\alarms1.xlsx",  # Local path
        "data/alarms1.xlsx",  # Data subfolder
    ]

    path = None
    for p in possible_paths:
        if os.path.exists(p):
            path = p
            break

    if path is not None:
        try:
            return load_data_from_file(path)
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {str(e)}")

    # File not found - show uploader
    st.warning("Fichier alarms1.xlsx introuvable! Veuillez télécharger le fichier.")
    uploaded_file = st.file_uploader("Télécharger le fichier Excel des alarmes", type=['xlsx'])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=5, engine='openpyxl')
            if df.shape[1] > 18:
                df = df.iloc[:, :18]

            df.columns = [
                'Root_Alarm', 'Severity', 'Alarm_Name', 'First_Occurrence', 'Last_Occurrence',
                'Duplication_Count', 'Alarm_Type', 'Alarm_Group', 'Location', 'Node',
                'Managed_Object', 'Managed_Object_Instance', 'Agent', 'Manager',
                'Alarm_Sequence_Number', 'Additional_Text', 'Acknowledgement_Status', 'Subnet'
            ]

            df['First_Occurrence'] = pd.to_datetime(df['First_Occurrence'], errors='coerce')
            df['Last_Occurrence'] = pd.to_datetime(df['Last_Occurrence'], errors='coerce')
            df['Duplication_Count'] = pd.to_numeric(df['Duplication_Count'], errors='coerce')
            df = df.dropna(how='all')

            if len(df) == 0:
                st.error("Le fichier Excel est vide ou mal formaté!")
                st.stop()

            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")
            st.stop()
    else:
        st.info("Téléchargez votre fichier Excel d'alarmes pour commencer.")
        st.stop()

df = load_data()


# CALCUL DES KPI GLOBAUX
def calculate_kpis(data):
    """Calcul des KPIs pour tous les dashboards"""
    kpis = {
        'total_alarms': len(data),
        'critical': len(data[data['Severity'] == 'Critical']),
        'major': len(data[data['Severity'] == 'Major']),
        'minor': len(data[data['Severity'] == 'Minor']),
        'warning': len(data[data['Severity'] == 'Warning']),
        'unacknowledged': len(data[data['Acknowledgement_Status'] == 'Unacknowledged']),
        'root_alarms': len(data[data['Root_Alarm'] == 'Root alarm']),
    }

    # Calcul du MTTR (Mean Time To Repair) en heures
    data_with_duration = data.dropna(subset=['First_Occurrence', 'Last_Occurrence'])
    if len(data_with_duration) > 0:
        data_with_duration['duration'] = (
            data_with_duration['Last_Occurrence'] - data_with_duration['First_Occurrence']
        ).dt.total_seconds() / 3600
        kpis['mttr'] = data_with_duration['duration'].mean()
    else:
        kpis['mttr'] = 0

    # Disponibilité réseau (estimation basée sur les alarmes critiques)
    total_hours = 24 * 30  # 30 jours
    if kpis['total_alarms'] > 0:
        downtime_hours = kpis['critical'] * (kpis['mttr'] if kpis['mttr'] > 0 else 1)
        kpis['availability'] = max(0, min(100, ((total_hours - downtime_hours) / total_hours) * 100))
    else:
        kpis['availability'] = 100

    return kpis


# INITIALISATION SESSION STATE
if 'dashboard_type' not in st.session_state:
    st.session_state.dashboard_type = None


# PAGE DE SÉLECTION DU DASHBOARD
if st.session_state.dashboard_type is None:
    # User welcome and logout
    col_welcome1, col_welcome2 = st.columns([4, 1])
    with col_welcome1:
        st.markdown(f"### 👋 Welcome, **{st.session_state.get('full_name', 'User')}**")
        st.caption(f"{st.session_state.get('email', 'N/A')} | Role: {st.session_state.get('role', 'N/A')}")
    with col_welcome2:
        if st.button("Logout", use_container_width=True, type="primary"):
            logout()

    st.markdown("---")

    st.markdown("""
    <div style='text-align: center; padding: 30px 0 40px 0;'>
        <h1 style='font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;'>
            🚨 DRS Alarm Management
        </h1>
        <p style='font-size: 20px; color: #94a3b8; font-weight: 300;'>Système de Gestion des Alarmes 5G</p>
        <p style='font-size: 16px; color: #64748b; margin-top: 5px;'>Direction Réseaux et Services</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistiques rapides en haut
    st.markdown("<h3 style='text-align: center; color: #cbd5e1; margin-bottom: 20px;'>📈 Vue d'Ensemble du Réseau</h3>", unsafe_allow_html=True)

    quick_kpis = calculate_kpis(df)
    q1, q2, q3, q4, q5 = st.columns(5)

    def quick_metric(col, icon, label, value, color):
        col.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}15, {color}05); border: 2px solid {color}40; 
                    border-radius: 16px; padding: 20px; text-align: center; height: 140px; display: flex; 
                    flex-direction: column; justify-content: center;'>
            <div style='font-size: 32px; margin-bottom: 8px;'>{icon}</div>
            <div style='font-size: 28px; font-weight: 700; color: {color}; margin-bottom: 4px;'>{value}</div>
            <div style='font-size: 13px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

    quick_metric(q1, "📊", "Total Alarmes", f"{quick_kpis['total_alarms']:,}", "#3b82f6")
    quick_metric(q2, "🔴", "Critiques", f"{quick_kpis['critical']:,}", "#ef4444")
    quick_metric(q3, "🟠", "Majeures", f"{quick_kpis['major']:,}", "#f97316")
    quick_metric(q4, "⚠️", "Non Acquittées", f"{quick_kpis['unacknowledged']:,}", "#eab308")
    quick_metric(q5, "✅", "Disponibilité", f"{quick_kpis['availability']:.1f}%", "#10b981")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #cbd5e1; margin: 40px 0 30px 0;'>🎯 Sélectionnez Votre Dashboard</h3>", unsafe_allow_html=True)

    # Cartes circulaires en grille 2x2
    col1, col2, col3, col4 = st.columns(4)

    dashboards = [
        {
            "col": col1,
            "icon": "🎯",
            "title": "Management",
            "subtitle": "Vue Stratégique",
            "description": "Analyse globale & KPIs",
            "color": "#3b82f6",
            "gradient": "linear-gradient(135deg, #1e40af, #3b82f6)",
            "key": "mgmt",
            "type": "Management",
        },
        {
            "col": col2,
            "icon": "📡",
            "title": "Radio RAN",
            "subtitle": "Support Radio",
            "description": "Équipements & Sites",
            "color": "#8b5cf6",
            "gradient": "linear-gradient(135deg, #6d28d9, #8b5cf6)",
            "key": "radio",
            "type": "Radio"
        },
        {
            "col": col3,
            "icon": "📶",
            "title": "Transmission",
            "subtitle": "Support FH",
            "description": "Faisceaux Hertziens",
            "color": "#10b981",
            "gradient": "linear-gradient(135deg, #059669, #10b981)",
            "key": "fh",
            "type": "FH"
        },
        {
            "col": col4,
            "icon": "🔋",
            "title": "Énergie",
            "subtitle": "Support Power",
            "description": "Alimentation & UPS",
            "color": "#f59e0b",
            "gradient": "linear-gradient(135deg, #d97706, #f59e0b)",
            "key": "energy",
            "type": "Energy"
        }
    ]

    for dashboard in dashboards:
        with dashboard["col"]:
            st.markdown(f"""
<div style='text-align: center; margin-bottom: 20px;'>
    <div style='width: 180px; height: 180px; margin: 0 auto 20px auto; 
                background: {dashboard["gradient"]}; border-radius: 50%; 
                display: flex; align-items: center; justify-content: center; 
                box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 0 8px {dashboard["color"]}20;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;'>
        <div style='font-size: 72px;'>{dashboard["icon"]}</div>
    </div>
    <h3 style='color: {dashboard["color"]}; font-size: 20px; font-weight: 700; margin: 0 0 5px 10px; padding: 0; text-align: center; display: block; width: 100%;'>{dashboard["title"]}</h3>
    <p style='color: #94a3b8; font-size: 13px; margin: 0 0 3px 0; padding: 0; font-weight: 600; text-align: center; display: block; width: 100%;'>{dashboard["subtitle"]}</p>
    <p style='color: #64748b; font-size: 12px; margin: 0 0 15px 0; padding: 0; text-align: center; display: block; width: 100%;'>{dashboard["description"]}</p>
</div>
""", unsafe_allow_html=True)

            if st.button("Accéder →", key=dashboard["key"], use_container_width=True, type="primary"):
                st.session_state.dashboard_type = dashboard["type"]
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Footer avec informations
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #1e293b, #0f172a); 
                border-radius: 16px; margin-top: 40px; border: 1px solid #334155;'>
        <p style='color: #94a3b8; font-size: 14px; margin: 0;'>
            <strong>Astuce:</strong> Utilisez les filtres latéraux pour affiner vos analyses | 
            Les données sont mises à jour en temps réel
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# HEADER COMMUN À TOUS LES DASHBOARDS
col_header1, col_header2, col_header3 = st.columns([3, 1, 1])
with col_header1:
    st.markdown(f"## 🚨 Dashboard {st.session_state.dashboard_type}")
    user_info = f" {st.session_state.get('full_name', 'User')} ({st.session_state.get('role', 'N/A')})"
    st.caption(f"{user_info} | 📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col_header2:
    if st.button("🔙 ", use_container_width=True):
        st.session_state.dashboard_type = None
        st.rerun()
with col_header3:
    if st.button("Déconnexion", use_container_width=True, type="primary"):
        logout()


# SIDEBAR FILTERS COMMUN
with st.sidebar:
    st.markdown("""
        <style>
        /* Advanced Sidebar Styling with Glassmorphism */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0f1e 0%, #0f172a 50%, #020617 100%) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        /* Main Filter Header with Glow Effect */
        .filter-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #6366f1 100%);
            padding: 20px 15px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            position: relative;
            overflow: hidden;
            animation: headerPulse 3s ease-in-out infinite;
        }
        
        .filter-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s linear infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }
        
        @keyframes headerPulse {
            0%, 100% { box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1) inset; }
            50% { box-shadow: 0 8px 40px rgba(59, 130, 246, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.15) inset; }
        }
        
        .filter-header h2 {
            position: relative;
            z-index: 1;
            margin: 0;
            color: white;
            font-size: 22px;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
        }
        
        /* Filter Sections with Glass Effect */
        .filter-section {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2),
                        0 0 0 1px rgba(255, 255, 255, 0.05) inset;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .filter-section:hover {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15),
                        0 0 0 1px rgba(255, 255, 255, 0.08) inset;
            transform: translateY(-2px);
        }
        
        .filter-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.6), transparent);
            border-radius: 14px 14px 0 0;
        }
        
        /* Section Titles with Icon Integration */
        .filter-section-title {
            color: #60a5fa;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            text-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
        }
        
        .filter-section-title::before {
            content: '';
            width: 3px;
            height: 16px;
            background: linear-gradient(180deg, #3b82f6, #6366f1);
            border-radius: 2px;
        }
        
        /* Enhanced Input Styling */
        .stMultiSelect > div > div {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stMultiSelect > div > div:hover {
            border-color: rgba(59, 130, 246, 0.6) !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2) !important;
        }
        
        .stDateInput > div > div > input {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
        }
        
        /* Filter Badge with Glow */
        .filter-badge {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(99, 102, 241, 0.2));
            color: #60a5fa;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
            margin: 3px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
        }
        
        .filter-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }
        
        /* Active Filters Summary Box */
        .filters-active-box {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(16, 185, 129, 0.1));
            border: 1px solid rgba(34, 197, 94, 0.4);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(34, 197, 94, 0.15),
                        0 0 0 1px rgba(255, 255, 255, 0.05) inset;
            animation: activeFilterPulse 2s ease-in-out infinite;
        }
        
        @keyframes activeFilterPulse {
            0%, 100% { box-shadow: 0 4px 20px rgba(34, 197, 94, 0.15); }
            50% { box-shadow: 0 4px 25px rgba(34, 197, 94, 0.25); }
        }
        
        .filters-active-text {
            color: #4ade80;
            font-weight: 700;
            font-size: 14px;
            text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);
        }
        
        /* Divider Line */
        .filter-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
            margin: 20px 0;
        }
        
        /* Reset Button Enhancement */
        .stButton > button {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2)) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            border-radius: 12px !important;
            color: #fca5a5 !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(220, 38, 38, 0.3)) !important;
            border-color: rgba(239, 68, 68, 0.6) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(239, 68, 68, 0.2) !important;
        }
        
        /* Scrollbar Styling */
        .stSidebar ::-webkit-scrollbar {
            width: 8px;
        }
        
        .stSidebar ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 10px;
        }
        
        .stSidebar ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #3b82f6, #6366f1);
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }
        
        .stSidebar ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #2563eb, #4f46e5);
        }
        
        /* Chip Button Styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(99, 102, 241, 0.3)) !important;
            border: 1px solid rgba(59, 130, 246, 0.6) !important;
            color: #60a5fa !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 8px 12px !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.5), rgba(99, 102, 241, 0.5)) !important;
            border-color: rgba(59, 130, 246, 0.8) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton > button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(71, 85, 105, 0.5) !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            padding: 8px 12px !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(30, 41, 59, 0.6) !important;
            border-color: rgba(71, 85, 105, 0.7) !important;
            color: #cbd5e1 !important;
            transform: translateY(-1px) !important;
        }
        
        /* Control Buttons (All/None) Styling */
        .stButton > button[key*="_all"],
        .stButton > button[key*="_none"] {
            font-size: 12px !important;
            padding: 6px 10px !important;
            font-weight: 600 !important;
        }
        
        /* Scrollable Container Styling */
        div[style*="max-height: 200px"],
        div[style*="max-height: 250px"] {
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 10px;
            padding: 8px;
            background: rgba(15, 23, 42, 0.3);
        }
        
        /* Gap between chips */
        .stButton {
            margin-bottom: 6px !important;
        }
        
        /* Reduce horizontal gap in columns */
        [data-testid="column"] {
            padding-left: 3px !important;
            padding-right: 3px !important;
        }
        
        /* Tighter spacing for chip rows */
        div[data-testid="stHorizontalBlock"] {
            gap: 6px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='filter-header'>
            <h2>Filtres</h2>
        </div>
    """, unsafe_allow_html=True)

    # Section 1: Filtres de Sévérité dans un expander
    with st.expander("Sévérité des Alarmes", expanded=True):
        severity = st.multiselect(
            "Sélectionner les niveaux",
            options=df['Severity'].unique(),
            default=list(df['Severity'].unique()),
            key="severity_filter"
        )

    # Section 2: Statut d'Acquittement dans un expander
    with st.expander("Statut d'Acquittement", expanded=False):
        ack = st.multiselect(
            "Sélectionner les statuts",
            options=df['Acknowledgement_Status'].unique(),
            default=list(df['Acknowledgement_Status'].unique()),
            key="ack_filter"
        )

    # Section 3: Type d'Alarme (Dashboard-specific) dans un expander
    if st.session_state.dashboard_type is not None:
        # Get unique alarm types for current dashboard
        alarm_types_available = df['Alarm_Type'].dropna().unique()

        if len(alarm_types_available) > 0:
            with st.expander("Types d'Alarmes Spécifiques", expanded=False):
                alarm_type_filter = st.multiselect(
                    "Filtrer par type d'alarme",
                    options=sorted(alarm_types_available),
                    default=list(alarm_types_available),
                    key="alarm_type_filter",
                    help="Sélectionnez des types d'alarmes spécifiques"
                )
        else:
            alarm_type_filter = []
    else:
        alarm_type_filter = []

    # Section 4: Équipements/Nodes dans un expander
    if st.session_state.dashboard_type is not None:
        # Get top nodes for filtering
        top_nodes = df['Node'].value_counts().head(30).index.tolist()

        with st.expander("Équipements (Nodes)", expanded=False):
            node_filter = st.multiselect(
                "Filtrer par équipement",
                options=sorted(top_nodes),
                default=[],
                key="node_filter",
                help="Filtrer par équipements spécifiques (Top 30)"
            )
    else:
        node_filter = []

    # Section 5: Sous-réseau dans un expander
    with st.expander("Sous-réseau", expanded=False):
        subnet = st.multiselect(
            "Sélectionner les sous-réseaux",
            options=df['Subnet'].unique(),
            default=list(df['Subnet'].unique()),
            key="subnet_filter"
        )

    # Section 6: Période dans un expander
    with st.expander("Période d'Analyse", expanded=False):
        date_range = st.date_input(
            "Sélectionner la période",
            value=(df['First_Occurrence'].min(), df['First_Occurrence'].max()),
            key="date_range"
        )

    # Filter summary with advanced styling
    st.markdown("<div class='filter-divider'></div>", unsafe_allow_html=True)

    total_filters_active = (
        (len(severity) < len(df['Severity'].unique())) +
        (len(ack) < len(df['Acknowledgement_Status'].unique())) +
        (len(subnet) < len(df['Subnet'].unique())) +
        (len(alarm_type_filter) > 0 and len(alarm_type_filter) < len(df['Alarm_Type'].dropna().unique()) if st.session_state.dashboard_type is not None else 0) +
        (len(node_filter) > 0)
    )

    if total_filters_active > 0:
        st.markdown(f"""
            <div class='filters-active-box'>
                <div style='font-size: 28px; margin-bottom: 5px;'>✓</div>
                <span class='filters-active-text'>{total_filters_active} Filtre(s) Actif(s)</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: rgba(59, 130, 246, 0.1); 
                        border: 1px solid rgba(59, 130, 246, 0.3);
                        border-radius: 12px; padding: 14px; text-align: center;'>
                <div style='font-size: 24px; margin-bottom: 5px;'>📊</div>
                <span style='color: #60a5fa; font-weight: 600; font-size: 13px;'>Tous les filtres actifs</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Reset button
    if st.button("Réinitialiser les filtres", use_container_width=True):
        st.rerun()

# Application des filtres
filtered = df[
    df['Severity'].isin(severity) &
    df['Acknowledgement_Status'].isin(ack) &
    df['Subnet'].isin(subnet)
]

# Apply alarm type filter if active
if alarm_type_filter and len(alarm_type_filter) > 0:
    filtered = filtered[filtered['Alarm_Type'].isin(alarm_type_filter)]

# Apply node filter if active
if node_filter and len(node_filter) > 0:
    filtered = filtered[filtered['Node'].isin(node_filter)]

# Apply date filter
if len(date_range) == 2:
    filtered = filtered[
        (filtered['First_Occurrence'].dt.date >= date_range[0]) &
        (filtered['First_Occurrence'].dt.date <= date_range[1])
    ]


# ============================================================================
# DASHBOARD MANAGEMENT - Vue Stratégique
# ============================================================================
if st.session_state.dashboard_type == "Management":

    kpis = calculate_kpis(filtered)

    # KPI Cards
    st.markdown("<div class='section-header'><h3>Indicateurs Clés de Performance</h3></div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, title, value, suffix="", decimals=0):
        if decimals > 0:
            formatted_value = f"{value:.{decimals}f}"
        else:
            formatted_value = f"{int(value):,}"
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{formatted_value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Total Alarmes", kpis['total_alarms'])
    kpi(k2, "Critiques", kpis['critical'])
    kpi(k3, "MTTR", kpis['mttr'], "h", decimals=1)
    kpi(k4, "Disponibilité", kpis['availability'], "%", decimals=1)
    kpi(k5, "Alarmes Racine", kpis['root_alarms'])

    # Section 1: Distribution et Tendances
    st.markdown("<div class='section-header'><h3>Distribution et Tendances</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Distribution par Sévérité")
        sev_count = filtered['Severity'].value_counts()
        colors = {'Critical': '#ef4444', 'Major': '#f97316', 'Minor': '#eab308', 'Warning': '#3b82f6'}
        fig = px.pie(
            values=sev_count.values,
            names=sev_count.index,
            hole=0.5,
            color=sev_count.index,
            color_discrete_map=colors
        )
        fig.update_layout(height=350, template="plotly_dark", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Évolution Temporelle")
        timeline = filtered.dropna(subset=['First_Occurrence'])
        timeline['Date'] = timeline['First_Occurrence'].dt.date
        timeline_grouped = timeline.groupby(['Date', 'Severity']).size().reset_index(name="Count")
        fig = px.area(
            timeline_grouped,
            x="Date",
            y="Count",
            color="Severity",
            template="plotly_dark",
            color_discrete_map=colors
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Section 2: Analyse par Domaine
    st.markdown("<div class='section-header'><h3>Analyse par Domaine Technique</h3></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Top 10 Types d'Alarmes")
        top_alarm = filtered['Alarm_Name'].value_counts().head(10)
        fig = px.bar(
            x=top_alarm.values,
            y=top_alarm.index,
            orientation="h",
            template="plotly_dark",
            color=top_alarm.values,
            color_continuous_scale="Reds"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("#### Distribution par Sous-réseau")
        top_subnet = filtered['Subnet'].value_counts().head(10)
        fig = px.bar(
            x=top_subnet.values,
            y=top_subnet.index,
            orientation="h",
            template="plotly_dark",
            color=top_subnet.values,
            color_continuous_scale="Blues"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # Section 3: Analyse des Causes Racines
    st.markdown("<div class='section-header'><h3>Analyse des Causes Racines</h3></div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("#### Alarmes Racine vs Secondaires")
        root_count = filtered['Root_Alarm'].value_counts()
        fig = px.bar(
            x=root_count.index,
            y=root_count.values,
            template="plotly_dark",
            color=root_count.values,
            color_continuous_scale="Purples"
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.markdown("#### Statut d'Acquittement")
        ack_count = filtered['Acknowledgement_Status'].value_counts()
        fig = px.pie(
            values=ack_count.values,
            names=ack_count.index,
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Oranges
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Section 4: Performance Opérationnelle
    st.markdown("<div class='section-header'><h3>⚡ Performance Opérationnelle</h3></div>", unsafe_allow_html=True)

    # Heatmap des alarmes par jour et heure
    timeline_hour = filtered.dropna(subset=['First_Occurrence']).copy()
    timeline_hour['Hour'] = timeline_hour['First_Occurrence'].dt.hour
    timeline_hour['Day'] = timeline_hour['First_Occurrence'].dt.day_name()

    heatmap_data = timeline_hour.groupby(['Day', 'Hour']).size().reset_index(name='Count')
    heatmap_pivot = heatmap_data.pivot(index='Day', columns='Hour', values='Count').fillna(0)

    # Réorganiser les jours de la semaine
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex([d for d in day_order if d in heatmap_pivot.index])

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Heure", y="Jour", color="Nombre d'Alarmes"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale="Reds",
        template="plotly_dark"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

    # Section 5: Tableau des Alarmes Critiques
    st.markdown("<div class='section-header'><h3>Alarmes Critiques Non Acquittées</h3></div>", unsafe_allow_html=True)
    critical_alarms = filtered[
        (filtered['Severity'] == 'Critical') &
        (filtered['Acknowledgement_Status'] == 'Unacknowledged')
    ][['First_Occurrence', 'Alarm_Name', 'Location', 'Node', 'Subnet', 'Managed_Object']].head(20)

    st.dataframe(critical_alarms, use_container_width=True, height=300)


# ============================================================================
# DASHBOARD RADIO - Support RAN
# ============================================================================
elif st.session_state.dashboard_type == "Radio":

    # Filtrer les alarmes Radio (basé sur le type ou le groupe d'alarme)
    radio_keywords = ['Radio', 'RAN', 'eNodeB', 'gNodeB', 'Cell', 'Antenna', 'RF']
    radio_filtered = filtered[
        filtered['Alarm_Name'].str.contains('|'.join(radio_keywords), case=False, na=False) |
        filtered['Alarm_Type'].str.contains('|'.join(radio_keywords), case=False, na=False) |
        filtered['Alarm_Group'].str.contains('|'.join(radio_keywords), case=False, na=False)
    ]

    kpis = calculate_kpis(radio_filtered)

    # KPI Cards
    st.markdown("<div class='section-header'><h3>KPIs Radio RAN</h3></div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, title, value, suffix="", decimals=0):
        if decimals > 0:
            formatted_value = f"{value:.{decimals}f}"
        else:
            formatted_value = f"{int(value):,}"
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{formatted_value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Alarmes Radio", kpis['total_alarms'])
    kpi(k2, "Critiques", kpis['critical'])
    kpi(k3, "Majeures", kpis['major'])
    kpi(k4, "MTTR", kpis['mttr'], "h", decimals=1)
    kpi(k5, "Disponibilité", kpis['availability'], "%", decimals=1)

    # Section 1: Analyse des Sites Radio
    st.markdown("<div class='section-header'><h3>Analyse des Sites Radio</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Top Sites avec Alarmes")
        top_nodes = radio_filtered['Node'].value_counts().head(15)
        fig = px.bar(
            x=top_nodes.values,
            y=top_nodes.index,
            orientation="h",
            template="plotly_dark",
            color=top_nodes.values,
            color_continuous_scale="Reds"
        )
        fig.update_layout(height=450, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Distribution par Sévérité")
        sev_count = radio_filtered['Severity'].value_counts()
        colors = {'Critical': '#ef4444', 'Major': '#f97316', 'Minor': '#eab308', 'Warning': '#3b82f6'}
        fig = px.pie(
            values=sev_count.values,
            names=sev_count.index,
            hole=0.5,
            color=sev_count.index,
            color_discrete_map=colors
        )
        fig.update_layout(height=450, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # Section 2: Types d'Alarmes Radio
    st.markdown("<div class='section-header'><h3>Types d'Alarmes Radio</h3></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Top 10 Alarmes Radio")
        top_alarm = radio_filtered['Alarm_Name'].value_counts().head(10)
        fig = px.bar(
            x=top_alarm.values,
            y=top_alarm.index,
            orientation="h",
            template="plotly_dark",
            color=top_alarm.values,
            color_continuous_scale="Oranges"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("#### Évolution Temporelle")
        timeline = radio_filtered.dropna(subset=['First_Occurrence'])
        timeline['Date'] = timeline['First_Occurrence'].dt.date
        timeline_grouped = timeline.groupby('Date').size().reset_index(name="Count")
        fig = px.line(
            timeline_grouped,
            x="Date",
            y="Count",
            markers=True,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        fig.update_traces(line_color='#3b82f6', marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    # Section 3: Analyse par Localisation
    st.markdown("<div class='section-header'><h3>Analyse Géographique</h3></div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("#### Top Localisations")
        top_location = radio_filtered['Location'].value_counts().head(10)
        fig = px.bar(
            x=top_location.values,
            y=top_location.index,
            orientation="h",
            template="plotly_dark",
            color=top_location.values,
            color_continuous_scale="Blues"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.markdown("#### Distribution par Sous-réseau")
        subnet_count = radio_filtered['Subnet'].value_counts().head(10)
        fig = px.pie(
            values=subnet_count.values,
            names=subnet_count.index,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Section 4: Alarmes Actives
    st.markdown("<div class='section-header'><h3>Alarmes Radio Actives</h3></div>", unsafe_allow_html=True)
    active_alarms = radio_filtered[
        radio_filtered['Acknowledgement_Status'] == 'Unacknowledged'
    ][['First_Occurrence', 'Severity', 'Alarm_Name', 'Node', 'Location', 'Managed_Object']].head(50)

    st.dataframe(active_alarms, use_container_width=True, height=400)


# ============================================================================
# DASHBOARD FH - Support Transmission
# ============================================================================
elif st.session_state.dashboard_type == "FH":

    # Filtrer les alarmes FH (Faisceaux Hertziens)
    fh_keywords = ['Transmission', 'FH', 'Microwave', 'Link', 'Transport', 'Backhaul', 'MW']
    fh_filtered = filtered[
        filtered['Alarm_Name'].str.contains('|'.join(fh_keywords), case=False, na=False) |
        filtered['Alarm_Type'].str.contains('|'.join(fh_keywords), case=False, na=False) |
        filtered['Alarm_Group'].str.contains('|'.join(fh_keywords), case=False, na=False)
    ]

    kpis = calculate_kpis(fh_filtered)

    # KPI Cards
    st.markdown("<div class='section-header'><h3>KPIs Transmission FH</h3></div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, title, value, suffix="", decimals=0):
        if decimals > 0:
            formatted_value = f"{value:.{decimals}f}"
        else:
            formatted_value = f"{int(value):,}"
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{formatted_value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Alarmes FH", kpis['total_alarms'])
    kpi(k2, "Critiques", kpis['critical'])
    kpi(k3, "Majeures", kpis['major'])
    kpi(k4, "MTTR", kpis['mttr'], "h", decimals=1)
    kpi(k5, "Disponibilité", kpis['availability'], "%", decimals=1)

    # Section 1: Analyse des Liens FH
    st.markdown("<div class='section-header'><h3>Analyse des Liens de Transmission</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Top Équipements FH avec Alarmes")
        top_nodes = fh_filtered['Node'].value_counts().head(15)
        fig = px.bar(
            x=top_nodes.values,
            y=top_nodes.index,
            orientation="h",
            template="plotly_dark",
            color=top_nodes.values,
            color_continuous_scale="Greens"
        )
        fig.update_layout(height=450, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Distribution par Sévérité")
        sev_count = fh_filtered['Severity'].value_counts()
        colors = {'Critical': '#ef4444', 'Major': '#f97316', 'Minor': '#eab308', 'Warning': '#3b82f6'}
        fig = px.pie(
            values=sev_count.values,
            names=sev_count.index,
            hole=0.5,
            color=sev_count.index,
            color_discrete_map=colors
        )
        fig.update_layout(height=450, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # Section 2: Types d'Alarmes FH
    st.markdown("<div class='section-header'><h3>Types d'Alarmes Transmission</h3></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Top 10 Alarmes FH")
        top_alarm = fh_filtered['Alarm_Name'].value_counts().head(10)
        fig = px.bar(
            x=top_alarm.values,
            y=top_alarm.index,
            orientation="h",
            template="plotly_dark",
            color=top_alarm.values,
            color_continuous_scale="Teal"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("#### Évolution Temporelle")
        timeline = fh_filtered.dropna(subset=['First_Occurrence'])
        timeline['Date'] = timeline['First_Occurrence'].dt.date
        timeline_grouped = timeline.groupby('Date').size().reset_index(name="Count")
        fig = px.line(
            timeline_grouped,
            x="Date",
            y="Count",
            markers=True,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        fig.update_traces(line_color='#10b981', marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    # Section 3: Analyse des Objets Managés
    st.markdown("<div class='section-header'><h3>Analyse des Équipements</h3></div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("#### Top Objets Managés")
        top_managed = fh_filtered['Managed_Object'].value_counts().head(10)
        fig = px.bar(
            x=top_managed.values,
            y=top_managed.index,
            orientation="h",
            template="plotly_dark",
            color=top_managed.values,
            color_continuous_scale="Purples"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.markdown("#### Statut d'Acquittement")
        ack_count = fh_filtered['Acknowledgement_Status'].value_counts()
        fig = px.pie(
            values=ack_count.values,
            names=ack_count.index,
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Section 4: Alarmes FH Actives
    st.markdown("<div class='section-header'><h3>Alarmes FH Actives</h3></div>", unsafe_allow_html=True)
    active_alarms = fh_filtered[
        fh_filtered['Acknowledgement_Status'] == 'Unacknowledged'
    ][['First_Occurrence', 'Severity', 'Alarm_Name', 'Node', 'Location', 'Managed_Object']].head(50)

    st.dataframe(active_alarms, use_container_width=True, height=400)


# ============================================================================
# DASHBOARD ÉNERGIE - Support Énergie
# ============================================================================
elif st.session_state.dashboard_type == "Energy":

    # Filtrer les alarmes Énergie
    energy_keywords = ['Power', 'Battery', 'Energy', 'Énergie', 'Alimentation', 'Voltage', 'Current', 'Temperature', 'AC', 'DC', 'Generator', 'UPS']
    energy_filtered = filtered[
        filtered['Alarm_Name'].str.contains('|'.join(energy_keywords), case=False, na=False) |
        filtered['Alarm_Type'].str.contains('|'.join(energy_keywords), case=False, na=False) |
        filtered['Alarm_Group'].str.contains('|'.join(energy_keywords), case=False, na=False)
    ]

    kpis = calculate_kpis(energy_filtered)

    # KPI Cards
    st.markdown("<div class='section-header'><h3>KPIs Énergie</h3></div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, title, value, suffix="", decimals=0):
        if decimals > 0:
            formatted_value = f"{value:.{decimals}f}"
        else:
            formatted_value = f"{int(value):,}"
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{formatted_value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi(k1, "Alarmes Énergie", kpis['total_alarms'])
    kpi(k2, "Critiques", kpis['critical'])
    kpi(k3, "Majeures", kpis['major'])
    kpi(k4, "MTTR", kpis['mttr'], "h", decimals=1)
    kpi(k5, "Disponibilité", kpis['availability'], "%", decimals=1)

    # Section 1: Analyse des Sites Énergie
    st.markdown("<div class='section-header'><h3>⚡ Analyse des Systèmes d'Alimentation</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Top Sites avec Alarmes Énergie")
        top_nodes = energy_filtered['Node'].value_counts().head(15)
        fig = px.bar(
            x=top_nodes.values,
            y=top_nodes.index,
            orientation="h",
            template="plotly_dark",
            color=top_nodes.values,
            color_continuous_scale="YlOrRd"
        )
        fig.update_layout(height=450, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Distribution par Sévérité")
        sev_count = energy_filtered['Severity'].value_counts()
        colors = {'Critical': '#ef4444', 'Major': '#f97316', 'Minor': '#eab308', 'Warning': '#3b82f6'}
        fig = px.pie(
            values=sev_count.values,
            names=sev_count.index,
            hole=0.5,
            color=sev_count.index,
            color_discrete_map=colors
        )
        fig.update_layout(height=450, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # Section 2: Types d'Alarmes Énergie
    st.markdown("<div class='section-header'><h3>Types d'Alarmes Énergie</h3></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Top 10 Alarmes Énergie")
        top_alarm = energy_filtered['Alarm_Name'].value_counts().head(10)
        fig = px.bar(
            x=top_alarm.values,
            y=top_alarm.index,
            orientation="h",
            template="plotly_dark",
            color=top_alarm.values,
            color_continuous_scale="Reds"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("#### Évolution Temporelle")
        timeline = energy_filtered.dropna(subset=['First_Occurrence'])
        timeline['Date'] = timeline['First_Occurrence'].dt.date
        timeline_grouped = timeline.groupby('Date').size().reset_index(name="Count")
        fig = px.line(
            timeline_grouped,
            x="Date",
            y="Count",
            markers=True,
            template="plotly_dark"
        )
        fig.update_layout(height=400)
        fig.update_traces(line_color='#f59e0b', marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    # Section 3: Analyse des Équipements
    st.markdown("<div class='section-header'><h3>Analyse des Équipements Énergie</h3></div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)

    with c5:
        st.markdown("#### Top Équipements")
        top_managed = energy_filtered['Managed_Object'].value_counts().head(10)
        fig = px.bar(
            x=top_managed.values,
            y=top_managed.index,
            orientation="h",
            template="plotly_dark",
            color=top_managed.values,
            color_continuous_scale="Oranges"
        )
        fig.update_layout(height=400, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.markdown("#### Statut d'Acquittement")
        ack_count = energy_filtered['Acknowledgement_Status'].value_counts()
        fig = px.pie(
            values=ack_count.values,
            names=ack_count.index,
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.YlOrRd
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Section 4: Alarmes Énergie Critiques
    st.markdown("<div class='section-header'><h3>Alarmes Énergie Actives</h3></div>", unsafe_allow_html=True)
    active_alarms = energy_filtered[
        energy_filtered['Acknowledgement_Status'] == 'Unacknowledged'
    ][['First_Occurrence', 'Severity', 'Alarm_Name', 'Node', 'Location', 'Managed_Object']].head(50)

    st.dataframe(active_alarms, use_container_width=True, height=400)

