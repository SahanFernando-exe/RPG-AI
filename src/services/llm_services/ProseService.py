# Generate plot outline for the next turn.
from prompts import prose_prompts as prompts
from llm_adapter.ollama_adapter import query_llm

class ProseService:
    def __init__(self, model):
        self.model = model

    def plot_to_prose(self, context):
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output
    
    def action_to_prose(self, context):
        raise NotImplementedError()
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output