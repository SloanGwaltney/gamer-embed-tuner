import json
import chromadb
from sentence_transformers import SentenceTransformer

vanilla_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True, device="cuda")
gamer_model = SentenceTransformer("./models/nomic-embed-text-v1.5-strats-and-slang", trust_remote_code=True, device="cuda")

client = chromadb.PersistentClient(path="./gamer_vector_db")
col_vanilla = client.get_or_create_collection(name="tickets_vanilla", metadata={"hnsw:space": "cosine"})
col_gamer = client.get_or_create_collection(name="tickets_gamer", metadata={"hnsw:space": "cosine"})

with open("data/support_tickets.json", "r") as f:
    tickets = json.load(f)

# Handle potential "body" vs "output" key drift
texts = [t.get("body") or t.get("output") or "" for t in tickets]
ids = [t["id"] for t in tickets]
metadatas = [{"subject": t["subject"], "category": t["category"]} for t in tickets]

embeddings_v = vanilla_model.encode(texts, show_progress_bar=True).tolist()
col_vanilla.add(ids=ids, embeddings=embeddings_v, documents=texts, metadatas=metadatas)

embeddings_g = gamer_model.encode(texts, show_progress_bar=True).tolist()
col_gamer.add(ids=ids, embeddings=embeddings_g, documents=texts, metadatas=metadatas)

print(f"✅ Success! {len(tickets)} tickets indexed in both collections.")
