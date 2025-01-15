import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from settings.logger import setup_logger


logger = setup_logger()

load_dotenv('.env')


class Settings(BaseSettings):
    arima_models_bucket_s3: str = os.environ.get('ARIMA_MODELS_BUCKET_S3', '')
    database_connection_string: str = os.environ.get('DATABASE_CONNECTION', '')
    dataset_id: str = os.environ.get('DATASET_ID', '')