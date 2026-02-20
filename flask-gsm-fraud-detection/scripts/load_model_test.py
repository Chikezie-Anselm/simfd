import sys, traceback
model_path = r"C:\Users\HP\Desktop\simfd\flask-gsm-fraud-detection\models\fraud_model.h5"
print('Attempting to import tensorflow...')
try:
    import tensorflow as tf
    print('tensorflow version:', tf.__version__)
    from tensorflow.keras.models import load_model
    print('Attempting to load model:', model_path)
    m = load_model(model_path)
    print('Model loaded. Summary:')
    try:
        m.summary()
    except Exception:
        print('Model summary not available')
except Exception as e:
    print('ERROR importing/loading model:')
    traceback.print_exc()
    sys.exit(1)
