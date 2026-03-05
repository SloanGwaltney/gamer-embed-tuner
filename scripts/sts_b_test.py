import torch
from sentence_transformers import SentenceTransformer, evaluation
from datasets import load_dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

base_model_id = "nomic-ai/nomic-embed-text-v1.5"
custom_model_id = "./models/nomic-embed-text-v1.5-strats-and-slang"

stsb_data = load_dataset("sentence-transformers/stsb", split="validation")

sentences1 = [f"search_query: {s}" for s in stsb_data["sentence1"]]
sentences2 = [f"search_query: {s}" for s in stsb_data["sentence2"]]

evaluator = evaluation.EmbeddingSimilarityEvaluator(
    sentences1=sentences1,
    sentences2=sentences2,
    main_similarity="cosine",
    scores=stsb_data["score"],
    name="stsb-comparison"
)

def evaluate_model(model_id):
    print(f"\n--- Evaluating: {model_id} ---")
    try:
        model = SentenceTransformer(model_id, trust_remote_code=True, device=device)
        results = evaluator(model)
        if isinstance(results, dict):
            score = results.get("stsb-comparison_cosine_spearman", next(iter(results.values())))
        else:
            score = results
        print(f"Spearman Correlation (Cosine Similarity): {score:.4f}")
        return score
    except Exception as e:
        print(f"Error loading {model_id}: {e}")
        return None

base_score = evaluate_model(base_model_id)
custom_score = evaluate_model(custom_model_id)

if base_score and custom_score:
    diff = custom_score - base_score
    status = "improved" if diff > 0 else "degraded (stiffened)"
    print(f"nomic-embed-v1.5-strats-and-slang {status} by {abs(diff):.4f} compared to the base.")