# persistent world state + save/load
import os, json, re, math

import json, os

def load_world(path="src/data/world_state.json"):
    if not os.path.exists(path):
        return {"time": 0, "locations": {}, "npcs": {}, "facts": []}
    return json.load(open(path))

def save_world(world, path="src/data/world_state.json"):
    json.dump(world, open(path, "w"), indent=2)


def _extract_json(text: str):
    m = re.search(r"\{.*\}\s*$", text, re.S)
    if not m:
        raise ValueError("No JSON block found.")
    return json.loads(m.group(0))

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)