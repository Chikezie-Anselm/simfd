from flask import Flask, request, jsonify
from app.models.ann_model import FraudDetectionModel

app = Flask(__name__)
model = FraudDetectionModel()

@app.route('/')
def index():
    return "Welcome to the GSM Fraud Detection System"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict(data)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)