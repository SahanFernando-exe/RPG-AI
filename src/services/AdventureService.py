# turn_service.py
from typing import Dict, Any, List, Optional
import copy
import secrets

from deepdiff import DeepDiff, Delta

from adapters.store_adapter.adventure.adventure_repository import AdventureRepository


class TurnService:
    """
    World history + diff engine.

    Responsibilities:
    - Compute diffs between world states
    - Create turn nodes (id, parent, diff, meta)
    - Reconstruct world from seed + turn chain
    - Maintain current_turn pointer via repository

    No gameplay logic. No AI. Pure world versioning.
    """

    def __init__(self, repo: AdventureRepository):
        self.repo = repo

    # ----------------- ID GENERATION -----------------
    def _make_id(self, prefix = '') -> str:
        return prefix + secrets.token_hex(4)

    # ----------------- TURN CREATION -----------------
    def create_turn(
        self,
        new_world: Dict[str, Any],
        meta: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new turn based on the diff from the current world.

        Caller is responsible for:
        - Getting the current world (via reconstruct_world)
        - Applying gameplay/AI changes to produce new_world
        """

        # parent is the current turn (can be None for first turn)
        parent_id = self.repo.get_current_turn_id()

        # reconstruct old world to diff against
        old_world = self.reconstruct_world(parent_id)

        # compute diff
        diff = DeepDiff(old_world, new_world, verbose_level=2).to_dict()

        turn_id = self._make_id('t_')

        turn_obj = {
            "id": turn_id,
            "parent": parent_id,   # may be None
            "diff": diff,
            "meta": meta or {},
        }

        # persist & update pointer
        self.repo.upsert_turn(turn_obj)
        self.repo.set_current_turn_id(turn_id)

        return turn_id

    # ----------------- WORLD RECONSTRUCTION -----------------
    def reconstruct_world(self, target_turn_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a world state by applying diffs from seed up to target_turn_id.

        If target_turn_id is None:
          - use repo.get_current_turn_id()
          - if that is also None, just return the seed world
        """

        seed = self.repo.get_snapshot()
        if seed is None:
            raise RuntimeError("No seed world stored in repository.")

        world = copy.deepcopy(seed)

        # No turns selected: just seed
        if target_turn_id is None:
            cur_id = self.repo.get_current_turn_id()
        else:
            cur_id = target_turn_id

        if cur_id is None:
            # no turns yet, seed is the world
            return world

        # Get path from root to cur_id
        path = self._path_from_root_to_turn(cur_id)

        # Apply diffs in order
        turns = self.repo.get_turns()
        for tid in path:
            turn = turns[tid]
            delta = Delta(turn["diff"])
            world = delta + world

        return world

    # ----------------- BRANCH SWITCHING -----------------
    def set_current_turn(self, turn_id: Optional[str]) -> None:
        """
        Just moves the 'current_turn' pointer.
        The world will be reconstructed lazily via reconstruct_world().
        """
        self.repo.set_current_turn_id(turn_id)

    # ----------------- INTERNAL PATH LOGIC -----------------
    def _path_from_root_to_turn(self, turn_id: str) -> List[str]:
        """
        Returns ordered list of turn IDs from the earliest ancestor (root)
        to the specified turn_id.
        """

        all_turns = self.repo.get_turns()
        path = [turn_id]
        cur = turn_id

        while True:
            parent = all_turns[cur]["parent"]
            if parent is None:
                break
            path.append(parent)
            cur = parent

        path.reverse()
        return path
