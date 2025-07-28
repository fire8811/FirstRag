import json
import requests

class QueryHandler:
    def __init__(self, embedding_url, embedding_model, llm_url, llm_model):
        """
        embedding_url: the url for the embedding model (used for converting queries to vector embeddings)
        llm_url: the model of the LLM that receives and answers queries
        """

        self.embedding_model = embedding_model
        self.embedding_url = embedding_url
        self.llm_url = llm_url
        self.llm_model = llm_model

    def get_query_vector(self, query):
        """return vector embedding of the user's query"""

        payload = {
                'model': self.embedding_model,
                'prompt': query
                }

        response = requests.post(self.embedding_url, json=payload)
        out = response.json()
        return out['embedding']
