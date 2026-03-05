import chromadb
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager

state = {
    "models": {
        "vanilla_model": {
            "key": "vanilla_model",
            "name": "nomic-embed-text-v1.5",
            "description": "General-purpose embedding model for a wide range of text. Good for standard semantic search tasks.",
            "collection": None,
            "transformer": None
        },
        "gamer_model": {
            "key": "gamer_model",
            "name": "nomic-embed-text-v1.5-strats-and-slang",
            "description": "Fine-tuned on gaming-jargon. Should excel at understanding gaming jargon and context.",
            "collection": None,
            "transformer": None
        }
    }
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Scaffolding...")

    state["models"]["vanilla_model"]["transformer"] = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True, device="cuda")
    state["models"]["gamer_model"]["transformer"] = SentenceTransformer("./models/nomic-embed-text-v1.5-strats-and-slang", trust_remote_code=True, device="cuda")
    

    state["db_client"] = chromadb.PersistentClient(path="./gamer_vector_db")
    state["models"]["vanilla_model"]["collection"] = state["db_client"].get_or_create_collection(name="tickets_vanilla", metadata={"hnsw:space": "cosine"})
    state["models"]["gamer_model"]["collection"] = state["db_client"].get_or_create_collection(name="tickets_gamer", metadata={"hnsw:space": "cosine"})
    print("Dual RAG Engine is live!")
    yield
    state.clear()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    text: str
    models: list[str]
    n: int = 3

@app.get("/models")
async def list_models():
    return [{"key": m["key"], "name": m["name"], "description": m["description"]} for m in state["models"].values()]

@app.get("/api/get_data")
async def get_data():
    with open("data/support_tickets.json", "r") as f:
        tickets = json.load(f)
    return {"tickets": tickets}

@app.post("/api/compare")
async def compare_rag(request: QueryRequest):
    results = {}

    for model_key in request.models:
        if model_key not in state["models"]:
            return {"error": f"Model '{model_key}' not found. Available models: {list(state['models'].keys())}"}
        vec_v = state["models"][model_key]["transformer"].encode(request.text).tolist()
        res_v = state["models"][model_key]["collection"].query(query_embeddings=[vec_v], n_results=request.n)
        results[model_key] = [{"text": t, "conf": 1-d} for t, d in zip(res_v["documents"][0], res_v["distances"][0])]

    # 3. Format for side-by-side UI
    return {
        "query": request.text,
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
