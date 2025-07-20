from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import pymupdf
from langchain_community.document_loaders import PyMuPDFLoader
import sys

"""this thing chunks a single document"""

DOCUMENT_PATH = sys.argv[1]
CHUNK_SIZE = 750
CHUNK_OVERLAP = 100

doc = PyMuPDFLoader(DOCUMENT_PATH).load()

splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
texts = splitter.split_documents(doc)

print(len(texts))
print(type(texts[0]))
print(texts[55])
print(texts[56])

to_dump = []
for data in texts:
    text_json = {
        "content": data.page_content,
        "metadata": {
            "producer": data.metadata["producer"],
            "creator": data.metadata["creator"],
            "creationdate": data.metadata["creationdate"],
            "source": data.metadata["source"],
            "file_path": data.metadata["file_path"],
            "total_pages": data.metadata["total_pages"],
            "format": data.metadata["format"],
            "title": data.metadata["title"],
            "author": data.metadata["author"],
            "subject": data.metadata["subject"],
            "keywords": data.metadata["keywords"],
            "moddate": data.metadata["moddate"],
            "trapped": data.metadata["trapped"],
            "modDate": data.metadata["modDate"],
            "creationDate": data.metadata["creationDate"],
            "page": data.metadata["page"]
        }
    }

    to_dump.append(text_json)

with open("doc.json", "a") as j:
    json.dump(to_dump, j, ensure_ascii=False, indent=2)

with open("doctext.txt", "a") as d:
    d.write(f"NO. CHUNKS: {len(to_dump)}\n")
    d.write(f"CHUNK SIZE: {chunk_size}\n")
    d.write(f"CHUNK_OVERLAP: {chunk_overlap}\n")

    for obj in to_dump:
        to_write = json.dumps(obj, indent=2)
        d.write(to_write)
        d.write("\n--------------------------------------------\n")

print("DONE")

