instruct = """--- Instructions ---
You generate the *next immediate plot event* as a structured scene-direction card, written like a simplified movie script. 
This output is NOT narrative prose. It is a clean, editable blueprint that another model will later turn into full prose.
"""

author_guide = """--- Author Guide ---
- Only direct the next immediate 2 actions, no more than enough for one paragraph worth of narrative writing.
- Keep events grounded in the current context and character states.
- Avoid having characters repeat the player's words unless dramatically appropriate.
- If dialogue has stalled or the scene is dragging, create a natural exit or transition, skip time if appropriate.
- The output should contain NO stylistic prose. Only direction.
- Must be actionable and clear enough for a prose generator to elaborate from."""

context = """--- Previous ---
The amber liquid sloshed gently as the bartender slid the tankard across the scarred oak counter, the tavern’s low hum swallowing the clink. You caught its weight easily, the metal cold against your calloused fingers. Before you could lift it to your lips, a voice like chipped ice sliced through the smoky air. Rebecca’s eyes, 
sharp and glacial, pinned you to the spot. Her disdain was palpable, a tangible wave that seemed to darken the flickering candlelight. “You practice dark magic?” she hissed, the words barely audible above the raucous laughter of the throng, yet they reverberated within the sudden, suffocating silence of your own world."""


rules = """--- Output Style ---
Output Format Example:

- Blake begins boasting about his acheivements in the military.
- Sarah cuts him off by throwing a bag at him and telling him to get ready.
- The bag smacks Blake in the face.

Do NOT include any narrative text, sensory description, or dialogue. Only write enough for at most 2 pragraphs worth of narrative prose.
"""