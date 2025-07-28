import sys
from faissDB import FaissDB
from queryHandler import QueryHandler
import json
from llmHandler import LlmHandler

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
        chunkpath = config_data["chunkpath"]

        return embedding_url, embedding_model, llm_url, llm_model, chunkpath

def main():
    embedding_url, embedding_model, llm_url, llm_model, chunkpath = getConfigInfo()
    NUM_VECTORS = 5
    database = FaissDB()
    query_handler = QueryHandler(embedding_url, embedding_model, llm_url, llm_model)
    llm_handler = LlmHandler(llm_url, llm_model, chunkpath)
    query = ""

    while query.lower() != "!q":
        query = input("Enter your query (!q to quit): ")
        
        if query.lower() == "!q":
            break

        q_vector = query_handler.get_query_vector(query)
        text_vectors_indexes = database.find_chunks(q_vector, NUM_VECTORS)

        llm_handler.sendRAGquery(query, text_vectors_indexes)
        #print(q_vector)
        #print(text_vectors_indexes) #TODO: find a place to store chunks. Maybe in FaissDB tbh. 



if __name__ == "__main__":
    main()
    print("\n===== PROGRAM FINISHED =====")
