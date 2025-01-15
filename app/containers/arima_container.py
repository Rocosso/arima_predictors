from operator import contains

from app.models.prediction_model import PredictionModel
from app.repositories.model_prediction_repository import PredictionRepository
from app.services.arima_prediction_service import ArimaPredictionService
from app.use_cases.train_arima_model_use_case import TrainARIMAUseCase

from dependency_injector import containers, providers
from app.services import ArimaPredictionService


class ArimaContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para la aplicación."""

    config = providers.Configuration()
    # repository
    repository = PredictionRepository(model)

    # services
    arima_service = providers.Factory(
        ArimaPredictionService(repository),
        model_path=config.model_path  # Ruta del modelo inyectada como dependencia
    )

    # use cases
    train_arima_use_case = providers.Factory(
        TrainARIMAUseCase,
        model_path=config.model_path  # Ruta del modelo inyectada como dependencia
    )