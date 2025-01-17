from statsmodels.tsa.statespace.sarimax import SARIMAX
from typing import Dict, Any, Optional

from services.data_preparation_service import DataPreparationService


class TrainARIMAUseCase:
    def __init__(self, repository, data_preparation_service: DataPreparationService):
        self.repository = repository
        self.data_preparation = data_preparation_service

    async def execute(
            self,
            product_id: str,
            store_id: str,
            parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Cargar y preparar datos
            raw_data = self.repository.load_data()  # Cargar dataset completo
            prepared_data = self.data_preparation.prepare_time_series(
                raw_data, product_id, store_id
            )

            # Configurar parámetros del modelo
            default_params = {
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 7),  # Estacionalidad semanal
                'trend': 'n',
                'enforce_stationarity': False,
                'enforce_invertibility': False
            }

            model_params = {**default_params, **(parameters or {})}

            # Entrenar modelo
            model = SARIMAX(
                prepared_data['Quantity'],
                exog=prepared_data['Price'],  # Usar precio como variable exógena
                **model_params
            )

            fitted_model = model.fit(disp=False)

            # Guardar modelo
            self.repository.save_model(
                model=fitted_model, product_id=product_id, store_id=store_id)

            # Preparar métricas y respuesta
            response = {
                "model_info": {
                    "aic": fitted_model.aic,
                    "bic": fitted_model.bic,
                    "parameters": model_params
                },
                "data_info": {
                    "training_start": prepared_data.index[0].strftime('%Y-%m-%d'),
                    "training_end": prepared_data.index[-1].strftime('%Y-%m-%d'),
                    "total_observations": len(prepared_data)
                }
            }

            return response

        except Exception as e:
            raise ValueError(f"Error training model: {str(e)}")
