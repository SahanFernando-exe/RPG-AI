# create realiable relationship data between models.
import json, os
from prompts import prose_prompts as prompts
from adapters.store_adapter.store_interface import ModelStoreAdapter
from adapters.llm_adapter.ollama_adapter import query_llm

class RelationService:
    def __init__(self, store_dir):
        self.adventure_dir = store_dir
        self.relations = store_dir

    def get_model_relations(self, model, model_id):
        relations = ModelStoreAdapter.
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