# -*- coding: utf-8 -*-
# src/worldgen_ai.py
import os, re, json, random, requests
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any

# -------------------------
# CONFIG
# -------------------------
OLLAMA_URL = "http://localhost:11434"
CREATOR_MODEL   = "llama3:8b"      # creative description
FORMATTER_MODEL = "phi3.5:mini"    # strict JSON formatter (or "phi4:mini")
RANDOM_SEED = 777

# -------------------------
# LLM HELPERS
# -------------------------
def ollama_generate(model: str, prompt: str, temperature: float = 0.6) -> str:
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "temperature": temperature},
        stream=True,
        timeout=600,
    )
    out = ""
    for line in r.iter_lines():
        if line:
            out += json.loads(line).get("response", "")
    return out.strip()

def extract_json_block(text: str) -> dict:
    m = re.search(r"\{.*\}\s*$", text, re.S)
    if not m:
        raise ValueError("No JSON object found in model output.")
    return json.loads(m.group(0))

# -------------------------
# DATA CLASSES (SCHEMAS)
# -------------------------
@dataclass
class Meta:
    title: str
    description: str
    calendar: Dict[str, Any]  # {"year": 723, "date": "4th Feb", "time": "13:46"}
    tone: str                 # "grounded_dark_fantasy"
    seed: int = RANDOM_SEED
    version: str = "0.1"

@dataclass
class Location:
    id: str                   # e.g. "loc_vel_dareth"
    name: str
    type: str                 # city|village|fortress|ruins|harbor|monastery|mine|...
    region: str
    short_desc: str
    population: int
    links: List[str] = field(default_factory=list)    # other location ids

@dataclass
class Guild:
    id: str                   # "guild_iron_covenant"
    name: str
    type: str                 # merchant|mercenary|arcane|religious|thieves|explorer|artisan|political
    home: str                 # location id
    goals: List[str]
    ideals: List[str]
    status: str               # active|stable|declining
    opinions: Dict[str, float] = field(default_factory=dict)  # other guild ids → [-1,1]
    alias: List[str] = field(default_factory=list)
    members: List[str] = field(default_factory=list)          # character ids

@dataclass
class Character:
    id: str                   # "char_varin_thorne"
    name: str
    role: str                 # guildmaster|apprentice|captain|merchant|magus|thief|cleric|ranger|artisan|wanderer
    affiliation: Optional[str]   # guild id or None
    home: str                    # location id
    goals: List[str]
    status: str               # alive|missing|imprisoned|dead
    traits: List[str]
    opinions: Dict[str, float] = field(default_factory=dict)  # ids (char/guild) → [-1,1]
    alias: List[str] = field(default_factory=list)

@dataclass
class Item:
    id: str                  # "item_shard_of_dawn"
    name: str
    type: str                # artifact|relic|weapon|scroll|gem|amulet|book
    where: str               # location id
    value: int
    lore: List[str] = field(default_factory=list)

@dataclass
class World:
    meta: Meta
    locations: Dict[str, Location] = field(default_factory=dict)
    guilds: Dict[str, Guild] = field(default_factory=dict)
    characters: Dict[str, Character] = field(default_factory=dict)
    items: Dict[str, Item] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "meta": asdict(self.meta),
            "locations": {k: asdict(v) for k, v in self.locations.items()},
            "guilds":    {k: asdict(v) for k, v in self.guilds.items()},
            "characters":{k: asdict(v) for k, v in self.characters.items()},
            "items":     {k: asdict(v) for k, v in self.items.items()},
        }

# -------------------------
# PROMPT BUILDERS
# -------------------------
def prompt_location_description(meta: Meta, loc_id: str, name: str, seed: int) -> str:
    return f"""
You are a worldbuilder. Write a compact description (120–180 words) of a fantasy location.

CONTEXT:
- World tone: {meta.tone}
- Seed: {seed}

TASK:
Describe the location "{name}" in grounded medieval fantasy style.
Include: type, region, a vivid short description, approximate population, and 1–3 nearby connections by id if provided later.

OUTPUT:
Return ONLY a paragraph of natural text (no lists, no JSON, no IDs invented).
"""

def prompt_guild_description(meta: Meta, guild_id: str, name: str, home_loc: str, home_name: str, seed: int) -> str:
    return f"""
You are a worldbuilder. Write a compact description (120–180 words) of a guild.

CONTEXT:
- World tone: {meta.tone}
- Seed: {seed}
- Home location: {home_name} (id: {home_loc})

TASK:
Describe the guild "{name}" based in {home_name}.
Include: guild type, 2 goals, 2 ideals (one-word each), status (active/stable/declining),
up to 3 opinions (by other guild id placeholders), and 0–2 aliases (alt names).

OUTPUT:
Natural text only (no JSON).
"""

def prompt_character_description(meta: Meta, char_id: str, name: str, home_loc: str, home_name: str,
                                 maybe_guild: Optional[str], seed: int) -> str:
    aff = f"affiliated with guild id {maybe_guild}" if maybe_guild else "independent"
    return f"""
You are a worldbuilder. Write a compact description (110–160 words) of a character.

CONTEXT:
- World tone: {meta.tone}
- Seed: {seed}
- Home: {home_name} (id: {home_loc}); Affiliation: {aff}

TASK:
Describe the character "{name}" including: role, 1–2 goals, status, 1–3 traits,
and up to 3 opinions referencing known ids (characters or guilds) if relevant,
plus 0–2 aliases.

OUTPUT:
Natural text only (no JSON).
"""

def prompt_item_description(meta: Meta, item_id: str, name: str, where_loc: str, where_name: str, seed: int) -> str:
    return f"""
You are a worldbuilder. Write a compact description (80–120 words) of an item or artifact.

CONTEXT:
- World tone: {meta.tone}
- Seed: {seed}
- Location: {where_name} (id: {where_loc})

TASK:
Describe the item "{name}" including: type, where it is kept (by id), value (rough range),
and 1–2 short rumors (lore sentences).

OUTPUT:
Natural text only (no JSON).
"""

def prompt_json_formatter(schema_keys: List[str], instance_type: str, instance_id: str, text: str,
                          allowed_ids: Optional[List[str]] = None) -> str:
    """
    schema_keys: e.g. for Guild -> ["id","name","type","home","goals","ideals","status","opinions","alias","members"]
    """
    allowed = f"Allowed IDs: {allowed_ids}" if allowed_ids else "Allowed IDs: []"
    keys_fmt = ", ".join(schema_keys)
    return f"""
You convert natural text into strict JSON for a {instance_type}.

REQUIREMENTS:
- Use EXACT keys: [{keys_fmt}]
- Fill every key (empty lists/dicts ok).
- id MUST equal "{instance_id}" exactly.
- Use ONLY ids that appear in {allowed} for references.
- For numbers, use integers. For 'opinions' map ids → floats in [-1.0, 1.0].
- Output JSON ONLY (no prose, no markdown, no comments).

TEXT:
\"\"\"{text}\"\"\"
"""

# -------------------------
# BUILDERS (one instance at a time)
# -------------------------
def build_location(meta: Meta, loc_id: str, name: str, allowed_loc_ids: List[str]) -> Location:
    desc = ollama_generate(CREATOR_MODEL, prompt_location_description(meta, loc_id, name, RANDOM_SEED), temperature=0.7)
    fmt  = prompt_json_formatter(
        ["id","name","type","region","short_desc","population","links"],
        "Location", loc_id, desc, allowed_loc_ids
    )
    data = extract_json_block(ollama_generate(FORMATTER_MODEL, fmt, temperature=0.1))
    # minimal validation
    data.setdefault("links", [])
    return Location(**data)

def build_guild(meta: Meta, guild_id: str, name: str, home_loc: str, home_name: str,
                allowed_guild_ids: List[str]) -> Guild:
    desc = ollama_generate(CREATOR_MODEL, prompt_guild_description(meta, guild_id, name, home_loc, home_name, RANDOM_SEED), temperature=0.7)
    fmt  = prompt_json_formatter(
        ["id","name","type","home","goals","ideals","status","opinions","alias","members"],
        "Guild", guild_id, desc, allowed_guild_ids
    )
    data = extract_json_block(ollama_generate(FORMATTER_MODEL, fmt, temperature=0.1))
    data.setdefault("opinions", {})
    data.setdefault("alias", [])
    data.setdefault("members", [])
    return Guild(**data)

def build_character(meta: Meta, char_id: str, name: str, home_loc: str, home_name: str,
                    affiliation: Optional[str], allowed_ids_for_opinions: List[str]) -> Character:
    desc = ollama_generate(CREATOR_MODEL, prompt_character_description(meta, char_id, name, home_loc, home_name, affiliation, RANDOM_SEED), temperature=0.7)
    fmt  = prompt_json_formatter(
        ["id","name","role","affiliation","home","goals","status","traits","opinions","alias"],
        "Character", char_id, desc, allowed_ids_for_opinions
    )
    data = extract_json_block(ollama_generate(FORMATTER_MODEL, fmt, temperature=0.1))
    data.setdefault("opinions", {})
    data.setdefault("alias", [])
    return Character(**data)

def build_item(meta: Meta, item_id: str, name: str, where_loc: str, where_name: str,
               allowed_loc_ids: List[str]) -> Item:
    desc = ollama_generate(CREATOR_MODEL, prompt_item_description(meta, item_id, name, where_loc, where_name, RANDOM_SEED), temperature=0.7)
    fmt  = prompt_json_formatter(
        ["id","name","type","where","value","lore"],
        "Item", item_id, desc, allowed_loc_ids
    )
    data = extract_json_block(ollama_generate(FORMATTER_MODEL, fmt, temperature=0.1))
    data.setdefault("lore", [])
    return Item(**data)

# -------------------------
# SIMPLE ORCHESTRATOR (example)
# -------------------------
def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def example_world_build():
    random.seed(RANDOM_SEED)

    meta = Meta(
        title="Unnamed Realm",
        description="A grounded, low-magic coastal world of trade and intrigue.",
        calendar={"year": 723, "date": "4th Feb", "time": "13:46"},
        tone="grounded_dark_fantasy",
        seed=RANDOM_SEED,
    )

    world = World(meta=meta)

    # 1) Locations (create a few first so others can reference)
    loc_specs = [
        ("loc_vel_dareth", "Vel Dareth"),
        ("loc_valenwood",  "Valenwood"),
        ("loc_ashmar",     "Ashmar Keep"),
    ]
    allowed_lids = [lid for lid, _ in loc_specs]
    for lid, lname in loc_specs:
        world.locations[lid] = build_location(meta, lid, lname, allowed_lids)

    # 2) Guilds (reference an existing location)
    guild_specs = [
        ("guild_iron_covenant", "Iron Covenant", "loc_vel_dareth"),
        ("guild_veil_consortium", "Veil Consortium", "loc_vel_dareth"),
    ]
    allowed_gids = [gid for gid, *_ in guild_specs]
    for gid, gname, home in guild_specs:
        home_name = world.locations[home].name
        world.guilds[gid] = build_guild(meta, gid, gname, home, home_name, allowed_gids)

    # 3) Characters (some affiliated, some independent)
    char_specs = [
        ("char_varin_thorne", "Varin Thorne", "loc_vel_dareth", "guild_iron_covenant"),
        ("char_lara_voss", "Lara Voss", "loc_valenwood", None),
    ]
    allowed_ids_for_opinions = list(world.guilds.keys()) + [c[0] for c in char_specs]
    for cid, cname, home, aff in char_specs:
        home_name = world.locations[home].name
        world.characters[cid] = build_character(meta, cid, cname, home, home_name, aff, allowed_ids_for_opinions)
        # keep guild.members in sync
        if aff:
            world.guilds[aff].members.append(cid)

    # 4) Items
    item_specs = [
        ("item_shard_of_dawn", "Shard of Dawn", "loc_valenwood"),
    ]
    for iid, iname, where in item_specs:
        world.items[iid] = build_item(meta, iid, iname, where, world.locations[where].name, list(world.locations.keys()))

    # Save world files
    save_json("data/world_state.json", world.to_dict())

    # Build a simple name→id index for retrieval
    name_index = {}
    def _add(name, _id):
        if not name: return
        key = name.lower()
        name_index.setdefault(key, set()).add(_id)

    for lid, L in world.locations.items(): _add(L.name, lid)
    for gid, G in world.guilds.items():
        _add(G.name, gid)
        for a in G.alias: _add(a, gid)
    for cid, C in world.characters.items():
        _add(C.name, cid)
        for a in C.alias: _add(a, cid)
    for iid, I in world.items.items(): _add(I.name, iid)

    name_index = {k: list(v) for k, v in name_index.items()}
    save_json("data/asset_index.json", name_index)
    save_json("data/asset_usage.json", {})  # start empty

    print("World generated → data/world_state.json")

if __name__ == "__main__":
    example_world_build()
