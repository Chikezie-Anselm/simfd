"""
evaluate_model.py

Load the trained model and preprocessing artifacts, evaluate on the test set,
print confusion matrix and common classification metrics, and save an ROC
curve plot to app/static/images/roc.png.

Usage: python evaluate_model.py
"""

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, classification_report
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import load_model
import joblib

from utils.preprocess import transform_for_model, load_artifacts


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def main():
    data_path = os.path.join('data', 'subscribers.csv')
    models_dir = 'models'
    roc_path = os.path.join('app', 'static', 'images')
    roc_file = os.path.join(roc_path, 'roc.png')

    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Run data generation first.")
        sys.exit(1)

    print('Loading data...')
    df = pd.read_csv(data_path)

    if 'is_fraud' not in df.columns:
        print('No `is_fraud` column found in data; cannot evaluate.')
        sys.exit(1)

    y = df['is_fraud'].astype(int).values

    # Load model and preprocessing artifacts
    try:
        model = load_model(os.path.join(models_dir, 'fraud_model.h5'))
    except Exception as e:
        print(f'Failed to load model: {e}')
        sys.exit(1)

    try:
        preprocessor, scaler, meta = load_artifacts(models_dir=models_dir)
    except Exception as e:
        print(f'Failed to load preprocessing artifacts: {e}')
        sys.exit(1)

    print('Preprocessing data...')
    # Use the transform helper (it will use provided artifacts)
    X = transform_for_model(df, preprocessor=preprocessor, scaler=scaler, meta=meta)

    # Use same split as training: 80/20, random_state=42, stratify by y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print(f'Evaluating on test set: {X_test.shape[0]} samples')

    # Predict probabilities and labels
    probs = model.predict(X_test, batch_size=32).reshape(-1)
    y_pred = (probs >= 0.5).astype(int)

    # Metrics
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print('\nConfusion Matrix:')
    print(cm)
    print('\nClassification report:')
    print(classification_report(y_test, y_pred, digits=4, zero_division=0))
    print(f'Accuracy: {acc:.4f}')
    print(f'Precision: {prec:.4f}')
    print(f'Recall: {rec:.4f}')
    print(f'F1-score: {f1:.4f}')

    # ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)

    ensure_dir(roc_path)
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(roc_file)
    plt.close()

    print(f'ROC curve saved to {roc_file}')

    # Short summary of what metrics indicate good performance
    print('\nSummary interpretation:')
    print('- A high AUC (close to 1.0) indicates strong separability between fraud and legitimate classes.')
    print('- Precision indicates the proportion of predicted frauds that were true frauds (important to limit false alarms).')
    print('- Recall (sensitivity) measures how many actual frauds were detected; for fraud detection recall is often more important to catch as many frauds as possible.')
    print('- F1-score balances precision and recall; a high F1 shows both are strong.')
    print('- Confusion matrix gives raw counts of true/false positives and negatives; inspect it to understand error types.')


if __name__ == '__main__':
    main()
