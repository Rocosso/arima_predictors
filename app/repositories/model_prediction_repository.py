import os

import joblib
import pandas as pd
from typing import Any
import gdown

from settings.logger import setup_logger
from interfaces.repository_interface import ModelRepository
from settings.config import Settings

settings = Settings()

log = setup_logger()


class PredictionRepository(ModelRepository):
    def __init__(self):
        self.model_path = settings.arima_models_bucket_s3
        self.dataset_path = f"{settings.database_connection}/{settings.dataset_file}"
        log.info(f"Dataset path: {self.dataset_path}")
        log.info(f"Model path: {self.model_path}")
        log.info(f"Dataset file: {settings.dataset_file}")
        log.info(f"Dataset id: {settings.dataset_id}")
        log.info(f"database conection {settings.database_connection}")

    def save_model(self, model: Any, product_id:str, store_id:str) -> None:
        model_name = f"{self.model_path}/-.-{product_id}-_-{store_id}.joblib"
        joblib.dump(model, model_name)
        log.info(f"Modelo ARIMA guardado exitosamente en: {model_name}")

    def load_model(self, product_id:str, store_id:str) -> Any:
        log.info("\nCargando el modelo ARIMA...")
        model_name = f"{self.model_path}/-.-{product_id}-_-{store_id}.joblib"
        if os.path.exists(model_name):
            model = joblib.load(model_name)
            log.info("modelo %s exitosamente cargado", self.model_path)
            return model
        log.info("No se encontro el modelo %s", self.model_path)
        return

    def load_data(self) -> pd.DataFrame:
        # Verificar si el archivo existe
        if os.path.exists(self.dataset_path):
            log.info("El archivo ya existe. No es necesario volver a descargarlo.\n")
            log.info("archivo: %s \n", self.dataset_path)
            return pd.read_csv(self.dataset_path)


        log.info("El archivo no existe. Procediendo a descargarlo...")

        # Construir el enlace de descarga
        download_url = f"https://drive.google.com/uc?id={settings.dataset_id}"

        # Descargar el archivo
        gdown.download(download_url, output=self.dataset_path, quiet=False)

        log.info(f"Archivo descargado en: {self.dataset_path}")
        return pd.read_csv(self.dataset_path)