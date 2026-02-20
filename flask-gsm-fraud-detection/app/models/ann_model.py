from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np

class FraudDetectionModel:
    def __init__(self, input_shape):
        self.model = self.build_model(input_shape)

    def build_model(self, input_shape):
        model = keras.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=input_shape))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, X_train, y_train, epochs=50, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def predict(self, X):
        return (self.model.predict(X) > 0.5).astype("int32")

    def save_model(self, filepath):
        self.model.save(filepath)

    def load_model(self, filepath):
        self.model = keras.models.load_model(filepath)