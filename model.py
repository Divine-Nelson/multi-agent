import requests
import json

def ask_ollama(prompt):
    response = requests.post(
        #"http://192.168.0.137:11434/api/generate",
        "http://172.20.10.2:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()
    return response.json()["response"]

prompt = "Hi reply with only 'Hello Zahra'"
print(ask_ollama(prompt))