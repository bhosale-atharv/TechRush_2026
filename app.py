import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="farmpro.ai | Precision Agriculture Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark Emerald Glassmorphism Theme
st.markdown("""
<style>
    /* Dark Forest Emerald Canvas */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #0D2C20 0%, #05140D 60%, #020A06 100%);
        color: #E2EFEA;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Hero Header Banner */
    .hero-header {
        background: linear-gradient(135deg, rgba(16, 54, 38, 0.85) 0%, rgba(6, 26, 18, 0.95) 100%);
        border: 1px solid rgba(0, 255, 157, 0.25);
        border-radius: 20px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .hero-header:hover {
        border-color: rgba(0, 255, 157, 0.5);
        box-shadow: 0 0 25px rgba(0, 255, 157, 0.15);
    }
    .hero-title {
        color: #00FF9D;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(0, 255, 157, 0.25);
    }
    .hero-subtitle {
        color: #A3C9B8;
        font-size: 1.08rem;
        margin-top: 6px;
    }
    
    /* Glassmorphism Dark Cards with Dynamic Hover Physics */
    .card {
        background: rgba(12, 36, 26, 0.65);
        border: 1px solid rgba(46, 204, 113, 0.2);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 255, 157, 0.4);
        box-shadow: 0 10px 30px rgba(0, 255, 157, 0.1);
    }
    .card-header {
        color: #2ECC71;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 14px;
    }
    
    /* Winning Crop Banner */
    .winner-card {
        background: linear-gradient(135deg, rgba(20, 70, 48, 0.9) 0%, rgba(8, 32, 21, 0.95) 100%);
        border: 2px solid #00FF9D;
        border-radius: 20px;
        padding: 26px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.15);
        transition: all 0.3s ease;
    }
    .winner-card:hover {
        transform: scale(1.01);
        box-shadow: 0 0 40px rgba(0, 255, 157, 0.25);
    }
    .winner-name {
        font-size: 2.7rem;
        font-weight: 900;
        color: #00FF9D;
        margin: 8px 0;
        text-shadow: 0 0 20px rgba(0, 255, 157, 0.4);
    }
    .winner-conf {
        font-size: 1.35rem;
        color: #F1C40F;
        font-weight: 800;
    }

    /* Organic Advisory Dark Glass Card */
    .organic-box {
        background: linear-gradient(135deg, rgba(18, 52, 36, 0.9) 0%, rgba(8, 28, 19, 0.95) 100%);
        border-left: 6px solid #F1C40F;
        border-radius: 16px;
        padding: 24px 28px;
        margin-top: 24px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    .organic-header {
        color: #F1C40F;
        font-size: 1.28rem;
        font-weight: 800;
        margin-bottom: 14px;
    }
    .organic-item {
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(241, 196, 15, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .organic-label {
        color: #00FF9D;
        font-weight: 700;
        font-size: 0.98rem;
    }
    .organic-desc {
        color: #D5E5DE;
        font-size: 0.95rem;
        margin-top: 4px;
        line-height: 1.55;
    }
    
    /* District Card Grid */
    .district-grid-card {
        background: rgba(14, 40, 29, 0.85);
        border: 1px solid rgba(0, 255, 157, 0.25);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: all 0.3s ease;
    }
    .district-grid-card:hover {
        border-color: #00FF9D;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "Guest Farmer", "state": "Maharashtra", "district": "Nashik", "acres": 5.0, "soil_card_id": "SHC-MH-2026-0000"}

# Header Banner
st.markdown("""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🌱 farmpro.ai</h1>
            <p class="hero-subtitle">Precision Agriculture Decision Engine & Agro-Climatic Intelligence</p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(0, 255, 157, 0.15); border: 1px solid #00FF9D; color: #00FF9D; padding: 8px 18px; border-radius: 30px; font-weight: 700; font-size: 0.9rem;">
                ⚡ Precision Engine Active
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch Location Database
@st.cache_data(ttl=600)
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
    sel_district = st.sidebar.selectbox("Select District (30+ Available)", districts, index=0)
    profile = loc_db[sel_state][sel_district]
else:
    sel_state = "Maharashtra"
    sel_district = "Nashik"
    profile = {
        "zone": "Western Maharashtra", "elevation_m": 580, "soil_type": "Black Basaltic Loam",
        "N": 23, "P": 133, "K": 200, "temp": 24.0, "humidity": 81, "ph": 6.0, "rainfall": 70, "soil_ec": 1.8, "market_pi": 9.3
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
        st.markdown("""<div class="card"><div class="card-header">📊 Soil & Climate Telemetry</div></div>""", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("N-P-K Ratio", f"{int(n_val)}-{int(p_val)}-{int(k_val)}")
        m2.metric("Soil pH", f"{ph_val:.1f}")
        m3.metric("Rainfall", f"{int(rain_val)} mm")
        
        m4, m5, m6 = st.columns(3)
        m4.metric("Temperature", f"{temp_val:.1f} °C")
        m5.metric("Soil EC", f"{ec_val:.1f} dS/m")
        m6.metric("Elevation", f"{int(elev_val)} m")

        # Dark Neon Radar Spider Chart
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
            line_color='#00FF9D',
            fillcolor='rgba(0, 255, 157, 0.25)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                bgcolor='rgba(12, 36, 26, 0.5)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#A0C4B4'),
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
            
            top_score = top_recs[0]["confidence"]
            
            st.markdown(f"""<div class="winner-card"><div style="color: #A0C4B4; text-transform: uppercase; font-size: 0.95rem; font-weight: 800;">🥇 Recommended Optimal Crop</div><div class="winner-name">{winner}</div><div class="winner-conf">{top_score:.1f}% Confidence Match</div></div>""", unsafe_allow_html=True)
            
            crops_list = [r["crop"] for r in top_recs[::-1]]
            confs_list = [r["confidence"] for r in top_recs[::-1]]
            
            fig_bar = go.Figure(go.Bar(
                x=confs_list,
                y=crops_list,
                orientation='h',
                marker=dict(
                    color=confs_list,
                    colorscale=[[0, '#1E513B'], [0.5, '#2ECC71'], [1.0, '#00FF9D']],
                    line=dict(color='#00FF9D', width=1.5)
                ),
                text=[f"{c:.1f}%" for c in confs_list],
                textposition='auto',
                textfont=dict(color='#051A10', size=13, family='sans-serif')
            ))
            fig_bar.update_layout(
                title=dict(text="🏆 Top 3 Suitable Crops", font=dict(color='#00FF9D', size=16)),
                xaxis=dict(range=[0, 105], showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E0EAE5'),
                height=210,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_bar, width="stretch")

    if response_data:
        st.markdown("---")
        org_html = f"""<div class="organic-box">
<div class="organic-header">🌿 Zero-Synthetic Organic Profitability Advisory for '{winner}'</div>
<p style="color: #D5E5DE; margin-bottom: 15px;">Maximize your net profit margin by reducing synthetic fertilizer expenses using proven natural farming techniques.</p>

<div class="organic-item">
<div class="organic-label">🧪 Bio-Fertilizer & Organic Nutrient Substitution:</div>
<div class="organic-desc">{organic_advisory['organic_fertilizers']}</div>
</div>

<div class="organic-item">
<div class="organic-label">🐞 Biological & Natural Pest Control:</div>
<div class="organic-desc">{organic_advisory['natural_pest_control']}</div>
</div>

<div class="organic-item">
<div class="organic-label">🌱 Natural Intercropping & Nitrogen Fixation:</div>
<div class="organic-desc">{organic_advisory['intercropping_profit']}</div>
</div>

<div class="organic-item">
<div class="organic-label">💰 Profit Maximization & Market Strategy:</div>
<div class="organic-desc">{organic_advisory['max_profit_tip']}</div>
</div>
</div>"""
        st.markdown(org_html, unsafe_allow_html=True)

# TAB 2: Searchable Geographical Representation & GIS Map
with tab_map:
    st.markdown("<h3 style='color: #00FF9D;'>🗺️ Searchable GIS Regional Agro-Climatic Map & Telemetry Explorer</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A3C9B8;'>Search by District name, Crop belt, or Agro-climatic zone to easily locate regional data.</p>", unsafe_allow_html=True)
    
    map_data_res = None
    try:
        m_res = requests.get(f"{BACKEND_URL}/crop-map-data")
        if m_res.status_code == 200:
            map_data_res = m_res.json()["data"]
    except Exception as e:
        pass
        
    if map_data_res:
        df_map = pd.DataFrame(map_data_res)
        
        # 🔍 Search & Filter Bar
        sf1, sf2, sf3 = st.columns([1.2, 1, 1])
        with sf1:
            search_query = st.text_input("🔍 Search District or State", "", placeholder="Type 'Nashik', 'Pune', 'Coorg'...")
        with sf2:
            crop_filter = st.multiselect("🌾 Filter Crop Belt", options=df_map["primary_crop"].unique(), default=[])
        with sf3:
            zone_filter = st.multiselect("📍 Filter Zone", options=df_map["zone"].unique(), default=[])

        # Filter Logic
        filtered_map_df = df_map.copy()
        if search_query:
            filtered_map_df = filtered_map_df[
                filtered_map_df["district"].str.contains(search_query, case=False, na=False) |
                filtered_map_df["state"].str.contains(search_query, case=False, na=False)
            ]
        if crop_filter:
            filtered_map_df = filtered_map_df[filtered_map_df["primary_crop"].isin(crop_filter)]
        if zone_filter:
            filtered_map_df = filtered_map_df[filtered_map_df["zone"].isin(zone_filter)]
            
        st.info(f"Showing **{len(filtered_map_df)}** of **{len(df_map)}** regional district data points.")
        
        if not filtered_map_df.empty:
            fig_geo = px.scatter_mapbox(
                filtered_map_df,
                lat="lat",
                lon="lon",
                hover_name="district",
                hover_data={
                    "state": True,
                    "zone": True,
                    "primary_crop": True,
                    "soil_type": True,
                    "elevation_m": True,
                    "rainfall": True,
                    "lat": False,
                    "lon": False
                },
                color="primary_crop",
                size="elevation_m",
                size_max=28,
                zoom=5.5,
                center={"lat": 19.5, "lon": 76.0},
                mapbox_style="carto-darkmatter",
                title="Searchable GIS Regional Crop Belt Distribution"
            )
            fig_geo.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00FF9D', family='sans-serif', size=13),
                title=dict(font=dict(color='#00FF9D', size=18, family='sans-serif')),
                legend=dict(
                    font=dict(color='#E2EFEA', size=12),
                    title=dict(font=dict(color='#00FF9D', size=13)),
                    bgcolor='rgba(12, 36, 26, 0.95)',
                    bordercolor='rgba(0, 255, 157, 0.3)',
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
<strong style="color: #00FF9D; font-size: 1.1rem;">📍 {row['district']}</strong>
<span style="background: rgba(0, 255, 157, 0.15); color: #00FF9D; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">{row['state']}</span>
</div>
<div style="color: #A3C9B8; font-size: 0.9rem; margin-top: 6px;">🌾 <b>Crop Belt:</b> {row['primary_crop']}</div>
<div style="color: #A3C9B8; font-size: 0.9rem;">🏔️ <b>Elevation:</b> {row['elevation_m']}m | 🌧️ <b>Rainfall:</b> {row['rainfall']}mm</div>
<div style="color: #A3C9B8; font-size: 0.9rem;">🧪 <b>Soil:</b> {row['soil_type']}</div>
</div>"""
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("No districts matched your search query. Try clearing the filters.")

# TAB 3: Dataset Explorer
with tab_data:
    st.markdown("<h3 style='color: #00FF9D;'>📊 Dataset & Raw Telemetry Explorer</h3>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color: #00FF9D;'>👤 Farmer Portal & Account Management</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        u = st.session_state.user_info
        st.success(f"Active Farmer Session: **{u['name']}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Farmer Name", u["name"])
        c2.metric("Land Size", f"{u['acres']} Acres")
        c3.metric("Soil Card ID", u["soil_card_id"])
        
        if st.button("🚪 Sign Out Account"):
            st.session_state.logged_in = False
            st.session_state.user_info = {"name": "Guest Farmer", "state": "Maharashtra", "district": "Nashik", "acres": 5.0, "soil_card_id": "SHC-MH-2026-0000"}
            st.rerun()
    else:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In to Account", "📝 Register New Farmer"])
        
        with auth_tab1:
            st.markdown("#### Sign in to access your Soil Health Card history & farm logs.")
            in_email = st.text_input("Email Address", "farmer@farmpro.ai", key="tab_login_email")
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
            r_email = st.text_input("Email", "aarav@farmpro.ai", key="reg_email")
            r_pass = st.text_input("Password", "secret123", type="password", key="reg_pass")
            r_state = st.selectbox("State", ["Maharashtra", "Punjab", "Karnataka", "Tamil Nadu", "Gujarat", "Assam"], key="reg_state")
            r_district = st.text_input("District", "Nashik", key="reg_district")
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
st.markdown("<p style='text-align: center; color: #5D8071; font-size: 0.9rem;'>farmpro.ai Platform • Precision Agriculture Decision Engine</p>", unsafe_allow_html=True)
