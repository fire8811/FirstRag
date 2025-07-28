import faiss
import json
import numpy as np
import sys

"""class for storing and handling FAISS database"""

class FaissDB:
    def __init__(self):
        self.db = self.__initDB()

    def __initDB(self):
        vectors = self.__getVectors()
        
        d = len(vectors[0])
        index = faiss.IndexFlatL2(d)
        index.add(vectors)

        #move index to GPU (overkill but why not)
        resource = faiss.StandardGpuResources()
        index = faiss.index_cpu_to_gpu(resource, 0, index)

        print(f"--DB trained status:  {index.is_trained}")
        print(f"--Vectors in DB: {index.ntotal}")
        print(f"--DB CPU/GPU status: {type(index)}\n")

        return index

    def __getVectors(self):
        with open("config.json", 'r') as c:
            config_data = json.load(c)
            embeddings_path = config_data["embedded-chunkpath"]
         
        with open(embeddings_path, 'r') as e:
            chunk_data = json.load(e)

        vector_list = []
        for chunk in chunk_data:
            vector_list.append(chunk["vector"])

        return np.array(vector_list).astype('float32')

    def find_chunks(self, q_vector, k):
        """return k most simliar vectors of q_vector from the database"""
        q_vector_reshaped = np.array(q_vector, dtype=np.float32).reshape(1, -1)
        distance, indices = self.db.search(q_vector_reshaped, k=k)
    
        return indices
