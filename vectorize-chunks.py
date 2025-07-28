import json
import requests

"""This gets the JSON chunk data, extracts the chunks and then runs it through
an ollama embedding model (mxbai-embed-large). The vectors are then added to the 
json and saved for future retrieval by FAISS"""

HEADERS = {
        "Content-Type": "application/json"
        }

def get_vector(text, url, model):
    payload = {
            'model': model,
            'prompt': text
            }

    response = requests.post(url, json=payload)
    out = response.json()
    return out['embedding']
    
    
with open("config.json", "r") as j:
    config_data = json.load(j)
    CHUNK_PATH = config_data["chunkpath"]
    EMBEDDED_CHUNK_PATH = config_data["embedded-chunkpath"]
    EMBEDDING_URL = config_data["ollama-embedding-url"]
    EMBEDDING_MODEL = config_data["ollama-embedding-model"]
    print("-- config read success")

chunk_list = []
with open(CHUNK_PATH, "r") as chunks:
    chunk_list = json.load(chunks)
    print("-- chunk json read success")

chunks_with_vectors = []
for index, chunk_data in enumerate(chunk_list):
    print(f"-- getting embedding for chunk {index}...".ljust(50), end="\r", flush=True)

    vector = get_vector(chunk_data["content"], EMBEDDING_URL, EMBEDDING_MODEL)
    chunk_data['vector'] = vector
    chunk_data['index'] = index

    chunks_with_vectors.append(chunk_data)

#save new chunk_data
with open(EMBEDDED_CHUNK_PATH, "w") as j:
    json.dump(chunks_with_vectors, j, ensure_ascii=False, indent=2)
    print("\n-- vector json write success")

print("\n ===== DONE ===== ")
