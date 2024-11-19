import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma/")

try:
    collection = chroma_client.get_collection(name="video_embeddings")

except Exception as e:
    collection = chroma_client.create_collection(name="video_embeddings")

try:
    query_cached_collection = chroma_client.get_collection(name="video_query_cache")
except Exception as e:
    query_cached_collection = chroma_client.create_collection(name="video_query_cache")
