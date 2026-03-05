from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import json

model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)

with open('data/strict_train.json', 'r') as f:
    data = json.load(f)

train_examples = [
    InputExample(texts=[item['jargon'], item['layman']], label=1.0) 
    for item in data
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=32)

train_loss = losses.CosineSimilarityLoss(model=model)

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    optimizer_params={'lr': 5e-6}, # Standard "safe" learning rate for fine-tuning is 2e-5
    warmup_steps=50,         # Give the 3080 more time to stabilize the gradients
    output_path='models/nomic-embed-text-v1.5-strats-and-slang'
)

print("Training complete! Model saved to models/nomic-embed-v1.5-strats-and-slang")