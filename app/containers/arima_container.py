from repositories.model_prediction_repository import PredictionRepository
from services.arima_prediction_service import ArimaPredictionService
from services.data_preparation_service import DataPreparationService
from services.top_product_service import TopProductService
from use_cases.train_arima_model_use_case import TrainARIMAUseCase

from dependency_injector import containers, providers


class ArimaContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para la aplicación."""

    config = providers.Configuration()

    # Repository
    repository = providers.Factory(
        PredictionRepository
    )

    # Services
    data_preparation_service = providers.Singleton(
        DataPreparationService
    )

    top_product_service = providers.Factory(
        TopProductService,
        repository=repository
    )

    # Services
    arima_service = providers.Factory(
        ArimaPredictionService,
        repository=repository,
        data_preparation_service=data_preparation_service
    )

    # Use cases
    train_arima_use_case = providers.Factory(
        TrainARIMAUseCase,
        repository=repository,
        data_preparation_service=data_preparation_service
    )