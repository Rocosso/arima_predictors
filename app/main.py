from fastapi import FastAPI
from routers import arima_router, health_check
from containers.arima_container import ArimaContainer

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar el contenedor
container = ArimaContainer()

# Incluir los routers
app.include_router(health_check.health_check_router)
app.include_router(arima_router.arima_router)

# Configurar el contenedor
@app.on_event("startup")
async def startup_event():
    container.wire(modules=[
        "routers.arima_router"
    ])