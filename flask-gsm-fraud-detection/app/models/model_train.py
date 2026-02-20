"""
model_train.py

Trains a sample ANN model for GSM subscription fraud detection using synthetic data.
Saves the model and preprocessing artifacts into the /models directory.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Generate synthetic training data
np.random.seed(42)
n_samples = 2000

data = {
    "registration_age": np.random.randint(18, 70, n_samples),
    "call_frequency": np.random.randint(0, 50, n_samples),
    "avg_call_duration": np.random.uniform(0.5, 15.0, n_samples),
    "top_up_amount": np.random.uniform(100, 5000, n_samples),
    "region": np.random.choice(["North", "South", "East", "West"], n_samples),
    "device_type": np.random.choice(["Smartphone", "FeaturePhone"], n_samples),
    "fraud": np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
}

df = pd.DataFrame(data)

# 2. Split into features and labels
X = df.drop(columns=["fraud"])
y = df["fraud"]

# 3. Preprocessing pipeline
numeric_features = ["registration_age", "call_frequency", "avg_call_duration", "top_up_amount"]
categorical_features = ["region", "device_type"]

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

X_preprocessed = preprocessor.fit_transform(X)

# Save preprocessing artifacts
joblib.dump(preprocessor, os.path.join(MODELS_DIR, "preprocessor.pkl"))
joblib.dump(numeric_transformer, os.path.join(MODELS_DIR, "scaler.pkl"))

meta = {
    "numeric_cols": numeric_features,
    "categorical_cols": categorical_features
}
joblib.dump(meta, os.path.join(MODELS_DIR, "feature_meta.pkl"))

# 4. Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

# 5. Build ANN model
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["accuracy"])

# 6. Train model
history = model.fit(X_train, y_train, epochs=15, batch_size=32, validation_split=0.2, verbose=1)

# 7. Save model
model.save(os.path.join(MODELS_DIR, "fraud_model.h5"))

print("\n✅ Model and preprocessing artifacts saved successfully in the 'models' folder!")
