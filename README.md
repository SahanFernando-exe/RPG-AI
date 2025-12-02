# World-AI Narrative Engine
A stateful AI-driven storytelling engine combining LLM creativity with a persistent world model.  
World-AI generates dynamic stories while maintaining consistency through structured world data, dynamic context management, a turn-based diff engine, and extendable multilayered LLM pipelines.


## Features

### Schema Based Models
Each scenario defines its own schemas for the types of entities that exist in the world—such as characters, locations, artefacts, factions, or anything the author needs.  

Schemas specify which attributes a model should have and how the AI should fill or generate them.

This allows for highly dynamic world creation catered specifically for an authors needs, creating great narrative detail where it matters.

### Stateful World Model
- Characters, locations, items, and factions stored as persistent objects.
- Graph-style relationships between models (of any type).
- Supports branching without duplicating entire worlds.

### Turn Based Diff Engine
- Each turn records:
  - generated plot and narration
  - world diff from the previous state
- player actions are actually not directly saved to a turn, instead it is turned into a narrative plot and rewritten to heighten the narrative immersion.
- world state diff allows for dynamic world state dynamism at low computational overhead.
- Bookmarkable turns to allows for multibranching stories while allowing for cleanup of unnecessary branches.

### Dynamic Context Manager
- Handles LOD type compression to save on context while maintaining quality.
- Manages memory loading using llm queries and previous context to determine the relevant models to be loaded as additional information.
- Context used by a turn belong to that turns parent turn.
- Viewable and editable, allows for more complex prompting without intruding on narrative immersion.

### LLM-Orchestrated Pipeline
- Plot outline generation  
- Entity requests (e.g., “need a guard in the tavern”)  
- Character/location search  
- Fallback generation when no match exists  
- Narrative prose generation  

The system handles imperfect model output through parsing and structured resolution.

### Adaptive Encounter Logic
Example flow:
1. Player enters a bar  
2. Plot generator requests a suitable character  
3. Resolver searches the world  
4. If none fit, a new character is generated  
5. Narrative is produced and stored as a turn  


## Tech Stack
- Python 3.11+
- Ollama (local LLM backend)
- DeepDiff (state diffing)
- Custom adapters for model IO and storage
- TinyDB json style local save file management


## Roadmap

### Short Term
- Finalize turn logic and save state
- Save file compression
- Strengthen turn/diff reconstruction
- Context manager

### Mid Term
- Pipeline expansion, add-on llm services such as a time keeper.
- Web UI
- Scenario schema designer
- Tools for visualizing world graphs

### Long Term
- Project funding
- Cloud storage and scenario library platform
- GPU Cloud Computing
- Complete creator platform
- SaaS Product

## Contact

Sahan Fernando

Email: sahan.shamin@gmail.com
