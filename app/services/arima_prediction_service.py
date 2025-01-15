from repositories.model_prediction_repository import PredictionRepository

class ArimaPredictionService:
    def __init__(self, repository: PredictionRepository):
        self.repository = repository

    def predict(self, steps: int, product_id: str, store_id: str):
        # Valida los datos y delega al repositorio
        if steps <= 0:
            raise ValueError("El número de pasos debe ser mayor que 0.")
        return self.repository.get_forecast(steps)
