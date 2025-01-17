from fastapi import APIRouter


health_check_router = APIRouter()


@health_check_router.get("/health_check")
def healt_check():
    """
    Ruta principal para verificar el estado de la API.
    """
    return {"message": "API de Predicción ARIMA está activa"}