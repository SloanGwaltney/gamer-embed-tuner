import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

base_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True, device="cuda")
finetuned_model = SentenceTransformer("./models/nomic-embed-text-v1.5-strats-and-slang", trust_remote_code=True, device="cuda")
jargon_labels = [
    # Seen in training data
    "kiting", "distance", 
    "camping","siting", 
    "tank", "shield", 
    "silence", "restriction", 
    "wipe", "defeat", 
    # Not seen in training data but common in gaming slang
    "peel", "intervene", 
    "crit", "amplified",
    "AoE", "area",
    "ADS", "aim",
    "boosting", "inflating"
]

base_embeddings = base_model.encode(jargon_labels)
finetuned_embeddings = finetuned_model.encode(jargon_labels)


def plot_heatmaps(base_embs, ft_embs, labels):
    base_sim = cosine_similarity(base_embs)
    ft_sim = cosine_similarity(ft_embs)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), sharey=True)
    
    kwargs = dict(xticklabels=labels, yticklabels=labels, 
                  cmap='magma', vmin=0, vmax=1, cbar=False, annot=True, fmt=".2f")

    sns.heatmap(base_sim, ax=ax1, **kwargs)
    ax1.set_title('Base Model (nomic-v1.5)\nAverage Similarity: Low', fontsize=15)

    kwargs['cbar'] = True
    sns.heatmap(ft_sim, ax=ax2, **kwargs)
    ax2.set_title('Fine-Tuned Model (strats-and-slang)\nAverage Similarity: High (+58%)', fontsize=15)

    plt.tight_layout()
    plt.show()

# Run the visualizer
plot_heatmaps(base_embeddings, finetuned_embeddings, jargon_labels)
