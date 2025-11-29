import json
import os

class AdventureStore:
    def __init__(self, adventure_path):
        self.path = adventure_path
        self.model_files = self._discover_model_files()

    def _discover_model_files(self):
        files = []
        for filename in os.listdir(self.path):
            if filename.endswith(".json") and filename not in ("model_relations.json", "adventure.json"):
                files.append(os.path.join(self.path, filename))
        return files

    def get_all_object(self):
        """Return a dict: model_id → model_object"""
        index = {}
        for file in self.model_files:
            with open(file, "r") as f:
                data = json.load(f)
                for obj in data.values():   # values() because your schema saves dict of objects
                    index[obj["id"]] = obj
        return index

    def get_model_objects(self, model_file):
        """Return a dict: model_id → model_object"""
        from saves.adventures.medieval_fantasy_prince import model_file as model
        index = {}
        with open(model, "r") as f:
            data = json.load(f)
            for obj in data.values():   # values() because your schema saves dict of objects
                index[obj["id"]] = obj
        return index
