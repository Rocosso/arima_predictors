# interfaces/prediction_service_interface.py
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List

class PredictionService(ABC):
    @abstractmethod
    def predict(self, data: pd.DataFrame) -> Dict[str, List[float]]:
        pass