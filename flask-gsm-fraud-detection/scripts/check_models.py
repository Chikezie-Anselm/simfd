import os
import traceback

BASE = r"C:\Users\HP\Desktop\simfd\flask-gsm-fraud-detection"
models_dir = os.path.join(BASE, 'models')
files = {
    'model': os.path.join(models_dir, 'fraud_model.h5'),
    'preprocessor': os.path.join(models_dir, 'preprocessor.pkl'),
    'scaler': os.path.join(models_dir, 'scaler.pkl'),
    'meta': os.path.join(models_dir, 'feature_meta.pkl')
}

print('Checking model artifacts in:', models_dir)
for name, path in files.items():
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 'N/A'
    print(f"{name}: {path} - exists={exists} size={size}")

# Try to load pickles with joblib
if os.path.exists(files['preprocessor']):
    try:
        import joblib
        _ = joblib.load(files['preprocessor'])
        print('Preprocessor: loaded OK')
    except Exception:
        print('Preprocessor: failed to load')
        traceback.print_exc()
else:
    print('Preprocessor file not present; skipping load test')

if os.path.exists(files['scaler']):
    try:
        import joblib
        _ = joblib.load(files['scaler'])
        print('Scaler: loaded OK')
    except Exception:
        print('Scaler: failed to load')
        traceback.print_exc()
else:
    print('Scaler file not present; skipping load test')

# Avoid loading model with tensorflow here (heavy). Just report presence.
if os.path.exists(files['model']):
    print('Model file present; not attempting to load here (tensorflow import skipped)')
else:
    print('Model file not present')
