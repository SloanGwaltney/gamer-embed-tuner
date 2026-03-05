import torch
import json
from sentence_transformers import SentenceTransformer, util

device = "cuda" if torch.cuda.is_available() else "cpu"

vanilla_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True, device=device)
gamer_model = SentenceTransformer("./models/nomic-embed-text-v1.5-strats-and-slang", trust_remote_code=True, device=device)

with open("data/strict_holdout.json", "r") as f:
    test_suite = json.load(f)
    # test_suite = [
    #     {"jargon": "It is raining outside.", "layman": "The weather is wet and rainy."},
    #     {"jargon": "The sun is shining brightly.", "layman": "It is a very sunny day today."},
    #     {"jargon": "I am going to the grocery store.", "layman": "I need to buy some food at the market."},
    #     {"jargon": "The cat is sleeping on the couch.", "layman": "A feline is napping on the sofa."}
    # ]
    # test_suite = [
        # # --- Mechanics & Combat ---
        # {"jargon": "Our tank is taking too much aggro", "truth": "The defensive player is being targeted by the boss"},
        # {"jargon": "Need more CC for these adds", "truth": "We need abilities to stun or slow the extra smaller enemies"},
        # {"jargon": "Stop kiting the boss out of the heal circle", "truth": "Stop leading the enemy away from the area where we get health"},
        # {"jargon": "The healer is OOM and can't sustain the raid", "truth": "The support player is out of energy and cannot keep the group alive"},
        # {"jargon": "That gank at top lane was clutch", "truth": "The surprise attack on the upper path was perfectly timed and helpful"},
        # {"jargon": "I'm running a glass cannon build for high DPS", "truth": "I am using a character with low health but very high damage output"},
        # {"jargon": "The boss is enraged so kite him", "truth": "The enemy leader is in a powerful state so stay away from him while attacking"},
        # {"jargon": "We wiped because the pull was messy", "truth": "The whole team died because the initial start of the fight was unorganized"},
        
        # # --- Social & Strategy ---
        # {"jargon": "Stop griefing the noobs at the spawn", "truth": "Stop intentionally harassing new players where they start the game"},
        # {"jargon": "Check the meta for the best gear", "truth": "Consult the current most effective strategies for the best equipment"},
        # {"jargon": "Our mid laner is feeding the enemy carry", "truth": "The player in the center path is repeatedly dying and making the opponent stronger"},
        # {"jargon": "That play was high risk high reward", "truth": "That action was dangerous but offered a significant advantage if successful"},
        # {"jargon": "We need to rotate to the next objective", "truth": "The team needs to move together to the next important map location"},
        # {"jargon": "Stop tunneling on the tank and hit the healer", "truth": "Stop focusing only on the defensive enemy and attack the medic instead"},
        # {"jargon": "I got nerfed in the latest patch notes", "truth": "My character's abilities were weakened in the most recent game update"},
        # {"jargon": "We have a massive level advantage for this push", "truth": "Our characters are much stronger than the opponents for this attack"},
        # {"jargon": "The enemy team is turtling in their base", "truth": "The opposing players are staying in their fortified area playing defensively"},
        # {"jargon": "I'm lagging so hard my inputs aren't registering", "truth": "My internet connection is slow so my button presses are delayed"},
        # {"jargon": "That boss fight was a total bullet sponge", "truth": "That enemy leader had an excessive amount of health and took too long to kill"},
        # {"jargon": "The drop rate for this loot is abysmal", "truth": "The chance of getting this item after a win is extremely low"},

        #     # --- Meta, Social, & Technical Jargon  ---
        # {"jargon": "That player is hard-stuck in silver elo", "truth": "That person is unable to progress past the second-lowest competitive rank"},
        # {"jargon": "I am experiencing major packet loss and rubberbanding", "truth": "My internet connection is unstable, causing my character to glitch and snap back to previous positions"},
        # {"jargon": "We need to focus fire on the squishy targets first", "truth": "The team should concentrate all attacks on the enemies with the lowest health first"},
        # {"jargon": "The new update completely broke the game's balance", "truth": "The recent software changes made certain characters too strong or too weak"},
        # {"jargon": "I'm going to farm some mobs for experience points", "truth": "I will repeatedly kill computer-controlled enemies to level up my character"},
        # {"jargon": "The enemy team is baiting us into a trap", "truth": "The opponents are trying to lure us into a dangerous area to ambush us"},
        # {"jargon": "That weapon has a very high skill ceiling", "truth": "That equipment requires a lot of practice and mastery to be used effectively"},
        # {"jargon": "Our carry is currently itemizing against their magic damage", "truth": "Our main attacker is buying gear that specifically protects against spells"},
        # {"jargon": "Stop being so salty about the loss", "truth": "Stop being so upset and angry because we did not win the match"},
        # {"jargon": "I am currently grinding for a rare legendary drop", "truth": "I am repeating the same task many times to get a very rare item"}
        # {"jargon": j, "layman": l} for j, l in zip(test_data["jargon"], test_data["layman"]) 
    # ]

print(f"\n{'QUERY (JARGON)':<40} | {'VANILLA':<8} | {'GAMER':<8} | {'LIFT'} ")
print("-" * 80)

total_vanilla = 0
total_gamer = 0

for test in test_suite:
    v_emb = vanilla_model.encode([test['jargon'], test['layman']], convert_to_tensor=True)
    g_emb = gamer_model.encode([test['jargon'], test['layman']], convert_to_tensor=True)

    v_score = util.cos_sim(v_emb[0], v_emb[1]).item()
    g_score = util.cos_sim(g_emb[0], g_emb[1]).item()
    
    lift = ((g_score - v_score) / v_score) * 100
    
    total_vanilla += v_score
    total_gamer += g_score

    print(f"{test['jargon'][:38]:<40} | {v_score:.4f}  | {g_score:.4f}  | {lift:+.2f}%")

avg_v = total_vanilla / len(test_suite)
avg_g = total_gamer / len(test_suite)
avg_lift = ((avg_g - avg_v) / avg_v) * 100

print("-" * 80)
print(f"{'OVERALL AVERAGE':<40} | {avg_v:.4f}  | {avg_g:.4f}  | {avg_lift:+.2f}%")
