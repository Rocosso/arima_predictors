import os
import pickle

import pandas as pd
import numpy as np
import gdown
from statsmodels.tsa.arima.model import ARIMA

from app.settings.config import Settings
from app.settings.logger import setup_logger

log = setup_logger()
settings = Settings()

class TrainARIMAUseCase:
    def execute(self, product_id, store_id):
        use_case = TrainARIMAUseCase()

        # ID del archivo en Google Drive (extraído del enlace compartido)
        file_id = settings.dataset_id

        # Ruta donde guardar el archivo
        output_path = "dataset.csv"

        # Descargar el archivo
        use_case.get_dataset(file_id=file_id, output_path=output_path)

        # Cargar el dataset
        dataframe = use_case.load_data(output_path=output_path)

        # Preprocesamiento
        data = use_case.preprosessing(data=dataframe)

        # Entrenar el modelo ARIMA
        trained_model = use_case.train_arima(data=data, product_id=product_id, store_id=store_id)

        # Guardar el modelo ARIMA
        model_path = f"arima_model-.-{product_id}-_-{store_id}.pkl"

        use_case.save_model(model=trained_model, model_path=model_path)

    # Modelo ARIMA
    def train_arima(self, data, product_id, store_id):
        df = data[(data['ProductID'] == product_id) & (data['StoreID'] == store_id)]
        df = df.set_index('Date').resample('M').sum()['Quantity']
        model = ARIMA(df, order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=12)
        return forecast

    def preprosessing(self, data):
        # Preprocesamiento general
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values(by='Date')
        return data

    def load_data(self, path):
        df = pd.read_csv(path)
        log.info(f"Dataset cargado:\n {path}\n")
        log.info(f"Dataset shape:\n {df.shape}\n")
        log.info(f"Dataset columns:\n {df.columns}\n")
        log.info(f"Dataset info:\n {df.info()}\n")
        log.info(f"Dataset head:\n {df.head()}\n")
        log.info(f"Dataset tail:\n {df.tail()}\n")
        log.info(f"describe:\n {df.describe()}\n")
        return df

    def get_dataset(self, file_id, output_path):
        """
            Descarga un archivo de Google Drive usando gdown.

            Args:
                file_id (str): El ID del archivo en Google Drive.
                output_path (str): Ruta donde se guardará el archivo descargado.
            """

        # Ruta donde debería estar el dataset
        dataset_path = "app/datasets/dataset.csv"

        # Verificar si el archivo existe
        if os.path.exists(dataset_path):
            print("El archivo ya existe. No es necesario volver a descargarlo.")
            return

        print("El archivo no existe. Procediendo a descargarlo...")

        # Construir el enlace de descarga
        download_url = f"https://drive.google.com/uc?id={file_id}"

        # Descargar el archivo
        gdown.download(download_url, output_path=output_path, quiet=False)
        log.info(f"Archivo descargado en: {output_path}")

    def save_model(self, model, model_path):

        #simulamos un Bucket s3 para salvar el modelo
        url= f"{settings.S3_BUCKET}/{model_path}"

        # Guardar el modelo ARIMA en un archivo
        with open(url, 'wb') as file:
            pickle.dump(model, file)
        print(f"Modelo ARIMA guardado en: {url}")



if __name__ == '__main__':
    product_id = 1
    store_id = 1

    use_case = TrainARIMAUseCase()
    model = use_case.execute(product_id=product_id, store_id=store_id)
