# 🌱 CropPro.Ai — Flagship Precision Agriculture & Crop Decision Engine

**CropPro.Ai** is an award-winning, state-of-the-art **Adaptive Precision Agriculture Decision Engine** built for major university hackathons. Powered by a multi-class **XGBoost Classifier (99.20% accuracy)** trained on **264,000+ synthetic & empirical telemetry records**, **SHAP TreeExplainer AI logic**, and an **Organic Zero-Synthetic Profitability Advisory**.

---

## 🏆 Key Features & Innovations

### 1. 🤖 High-Precision XGBoost Classifier (99.20% Test Accuracy)
- Trained on **264,000 rows across 33 crop categories** (including major Indian staples, plantation crops, and Maharashtra specialties like Sugarcane, Jowar, Bajra, Maize, Cotton, Soybean, Paddy, Pigeonpea, Onion, Banana, Grapes, Mango, and Cashew).
- Inputs 10 key soil and climate telemetry features:
  `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_ec', 'market_profitability_index', 'elevation_m']`

### 2. 🌿 Zero-Synthetic Organic Profitability Advisory
- For every recommended crop, provides custom natural farming advisories:
  - 🧪 **Bio-Fertilizer Substitution**: Azospirillum, PSB, Vermicompost, and FYM recipes to reduce synthetic fertilizer costs by 40-50%.
  - 🐞 **Biological Pest Control**: Neem Seed Kernel Extract, Dashparni Arka, Trichogramma egg parasitoids.
  - 🌱 **Natural Intercropping**: Leguminous nitrogen-fixation arrangements.
  - 💰 **Profit Maximization**: Farmgate sales, steam boiling, and cold storage holding strategies.

### 3. 🗺️ Searchable GIS Regional Map & Telemetry Explorer
- Interactive **Plotly Mapbox GIS Map** (`carto-darkmatter` style) with real-time **District Text Search**, **Crop Belt Multi-Select Filter**, and **Regional Datasets**.
- Side-by-side **District Telemetry Cards Grid** and full **CSV Benchmark Dataset Export**.

### 4. 👤 Farmer Account Portal
- Session state authentication (`/login` and `/signup`) for soil health card tracking and land acreage management.

---
---

## 🚀 Quickstart Guide

### 1. Backend REST Server:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
- API Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### 2. Streamlit Web UI:
```bash
python -m streamlit run frontend/app.py --server.port 8501 --server.headless true
```
- Web Application: **[http://localhost:8501](http://localhost:8501)**

---

## 📊 Model Training Specs
- **Model Name**: CropPro.Ai
- **Rows**: 264,000
- **Features**: 10
- **Classes**: 33
- **Test Accuracy**: 99.20%
- **Artifacts**: `xgb_model.pkl`, `label_encoder.pkl`

