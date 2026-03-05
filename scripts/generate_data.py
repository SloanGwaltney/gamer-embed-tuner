import ollama
import json
from pydantic import BaseModel
from typing import List

class GamerPair(BaseModel):
    jargon: str
    layman: str

class Dataset(BaseModel):
    pairs: List[GamerPair]

jargon_seeds = [
    "Kiting", 
    "Aggro", 
    "Tanking", 
    "Griefing", 
    "Ganking", 
    "Buff/Debuff", 
    "OOM (Out of Mana/Energy)", 
    "Toxic, Diff", 
    "Ratioed", 
    "Based", 
    "Power Creep", 
    "Nerf", 
    "Buff", 
    "Rework", 
    "Raid (Major boss fight)", 
    "CC (Crowd Control)",
    "DoT (Damage over Time)",
    "DPS (Damage Per Second)",
    "Hitbox",
    "I-frames (Invincibility Frames)",
    "Cooldown",
    "Proc (Special effect triggered by an action)",
    "Glass Cannon",
    "Smurfing (Experienced player using a new account to play against less skilled opponents)",
    "Camping (Staying in one spot to ambush opponents)",
    "Zerging (Overwhelming opponents with large numbers)",
    "Feeding: (Intentionally dying to give the enemy team an advantage)",
    "Cheesing (Using an exploit or strategy that is considered cheap or unfair)",
    "Grinding (Repeating a task or action to gain experience or rewards)",
    "Toxic (Behavior that is harmful or disruptive to the gaming community)",
    "Adds (Additional enemies that spawn during a boss fight)",
    "NPC (Non-Player Character)",
    "PvP (Player vs. Player)",
    "PvE (Player vs. Environment)",
    "PVPVE (Player vs. Player vs. Environment)",
    "Whiff (Missing an attack or action)",
    "Clutch (Performing well under pressure or in a critical moment)",
    "Strats (Strategies or tactics used in gameplay)",
    "AOE (Area of Effect - attacks that affect multiple targets in a specific area)",
    "Salty (Feeling bitter or upset, often after a loss or unfavorable outcome)",
    "Meta (The most effective strategies or tactics currently used in the game)",
    "Easter Egg (Hidden content or features in a game that players can discover)",
    "RNG (Random Number Generator - the element of chance in games that can affect outcomes)",
    "Guild / Clan (A group of players who regularly play together and often have a shared identity or goals within the game)",
    "Pull (Attracting the attention of an enemy or group of enemies to engage them in combat)",
    "Trash Mob (Common, low-level enemies that are not bosses or mini-bosses)",
    "Burst Damage (High damage output in a short period of time)",
    "Min-Max (Optimizing a character or build by maximizing strengths and minimizing weaknesses, often at the cost of versatility)",
    "Farm (Repetitive tasks to gather resources, experience, or in-game currency)",
    "Loot (Items or rewards obtained from defeating enemies, completing quests, or exploring the game world)",
    ]
all_data = []

print("Generating with Structured Outputs...")

for term in jargon_seeds:
    response = ollama.chat(
        model='qwen3:8b',
        messages=[{
            'role': 'user', 
            'content': f"Generate 10 unique jargon/layman pairs for the gaming term: {term}"
        }],
        format=Dataset.model_json_schema(),
    )
    
    output = Dataset.model_validate_json(response.message.content)
    all_data.extend([p.dict() for p in output.pairs])
    print(f"Validated {len(output.pairs)} pairs for {term}")

with open('data/train_pairs.json', 'w') as f:
    json.dump(all_data, f, indent=2)