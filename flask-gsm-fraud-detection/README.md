# Flask GSM Fraud Detection

This project implements a Flask-based web application that detects fraudulent GSM subscriber registrations using an Artificial Neural Network (ANN). The application is designed to provide a user-friendly interface for uploading subscriber data and receiving fraud detection results.

## Project Structure

```
flask-gsm-fraud-detection
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models
│   │   └── ann_model.py
│   ├── static
│   └── templates
│       └── index.html
├── data
│   └── sample_data.csv
├── venv/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-gsm-fraud-detection
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application:**
   ```
   flask run
   ```

2. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

3. **Upload subscriber data:**
   Use the provided interface to upload a CSV file containing subscriber registration data for fraud detection.

## Dependencies

- Flask
- TensorFlow
- scikit-learn
- pandas
- numpy
- matplotlib
- joblib

## License

This project is licensed under the MIT License. See the LICENSE file for details.