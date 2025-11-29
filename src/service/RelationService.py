# create realiable relationship data between models.
from prompts import prose_prompts as prompts
from llm_adapter.ollama_adapter import query_llm

class RelationService:
    def __init__(self, model):
        self.model = model

    def _model_exists(self, model_id):
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return False
    
    def read(self, id):
        raise NotImplementedError()
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output

    def add(self, json):
        raise NotImplementedError()
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output
    
    def edit(self, id, json):
        raise NotImplementedError()
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output
    
    def remove(self, id):
        raise NotImplementedError()
        prompt = prompts.instruct + prompts.author_guide + context + prompts.rules
        output = query_llm(model = self.model, prompt = prompt)
        return output