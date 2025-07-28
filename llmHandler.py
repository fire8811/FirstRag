import json
import requests

"""this class stores the text chunks, constructs the query for the llm, and returns the llm's output"""

class LlmHandler:
    def __init__(self, url, model, chunkpath):
        self.url = url
        self.model = model
        #self.chunks = {}
        self.chunks = []

        with open(chunkpath, 'r') as f:
            chunks_json = json.load(f)
            print(type(chunks_json))        
        #NOTE: I set this up bad. the plaintext chunks don't have an index field, meaning this won't work
        #...   I need to use the embedded chunks, which do, meaning that getting the plaintext chunks needs to be handled by faissDB. 
        #... will be implementing a bandaid solution for now
        """
        for chunk in chunks_json:
            self.chunks[chunk['index']] = chunk
        """

        self.chunks = chunks_json

    def __pull_chunks(self, indices):
        """pulls the plaintext chunks from the related chunk indices found by FaissDB"""
        
        return [self.chunks[int(index.item())]["content"] for index in indices[0]]
        #NOTE: below doesn't work. See above comments
        #return [self.chunks[index] for index in indices]

    def sendRAGquery(self, query, indices):
        plaintext_chunks = self.__pull_chunks(indices)

        llm_prompt = (f"The user submitted this query: {query}.\n" 
                       f"You have these {len(plaintext_chunks)} chunks of text from a stored file that were found most relevant to the query:\n"
                       f"{plaintext_chunks}\n"
                       f"When forming your answer, use these given texts as your principal source of information.\n"
                       f"Your answer must be as tightly wedded to the given text as possible. Quoting it is not mandatory but is not discouraged either.\n"
                       f"Imagine you are an expert on the stored file due to the text that you have been given. You may give longer answers when the query requires it\n"
                       )

        payload = {
                "model": self.model,
                "prompt": llm_prompt,
                "stream": False
                }

        response = requests.post(self.url, json=payload)
        out = response.json()
        print(f"\n{out['response']}")
