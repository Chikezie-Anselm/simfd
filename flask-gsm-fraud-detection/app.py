"""
app.py

Flask application that loads the trained ANN model and preprocessing artifacts,
accepts CSV uploads, predicts fraud probabilities for each subscriber, and
renders results with summary analytics.

Templates are expected in the existing `app/templates` folder and static files
in `app/static` (the Flask app is configured to look there).

Run with: python app.py
"""

import os
from datetime import datetime
from io import StringIO

import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, send_from_directory, session, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import joblib
from utils.preprocess import transform_for_model, load_artifacts as load_preprocess_artifacts
from database import init_db, save_results, list_uploads as db_list_uploads, get_upload_by_file
from database import create_user, get_user_by_email, get_user_by_id


# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'data', 'uploads')
# Allow overriding the models directory via environment variable for deployments
MODELS_DIR = os.environ.get('MODELS_DIR', os.path.join(BASE_DIR, 'models'))
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create Flask app, point templates/static to existing app/ directories
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'app', 'templates'), static_folder=os.path.join(BASE_DIR, 'app', 'static'))
# SECRET_KEY should be provided as an environment variable in production
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

# Enable CORS for the frontend origin(s). In development, default to http://localhost:3000.
# For production, set CORS_ORIGINS environment variable (comma-separated list).
# Allow both localhost and 127.0.0.1 origins by default for dev
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
# flask-cors accepts a list or a string; split on commas to allow multiple origins
CORS(app, resources={r"/*": {"origins": [o.strip() for o in cors_origins.split(',')]},}, supports_credentials=True)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Allow CORS preflight (OPTIONS) requests to pass through without redirecting
        # Redirecting an OPTIONS preflight causes the browser to block the request.
        if request.method == 'OPTIONS':
            return ('', 204)
        if 'user_id' not in session:
            # If this is an AJAX/JSON request, return 401 JSON instead of redirecting
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
                return jsonify({'error': 'Authentication required'}), 401
            flash('Please sign in to access that page')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_artifacts():
    """Load model and preprocessing artifacts from the models directory."""
    model_path = os.path.join(MODELS_DIR, 'fraud_model.h5')
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    preprocessor_path = os.path.join(MODELS_DIR, 'preprocessor.pkl')
    meta_path = os.path.join(MODELS_DIR, 'feature_meta.pkl')

    model = None
    preprocessor = None
    scaler = None
    meta = {}

    # Try to load model; if missing, return None for model so we can fallback
    if os.path.exists(model_path):
        try:
            # Import ML runtime only when needed to avoid heavy startup cost when model is absent
            try:
                import importlib
                keras_models = importlib.import_module('tensorflow.keras.models')
                load_model = getattr(keras_models, 'load_model')
            except Exception:
                # If tensorflow is not available or import fails, raise to be caught below
                raise
            model = load_model(model_path)
        except Exception as e:
            # If loading fails (or tensorflow missing), keep model None and log
            print(f"Warning: Failed to load model: {e}")
    else:
        print(f"Model file not found: {model_path}")

    if os.path.exists(preprocessor_path):
        try:
            preprocessor = joblib.load(preprocessor_path)
        except Exception as e:
            print(f"Warning: Failed to load preprocessor: {e}")
    else:
        print(f"Preprocessor not found: {preprocessor_path}")

    if os.path.exists(scaler_path):
        try:
            scaler = joblib.load(scaler_path)
        except Exception as e:
            print(f"Warning: Failed to load scaler: {e}")
    else:
        print(f"Scaler not found: {scaler_path}")

    if os.path.exists(meta_path):
        try:
            meta = joblib.load(meta_path)
        except Exception as e:
            print(f"Warning: Failed to load feature meta: {e}")

    return model, preprocessor, scaler, meta


def dummy_predict(df: pd.DataFrame):
    """Generate deterministic placeholder probabilities for a DataFrame.

    Uses numeric column sums (if available) to create a normalized score between 0 and 1.
    This is intended only for UI testing when a real trained model is not present.
    """
    rng = np.random.RandomState(42)
    # Prefer numeric columns
    numeric = df.select_dtypes(include=[np.number]).fillna(0)
    if numeric.shape[1] == 0:
        # No numeric columns - produce small random noise but deterministic by index
        probs = rng.rand(len(df)) * 0.3
    else:
        s = numeric.sum(axis=1).values.astype(float)
        s_min, s_max = s.min(), s.max()
        if s_max - s_min == 0:
            norm = np.zeros_like(s)
        else:
            norm = (s - s_min) / (s_max - s_min)
        # Map normalized score into a probability-like number with a mild sigmoid
        probs = 1.0 / (1.0 + np.exp(-6.0 * (norm - 0.5)))

    # Ensure shape (n,)
    return probs.reshape(-1)


def preprocess_for_prediction(df: pd.DataFrame, preprocessor, scaler, meta: dict):
    """Mirror the preprocessing used in training to produce model-ready numpy array.

    Expects `registration_date` and other fields to exist. Raises ValueError on missing columns.
    """
    df = df.copy()

    expected_cols = set(meta.get('numeric_cols', []) + meta.get('categorical_cols', []))
    # registration_date may have been transformed into days_since_first_reg during training; check and create
    if 'registration_date' in df.columns:
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
        min_date = df['registration_date'].min()
        df['registration_date'].fillna(min_date, inplace=True)
        df['days_since_first_reg'] = (df['registration_date'] - min_date).dt.days.astype(float)
        df.drop(columns='registration_date', inplace=True)

    # Drop identifier columns if present
    for col in ['subscriber_id', 'IMEI']:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # Ensure all categorical columns exist in the dataframe (if not, create with default blank)
    categorical_cols = meta.get('categorical_cols', [])
    for c in categorical_cols:
        if c not in df.columns:
            df[c] = ''

    # Ensure numeric columns exist
    numeric_cols = meta.get('numeric_cols', [])
    for c in numeric_cols:
        if c not in df.columns:
            df[c] = 0.0

    # Use preprocessor to create encoded + numeric array, then scale numeric tail
    X_partial = preprocessor.transform(df)

    # Calculate number of onehot columns from the fitted OneHotEncoder
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


@app.route('/')
def home():
    # Redirect visitors to the registration page so they see the sign-up form immediately.
    # Other pages remain accessible without forcing authentication.
    return redirect(url_for('register'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # Load artifacts once per request
    try:
        model, preprocessor, scaler, meta = load_artifacts()
    except Exception as e:
        # If the client expects JSON (AJAX), return JSON error so frontend can handle it
        if request.accept_mimetypes.accept_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
            return jsonify({'error': str(e)}), 500
        return render_template('index.html', error=str(e))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            save_name = f"{timestamp}_{filename}"
            save_path = os.path.join(UPLOAD_DIR, save_name)
            file.save(save_path)

            # Read CSV and predict
            try:
                df = pd.read_csv(save_path)
                # Detect accidentally prepended informational lines (e.g. "Here are the contents for the file: ...")
                # which result in a single bogus column name or a column name containing that phrase.
                first_cols = list(df.columns)
                if any(isinstance(c, str) and 'Here are the contents' in c for c in first_cols) or len(first_cols) == 1 and first_cols[0].strip().startswith('Here are the contents'):
                    # Re-read skipping the first row
                    df = pd.read_csv(save_path, skiprows=1)
                # Normalize common headers: some sample files use 'id' instead of 'subscriber_id'
                if 'id' in df.columns and 'subscriber_id' not in df.columns:
                    df.rename(columns={'id': 'subscriber_id'}, inplace=True)
                # Ensure subscriber_type column exists so outputs include it
                if 'subscriber_type' not in df.columns:
                    df['subscriber_type'] = ''
            except Exception as e:
                # If this is an API request, return JSON error instead of redirecting
                if request.accept_mimetypes.accept_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
                    return jsonify({'error': f'Failed to read CSV: {e}'}), 400
                flash(f'Failed to read CSV: {e}')
                return redirect(request.url)

            # If preprocessor or scaler missing, fall back to dummy predictor
            use_dummy_due_to_preproc = False
            X = None
            if preprocessor is None or scaler is None:
                use_dummy_due_to_preproc = True
                print('Preprocessor or scaler missing - falling back to dummy predictor')
            else:
                try:
                    # Use the central preprocessing helper in utils
                    X = transform_for_model(df, preprocessor=preprocessor, scaler=scaler, meta=meta)
                except Exception as e:
                    # Fall back to dummy predictor if preprocessing fails
                    print(f'Preprocessing failed: {e} - falling back to dummy predictor')
                    use_dummy_due_to_preproc = True

            # Determine whether to use dummy predictor
            if model is None or use_dummy_due_to_preproc:
                print('Using dummy predictor for this request')
                try:
                    probs = dummy_predict(df)
                    used_dummy = True
                except Exception as e:
                    if request.accept_mimetypes.accept_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
                        return jsonify({'error': f'Dummy prediction error: {e}'}), 500
                    flash(f'Dummy prediction error: {e}')
                    return redirect(request.url)
            else:
                try:
                    # We have both model and preprocessed features
                    probs = model.predict(X, batch_size=32)
                    used_dummy = False
                except Exception as e:
                    # If model prediction fails, fall back to dummy predictor
                    print(f'Model prediction failed: {e} - falling back to dummy predictor')
                    try:
                        probs = dummy_predict(df)
                        used_dummy = True
                    except Exception as e2:
                        if request.accept_mimetypes.accept_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
                            return jsonify({'error': f'Model and dummy prediction failed: {e2}'}), 500
                        flash(f'Model and dummy prediction failed: {e2}')
                        return redirect(request.url)

            # Flatten probabilities
            probs = probs.reshape(-1)
            df_out = df.copy()
            df_out['fraud_probability'] = probs
            df_out['predicted_fraud'] = (df_out['fraud_probability'] >= 0.5).astype(int)
            # Add classification label for display
            df_out['classification'] = df_out['predicted_fraud'].map({1: 'Fraud', 0: 'Legitimate'})

            results_name = os.path.join(UPLOAD_DIR, f"predictions_{save_name}")
            df_out.to_csv(results_name, index=False)

            # If the client expects JSON (AJAX from the React/Next.js frontend), return a JSON payload
            if request.accept_mimetypes.accept_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or ''):
                total = len(df_out)
                avg_prob = float(df_out['fraud_probability'].mean()) if 'fraud_probability' in df_out.columns else 0.0
                predicted_frauds = int(df_out['predicted_fraud'].sum()) if 'predicted_fraud' in df_out.columns else 0
                legit_count = total - predicted_frauds
                # Return a small sample of rows for immediate display (first 50)
                sample_rows = df_out.head(50).to_dict(orient='records')
                resp = {
                    'total': total,
                    'avg_prob': avg_prob,
                    'predicted_frauds': predicted_frauds,
                    'legit_count': legit_count,
                    'sample': sample_rows,
                    'results_file': os.path.basename(results_name)
                }

                if model is None or use_dummy_due_to_preproc or used_dummy:
                    resp['note'] = 'Model or preprocessing artifacts not found; results were generated by a deterministic dummy predictor for UI testing.'

                # Persist metadata and sample rows in the database (best-effort)
                try:
                    save_results(os.path.basename(results_name), results_name, sample_rows, total, predicted_frauds, legit_count, avg_prob, resp.get('note'))
                except Exception as e:
                    print('Warning: failed to save results to DB:', e)

                return jsonify(resp)

            # Save a small summary and pass to results page via filename param for browser navigation
            return redirect(url_for('results', results_file=os.path.basename(results_name)))
        else:
            flash('Invalid file type — please upload a CSV file')
            return redirect(request.url)

    # GET
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user = None
    try:
        user = get_user_by_id(user_id)
    except Exception:
        user = None
    if user:
        user.pop('password_hash', None)
    return render_template('profile.html', user=user)


@app.route('/results')
def results():
    results_file = request.args.get('results_file')
    if not results_file:
        flash('No results file specified')
        return redirect(url_for('home'))

    results_path = os.path.join(UPLOAD_DIR, results_file)
    if not os.path.exists(results_path):
        flash('Results file not found')
        return redirect(url_for('home'))

    try:
        df = pd.read_csv(results_path)
        # Normalize past results that used 'id' as the first column
        if 'id' in df.columns and 'subscriber_id' not in df.columns:
            df.rename(columns={'id': 'subscriber_id'}, inplace=True)
        if 'subscriber_type' not in df.columns:
            df['subscriber_type'] = ''
    except Exception as e:
        flash(f'Failed to read results file: {e}')
        return redirect(url_for('home'))

    # Summary analytics
    total = len(df)
    avg_prob = float(df['fraud_probability'].mean()) if 'fraud_probability' in df.columns else 0.0
    predicted_frauds = int(df['predicted_fraud'].sum()) if 'predicted_fraud' in df.columns else 0
    legit_count = total - predicted_frauds

    # Limit table size for display
    # Add color badges to the DataFrame HTML for quick visual inspection
    df_display = df.copy()
    # Format probability as percentage
    if 'fraud_probability' in df_display.columns:
        df_display['fraud_probability_pct'] = (df_display['fraud_probability'] * 100).map(lambda x: f"{x:.2f}%")

    # Prepare an HTML column for classification with colored badges
    def badge_html(row):
        # Use the model's prediction (predicted_fraud) to render the classification badge so
        # the table aligns with fraud_probability and summary statistics.
        if int(row.get('predicted_fraud', 0)) == 1:
            return '<span class="badge bg-danger">Fraud</span>'
        else:
            return '<span class="badge bg-success">Legitimate</span>'

    df_display['classification_badge'] = df_display.apply(badge_html, axis=1)

    # Select preferred columns for display if they exist (include subscriber_type)
    display_cols = []
    # Prefer to show predicted_fraud (prediction) instead of is_fraud (ground truth) so
    # displayed badges and summary match the probability field.
    for c in ['subscriber_id', 'subscriber_type', 'registration_date', 'age', 'income', 'predicted_fraud', 'IMEI', 'fraud_probability_pct']:
        if c in df_display.columns:
            display_cols.append(c)
    if not display_cols:
        display_cols = df_display.columns.tolist()

    table_html = df_display.head(200)[display_cols].to_html(classes='table table-striped table-sm', index=False, escape=False)

    return render_template('results.html', table_html=table_html, total=total, avg_prob=avg_prob, predicted_frauds=predicted_frauds, legit_count=legit_count, results_file=results_file)


@app.route('/api/uploads', methods=['GET'])
def api_list_uploads():
    try:
        rows = db_list_uploads()
        return jsonify({'uploads': rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/uploads/<results_file>', methods=['GET'])
def api_get_upload(results_file):
    try:
        rec = get_upload_by_file(results_file)
        if not rec:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(rec)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/uploads')
def uploads_page():
    try:
        uploads = db_list_uploads(100)
    except Exception as e:
        uploads = []
        print('Warning: failed to list uploads:', e)
    return render_template('uploads.html', uploads=uploads)


@app.before_request
def load_current_user():
    # Make `g.user` or `session` available to templates via context
    from flask import g
    g.user = None
    user_id = session.get('user_id')
    if user_id:
        try:
            g.user = get_user_by_id(user_id)
        except Exception:
            g.user = None


@app.context_processor
def inject_user():
    return {'current_user': g.get('user')}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        email = data.get('email')
        password = data.get('password')
        display_name = data.get('display_name') or None
        if not email or not password:
            flash('Email and password required')
            return redirect(url_for('register'))
        if get_user_by_email(email):
            flash('A user with that email already exists')
            return redirect(url_for('register'))
        pw_hash = generate_password_hash(password)
        try:
            uid = create_user(email, pw_hash, display_name)
            session['user_id'] = uid
            flash('Registration successful')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Failed to create user: {e}')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        email = data.get('email')
        password = data.get('password')
        user = get_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            # If this is an AJAX/JSON request, return JSON error
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Invalid email or password'}), 401
            flash('Invalid email or password')
            return redirect(url_for('login'))
        session['user_id'] = user['id']
        # For JSON requests, return a simple success status
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'ok'}), 200
        flash('Signed in successfully')
        next_url = request.args.get('next') or url_for('home')
        return redirect(next_url)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Signed out')
    return redirect(url_for('home'))


@app.route('/api/uploads/<results_file>/download', methods=['GET'])
def download_upload(results_file):
    """Serve a saved CSV file from the uploads folder as an attachment."""
    safe_name = secure_filename(results_file)
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(UPLOAD_DIR, safe_name, as_attachment=True)


@app.route('/api/me', methods=['GET'])
def api_me():
    """Return the currently signed-in user info (if any)."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'user': None}), 200
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'user': None}), 200
        # Do not expose password hash
        user.pop('password_hash', None)
        return jsonify({'user': user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/<results_file>', methods=['GET'])
def api_results(results_file):
    """Return JSON summary and sample rows for a previously processed results file."""
    results_path = os.path.join(UPLOAD_DIR, results_file)
    if not os.path.exists(results_path):
        return jsonify({'error': 'Results file not found'}), 404

    try:
        df = pd.read_csv(results_path)
        # Normalize legacy header names for API consumers
        if 'id' in df.columns and 'subscriber_id' not in df.columns:
            df.rename(columns={'id': 'subscriber_id'}, inplace=True)
        if 'subscriber_type' not in df.columns:
            df['subscriber_type'] = ''
    except Exception as e:
        return jsonify({'error': f'Failed to read results file: {e}'}), 500

    total = len(df)
    avg_prob = float(df['fraud_probability'].mean()) if 'fraud_probability' in df.columns else 0.0
    predicted_frauds = int(df['predicted_fraud'].sum()) if 'predicted_fraud' in df.columns else 0
    legit_count = total - predicted_frauds
    sample_rows = df.head(50).to_dict(orient='records')

    return jsonify({
        'total': total,
        'avg_prob': avg_prob,
        'predicted_frauds': predicted_frauds,
        'legit_count': legit_count,
        'sample': sample_rows,
        'results_file': results_file
    })


if __name__ == '__main__':
    # Run in debug mode for development
    print('Starting Flask app...')
    try:
        init_db()
        print('Initialized SQLite DB')
    except Exception as e:
        print('Warning: failed to initialize DB:', e)
    app.run(host='127.0.0.1', port=5000, debug=True)
    print('App ready at http://127.0.0.1:5000')
