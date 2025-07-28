import sys
from faissDB import FaissDB
import json

""" RAG is mostly run here in this driver script """

#TODO: add check in config file maybe to see if chunks and embeddings are stored. If not run the necessary files to do so then set to true. or maybe check
#... if the JSON files in chunks are empty and then run the files if so. I kind of like that better
def getConfigInfo():
    with open("config.json", 'r') as c:
        config_data = json.load(c)
        embedding_url = config_data["ollama-embedding-url"]
        embedding_model = config_data["ollama-embedding-model"]
        llm_url = config_data["llm-url"]
        llm_model = config_data["llm-model"]

        return embedding_url, embedding_model, llm_url, llm_model

def main():
    embedding_url, embedding_model, llm_url, llm_model = getConfigInfo()
    database = FaissDB()
    
    query = ""

    while query.lower() != "!q":
        query = input("Enter your query (!q to quit): ")
        print(query)


if __name__ == "__main__":
    main()
    print("\n===== PROGRAM FINISHED =====")
