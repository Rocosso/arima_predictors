from fastapi import FastAPI

from routers.arima_router import arima_router
from routers.health_check import appHealthCheck as HealthCheckRouter

# Crear la aplicación FastAPI
app = FastAPI()

# Registrar los routers
app.include_router(arima_router, prefix="/arima", tags=["ARIMA"])
app.include_router(HealthCheckRouter, prefix="/health_check", tags=["Health Check"])