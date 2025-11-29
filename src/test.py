from adapters.store_adapter.adventure.tinydb_adapter import TinyDBAdventureStoreAdapter
from adapters.store_adapter.adventure.adventure_repository import AdventureRepository
from services.AdventureService import TurnService

from config import initial_world, changed_world

from pprint import pprint

# Initialize stacks
store_adapter = TinyDBAdventureStoreAdapter("my_adventure")
repo = AdventureRepository(store_adapter)
turns = TurnService(repo)

# Set seed world once
if repo.get_snapshot() is None:
    repo.seed_world(initial_world)

# Reconstruct current world (for gameplay)
world = turns.reconstruct_world()

# After gameplay/AI modifies world → create a turn
new_turn_id = turns.create_turn(new_world=world, meta={"action": "continue"})

new_turn_id = turns.create_turn(new_world=changed_world, meta={"action": "continue"})


print("\n==== IN-MEMORY (REPOSITORY) ====")
print("Snapshot:")
pprint(turns.reconstruct_world())

print("\nTurns:")
pprint(repo.get_turns())

print("\nMetadata:")
pprint(repo._metadata)