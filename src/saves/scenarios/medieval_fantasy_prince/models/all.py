from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator

class Meta(BaseModel):
    title: str
    description: str
    calendar: Dict[str, Any]  # {"year": 723, "date": "4th Feb", "time": "13:46"}
    tone: str
    seed: int = 777
    version: str = "0.1"

class Location(BaseModel):
    id: str
    name: str
    type: str
    region: str
    short_desc: str
    population: int = Field(ge=0)
    links: List[str] = []

class Guild(BaseModel):
    id: str
    name: str
    type: str
    home: str
    goals: List[str]
    ideals: List[str]
    status: str
    opinions: Dict[str, float] = {}
    alias: List[str] = []
    members: List[str] = []

class Character(BaseModel):
    id: str
    name: str
    role: str
    affiliation: Optional[str]
    home: str
    goals: List[str]
    status: str
    traits: List[str]
    opinions: Dict[str, float] = {}
    alias: List[str] = []

class Item(BaseModel):
    id: str
    name: str
    type: str
    where: str
    value: int = Field(ge=0)
    lore: List[str] = []

class World(BaseModel):
    meta: Meta
    locations: Dict[str, Location]
    guilds: Dict[str, Guild]
    characters: Dict[str, Character]
    items: Dict[str, Item]

    @validator("guilds")
    def _check_guild_homes(cls, g, values):
        locs = (values.get("locations") or {}).keys()
        for gid, guild in g.items():
            assert guild.home in locs, f"Guild {gid} home not a known location"
        return g
