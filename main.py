import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np


# PAGE CONFIG

st.set_page_config(
    page_title="DRS - 5G Alarm Management System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
            .then(reg => console.log('✅ Service Worker registered'))
            .catch(err => console.log('❌ Service Worker registration failed:', err));
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
    installBtn.innerHTML = '📱 Installer l\\'app';
    installBtn.onclick = () => {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('✅ User accepted the install prompt');
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
    console.log('📱 Mobile device detected - optimizations applied');
}

// Handle orientation change
window.addEventListener('orientationchange', () => {
    setTimeout(() => {
        window.scrollTo(0, 1);
    }, 100);
});

// Add to home screen detection
window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully!');
});
</script>

""", unsafe_allow_html=True)


# LOAD DATA

@st.cache_data
def load_data():
    path = r"C:\Users\t14\Downloads\alarms1.xlsx"
    df = pd.read_excel(path, header=5).iloc[:, :18]

    df.columns = [
        'Root_Alarm', 'Severity', 'Alarm_Name', 'First_Occurrence', 'Last_Occurrence',
        'Duplication_Count', 'Alarm_Type', 'Alarm_Group', 'Location', 'Node',
        'Managed_Object', 'Managed_Object_Instance', 'Agent', 'Manager',
        'Alarm_Sequence_Number', 'Additional_Text', 'Acknowledgement_Status', 'Subnet'
    ]

    df['First_Occurrence'] = pd.to_datetime(df['First_Occurrence'], errors='coerce')
    df['Last_Occurrence'] = pd.to_datetime(df['Last_Occurrence'], errors='coerce')
    df['Duplication_Count'] = pd.to_numeric(df['Duplication_Count'], errors='coerce')

    return df

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
            "type": "Management"
        },
        {
            "col": col2,
            "icon": "📡",
            "title": "Radio RAN",
            "subtitle": "    Support Radio",
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
                <h3 style='color: {dashboard["color"]}; font-size: 20px; font-weight: 700; margin-bottom: 5px;'>
                    {dashboard["title"]}
                </h3>
                <p style='color: #94a3b8; font-size: 13px; margin-bottom: 3px; font-weight: 600;'>
                    {dashboard["subtitle"]}
                </p>
                <p style='color: #64748b; font-size: 12px; margin-bottom: 15px;'>
                    {dashboard["description"]}
                </p>
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
            💡 <strong>Astuce:</strong> Utilisez les filtres latéraux pour affiner vos analyses | 
            🔄 Les données sont mises à jour en temps réel
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# HEADER COMMUN À TOUS LES DASHBOARDS
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.markdown(f"## 🚨 Dashboard {st.session_state.dashboard_type}")
    st.caption(f"📅 Dernière mise à jour : **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
with col_header2:
    if st.button("🔙 Retour à la sélection", use_container_width=True):
        st.session_state.dashboard_type = None
        st.rerun()


# SIDEBAR FILTERS COMMUN
with st.sidebar:
    st.markdown("## 🔍 Filtres")

    # Filtres de base
    severity = st.multiselect("Sévérité", df['Severity'].unique(), df['Severity'].unique())
    ack = st.multiselect("Statut Acquittement", df['Acknowledgement_Status'].unique(),
                         df['Acknowledgement_Status'].unique())
    subnet = st.multiselect("Sous-réseau", df['Subnet'].unique(), df['Subnet'].unique())

    # Filtre par date
    st.markdown("### 📅 Période")
    date_range = st.date_input(
        "Sélectionner la période",
        value=(df['First_Occurrence'].min(), df['First_Occurrence'].max()),
        key="date_range"
    )

# Application des filtres
filtered = df[
    df['Severity'].isin(severity) &
    df['Acknowledgement_Status'].isin(ack) &
    df['Subnet'].isin(subnet)
]

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
    st.markdown("<div class='section-header'><h3>📊 Indicateurs Clés de Performance</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📈 Distribution et Tendances</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🏢 Analyse par Domaine Technique</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🔍 Analyse des Causes Racines</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🚨 Alarmes Critiques Non Acquittées</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 KPIs Radio RAN</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📡 Analyse des Sites Radio</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 Types d'Alarmes Radio</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🗺️ Analyse Géographique</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🚨 Alarmes Radio Actives</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 KPIs Transmission FH</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📶 Analyse des Liens de Transmission</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 Types d'Alarmes Transmission</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🔧 Analyse des Équipements</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🚨 Alarmes FH Actives</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 KPIs Énergie</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>📊 Types d'Alarmes Énergie</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🔌 Analyse des Équipements Énergie</h3></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-header'><h3>🚨 Alarmes Énergie Actives</h3></div>", unsafe_allow_html=True)
    active_alarms = energy_filtered[
        energy_filtered['Acknowledgement_Status'] == 'Unacknowledged'
    ][['First_Occurrence', 'Severity', 'Alarm_Name', 'Node', 'Location', 'Managed_Object']].head(50)

    st.dataframe(active_alarms, use_container_width=True, height=400)

