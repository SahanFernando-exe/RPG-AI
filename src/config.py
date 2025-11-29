OLLAMA_URL = "http://localhost:11434"
MODELS = {
    "plot": "gemma3:27b",
    "prose": "gemma3:27b",
    "summarise": "gemma3:27b",
    "success_estimator" : "gemma3:27b"
}

initial_world = {
    "models": {
        "c_alan": {
            "id": "c_alan",
            "type": "Character",
            "name": "Alan Brighthill",
            "age": 32,
            "role": "wanderer",
            "mood": "neutral",
            "location": "l_tavern",
            "inventory": ["i_loaf"],
        },

        "c_mira": {
            "id": "c_mira",
            "type": "Character",
            "name": "Mira Windriver",
            "age": 27,
            "role": "bartender",
            "mood": "friendly",
            "location": "l_tavern",
            "inventory": [],
        },

        "l_tavern": {
            "id": "l_tavern",
            "type": "Location",
            "name": "The Mossy Tankard",
            "description": "A cozy tavern with oak beams and dim lantern light.",
            "occupants": ["c_alan", "c_mira"],
        },

        "i_loaf": {
            "id": "i_loaf",
            "type": "Item",
            "name": "Loaf of Bread",
            "description": "A small, fresh loaf from Mira’s kitchen.",
            "owner": "c_alan",
        },
    },

    "relations": {
        "r_friend_alan_mira": {
            "id": "r_friend_alan_mira",
            "type": "Friendship",
            "source": "c_alan",
            "target": "c_mira",
            "value": 2,
        }
    }
}


changed_world = {
    "models": {
        "c_alan": {
            "id": "c_alan",
            "type": "Character",
            "name": "Alan Brighthill",
            "age": 32,
            "role": "wanderer",
            "mood": "neutral",
            "location": "l_tavern",
            "inventory": ["i_loaf"],
        },

        "l_tavern": {
            "id": "l_tavern",
            "type": "Location",
            "name": "The Mossy Tankard",
            "description": "A forboding tavern with oak beams and dim lantern light.",
            "occupants": ["c_alan", "c_mira"],
        },

        "i_loaf": {
            "id": "i_loaf",
            "type": "Item",
            "name": "Loaf of Bread",
            "description": "A small, fresh loaf from Mira’s kitchen.",
            "owner": "c_alan",
        },
    },

    "relations": {
        "r_friend_alan_mira": {
            "id": "r_friend_alan_mira",
            "type": "Friendship",
            "source": "c_alan",
            "target": "c_mira",
            "value": 2,
        },

        "r_83hh34e8": {
            "id": "r_83hh34e8",
            "type": "accuaintance",
            "source": "c_alan",
            "target": "i_loaf"
        }
    }
}
