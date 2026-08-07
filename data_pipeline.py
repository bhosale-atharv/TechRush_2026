import pandas as pd
import numpy as np

# Seed for reproducible scientific dataset generation
np.random.seed(42)

# Factual Agronomic & Agro-Climatic Baseline Distributions (ICAR, Krishi Vidyapeeth, NHB)
CROP_PROFILES = {
    # 🌾 Major Food Grains & Cereals
    "rice": {"N": (60, 120), "P": (35, 60), "K": (35, 50), "temp": (20, 29), "hum": (80, 95), "ph": (5.0, 6.8), "rain": (180, 300), "ec": (0.8, 1.8), "mpi": (6.5, 8.5), "elev": (0, 600)},
    "wheat": {"N": (80, 120), "P": (40, 60), "K": (30, 45), "temp": (12, 22), "hum": (45, 65), "ph": (6.0, 7.5), "rain": (60, 100), "ec": (0.5, 1.2), "mpi": (7.0, 8.5), "elev": (100, 800)},
    "maize": {"N": (75, 100), "P": (40, 60), "K": (35, 50), "temp": (18, 28), "hum": (55, 75), "ph": (5.8, 7.2), "rain": (80, 130), "ec": (0.6, 1.4), "mpi": (6.8, 8.2), "elev": (50, 1000)},
    "jowar": {"N": (60, 85), "P": (30, 45), "K": (30, 45), "temp": (24, 34), "hum": (35, 60), "ph": (6.0, 8.2), "rain": (45, 75), "ec": (0.8, 2.0), "mpi": (6.0, 7.8), "elev": (200, 800)},
    "bajra": {"N": (50, 75), "P": (25, 40), "K": (25, 40), "temp": (26, 36), "hum": (30, 55), "ph": (6.2, 8.3), "rain": (35, 65), "ec": (0.9, 2.2), "mpi": (5.8, 7.5), "elev": (150, 750)},
    "barley": {"N": (65, 85), "P": (30, 45), "K": (25, 40), "temp": (12, 20), "hum": (40, 60), "ph": (6.2, 7.8), "rain": (50, 85), "ec": (0.5, 1.3), "mpi": (6.2, 7.8), "elev": (300, 1200)},

    # 🫘 Pulses & Legumes
    "chickpea": {"N": (35, 55), "P": (55, 80), "K": (75, 95), "temp": (17, 24), "hum": (15, 30), "ph": (6.0, 7.8), "rain": (65, 95), "ec": (0.6, 1.5), "mpi": (7.5, 9.0), "elev": (200, 900)},
    "kidneybeans": {"N": (15, 35), "P": (55, 75), "K": (15, 30), "temp": (15, 24), "hum": (18, 30), "ph": (5.5, 6.5), "rain": (90, 120), "ec": (0.5, 1.2), "mpi": (7.8, 9.2), "elev": (400, 1400)},
    "pigeonpeas": {"N": (15, 35), "P": (55, 75), "K": (15, 30), "temp": (24, 32), "hum": (45, 65), "ph": (5.5, 7.5), "rain": (90, 130), "ec": (0.7, 1.6), "mpi": (7.2, 8.8), "elev": (100, 800)},
    "mothbeans": {"N": (15, 30), "P": (40, 60), "K": (15, 25), "temp": (25, 32), "hum": (45, 65), "ph": (6.0, 8.0), "rain": (40, 70), "ec": (0.8, 1.8), "mpi": (6.5, 8.0), "elev": (150, 700)},
    "mungbean": {"N": (15, 30), "P": (40, 60), "K": (15, 25), "temp": (25, 32), "hum": (80, 92), "ph": (6.2, 7.5), "rain": (40, 60), "ec": (0.6, 1.4), "mpi": (7.0, 8.5), "elev": (100, 750)},
    "blackgram": {"N": (35, 55), "P": (55, 75), "K": (20, 35), "temp": (26, 34), "hum": (60, 75), "ph": (6.5, 7.8), "rain": (60, 90), "ec": (0.6, 1.5), "mpi": (7.2, 8.6), "elev": (100, 800)},
    "lentil": {"N": (15, 30), "P": (55, 75), "K": (15, 30), "temp": (18, 26), "hum": (60, 72), "ph": (6.0, 7.2), "rain": (45, 60), "ec": (0.5, 1.2), "mpi": (7.4, 8.8), "elev": (200, 1000)},
    "soybean": {"N": (25, 45), "P": (60, 85), "K": (40, 65), "temp": (22, 32), "hum": (60, 78), "ph": (6.0, 7.5), "rain": (75, 110), "ec": (0.7, 1.5), "mpi": (7.8, 9.1), "elev": (150, 750)},

    # 🫚 Spices & Special Commercial Crops (Maharashtra Focus)
    "ginger": {"N": (70, 95), "P": (50, 70), "K": (90, 125), "temp": (20, 32), "hum": (70, 88), "ph": (5.5, 6.8), "rain": (150, 260), "ec": (0.5, 1.3), "mpi": (8.8, 9.8), "elev": (400, 1200)},
    "turmeric": {"N": (80, 110), "P": (50, 75), "K": (90, 130), "temp": (22, 34), "hum": (70, 86), "ph": (5.8, 7.4), "rain": (130, 220), "ec": (0.6, 1.4), "mpi": (8.5, 9.6), "elev": (200, 900)},
    "onion": {"N": (80, 105), "P": (50, 68), "K": (80, 105), "temp": (15, 28), "hum": (60, 75), "ph": (6.0, 7.5), "rain": (65, 95), "ec": (0.8, 1.7), "mpi": (8.2, 9.5), "elev": (150, 800)},
    "sugarcane": {"N": (130, 165), "P": (50, 70), "K": (50, 70), "temp": (24, 34), "hum": (70, 85), "ph": (6.2, 7.8), "rain": (120, 200), "ec": (0.8, 1.8), "mpi": (7.8, 9.0), "elev": (50, 700)},
    "cotton": {"N": (100, 135), "P": (35, 60), "K": (15, 30), "temp": (22, 30), "hum": (75, 88), "ph": (6.5, 8.0), "rain": (60, 90), "ec": (0.9, 2.0), "mpi": (7.8, 9.2), "elev": (100, 600)},
    "jute": {"N": (65, 90), "P": (35, 55), "K": (35, 55), "temp": (23, 27), "hum": (70, 85), "ph": (6.0, 7.4), "rain": (150, 200), "ec": (0.6, 1.4), "mpi": (6.8, 8.0), "elev": (0, 300)},

    # 🍎 Fruits & Horticulture
    "pomegranate": {"N": (15, 35), "P": (115, 145), "K": (180, 215), "temp": (18, 25), "hum": (85, 95), "ph": (5.5, 7.2), "rain": (35, 65), "ec": (1.0, 2.2), "mpi": (8.5, 9.8), "elev": (200, 800)},
    "banana": {"N": (80, 120), "P": (70, 95), "K": (45, 60), "temp": (25, 30), "hum": (75, 85), "ph": (5.5, 6.8), "rain": (90, 120), "ec": (0.7, 1.5), "mpi": (8.0, 9.4), "elev": (50, 600)},
    "mango": {"N": (15, 35), "P": (15, 35), "K": (25, 40), "temp": (27, 35), "hum": (48, 55), "ph": (4.5, 6.8), "rain": (85, 110), "ec": (0.8, 1.8), "mpi": (8.8, 9.8), "elev": (0, 500)},
    "grapes": {"N": (15, 35), "P": (115, 145), "K": (185, 215), "temp": (8, 42), "hum": (78, 85), "ph": (5.5, 6.5), "rain": (60, 80), "ec": (1.2, 2.4), "mpi": (9.0, 10.0), "elev": (450, 750)},
    "watermelon": {"N": (80, 110), "P": (10, 30), "K": (45, 55), "temp": (24, 27), "hum": (80, 90), "ph": (6.0, 7.0), "rain": (40, 60), "ec": (0.8, 1.8), "mpi": (7.2, 8.6), "elev": (0, 400)},
    "muskmelon": {"N": (80, 110), "P": (10, 30), "K": (45, 55), "temp": (27, 29), "hum": (90, 95), "ph": (6.0, 6.8), "rain": (20, 35), "ec": (0.8, 1.7), "mpi": (7.4, 8.8), "elev": (0, 400)},
    "apple": {"N": (15, 35), "P": (120, 145), "K": (185, 215), "temp": (12, 16), "hum": (70, 80), "ph": (5.5, 6.5), "rain": (100, 125), "ec": (0.3, 0.9), "mpi": (8.8, 9.8), "elev": (1400, 2400)},
    "orange": {"N": (15, 35), "P": (10, 30), "K": (5, 20), "temp": (10, 35), "hum": (90, 95), "ph": (6.0, 7.5), "rain": (100, 120), "ec": (0.6, 1.4), "mpi": (8.2, 9.5), "elev": (200, 600)},
    "sweetlime": {"N": (95, 125), "P": (40, 65), "K": (50, 75), "temp": (22, 34), "hum": (50, 70), "ph": (6.5, 7.8), "rain": (60, 90), "ec": (0.7, 1.5), "mpi": (8.2, 9.5), "elev": (300, 700)},
    "papaya": {"N": (40, 60), "P": (45, 65), "K": (45, 65), "temp": (33, 44), "hum": (90, 95), "ph": (6.5, 7.2), "rain": (40, 250), "ec": (0.6, 1.4), "mpi": (7.8, 9.2), "elev": (0, 600)},
    "coconut": {"N": (15, 35), "P": (10, 30), "K": (25, 35), "temp": (25, 28), "hum": (90, 98), "ph": (5.0, 6.5), "rain": (130, 230), "ec": (1.0, 2.5), "mpi": (7.5, 9.0), "elev": (0, 300)},
    "cashew": {"N": (25, 45), "P": (20, 35), "K": (30, 45), "temp": (22, 34), "hum": (65, 85), "ph": (5.0, 6.5), "rain": (150, 250), "ec": (0.5, 1.4), "mpi": (8.5, 9.6), "elev": (0, 600)},

    # ☕ High-Altitude Plantation Crops
    "coffee": {"N": (90, 110), "P": (15, 35), "K": (25, 35), "temp": (19, 27), "hum": (70, 85), "ph": (6.0, 6.8), "rain": (160, 230), "ec": (0.4, 1.0), "mpi": (9.0, 10.0), "elev": (1100, 1800)},
    "tea": {"N": (100, 125), "P": (20, 38), "K": (35, 55), "temp": (16, 24), "hum": (80, 92), "ph": (4.5, 5.5), "rain": (220, 320), "ec": (0.3, 0.9), "mpi": (9.0, 10.0), "elev": (1000, 2000)}
}

SAMPLES_PER_CROP = 8000

def generate_crop_dataset():
    data = []
    
    for crop, prof in CROP_PROFILES.items():
        n = np.random.uniform(prof["N"][0], prof["N"][1], SAMPLES_PER_CROP)
        p = np.random.uniform(prof["P"][0], prof["P"][1], SAMPLES_PER_CROP)
        k = np.random.uniform(prof["K"][0], prof["K"][1], SAMPLES_PER_CROP)
        temp = np.random.uniform(prof["temp"][0], prof["temp"][1], SAMPLES_PER_CROP)
        hum = np.random.uniform(prof["hum"][0], prof["hum"][1], SAMPLES_PER_CROP)
        ph = np.random.uniform(prof["ph"][0], prof["ph"][1], SAMPLES_PER_CROP)
        rain = np.random.uniform(prof["rain"][0], prof["rain"][1], SAMPLES_PER_CROP)
        ec = np.random.uniform(prof["ec"][0], prof["ec"][1], SAMPLES_PER_CROP)
        mpi = np.random.uniform(prof["mpi"][0], prof["mpi"][1], SAMPLES_PER_CROP)
        elev = np.random.uniform(prof["elev"][0], prof["elev"][1], SAMPLES_PER_CROP)
        
        # Micro Gaussian Noise Injection for realistic field variance
        n += np.random.normal(0, 1.5, SAMPLES_PER_CROP)
        p += np.random.normal(0, 1.5, SAMPLES_PER_CROP)
        k += np.random.normal(0, 1.5, SAMPLES_PER_CROP)
        temp += np.random.normal(0, 0.4, SAMPLES_PER_CROP)
        hum += np.random.normal(0, 0.8, SAMPLES_PER_CROP)
        ph += np.random.normal(0, 0.05, SAMPLES_PER_CROP)
        rain += np.random.normal(0, 2.0, SAMPLES_PER_CROP)
        ec += np.random.normal(0, 0.03, SAMPLES_PER_CROP)
        mpi += np.random.normal(0, 0.05, SAMPLES_PER_CROP)
        elev += np.random.normal(0, 5.0, SAMPLES_PER_CROP)

        # Boundary Clips
        n = np.clip(n, 0, 250)
        p = np.clip(p, 0, 200)
        k = np.clip(k, 0, 250)
        temp = np.clip(temp, 5, 50)
        hum = np.clip(hum, 10, 100)
        ph = np.clip(ph, 3.5, 9.5)
        rain = np.clip(rain, 10, 450)
        ec = np.clip(ec, 0.1, 5.0)
        mpi = np.clip(mpi, 1.0, 10.0)
        elev = np.clip(elev, 0, 2600)
        
        df_crop = pd.DataFrame({
            "N": n, "P": p, "K": k,
            "temperature": temp, "humidity": hum,
            "ph": ph, "rainfall": rain,
            "soil_ec": ec, "market_profitability_index": mpi,
            "elevation_m": elev,
            "label": crop
        })
        data.append(df_crop)
        
    df_full = pd.concat(data, ignore_index=True)
    df_full = df_full.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    df_full.to_csv("massive_crop_data.csv", index=False)
    print(f"Generated {len(df_full):,} rows across {len(CROP_PROFILES)} crops including Ginger, Sugarcane, Turmeric, Soybean, Jowar, Bajra, Onion, Sweet Lime!")
    return df_full

if __name__ == "__main__":
    generate_crop_dataset()
