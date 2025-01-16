from pydantic import BaseModel, Field, constr
from typing import Optional, Dict, Any, List


class ARIMAParameters(BaseModel):
    order: List[int] = Field(
        default=[1, 1, 1],
        description="ARIMA order parameters (p, d, q)",
        example=[1, 1, 1]
    )
    seasonal_order: List[int] = Field(
        default=[1, 1, 1, 7],
        description="Seasonal order parameters (P, D, Q, s) where s is the number of periods in a season",
        example=[1, 1, 1, 7]
    )
    trend: str = Field(
        default="n",
        description="Trend parameter: 'n' for no trend, 'c' for constant, 't' for linear, etc.",
        example="n"
    )
    enforce_stationarity: bool = Field(
        default=False,
        description="Whether to enforce stationarity in the model",
        example=False
    )
    enforce_invertibility: bool = Field(
        default=False,
        description="Whether to enforce invertibility in the model",
        example=False
    )

    class Config:
        schema_extra = {
            "example": {
                "order": [1, 1, 1],
                "seasonal_order": [1, 1, 1, 7],
                "trend": "n",
                "enforce_stationarity": False,
                "enforce_invertibility": False
            }
        }

class TrainRequest(BaseModel):
    product_id: constr(min_length=1) = Field(
        ...,
        description="Unique identifier for the product",
        example="16a562fb5931"
    )
    store_id: constr(min_length=1) = Field(
        ...,
        description="Unique identifier for the store",
        example="14bce06b5959"
    )
    parameters: Optional[ARIMAParameters] = Field(
        default=None,
        description="Optional ARIMA model parameters. If not provided, default parameters will be used."
    )

    class Config:
        schema_extra = {
            "example": {
                "product_id": "16a562fb5931",
                "store_id": "14bce06b5959",
                "parameters": {
                    "order": [1, 1, 1],
                    "seasonal_order": [1, 1, 1, 7],
                    "trend": "n",
                    "enforce_stationarity": False,
                    "enforce_invertibility": False
                }
            }
        }

class PredictRequest(BaseModel):
    product_id: constr(min_length=1) = Field(
        ...,
        description="Unique identifier for the product",
        example="16a562fb5931"
    )
    store_id: constr(min_length=1) = Field(
        ...,
        description="Unique identifier for the store",
        example="14bce06b5959"
    )
    steps: int = Field(
        ...,
        gt=0,
        le=30,
        description="Number of future time periods to predict (1-30 days)",
        example=7
    )
    future_prices: Optional[List[float]] = Field(
        None,
        description="Optional list of future prices for the prediction period",
        example=[10.99, 10.99, 10.99, 11.99, 11.99, 11.99, 11.99]
    )

    class Config:
        schema_extra = {
            "example": {
                "product_id": "16a562fb5931",
                "store_id": "14bce06b5959",
                "steps": 7,
                "future_prices": [10.99, 10.99, 10.99, 11.99, 11.99, 11.99, 11.99]
            }
        }

class PredictionData(BaseModel):
    predictions: List[float] = Field(..., description="Predicted values")
    dates: List[str] = Field(..., description="Dates for the predictions")
    prices_used: List[float] = Field(..., description="Prices used for the predictions")
    metrics: Dict[str, float] = Field(..., description="Model performance metrics")

class ModelResponse(BaseModel):
    status: str = Field(..., description="Response status", example="success")
    message: str = Field(..., description="Response message", example="Predictions generated successfully")
    data: Dict[str, Any] = Field(
        ...,
        description="Response data containing predictions or training results"
    )

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Predictions generated for product 16a562fb5931 in store 14bce06b5959",
                "data": {
                    "predictions": [145.23, 152.45, 149.87, 155.32, 158.91, 153.45, 157.78],
                    "dates": ["2025-01-17", "2025-01-18", "2025-01-19", "2025-01-20",
                             "2025-01-21", "2025-01-22", "2025-01-23"],
                    "prices_used": [10.99, 10.99, 10.99, 11.99, 11.99, 11.99, 11.99],
                    "metrics": {
                        "aic": 789.45,
                        "bic": 801.23
                    }
                }
            }
        }

