from itertools import product

from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject

from app.services.arima_prediction_service import ArimaPredictionService
from app.containers.arima_container import get_prediction_service
from app.use_cases.train_arima_model_use_case import TrainARIMAUseCase

# Crear el router específico para ARIMA
arima_router = APIRouter()

@inject
@arima_router.post("/predict/")
async def predict(steps: int,
                  service: ArimaPredictionService = Depends(get_prediction_service),
                  product_id: int = 1,
                  store_id: int = 1
                  ):
    """
    Endpoint para predecir valores utilizando el modelo ARIMA.
    """
    try:
        result = await service.predict(steps=steps, product_id=product_id, store_id=store_id)
        return {"forecast": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@inject
@arima_router.post("/train/",
             tags=["train"],
             summary="endpoint para Entrenar el modelo ARIMA",)
async def train(steps: int,
                use_case: TrainARIMAUseCase = Depends(),
                product_id: int = 1,
                store_id: int = 1
                ):
    """
    Endpoint para entrenar el modelo ARIMA.
    """
    try:
        result = use_case.execute(product_id=product_id, store_id=store_id)

        return {"forecast": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

