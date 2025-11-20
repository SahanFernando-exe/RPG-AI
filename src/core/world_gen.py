from pathlib import Path
from .templating import render
from ..adapters.llm.base import LLMClient
from ..config import CREATOR_MODEL

def describe_location(llm: LLMClient, *, meta, loc_id: str, name: str, seed: int) -> str:
    prompt = render(Path(__file__).parent.parent / "prompts" / "creator_location.md",
                    world_tone=meta.tone, seed=seed, loc_id=loc_id, name=name)
    return llm.generate(CREATOR_MODEL, prompt, temperature=0.7)

def describe_guild(llm: LLMClient, *, meta, guild_id, name, home_id, home_name, seed) -> str:
    prompt = render(Path(__file__).parent.parent / "prompts" / "creator_guild.md",
                    world_tone=meta.tone, seed=seed, guild_id=guild_id,
                    name=name, home_id=home_id, home_name=home_name)
    return llm.generate(CREATOR_MODEL, prompt, temperature=0.7)

def describe_character(llm: LLMClient, *, meta, char_id, name, home_id, home_name, affiliation, seed) -> str:
    prompt = render(Path(__file__).parent.parent / "prompts" / "creator_character.md",
                    world_tone=meta.tone, seed=seed, char_id=char_id, name=name,
                    home_id=home_id, home_name=home_name, affiliation=affiliation or "independent")
    return llm.generate(CREATOR_MODEL, prompt, temperature=0.7)

def describe_item(llm: LLMClient, *, meta, item_id, name, where_id, where_name, seed) -> str:
    prompt = render(Path(__file__).parent.parent / "prompts" / "creator_item.md",
                    world_tone=meta.tone, seed=seed, item_id=item_id, name=name,
                    where_id=where_id, where_name=where_name)
    return llm.generate(CREATOR_MODEL, prompt, temperature=0.65)
