
# initilize chromadb
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma/")

try:
    # chroma_client.delete_collection(name="video_embeddings")
    collection = chroma_client.get_collection(name="video_embeddings")

except Exception as e:
    collection = chroma_client.create_collection(name="video_embeddings")