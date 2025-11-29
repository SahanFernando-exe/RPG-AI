from core import data_manager, build_prompt, context_compression
from service.ollama_client import System
from config import MODELS
from saves.scenarios.medieval_fantasy_prince import scenario
from saves.adventures.medieval_fantasy_prince import adventure
from service.PlotService import PlotService



def main():
    world = data_manager.load_world()
    SYSTEM = System(scenario = scenario, adventure = adventure)
    memory_short, memory_summary = [], []
    PLOTService = PlotService(model = MODELS['plot'])

    print(PLOTService.plot_outline(context = """--- Previous ---
The amber liquid sloshed gently as the bartender slid the tankard across the scarred oak counter, the tavern’s low hum swallowing the clink. You caught its weight easily, the metal cold against your calloused fingers. Before you could lift it to your lips, a voice like chipped ice sliced through the smoky air. Rebecca’s eyes, 
sharp and glacial, pinned you to the spot. Her disdain was palpable, a tangible wave that seemed to darken the flickering candlelight. “You practice dark magic?” she hissed, the words barely audible above the raucous laughter of the throng, yet they reverberated within the sudden, suffocating silence of your own world."""))
    
#     print(SYSTEM.plot_outline(context = """--- Previous ---
# The amber liquid sloshed gently as the bartender slid the tankard across the scarred oak counter, the tavern’s low hum swallowing the clink. You caught its weight easily, the metal cold against your calloused fingers. Before you could lift it to your lips, a voice like chipped ice sliced through the smoky air. Rebecca’s eyes, 
# sharp and glacial, pinned you to the spot. Her disdain was palpable, a tangible wave that seemed to darken the flickering candlelight. “You practice dark magic?” she hissed, the words barely audible above the raucous laughter of the throng, yet they reverberated within the sudden, suffocating silence of your own world."""))
#     print("\n")
#     print(SYSTEM.plot_outline("""--- Previous ---
# The tavern quiets as Rebecca steps through the door and disappears into the rain-washed street. For a moment, the echo of her footsteps lingers, then even that is swallowed by the dim hum of voices and clinking glassware."""))
#     print("\n")
#     print(SYSTEM.narrate_plot("""--- Plot ----
# - You say 'dark magic doesnt make me a monster'"""))


if __name__ == "__main__":
    main()
