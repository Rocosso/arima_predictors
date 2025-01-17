from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from services.arima_prediction_service import ArimaPredictionService
from containers.arima_container import ArimaContainer
from use_cases.train_arima_model_use_case import TrainARIMAUseCase
from models.data_models import TrainRequest, PredictRequest, ModelResponse

arima_router = APIRouter(prefix="/arima", tags=["ARIMA Model"])


@arima_router.post(
    "/predict",
    response_model=ModelResponse,
    summary="Generar predicciones para un producto específico en una tienda"
)
@inject
async def predict(
    request: PredictRequest,
    service: ArimaPredictionService = Depends(Provide[ArimaContainer.arima_service])
) -> ModelResponse:
    try:
        # Convertir future_prices a pd.Series si se proporcionan
        future_prices = None
        if request.future_prices:
            future_prices = pd.Series(
                request.future_prices,
                index=pd.date_range(start=pd.Timestamp.now(), periods=request.steps, freq='D')
            )

        result = await service.predict(
            steps=request.steps,
            product_id=request.product_id,
            store_id=request.store_id,
            future_prices=future_prices
        )

        return ModelResponse(
            status="success",
            message=f"Predictions generated for product {request.product_id} in store {request.store_id}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@arima_router.post(
    "/train",
    response_model=ModelResponse,
    summary="Entrenar modelo para un producto específico en una tienda"
)
@inject
async def train(
        request: TrainRequest,
        use_case: TrainARIMAUseCase = Depends(Provide[ArimaContainer.train_arima_use_case])
) -> ModelResponse:
    try:
        result = await use_case.execute(
            product_id=request.product_id,
            store_id=request.store_id,
            parameters=request.parameters
        )

        return ModelResponse(
            status="success",
            message=f"Model trained successfully for product {request.product_id} in store {request.store_id}",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
