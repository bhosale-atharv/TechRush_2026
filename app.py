import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="CropPro.Ai | Precision Agriculture Decision Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Premium Daylight Agricultural Theme (Zero Crop Background Images)
st.markdown("""
<style>
    /* Daylight Clean Canvas */
    .stApp {
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Sidebar Daylight Theme Overrides */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9 !important;
        border-right: 1px solid #CBD5E1 !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        color: #065F46 !important;
        font-weight: 800 !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #94A3B8 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #94A3B8 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] button {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #94A3B8 !important;
    }

    /* BaseWeb Selectbox Dropdown Menu & Popover Light Theme Styling */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] *,
    li[role="option"],
    li[role="option"] * {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }

    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] ul,
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        padding: 4px 0 !important;
    }

    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    ul[role="listbox"] li,
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 10px 16px !important;
    }

    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #ECFDF5 !important;
        color: #047857 !important;
    }

    /* Strict High-Contrast Metric Overrides */
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #047857 !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #10B981 !important;
    }
    
    /* Tabs High Contrast Styling */
    button[data-baseweb="tab"] p {
        color: #334155 !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #047857 !important;
        font-weight: 800 !important;
    }

    /* Form Labels & Input High Contrast */
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stMultiSelect label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }
    
    /* Main Content Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #065F46 !important;
        font-weight: 800 !important;
    }
    p, span, div {
        color: #1E293B;
    }
    
    /* Clean Hero Header Banner */
    .hero-header {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1.5px solid #A7F3D0;
        border-radius: 18px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.08);
        transition: all 0.3s ease;
    }
    .hero-title {
        color: #065F46;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #047857;
        font-size: 1.02rem;
        margin-top: 4px;
        font-weight: 500;
    }
    
    /* Clean Daylight Cards */
    .card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
    }
    .card:hover {
        border-color: #6EE7B7;
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.08);
    }
    .card-header {
        color: #047857;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* Pure Gradient Winning Crop Card (Zero Image) */
    .winner-card-clean {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 50%, #A7F3D0 100%);
        border: 2.5px solid #10B981;
        border-radius: 20px;
        padding: 30px 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
        position: relative;
    }
    .winner-card-title {
        color: #065F46;
        text-transform: uppercase;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: 0.8px;
    }
    .winner-card-name {
        font-size: 2.9rem;
        font-weight: 900;
        color: #065F46;
        margin: 8px 0;
        letter-spacing: -0.5px;
    }
    .winner-card-pill {
        display: inline-block;
        background: #FFFFFF;
        color: #B45309;
        font-weight: 800;
        font-size: 1.2rem;
        padding: 6px 22px;
        border-radius: 30px;
        border: 1.5px solid #FCD34D;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Confidence Advantage Rationale Box */
    .advantage-box {
        background: #FFFBEB;
        border: 1px solid #FCD34D;
        border-left: 5px solid #F59E0B;
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.05);
    }
    .advantage-title {
        color: #92400E;
        font-size: 1.08rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .advantage-badge {
        display: inline-block;
        background: #FEF3C7;
        color: #B45309;
        font-weight: 800;
        font-size: 0.88rem;
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 10px;
        border: 1px solid #FDE68A;
    }
    .advantage-text {
        color: #451A03;
        font-size: 0.96rem;
        line-height: 1.6;
        font-weight: 500;
    }

    /* AI Reasoning Box */
    .ai-reasoning-box {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        border-left: 5px solid #10B981;
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 16px;
        margin-bottom: 16px;
    }
    .ai-reasoning-header {
        color: #065F46;
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 4px;
    }
    .ai-reasoning-body {
        color: #1E293B;
        font-size: 0.95rem;
        line-height: 1.5;
        font-weight: 500;
    }

    /* Organic Advisory Modern Grid Container */
    .organic-box-modern {
        background: #F0FDF4;
        border: 1.5px solid #A7F3D0;
        border-radius: 18px;
        padding: 24px 28px;
        margin-top: 24px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.06);
    }
    .organic-header-modern {
        color: #065F46;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 16px;
    }
    .organic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
    }
    .organic-card-item {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #10B981;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .organic-card-item:hover {
        border-color: #34D399;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }
    .organic-card-label {
        color: #047857;
        font-weight: 800;
        font-size: 0.98rem;
        margin-bottom: 6px;
    }
    .organic-card-desc {
        color: #334155;
        font-size: 0.92rem;
        line-height: 1.55;
        font-weight: 500;
    }
    
    /* District Grid Daylight Card */
    .district-grid-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .district-grid-card:hover {
        border-color: #10B981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
        transform: translateY(-2px);
    }
    
    /* Mobile Responsive UI Breakpoints */
    @media (max-width: 768px) {
        .hero-header {
            padding: 16px 20px !important;
            border-radius: 14px !important;
        }
        .hero-title {
            font-size: 1.8rem !important;
        }
        .hero-subtitle {
            font-size: 0.92rem !important;
        }
        .card {
            padding: 16px !important;
            border-radius: 14px !important;
        }
        .organic-box-modern {
            padding: 16px 18px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "Guest Farmer", "state": "Maharashtra", "district": "Ahmednagar", "acres": 5.0, "soil_card_id": "SHC-MH-2026-0000"}

# Header Banner
st.markdown("""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🌱 CropPro.Ai</h1>
            <p class="hero-subtitle">Precision Agriculture Decision Engine & Agro-Climatic Intelligence Platform</p>
        </div>
        <div style="text-align: right;">
            <span style="background: #DCFCE7; border: 1px solid #A7F3D0; color: #047857; padding: 8px 18px; border-radius: 30px; font-weight: 800; font-size: 0.88rem;">
                ⚡ CropPro.Ai Model v5.2 Active (99.26% Accuracy)
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch Location Database
def fetch_location_db():
    try:
        res = requests.get(f"{BACKEND_URL}/universal-locations")
        if res.status_code == 200:
            return res.json()["database"]
    except Exception as e:
        pass
    return None

loc_db = fetch_location_db()

# Sidebar: Telemetry & Controls
st.sidebar.markdown("### 📍 Location & Soil Telemetry")
if loc_db:
    states = list(loc_db.keys())
    sel_state = st.sidebar.selectbox("Select State", states, index=0)
    districts = list(loc_db[sel_state].keys())
    sel_district = st.sidebar.selectbox("Select District (Maharashtra Crop Hubs)", districts, index=0)
    profile = loc_db[sel_state][sel_district]
else:
    sel_state = "Maharashtra"
    sel_district = "Ahmednagar"
    profile = {
        "elevation_m": 650, "soil_type": "Medium Black Fertile Soil",
        "primary_crop": "Sugarcane, Bajra & Jowar (Sugar Hub)",
        "N": 140, "P": 60, "K": 60, "temp": 27.5, "humidity": 55, "ph": 7.2, "rainfall": 60, "soil_ec": 1.2, "market_pi": 9.4
    }

st.sidebar.markdown("---")
st.sidebar.markdown("### ✏️ Direct Typed Farm Telemetry")
n_val = st.sidebar.number_input("Nitrogen (N) [kg/ha]", 0.0, 200.0, float(profile["N"]), step=1.0)
p_val = st.sidebar.number_input("Phosphorus (P) [kg/ha]", 0.0, 200.0, float(profile["P"]), step=1.0)
k_val = st.sidebar.number_input("Potassium (K) [kg/ha]", 0.0, 250.0, float(profile["K"]), step=1.0)
ph_val = st.sidebar.number_input("Soil pH Level", 3.5, 9.5, float(profile["ph"]), step=0.1)
temp_val = st.sidebar.number_input("Temperature (°C)", 5.0, 50.0, float(profile["temp"]), step=0.5)
hum_val = st.sidebar.number_input("Humidity (%)", 10.0, 100.0, float(profile["humidity"]), step=1.0)
rain_val = st.sidebar.number_input("Annual Rainfall (mm)", 10.0, 400.0, float(profile["rainfall"]), step=5.0)
ec_val = st.sidebar.number_input("⚡ Soil EC (dS/m)", 0.1, 5.0, float(profile["soil_ec"]), step=0.1)
elev_val = st.sidebar.number_input("🏔️ Elevation (meters)", 0.0, 2500.0, float(profile["elevation_m"]), step=10.0)
mpi_val = st.sidebar.number_input("📈 Market Index (1-10)", 1.0, 10.0, float(profile["market_pi"]), step=0.1)

st.sidebar.markdown("---")
drought_flag = st.sidebar.toggle("🌵 Drought Mitigation Mode", value=False)
salinity_flag = st.sidebar.toggle("🧂 High Salinity Warning Mode", value=False)
market_flag = st.sidebar.toggle("📈 Market ROI Priority Mode", value=False)

# Main Navigation Tabs
tab_recommend, tab_map, tab_data, tab_auth = st.tabs([
    "🌱 Crop Recommendation",
    "🗺️ Searchable GIS Map",
    "📊 Dataset Explorer",
    "👤 Farmer Account Portal"
])

# TAB 1: Recommendation Engine
with tab_recommend:
    col_left, col_right = st.columns([1, 1.15])

    with col_left:
        st.markdown("""<div class="card"><div class="card-header">📊 Soil & Climate Telemetry Summary</div></div>""", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("N-P-K Ratio", f"{int(n_val)}-{int(p_val)}-{int(k_val)}")
        m2.metric("Soil pH", f"{ph_val:.1f}")
        m3.metric("Rainfall", f"{int(rain_val)} mm")
        
        m4, m5, m6 = st.columns(3)
        m4.metric("Temperature", f"{temp_val:.1f} °C")
        m5.metric("Soil EC", f"{ec_val:.1f} dS/m")
        m6.metric("Elevation", f"{int(elev_val)} m")

        # Daylight Radar Spider Chart
        categories = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Rainfall', 'Soil EC', 'Elevation']
        values = [
            n_val / 200 * 100, p_val / 200 * 100, k_val / 250 * 100,
            temp_val / 45 * 100, hum_val, rain_val / 400 * 100,
            ec_val / 5.0 * 100, elev_val / 2500 * 100
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Farm Telemetry',
            line_color='#10B981',
            fillcolor='rgba(16, 185, 129, 0.18)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                bgcolor='#FAFAFA'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#0F172A', family='sans-serif', size=12),
            margin=dict(l=40, r=40, t=20, b=20),
            height=320,
            showlegend=False
        )
        st.plotly_chart(fig_radar, width="stretch")

    payload = {
        "N": n_val, "P": p_val, "K": k_val,
        "temperature": temp_val, "humidity": hum_val,
        "ph": ph_val, "rainfall": rain_val,
        "soil_ec": ec_val, "market_profitability_index": mpi_val,
        "elevation_m": elev_val,
        "drought_mode": drought_flag,
        "salinity_alert": salinity_flag,
        "market_priority_mode": market_flag
    }

    response_data = None
    try:
        res = requests.post(f"{BACKEND_URL}/predict", json=payload)
        if res.status_code == 200:
            response_data = res.json()
    except Exception as e:
        st.error("Error communicating with Backend API.")

    with col_right:
        if response_data:
            winner = response_data["winning_crop"]
            top_recs = response_data["top_recommendations"]
            shap_explanation = response_data["shap_explanation"]
            feature_impacts = response_data["feature_impacts"]
            organic_advisory = response_data["organic_advisory"]
            conf_advantage = response_data.get("confidence_advantage", None)
            
            top_score = top_recs[0]["confidence"]
            
            # 🏆 Clean Gradient Winning Crop Card (Zero Image)
            st.markdown(f"""
            <div class="winner-card-clean">
                <div class="winner-card-title">🥇 Recommended Optimal Crop</div>
                <div class="winner-card-name">{winner}</div>
                <div class="winner-card-pill">{top_score:.1f}% Confidence Match</div>
            </div>
            """, unsafe_allow_html=True)
            
            crops_list = [r["crop"] for r in top_recs[::-1]]
            confs_list = [r["confidence"] for r in top_recs[::-1]]
            
            fig_bar = go.Figure(go.Bar(
                x=confs_list,
                y=crops_list,
                orientation='h',
                marker=dict(
                    color=confs_list,
                    colorscale=[[0, '#A7F3D0'], [0.5, '#34D399'], [1.0, '#059669']],
                    line=dict(color='#047857', width=1.2)
                ),
                text=[f"{c:.1f}%" for c in confs_list],
                textposition='auto',
                textfont=dict(color='#FFFFFF', size=12, family='sans-serif', weight='bold')
            ))
            fig_bar.update_layout(
                title=dict(text="🏆 Top 3 Suitable Crops", font=dict(color='#065F46', size=16, family='sans-serif')),
                xaxis=dict(range=[0, 105], showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color='#0F172A', size=12)),
                yaxis=dict(tickfont=dict(color='#0F172A', size=13, family='sans-serif')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#0F172A'),
                height=210,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_bar, width="stretch")

            # 💡 High-Contrast Confidence Advantage Rationale Box
            if conf_advantage:
                st.markdown(f"""<div class="advantage-box"><div class="advantage-title">💡 Why {conf_advantage['winner']} Won Over Other Options</div><div class="advantage-badge">🏆 {conf_advantage['winner']} ({conf_advantage['winner_confidence']}%) vs 🥈 {conf_advantage['runner_up']} ({conf_advantage['runner_up_confidence']}%) — Lead: +{conf_advantage['advantage_delta']}%</div><div class="advantage-text">{conf_advantage['rationale']}</div></div>""", unsafe_allow_html=True)

            # 🌾 Custom High-Contrast Agronomic Decision Rationale Box
            st.markdown(f"""<div class="ai-reasoning-box"><div class="ai-reasoning-header">🌾 Agronomic Decision Rationale</div><div class="ai-reasoning-body">{shap_explanation}</div></div>""", unsafe_allow_html=True)

    if response_data:
        st.markdown("---")
        st.markdown(f"### 🌿 Zero-Synthetic Organic Profitability Advisory for '{winner}'")
        st.caption("Maximize your net profit margin by reducing synthetic fertilizer expenses using proven natural farming techniques.")
        
        ad1, ad2 = st.columns(2)
        with ad1:
            st.markdown(f"""<div class="organic-card-item"><div class="organic-card-label">🧪 Bio-Fertilizer Substitution:</div><div class="organic-card-desc">{organic_advisory['organic_fertilizers']}</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="organic-card-item"><div class="organic-card-label">🌱 Natural Intercropping & N-Fixation:</div><div class="organic-card-desc">{organic_advisory['intercropping_profit']}</div></div>""", unsafe_allow_html=True)

        with ad2:
            st.markdown(f"""<div class="organic-card-item"><div class="organic-card-label">🐞 Biological Pest Control:</div><div class="organic-card-desc">{organic_advisory['natural_pest_control']}</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="organic-card-item"><div class="organic-card-label">💰 Profit Maximization Strategy:</div><div class="organic-card-desc">{organic_advisory['max_profit_tip']}</div></div>""", unsafe_allow_html=True)

# TAB 2: Searchable Geographical Representation & GIS Map
with tab_map:
    st.markdown("<h3 style='color: #065F46;'>🗺️ Searchable GIS Regional Agro-Climatic Map & Telemetry Explorer</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Search by District name or Primary Crop belt to easily locate essential regional data.</p>", unsafe_allow_html=True)
    
    map_data_res = None
    try:
        m_res = requests.get(f"{BACKEND_URL}/crop-map-data")
        if m_res.status_code == 200:
            map_data_res = m_res.json()["data"]
    except Exception as e:
        pass
        
    df_map = pd.DataFrame()
    if map_data_res:
        df_map = pd.DataFrame(map_data_res)
    elif loc_db:
        map_points = []
        for state, districts in loc_db.items():
            for dist_name, data in districts.items():
                map_points.append({
                    "state": state,
                    "district": dist_name,
                    "lat": data.get("lat", 19.0),
                    "lon": data.get("lon", 75.0),
                    "elevation_m": data.get("elevation_m", 500),
                    "soil_type": data.get("soil_type", "Medium Black"),
                    "primary_crop": data.get("primary_crop", "Crops"),
                    "N": data.get("N", 90),
                    "P": data.get("P", 50),
                    "K": data.get("K", 50),
                    "rainfall": data.get("rainfall", 100),
                    "market_pi": data.get("market_pi", 8.0)
                })
        df_map = pd.DataFrame(map_points)

    if not df_map.empty:
        if "N" not in df_map.columns:
            df_map["N"] = df_map.apply(lambda r: loc_db.get(r.get("state",""), {}).get(r.get("district",""), {}).get("N", "-") if loc_db else "-", axis=1)
        if "P" not in df_map.columns:
            df_map["P"] = df_map.apply(lambda r: loc_db.get(r.get("state",""), {}).get(r.get("district",""), {}).get("P", "-") if loc_db else "-", axis=1)
        if "K" not in df_map.columns:
            df_map["K"] = df_map.apply(lambda r: loc_db.get(r.get("state",""), {}).get(r.get("district",""), {}).get("K", "-") if loc_db else "-", axis=1)

        # 🔍 Search & Filter Bar
        sf1, sf2 = st.columns([1.5, 1])
        with sf1:
            search_query = st.text_input("🔍 Search District or State", "", placeholder="Type 'Ahmednagar', 'Kolhapur', 'Nagpur', 'Nashik'...")
        with sf2:
            crop_filter = st.multiselect("🌾 Filter Primary Crop Belt", options=df_map["primary_crop"].unique(), default=[])

        # Filter Logic
        filtered_map_df = df_map.copy()
        if search_query:
            filtered_map_df = filtered_map_df[
                filtered_map_df["district"].str.contains(search_query, case=False, na=False) |
                filtered_map_df["state"].str.contains(search_query, case=False, na=False)
            ]
        if crop_filter:
            filtered_map_df = filtered_map_df[filtered_map_df["primary_crop"].isin(crop_filter)]
            
        st.info(f"Showing **{len(filtered_map_df)}** of **{len(df_map)}** essential regional district data points.")
        
        if not filtered_map_df.empty:
            hover_dict = {"lat": False, "lon": False}
            for col in ["state", "primary_crop", "N", "P", "K", "soil_type", "elevation_m", "rainfall"]:
                if col in filtered_map_df.columns:
                    hover_dict[col] = True

            fig_geo = px.scatter_mapbox(
                filtered_map_df,
                lat="lat",
                lon="lon",
                hover_name="district",
                hover_data=hover_dict,
                color="primary_crop",
                size="elevation_m",
                size_max=28,
                zoom=5.8,
                center={"lat": 19.2, "lon": 76.0},
                mapbox_style="carto-positron",
                title="Searchable GIS Regional Crop Distribution (CropPro.Ai)"
            )
            fig_geo.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1E293B', family='sans-serif', size=13),
                title=dict(font=dict(color='#065F46', size=18, family='sans-serif')),
                legend=dict(
                    font=dict(color='#1E293B', size=12),
                    title=dict(font=dict(color='#065F46', size=13)),
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#CBD5E1',
                    borderwidth=1
                ),
                height=580,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig_geo, width="stretch")
            
            # 📋 Side-by-Side District Telemetry Cards Grid
            st.markdown("#### 📋 Regional District Telemetry Cards")
            d_cols = st.columns(3)
            for idx, row in filtered_map_df.reset_index().iterrows():
                col_idx = idx % 3
                with d_cols[col_idx]:
                    card_html = f"""<div class="district-grid-card">
<div style="display: flex; justify-content: space-between; align-items: center;">
<strong style="color: #065F46; font-size: 1.08rem;">📍 {row['district']}</strong>
<span style="background: #E2E8F0; color: #334155; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">{row['state']}</span>
</div>
<div style="color: #475569; font-size: 0.88rem; margin-top: 6px;">🌾 <b>Primary Crops:</b> {row['primary_crop']}</div>
<div style="color: #475569; font-size: 0.88rem;">🧪 <b>Baseline NPK:</b> {row.get('N','-')}-{row.get('P','-')}-{row.get('K','-')}</div>
<div style="color: #475569; font-size: 0.88rem;">🏔️ <b>Elevation:</b> {row['elevation_m']}m | 🌧️ <b>Rainfall:</b> {row['rainfall']}mm</div>
<div style="color: #475569; font-size: 0.88rem;">🌱 <b>Soil:</b> {row['soil_type']}</div>
</div>"""
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("No districts matched your search query. Try clearing the filters.")

# TAB 3: Dataset Explorer
with tab_data:
    st.markdown("<h3 style='color: #065F46;'>📊 Dataset & Raw Telemetry Explorer</h3>", unsafe_allow_html=True)
    st.markdown("Explore, search, filter, and export underlying agronomic benchmarks.")
    
    if map_data_res:
        df_exp = pd.DataFrame(map_data_res)
        
        st.markdown("#### 🔍 Filter Regional Telemetry")
        f_state = st.multiselect("Filter by State", df_exp["state"].unique(), default=df_exp["state"].unique())
        filtered_df = df_exp[df_exp["state"].isin(f_state)]
        
        st.dataframe(filtered_df, width="stretch")
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download District Telemetry Benchmark Dataset (CSV)",
            data=csv_data,
            file_name="district_agricultural_benchmarks.csv",
            mime="text/csv"
        )

# TAB 4: Farmer Portal
with tab_auth:
    st.markdown("<h3 style='color: #065F46;'>👤 Farmer Portal & Account Management</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        u = st.session_state.user_info
        st.success(f"Active Farmer Session: **{u['name']}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Farmer Name", u["name"])
        c2.metric("Land Size", f"{u['acres']} Acres")
        c3.metric("Soil Card ID", u["soil_card_id"])
        
        if st.button("🚪 Sign Out Account"):
            st.session_state.logged_in = False
            st.session_state.user_info = {"name": "Guest Farmer", "state": "Maharashtra", "district": "Ahmednagar", "acres": 5.0, "soil_card_id": "SHC-MH-2026-0000"}
            st.rerun()
    else:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In to Account", "📝 Register New Farmer"])
        
        with auth_tab1:
            st.markdown("#### Sign in to access your Soil Health Card history & farm logs.")
            in_email = st.text_input("Email Address", "farmer@croppro.ai", key="tab_login_email")
            in_pass = st.text_input("Password", "password123", type="password", key="tab_login_pass")
            
            if st.button("🔓 Sign In Now", key="btn_signin"):
                try:
                    res = requests.post(f"{BACKEND_URL}/login", json={"email": in_email, "password": in_pass})
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.logged_in = True
                        st.session_state.user_info = data["user"]
                        st.success(f"Welcome back, {data['user']['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error("Backend API connection error.")
                    
        with auth_tab2:
            st.markdown("#### Register a new farmer profile to get customized soil advisory.")
            r_name = st.text_input("Full Name", "Aarav Patel", key="reg_name")
            r_email = st.text_input("Email", "aarav@croppro.ai", key="reg_email")
            r_pass = st.text_input("Password", "secret123", type="password", key="reg_pass")
            r_state = st.selectbox("State", ["Maharashtra", "Punjab", "Karnataka", "Tamil Nadu", "Gujarat", "Assam"], key="reg_state")
            r_district = st.text_input("District", "Ahmednagar", key="reg_district")
            r_acres = st.number_input("Land Acreage (Acres)", 1.0, 500.0, 5.0, key="reg_acres")
            
            if st.button("📝 Create Farmer Account", key="btn_signup"):
                try:
                    res = requests.post(f"{BACKEND_URL}/signup", json={
                        "name": r_name, "email": r_email, "password": r_pass,
                        "state": r_state, "district": r_district, "acres": r_acres
                    })
                    if res.status_code == 200:
                        st.session_state.logged_in = True
                        st.session_state.user_info = {
                            "name": r_name, "state": r_state, "district": r_district,
                            "acres": r_acres, "soil_card_id": f"SHC-{r_state[:2].upper()}-2026-99"
                        }
                        st.success("Farmer account registered successfully!")
                        st.rerun()
                except Exception as e:
                    st.error("Backend API connection error.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.9rem;'>CropPro.Ai Platform • Precision Agriculture Decision Engine</p>", unsafe_allow_html=True)
