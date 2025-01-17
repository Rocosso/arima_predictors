from typing import Optional, Dict, Any
import pandas as pd
from settings.logger import setup_logger
from repositories.model_prediction_repository import PredictionRepository

log = setup_logger()


class TopProductService:
    def __init__(self, repository: PredictionRepository):
        self.repository = repository

    async def get_top_product(
            self,
            start_date: str,
            end_date: str,
            store_id: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            # Cargar datos usando el PredictionRepository
            raw_data = self.repository.load_data()

            # Log para debugging
            log.info(f"Columns in raw_data: {raw_data.columns.tolist()}")

            # Renombrar columnas para coincidir con el formato esperado
            column_mapping = {
                'Date': 'date',
                'ProductID': 'product_id',
                'StoreID': 'store_id',
                'Quantity': 'quantity',
                'Price': 'price'
            }

            # Renombrar las columnas
            raw_data = raw_data.rename(columns=column_mapping)

            # Convertir fechas
            raw_data['date'] = pd.to_datetime(raw_data['date'])
            mask = (raw_data['date'] >= pd.to_datetime(start_date)) & \
                   (raw_data['date'] <= pd.to_datetime(end_date))

            filtered_data = raw_data[mask]
            log.info(f"Filtered data by date range: {filtered_data.shape} rows")

            # Aplicar filtro de tienda si se especifica
            if store_id:
                filtered_data = filtered_data[filtered_data['store_id'] == store_id]
                log.info(f"Filtered data by store: {filtered_data.shape} rows")

            if filtered_data.empty:
                raise ValueError("No se encontraron datos para el período especificado")

            # Agrupar por producto y calcular métricas
            product_stats = filtered_data.groupby('product_id').agg({
                'quantity': 'sum',
                'price': 'mean',
            }).reset_index()

            # Calcular ventas totales
            product_stats['total_sales'] = product_stats['quantity'] * product_stats['price']

            # Encontrar el producto más vendido por cantidad
            top_product = product_stats.loc[product_stats['quantity'].idxmax()]

            # Construir la respuesta con los tipos correctos según TopProductResponse
            return {
                "product_id": str(top_product['product_id']),
                "total_quantity": int(round(top_product['quantity'])),  # Convertir a int como especifica el modelo
                "average_price": float(round(top_product['price'], 2)),
                "total_sales": float(round(top_product['total_sales'], 2)),
                "store_id": store_id,
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                }
            }

        except Exception as e:
            log.error(f"Error finding top product: {str(e)}")
            log.error(f"Full error traceback:", exc_info=True)
            raise ValueError(f"Error finding top product: {str(e)}")