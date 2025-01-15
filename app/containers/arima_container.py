from dependency_injector import containers, providers

from services.arima_prediction_service import ArimaPredictionService
from repositories.model_prediction_repository import PredictionRepository
from use_cases.train_arima_model_use_case import TrainARIMAUseCase
from models.prediction_model import PredictionModel

class ArimaContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para la aplicación."""

    config = providers.Configuration()

    # repository
    repository = providers.Factory(
        PredictionRepository,
        model=providers.Singleton(PredictionModel, model_path=config.model_path)
    )

    # services
    arima_service = providers.Factory(
        ArimaPredictionService,
        repository=repository,
        model_path=config.model_path
    )

    # use cases
    train_arima_use_case = providers.Factory(
        TrainARIMAUseCase,
        model_path=config.model_path
    )
