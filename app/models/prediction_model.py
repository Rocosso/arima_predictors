import pickle
import numpy as np

class PredictionModel:
    def __init__(self, model_path: str):
        # Cargar el modelo ARIMA desde un archivo
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def forecast(self, steps: int):
        # Genera la predicción
        forecast = self.model.forecast(steps=steps)[0]
        return forecast
