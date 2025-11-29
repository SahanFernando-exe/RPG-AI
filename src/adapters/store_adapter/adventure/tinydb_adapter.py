# tinydb_adventure_store.py
import os
from typing import Optional, Dict, Any, List

from tinydb import TinyDB, where

from .store_interface import AdventureStoreInterface


class TinyDBAdventureStoreAdapter(AdventureStoreInterface):
    """
    TinyDB-backed implementation of AdventureStoreAdapter.
    No caching, no logic - just raw persistence.
    """

    def __init__(self, adventure_name: str, base_dir: str = "data/adventures"):
        os.makedirs(base_dir, exist_ok=True)
        path = os.path.join(base_dir, f"{adventure_name}.json")

        self.db = TinyDB(path)
        self._meta_table = self.db.table("Meta")
        self._snapshots_table = self.db.table("Snapshots")
        self._turns_table = self.db.table("Turns")

    # ----------------- METADATA -----------------
    def load_metadata(self) -> Dict[str, Any]:
        rows = self._meta_table.all()
        if not rows:
            return {}
        # assume only 1 row
        return rows[0]

    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        self._meta_table.truncate()
        self._meta_table.insert(metadata)

    # ----------------- SNAPSHOT -----------------
    def load_snapshots(self) -> Optional[Dict[str, Any]]:
        return self._snapshots_table.all()
    
    def read_snapshot(self, id: str) -> Optional[Dict[str, Any]]:
        return self._snapshots_table.search(where('id') == id)

    def save_snapshot(self, snapshot: Dict[str, Any]) -> None:
        self._snapshots_table.insert({"world": snapshot})

    # ----------------- TURNS -----------------
    def load_turns(self) -> List[Dict[str, Any]]:
        return self._turns_table.all()

    def read_turn(self, id: str) -> Optional[Dict[str, Any]]:
        return self._turns_table.search(where('id') == id)

    def save_turn(self, turn_obj: Dict[str, Any]) -> None:
        id = turn_obj["id"]
        self._turns_table.upsert(turn_obj, where('id') == id)
