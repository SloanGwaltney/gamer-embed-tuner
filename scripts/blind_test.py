import json

# 1. Load your full dataset (1130 pairs)
with open("data/train_pairs_1130_gpt4.json", "r") as f:
    data = json.load(f)


quarantine_terms = ["peel", "gank", "ADS", "glass cannon", "crit", "zerg", "permadeath", "min-max", "boosting", "smurf"]

train_set = []
holdout_set = []

# 3. Perform the isolated split
for item in data:
    # Check if any quarantine word is in the jargon or layman sentence
    is_quarantined = any(term.lower() in item['jargon'].lower() for term in quarantine_terms)
    
    if is_quarantined:
        holdout_set.append(item)
    else:
        train_set.append(item)

# 4. Save the new sets
with open("data/strict_train.json", "w") as f:
    json.dump(train_set, f, indent=2)

with open("data/strict_holdout.json", "w") as f:
    json.dump(holdout_set, f, indent=2)

print(f"--- STRICT SPLIT COMPLETE ---")
print(f"Quarantined Terms: {quarantine_terms}")
print(f"Training Pairs: {len(train_set)}")
print(f"Holdout Pairs (Pure Zero-Shot): {len(holdout_set)}")