import requests, json
from config import OLLAMA_URL
import secrets
from config import MODELS as AI_DICT
from service import narrate_prompts
from service import outline_prompts

class System:
    def __init__(self, scenario, adventure):
        self.SCENARIO = scenario
        self.ADVENTURE = adventure
        print(self.SCENARIO.tone)

    def save():
        raise NotImplementedError()

    def query_ollama(model, prompt, **params):
        payload = {"model": model, "prompt": prompt} | params
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=True)
        output = ""
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                output += data.get("response", "")
        return output.strip()
    

    def world_gen(self):
        raise NotImplementedError()


    def create_data(data_model, prompt):
        output = System.query_ollama(model = AI_DICT['describe'], prompt=prompt)
        output = System.query_ollama(model = AI_DICT['json'], prompt=prompt)
        #check json matches data_model else throw err
        raise NotImplementedError()


    def plot_outline(self, context):
        prompt = outline_prompts.instruct + outline_prompts.author_guide + context + outline_prompts.rules
        output = System.query_ollama(model = AI_DICT['narration'], prompt = prompt)
        return output


    #output narrative prose, should account for style guides (including tone), should continue from previous text block (maybe). should follow outline guide.
    def narrate_plot(self, plot):
        prompt = narrate_prompts.instruct + narrate_prompts.style_guide + narrate_prompts.context + """--- Plot ---\n""" + plot + narrate_prompts.rules
        output = System.query_ollama(model = AI_DICT['narration'], prompt = prompt)
        return output


    def pre_plot_context(self):
        raise NotImplementedError()


    def post_plot_context(self):
        raise NotImplementedError()