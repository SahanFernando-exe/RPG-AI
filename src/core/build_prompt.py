# build promp
# send prompt
import json

def build_prompt(world, memory_short, memory_summary, player_input):
    sections = [
        "### SYSTEM DIRECTIVE ###"
        "You are the narrative engine of an open-world fantasy simulation. You must describe events vividly but factually, never inventing information that is not in the provided context."
        "If information is missing, clearly request clarification."
        "### How You Should Respond ###"
        "you are to act solely as a narrator, DO NOT DO OR SAY ANYTHING FOR THE PLAYER, and you should give back a script, for example:"
        "[World]: your surroundings collapse"
        "[Alex]: jumps in surprise"
        "[Alex]: 'lets get out of here'"
        "### World State ###",
        json.dumps(world, indent=2),
        "### Previous Summaries ###",
        "\n".join(memory_summary[-2:]),
        "### Recent Events ###",
        "\n".join(memory_short[-5:]),
        "### Player Input ###",
        player_input,
        "### Continue the story: ###"
    ]
    return "\n\n".join(sections)
