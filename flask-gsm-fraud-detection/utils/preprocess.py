"""
utils/preprocess.py

Helper functions for loading CSVs, handling missing values, and transforming
data into numpy arrays suitable for model prediction. Uses saved artifacts
from the `models/` directory when available (preprocessor, scaler, feature_meta).

Functions:
 - load_csv(path)
 - handle_missing_values(df)
 - load_artifacts(models_dir)
 - transform_for_model(df, models_dir)

These functions are intentionally small and composable so they can be used in
both training and inference code paths.
"""

from typing import Tuple, Dict, Any
import os

import numpy as np
import pandas as pd
import joblib


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Raises FileNotFoundError or pandas parser errors.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    df = pd.read_csv(path)
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in a DataFrame.

    - Numeric columns: fill with median
    - Object / categorical columns: fill with 'unknown'
    - registration_date: leave to downstream code to parse; fill NaT with earliest date

    Returns a new DataFrame (does not modify in place).
    """
    df = df.copy()

    # Numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in numeric_cols:
        median = df[c].median()
        if pd.isna(median):
            median = 0.0
        df[c].fillna(median, inplace=True)

    # Object / categorical columns
    obj_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for c in obj_cols:
        df[c].fillna('unknown', inplace=True)

    return df


def load_artifacts(models_dir: str = 'models') -> Tuple[Any, Any, Dict[str, Any]]:
    """Load preprocessor, scaler, and feature metadata from models directory.

    Returns (preprocessor, scaler, meta_dict). If artifacts are missing, raises FileNotFoundError.
    """
    preprocessor_path = os.path.join(models_dir, 'preprocessor.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    meta_path = os.path.join(models_dir, 'feature_meta.pkl')

    if not os.path.exists(preprocessor_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError('Preprocessor or scaler not found in models directory')

    preprocessor = joblib.load(preprocessor_path)
    scaler = joblib.load(scaler_path)
    meta = joblib.load(meta_path) if os.path.exists(meta_path) else {}
    return preprocessor, scaler, meta


def transform_for_model(df: pd.DataFrame, models_dir: str = 'models', preprocessor=None, scaler=None, meta: dict = None) -> np.ndarray:
    """Transform a raw DataFrame into a numpy array ready for model.predict().

    This attempts to mirror the preprocessing used during training:
    - Convert/derive registration date into days_since_first_reg
    - Drop identifier columns (subscriber_id, IMEI)
    - Ensure expected categorical/numeric columns exist (from feature_meta)
    - Use saved ColumnTransformer (preprocessor) to encode categorical features
    - Scale numeric tail using saved StandardScaler

    Returns: numpy array of shape (n_rows, n_features)
    """
    # Load artifacts if not provided
    if preprocessor is None or scaler is None or meta is None:
        preprocessor, scaler, meta = load_artifacts(models_dir=models_dir)

    df_work = df.copy()

    # Parse registration_date into days_since_first_reg if present
    if 'registration_date' in df_work.columns:
        df_work['registration_date'] = pd.to_datetime(df_work['registration_date'], errors='coerce')
        min_date = df_work['registration_date'].min()
        if pd.isna(min_date):
            # if all dates are invalid, set zeros
            df_work['days_since_first_reg'] = 0.0
        else:
            df_work['registration_date'].fillna(min_date, inplace=True)
            df_work['days_since_first_reg'] = (df_work['registration_date'] - min_date).dt.days.astype(float)
        df_work.drop(columns=['registration_date'], inplace=True, errors='ignore')
    else:
        # ensure column exists if the model expects it
        if 'days_since_first_reg' not in df_work.columns:
            df_work['days_since_first_reg'] = 0.0

    # Drop identifier columns if present
    for col in ['subscriber_id', 'IMEI']:
        if col in df_work.columns:
            df_work.drop(columns=col, inplace=True)

    # Fill missing values using the handler
    df_work = handle_missing_values(df_work)

    # Ensure expected columns exist (categorical/numeric)
    categorical_cols = meta.get('categorical_cols', [])
    numeric_cols = meta.get('numeric_cols', [])

    for c in categorical_cols:
        if c not in df_work.columns:
            df_work[c] = ''

    for c in numeric_cols:
        if c not in df_work.columns:
            df_work[c] = 0.0

    # Use preprocessor to encode and pass through numeric columns
    X_partial = preprocessor.transform(df_work)

    # Determine number of onehot columns from fitted OneHotEncoder
    n_onehot = 0
    if categorical_cols and 'onehot' in preprocessor.named_transformers_:
        ohe = preprocessor.named_transformers_['onehot']
        n_onehot = sum(len(categories) for categories in ohe.categories_)

    X_onehot = X_partial[:, :n_onehot] if n_onehot > 0 else np.empty((X_partial.shape[0], 0))
    X_numeric = X_partial[:, n_onehot:]

    if X_numeric.size > 0:
        X_scaled_numeric = scaler.transform(X_numeric)
    else:
        X_scaled_numeric = X_numeric

    X = np.hstack([X_onehot, X_scaled_numeric]) if X_onehot.size != 0 else X_scaled_numeric
    return X


__all__ = [
    'load_csv',
    'handle_missing_values',
    'load_artifacts',
    'transform_for_model',
]
