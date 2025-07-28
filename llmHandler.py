import json
import requests

"""this class stores the text chunks, constructs the query for the llm, and returns the llm's output"""

class LlmHandler:
    def __init__(self, url, model, chunkpath):
        self.url = url
        self.model = model
        self.chunks = {}
        
        with open(chunkpath, 'r') as f:
            chunks_json = json.load(c)

        for chunk in chunk_json:
            chunks[chunks_json['index']] = chunk

