import pandas as pd
from typing import Dict, Any, Optional
from interfaces.prediction_service_interface import PredictionService
from services.data_preparation_service import DataPreparationService
from settings.logger import setup_logger

log = setup_logger()


class ArimaPredictionService(PredictionService):
    def __init__(self, repository, data_preparation_service: DataPreparationService):
        self.repository = repository
        self.data_preparation = data_preparation_service

    async def predict(self, steps: int, product_id: str, store_id: str, future_prices: Optional[pd.Series] = None) -> \
    Dict[str, Any]:
        try:
            # Cargar modelo específico para producto/tienda
            model = self.repository.load_model(product_id, store_id)

            # Obtener la última fecha de los datos históricos
            raw_data = self.repository.load_data()
            historical_data = self.data_preparation.prepare_time_series(raw_data, product_id, store_id)
            last_date = historical_data.index[-1]

            if future_prices is None:
                # Si no se proporcionan precios futuros, intentar obtenerlos
                log.info(f"Obteniendo precios futuros para {steps} días")
                future_prices = self.data_preparation.get_future_prices(
                    raw_data,
                    product_id,
                    store_id,
                    start_date=last_date + pd.Timedelta(days=1),
                    periods=steps
                )

            # Validar los precios futuros
            if not isinstance(future_prices, (pd.Series, pd.DataFrame)):
                raise ValueError("future_prices debe ser una Serie o DataFrame de pandas")

            if len(future_prices) != steps:
                raise ValueError(f"future_prices debe contener {steps} períodos de datos")

            # Realizar predicción
            log.info(f"**** Generando predicciones para producto {product_id} en tienda {store_id}")
            forecast = model.forecast(steps=steps, exog=future_prices)
            log.info(f"**** Predicciones generadas para producto {product_id} en tienda {store_id}")

            # Preparar respuesta
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=steps,
                freq='D'
            )

            response = {
                "predictions": forecast.tolist(),
                "dates": future_dates.strftime('%Y-%m-%d').tolist(),
                "prices_used": future_prices.tolist(),
                "metrics": {
                    "aic": getattr(model, 'aic', None),
                    "bic": getattr(model, 'bic', None)
                }
            }

            return response

        except Exception as e:
            log.error(f"Error generando predicciones: {str(e)}")
            raise ValueError(f"Error generando predicciones: {str(e)}")