from models.prediction_model import PredictionModel

class PredictionRepository:
    def __init__(self, model: PredictionModel):
        self.model = model

    def get_forecast(self, steps: int):
        # Llama al modelo para obtener la predicción
        return self.model.forecast(steps)
