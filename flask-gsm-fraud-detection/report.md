# Chapter 4 — Technical Summary

This document summarizes the GSM Subscription Fraud Detection system included in this repository. It is written as a short technical report suitable for inclusion in an academic Chapter 4 (System implementation and results).

---

## 4.1 Model architecture and training

- Model type: Artificial Neural Network (Keras Sequential, TensorFlow backend).
- Input preprocessing: categorical `location` is one-hot encoded (ColumnTransformer + OneHotEncoder), `registration_date` converted to numeric `days_since_first_reg`, numeric features standardized with `StandardScaler`.
- Input features (expected): `initial_call_count`, `average_call_duration`, `device_switch_count`, `days_since_first_reg` plus one-hot encoded `location` categories. Identifier columns (`subscriber_id`, `IMEI`) are dropped before training.
- Network architecture:
  - Dense(128) + ReLU + Dropout(0.3)
  - Dense(64) + ReLU + Dropout(0.2)
  - Dense(32) + ReLU + Dropout(0.1)
  - Dense(1) + Sigmoid (binary output)
- Loss / optimizer / metrics: binary_crossentropy, Adam optimizer, metric=accuracy.
- Training configuration: 50 epochs, batch_size=32, validation split performed via an 80/20 train/test split (stratified on `is_fraud`).

Notes about training performance
- The repository includes `model_train.py` which prints training and validation loss/accuracy at each epoch and saves the trained model to `models/fraud_model.h5` and preprocessing artifacts to `models/`.
- No numeric performance results are embedded in this summary because results depend on the dataset used. To reproduce and capture metrics, run:

```powershell
python generate_sample_data.py    # creates data/subscribers.csv (synthetic)
python model_train.py            # trains model and saves artifacts in models/
python evaluate_model.py         # evaluates on held-out test set and saves ROC plot
```

The `evaluate_model.py` script prints a confusion matrix, accuracy, precision, recall, F1-score, and saves an ROC plot to `app/static/images/roc.png`.

## 4.2 Flask app structure

Project layout (relevant files/folders):

- `app.py` — Flask application entry point; handles file uploads (`/upload`), prediction and serving results (`/results`).
- `app/templates/` — HTML templates (Bootstrap): `base.html`, `index.html`, `upload.html`, `results.html`, `about.html`.
- `app/static/` — static assets (CSS/JS/images); ROC plot saved to `app/static/images/roc.png` by evaluation.
- `data/` — input datasets and uploaded CSVs (uploads saved to `data/uploads/`). Example synthetic data produced by `generate_sample_data.py`.
- `models/` — saved artifacts produced by training: `fraud_model.h5`, `preprocessor.pkl`, `scaler.pkl`, `feature_meta.pkl`.
- `utils/preprocess.py` — reusable preprocessing utilities for loading CSVs, handling missing values, and transforming raw rows to model-ready numpy arrays.
- `model_train.py` — training script (builds the ANN, trains for 50 epochs, saves artifacts).
- `evaluate_model.py` — evaluation script that prints metrics and saves ROC curve.

User-facing endpoints:

- `GET /` — home page with upload form (index.html)
- `POST /upload` — accepts CSV files, runs preprocessing and model.predict, saves results to `data/uploads/`, and redirects to `/results`.
- `GET /results?results_file=...` — view predictions table, summary counts, and a Chart.js pie chart (fraud vs legitimate).

## 4.3 System requirements

- Python: 3.10 – 3.13 recommended (repository contains Python 3.13 bytecode files). Use the same minor version used for development when possible.
- Main Python packages (included in `requirements.txt`):
  - flask
  - tensorflow
  - scikit-learn
  - pandas
  - numpy
  - matplotlib
  - joblib

- Hardware:
  - CPU-only: OK for small datasets and experimentation. Training on larger datasets can be slow.
  - GPU: Recommended for faster training (TensorFlow GPU builds + compatible CUDA/cuDNN required).

Installation (recommended virtual environment on Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4.4 Example usage (end-to-end)

1. Generate synthetic data (optional):

```powershell
python generate_sample_data.py
```

2. Train model:

```powershell
python model_train.py
```

3. Evaluate (prints metrics + saves ROC):

```powershell
python evaluate_model.py
```

4. Run the web app and upload a CSV for batch prediction:

```powershell
python app.py
# Then open http://127.0.0.1:5000 in your browser and upload data/subscribers.csv
```

After upload, the web UI `/results` shows a table of predictions with columns such as Subscriber ID, IMEI, Fraud Probability (%), and a classification column (Fraud / Legitimate) with colored badges. A Chart.js pie chart summarizes fraud vs legitimate counts.

## 4.5 Key findings and limitations

Key findings (implementation notes):

- A compact ANN with three hidden layers trained on engineered behavioral features can separate legitimate from potentially fraudulent registrations when informative patterns exist (e.g., frequent device switches, abnormal call counts, unusual registration timing).
- The system is end-to-end: synthetic data generation → preprocessing → training → evaluation → batch prediction via a Flask UI.

Limitations and considerations:

- Data quality & realism: the included dataset generator produces synthetic records; real-world deployment requires high-quality labeled fraud data and domain-specific features (SIM-change histories, device fingerprints, network metadata, geolocation consistency, etc.).
- Class imbalance: fraud is typically rare. Metrics such as accuracy become misleading; use precision, recall, F1, and PR-AUC. Consider resampling, class-weighting, or anomaly-detection approaches.
- Explainability: Keras ANNs are black boxes. For operational use, add explainability (SHAP/LIME) and human-in-the-loop review for flagged cases.
- Performance & scaling: the Flask demo is for batch prediction and prototyping. For production, serve the model via a scalable inference service (TensorFlow Serving, FastAPI + gunicorn, or containerized microservice) and harden security for file uploads.
- Evaluation stability: current scripts use a single random split and synthetic data. For robust evaluation, use cross-validation, multiple random seeds, and external holdout datasets.

---

If you want, I can augment this report with:

- Concrete training/evaluation numbers (confusion matrix, AUC, precision/recall) produced by running the training and evaluation pipeline here.
- A small plots folder with training/validation loss and accuracy curves for inclusion in the written thesis.

Tell me which augmentation you'd like and I will run the pipeline and add the results to this report.
