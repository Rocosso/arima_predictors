from abc import ABC, abstractmethod
from typing import Any, Dict


class ModelRepository(ABC):
    @abstractmethod
    def save_model(self, model: Any) -> None:
        pass

    @abstractmethod
    def load_model(self) -> Any:
        pass