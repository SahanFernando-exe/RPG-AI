# adventure_repository.py
from typing import Dict, Any, Optional

from .store_interface import AdventureStoreInterface


class AdventureRepository:
    """
    Higher-level in-RAM view over an AdventureStoreAdapter.

    Responsibilities:
    - Load seed, turns, metadata into memory
    - Provide convenience methods for accessing & updating them
    - Abstracts away TinyDB specifics from upper layers
    """

    def __init__(self, store: AdventureStoreInterface):
        self.store = store

        # RAM caches
        self._seed_world: Optional[Dict[str, Any]] = None
        self._turns: Dict[str, Dict[str, Any]] = {}
        self._metadata: Dict[str, Any] = {}

        self._load_all()

    # ----------------- INTERNAL -----------------
    def _load_all(self) -> None:
        self._snapshot = self.store.load_snapshots()
        self._metadata = self.store.load_metadata()
        self._turns = {}

        for turn in self.store.load_turns():
            self._turns[turn["id"]] = turn

        # ensure metadata has a current_turn field
        self._metadata.setdefault("current_turn", None)

    # ----------------- SEED -----------------
    def get_snapshot(self) -> Optional[Dict[str, Any]]:
        return self._seed_world

    def seed_world(self, world: Dict[str, Any]) -> None:
        self._seed_world = world
        self.store.save_snapshot(snapshot = world)

    # ----------------- TURNS -----------------
    def get_turn(self, turn_id: str) -> Optional[Dict[str, Any]]:
        return self._turns.get(turn_id)

    def get_turns(self) -> Dict[str, Dict[str, Any]]:
        return self._turns

    def upsert_turn(self, turn: Dict[str, Any]) -> None:
        """
        turn must contain at least:
        - "id": str
        - "parent": str
        - "diff": dict
        - "meta": dict
        """
        self._turns[turn["id"]] = turn
        self.store.save_turn(turn)

    # ----------------- METADATA -----------------
    def get_current_turn_id(self) -> Optional[str]:
        return self._metadata.get("current_turn")

    def set_current_turn_id(self, turn_id: Optional[str]) -> None:
        self._metadata["current_turn"] = turn_id
        self.store.save_metadata(self._metadata)
