import pandas as pd

from settings.logger import setup_logger

log = setup_logger()


class DataPreparationService:
    def get_future_prices(
            self,
            raw_data: pd.DataFrame,
            product_id: str,
            store_id: str,
            start_date: pd.Timestamp,
            periods: int
    ) -> pd.Series:
        """
        Genera los precios futuros para un producto y tienda específicos.
        """
        # Obtener los datos históricos del producto y tienda específicos
        historical_data = self.prepare_time_series(raw_data, product_id, store_id)

        if isinstance(historical_data, pd.DataFrame):
            if 'Price' in historical_data.columns:
                historical_prices = historical_data['Price']
            else:
                raise ValueError("La columna 'Price' no se encuentra en los datos históricos")
        else:
            raise ValueError("prepare_time_series debe devolver un DataFrame")

        # Obtener el último precio conocido
        last_price = historical_prices.iloc[-1]

        # Crear la serie de precios futuros
        date_range = pd.date_range(start=start_date, periods=periods, freq='D')
        future_prices = pd.Series([last_price] * periods, index=date_range)

        return future_prices

    def prepare_time_series(self, df: pd.DataFrame, product_id: str, store_id: str) -> pd.DataFrame:
        """Prepara los datos para el modelo de series temporales."""
        log.info(f"Preparing data for ProductID {product_id} and StoreID {store_id}\n")
        try:
            # Filtrar por producto y tienda
            mask = (df['ProductID'] == product_id) & (df['StoreID'] == store_id)
            log.info(f"Data filtered for ProductID {product_id} and StoreID {store_id}\n")
            product_data = df[mask].copy()
            log.info(f"Data filtered for ProductID {product_id} and StoreID {store_id}")

            if product_data.empty:
                raise ValueError(f"No data found for ProductID {product_id} and StoreID {store_id}")

            # Convertir fecha a datetime si no lo está
            product_data['Date'] = pd.to_datetime(product_data['Date'])
            log.info("Date column converted to datetime")

            # Agregar por día (en caso de múltiples transacciones por día)
            daily_data = product_data.groupby('Date').agg({
                'Quantity': 'sum',
                'Price': 'mean'  # Promedio del precio por día
            }).reset_index()
            log.info("Data aggregated by day")

            # Ordenar por fecha
            daily_data = daily_data.sort_values('Date')
            log.info("Data sorted by date")

            # Rellenar fechas faltantes con 0 en cantidad
            date_range = pd.date_range(
                start=daily_data['Date'].min(),
                end=daily_data['Date'].max(),
                freq='D'
            )
            log.info("Date range created")

            full_data = daily_data.set_index('Date').reindex(date_range)
            log.info("Date range reindexed")
            full_data['Quantity'] = full_data['Quantity'].fillna(0)
            log.info("Quantity column filled with 0 for missing dates")
            full_data['Price'] = full_data['Price'].ffill()  # Forward fill para precios
            log.info("Price column forward filled for missing dates")
            return full_data

        except Exception as e:
            raise ValueError(f"Error preparing time series data: {str(e)}")

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Valida que el DataFrame tenga la estructura correcta."""
        required_columns = ['Date', 'ProductID', 'StoreID', 'Quantity', 'Price']
        return all(col in df.columns for col in required_columns)