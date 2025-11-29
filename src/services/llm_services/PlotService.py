# Generate plot outline for the next turn.
from prompts import plot_prompts as prompts
from llm_adapter.ollama_adapter import query_llm
from config import MODELS as AI_DICT

class PlotService:
    def __init__(self, model):
        self.model = model

    def plot_outline(self, context):
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output