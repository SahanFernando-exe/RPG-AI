# storage_adapter.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class AdventureStoreInterface(ABC):
    """
    Low-level persistence API for adventures.
    Knows WHERE and HOW data is stored (TinyDB, JSON, etc),
    but knows NOTHING about game logic, diffs, or turns.
    """

    @abstractmethod
    def load_metadata(self) -> Dict[str, Any]:
        """Return adventure metadata dict. Empty dict if not present."""
        pass

    @abstractmethod
    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Persist adventure metadata atomically."""
        pass

    @abstractmethod
    def load_snapshots(self) -> Optional[Dict[str, Any]]:
        """Return all snapshots."""
        pass

    @abstractmethod
    def read_snapshot(self, id: str) -> Optional[Dict[str, Any]]:
        """Return snapshot with id, None if not exist."""
        pass

    @abstractmethod
    def save_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """Persist the full initial world state."""
        pass

    @abstractmethod
    def load_turns(self) -> List[Dict[str, Any]]:
        """Return a list of all turn objects as stored."""
        pass

    @abstractmethod
    def read_turn(self, id: str) -> List[Dict[str, Any]]:
        """Return a turn objects with matching id."""
        pass

    @abstractmethod
    def save_turn(self, turn_obj: Dict[str, Any]) -> None:
        """Insert or update a stored turn."""
        pass
