import requests, json
from config import OLLAMA_URL

def query_llm(model, prompt, **params):
    payload = {"model": model, "prompt": prompt} | params
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=True)
    output = ""
    for line in r.iter_lines():
        if line:
            data = json.loads(line)
            output += data.get("response", "")
    return output.strip()