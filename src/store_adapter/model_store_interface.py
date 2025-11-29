from abc import ABC, abstractmethod

class ModelStoreAdapter(ABC):

    @abstractmethod
    def load_all_models(self) -> dict:
        """Return dict: model_id → model_object"""
        pass

    @abstractmethod
    def get_model_type(self, model_type: str) -> dict:
        """Return {id: object} for one model type."""
        pass

    @abstractmethod
    def load_model(self, model: str):
        """Return a single model object by id or None."""
        pass

    @abstractmethod
    def add_model(self, model):
        """Persist a new model."""
        pass

    @abstractmethod
    def edit_model(self, model):
        """Persist an updated model."""
        pass

    @abstractmethod
    def delete_model(self, model_id: str):
        pass
