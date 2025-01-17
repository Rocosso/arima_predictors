from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from settings.logger import setup_logger

logger = setup_logger()

load_dotenv('.env')


class Settings(BaseSettings):
    arima_models_bucket_s3: str
    database_connection: str
    dataset_id: str
    dataset_file: str

    class Config:
        env_file = ".env"  # Archivo desde donde se cargarán las variables de entorno
        env_file_encoding = "utf-8"  # Codificación del archivo

