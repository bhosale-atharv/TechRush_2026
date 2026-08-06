import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import shap
import joblib
import time
import os

print("=" * 75)
print("UPGRADED ML ENGINE & SHAP EXPLAINABILITY ENGINE (10 FEATURES)")
print("=" * 75)

# 1. Load Dataset
data_path = "massive_crop_data.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError("Dataset massive_crop_data.csv not found. Run data_pipeline.py first.")

print(f"Loading dataset from '{data_path}'...")
start_time = time.time()
df = pd.read_csv(data_path)
print(f"Loaded {len(df):,} rows successfully in {time.time() - start_time:.2f}s.")

# Features & Label separation (10 features including topography/elevation_m)
feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_ec', 'market_profitability_index', 'elevation_m']
X = df[feature_cols]
y = df['label']

# Encode Labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
class_names = list(label_encoder.classes_)
num_classes = len(class_names)

print(f"Number of target crop classes: {num_classes}")

# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.15, random_state=42, stratify=y_encoded)

# 2. Train XGBoost Model
print("Training XGBoost Classifier on 10 features including Topography...")
train_start = time.time()

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.15,
    objective='multi:softprob',
    num_class=num_classes,
    n_jobs=-1,
    random_state=42,
    eval_metric='mlogloss',
    tree_method='hist'
)

model.fit(X_train, y_train)
train_time = time.time() - train_start
print(f"Model training completed in {train_time:.2f} seconds.")

# Evaluate Model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n--- MODEL ACCURACY: {acc * 100:.2f}% ---")

# 3. Real-World Constraint Modifier Engine
class RealWorldConstraintEngine:
    WATER_INTENSIVE_CROPS = {"Rice", "Sugarcane", "Jute", "Papaya", "Tea", "Banana"}
    DROUGHT_TOLERANT_CROPS = {"Mothbeans", "Mungbean", "Chickpea", "Watermelon", "Barley", "Pomegranate"}
    SALT_SENSITIVE_CROPS = {"Kidneybeans", "Apple", "Mungbean", "Chickpea", "Lentil"}
    SALT_TOLERANT_CROPS = {"Barley", "Cotton", "Coconut", "Pomegranate", "Sugarcane"}

    @classmethod
    def apply_constraints(cls, probs, class_names, input_features, drought_mode=False, salinity_alert=False, market_priority_mode=False):
        adj_probs = probs.copy()
        
        for i, crop in enumerate(class_names):
            mult = 1.0
            
            if drought_mode:
                if crop in cls.WATER_INTENSIVE_CROPS:
                    mult *= 0.25
                elif crop in cls.DROUGHT_TOLERANT_CROPS:
                    mult *= 1.6
            
            if salinity_alert or input_features.get('soil_ec', 0.0) > 1.8:
                if crop in cls.SALT_SENSITIVE_CROPS:
                    mult *= 0.3
                elif crop in cls.SALT_TOLERANT_CROPS:
                    mult *= 1.5
            
            if market_priority_mode:
                mpi = input_features.get('market_profitability_index', 5.0)
                mult *= (mpi / 7.0)
                
            adj_probs[i] *= mult
            
        sum_p = np.sum(adj_probs)
        if sum_p > 0:
            adj_probs = adj_probs / sum_p
            
        return adj_probs


# 4. SHAP Explainability Engine
print("Initializing SHAP TreeExplainer for AI Logic Explainability...")
explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")

def explain_prediction(model, explainer, input_df, label_encoder, top_crop):
    top_class_idx = int(label_encoder.transform([top_crop])[0])
    shap_vals = explainer(input_df)
    
    if len(shap_vals.shape) == 3:
        crop_shap = shap_vals.values[0, :, top_class_idx]
    elif len(shap_vals.shape) == 2:
        crop_shap = shap_vals.values[0, :]
    else:
        crop_shap = np.array(shap_vals.values)[0]

    feature_names = input_df.columns.tolist()
    feature_val_dict = input_df.iloc[0].to_dict()
    
    impact_pairs = list(zip(feature_names, crop_shap, [feature_val_dict[f] for f in feature_names]))
    impact_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    
    top_drivers = []
    for feat, shap_val, orig_val in impact_pairs[:3]:
        direction = "strongly favored" if shap_val > 0 else "reduced likelihood for"
        top_drivers.append(f"{feat} ({orig_val}) {direction}")
        
    explanation_sentence = f"AI Logic Analysis for Top Recommendation '{top_crop}': Key drivers were " + ", ".join(top_drivers) + "."
    feature_impacts = {feat: float(shap_val) for feat, shap_val, _ in impact_pairs}
    
    return explanation_sentence, feature_impacts

# 5. Save Artifacts
print("\nSaving trained model and label encoder...")
joblib.dump(model, "xgb_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

# Verify SHAP on sample row
sample_input = pd.DataFrame([{
    'N': 85.0, 'P': 45.0, 'K': 40.0,
    'temperature': 24.5, 'humidity': 82.0, 'ph': 6.5,
    'rainfall': 230.0, 'soil_ec': 1.2, 'market_profitability_index': 8.5,
    'elevation_m': 150.0
}])

raw_probs = model.predict_proba(sample_input)[0]
top_idx = np.argmax(raw_probs)
top_crop = label_encoder.inverse_transform([top_idx])[0]

exp_sentence, impacts = explain_prediction(model, explainer, sample_input, label_encoder, top_crop)

print("\n--- SAMPLE PREDICTION TEST ---")
print(f"Top Crop Predicted: {top_crop} ({raw_probs[top_idx]*100:.1f}% raw confidence)")
print(f"SHAP Explanation:\n  -> {exp_sentence}")

print("\nUpgraded ML Engine completed successfully!")
