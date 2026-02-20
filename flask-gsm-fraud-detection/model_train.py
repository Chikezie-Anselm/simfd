"""
model_train.py

Loads data/subscribers.csv, preprocesses features, trains an ANN (Keras Sequential)
for fraud detection, and saves the trained model and scaler to the models/ folder.

Usage: python model_train.py

This script expects a CSV at data/subscribers.csv with columns including:
subscriber_id, IMEI, registration_date, location, initial_call_count,
average_call_duration, device_switch_count, is_fraud

Requires: pandas, numpy, scikit-learn, tensorflow, joblib
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import joblib

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


def load_data(path: str) -> pd.DataFrame:
    """Load CSV into a DataFrame. Exits with an informative message if not found."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    return df


def preprocess(df: pd.DataFrame):
    """Preprocess the subscribers DataFrame and return X, y and fitted scaler.

    - Drops identifier columns
    - Converts registration_date to numeric days-since-first-registration
    - One-hot encodes `location`
    - Scales numeric features with StandardScaler
    """
    df = df.copy()

    # Target
    if 'is_fraud' not in df.columns:
        raise KeyError('Expected `is_fraud` column in data')
    y = df['is_fraud'].astype(int).values

    # Drop identifiers that should not be used as predictive features
    for col in ['subscriber_id', 'IMEI']:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # Parse registration_date into numeric feature (days since earliest registration)
    if 'registration_date' in df.columns:
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
        # Replace NaT with earliest date to avoid losing rows
        min_date = df['registration_date'].min()
        df['registration_date'].fillna(min_date, inplace=True)
        df['days_since_first_reg'] = (df['registration_date'] - min_date).dt.days.astype(float)
        df.drop(columns='registration_date', inplace=True)
    else:
        df['days_since_first_reg'] = 0.0

    # Identify numeric and categorical features
    numeric_cols = []
    possible_numeric = ['initial_call_count', 'average_call_duration', 'device_switch_count', 'days_since_first_reg']
    for c in possible_numeric:
        if c in df.columns:
            numeric_cols.append(c)

    categorical_cols = [c for c in df.columns if c not in numeric_cols + ['is_fraud']]

    # ColumnTransformer: OneHot encode categorical, pass through numeric (we'll scale numeric separately)
    preprocessor = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ],
        remainder='passthrough'  # numeric columns will be passed through in their original order
    )

    # Fit the preprocessor to get encoded categorical feature shapes
    X_partial = preprocessor.fit_transform(df.drop(columns=['is_fraud']))

    # After ColumnTransformer with remainder='passthrough', the order is: encoded categorical columns, then numeric columns
    # We'll scale the numeric tail using StandardScaler. Find index where numeric columns begin.
    n_onehot = 0
    if len(categorical_cols) > 0:
        # OneHotEncoder creates n_columns equal to sum of categories per feature
        ohe = preprocessor.named_transformers_['onehot']
        n_onehot = sum(len(categories) for categories in ohe.categories_)

    # Split encoded array
    X_onehot = X_partial[:, :n_onehot] if n_onehot > 0 else np.empty((X_partial.shape[0], 0))
    X_numeric = X_partial[:, n_onehot:]

    # Scale numeric features
    scaler = StandardScaler()
    if X_numeric.size == 0:
        X_scaled_numeric = X_numeric
    else:
        X_scaled_numeric = scaler.fit_transform(X_numeric)

    # Combine back
    X = np.hstack([X_onehot, X_scaled_numeric]) if X_onehot.size != 0 else X_scaled_numeric

    return X, y, preprocessor, scaler, numeric_cols, categorical_cols


def build_model(input_dim: int) -> tf.keras.Model:
    """Builds a Keras Sequential model with 3 hidden layers."""
    model = Sequential()
    # Hidden layer 1
    model.add(Dense(128, activation='relu', input_shape=(input_dim,)))
    model.add(Dropout(0.3))
    # Hidden layer 2
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    # Hidden layer 3
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.1))
    # Output
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def main():
    data_path = os.path.join('data', 'subscribers.csv')
    print(f"Loading data from {data_path}...")
    df = load_data(data_path)

    print('Preprocessing...')
    X, y, preprocessor, scaler, numeric_cols, categorical_cols = preprocess(df)

    print('Splitting into train/test (80/20)...')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f'Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}')

    # Build model
    model = build_model(input_dim=X_train.shape[1])

    # Train
    print('Training model for 50 epochs...')
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=2)

    # Print final metrics
    final_loss = history.history['loss'][-1]
    final_acc = history.history['accuracy'][-1]
    val_loss = history.history['val_loss'][-1]
    val_acc = history.history['val_accuracy'][-1]
    print(f"Final training loss: {final_loss:.4f}, accuracy: {final_acc:.4f}")
    print(f"Final validation loss: {val_loss:.4f}, accuracy: {val_acc:.4f}")

    # Ensure models dir exists
    models_dir = 'models'
    os.makedirs(models_dir, exist_ok=True)

    # Save Keras model
    model_path = os.path.join(models_dir, 'fraud_model.h5')
    print(f'Saving trained model to {model_path}...')
    model.save(model_path)

    # Save preprocessing objects separately so downstream code can load the scaler easily
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    preprocessor_path = os.path.join(models_dir, 'preprocessor.pkl')
    meta_path = os.path.join(models_dir, 'feature_meta.pkl')
    print(f'Saving scaler to {scaler_path}...')
    joblib.dump(scaler, scaler_path)
    print(f'Saving preprocessor to {preprocessor_path}...')
    joblib.dump(preprocessor, preprocessor_path)
    print(f'Saving feature metadata to {meta_path}...')
    joblib.dump({'numeric_cols': numeric_cols, 'categorical_cols': categorical_cols}, meta_path)

    print('Done.')


if __name__ == '__main__':
    main()
