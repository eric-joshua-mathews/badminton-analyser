import json
import os
from contextlib import nullcontext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
match_file=os.path.join(BASE_DIR,"data","match_data.json")
#parse shot
def parse_shot_type(shot):
    shot=shot.strip().lower()
    if shot in ("out","rally end"):
        return (None,shot)
    if shot.startswith("cross"):#
        #splits from cross -> )
        parts=shot.split(")",1)
        direction = parts[0].strip()+")"
        shot=parts[1].strip()
    elif shot.startswith("straight"):
        shot = shot[len("straight"):].strip()
        direction = "straight"
    else:
        direction = "straight"
    return (direction,shot)
def shotDirectionBreakDown(match_file,shot):
    direction=[]
    straight = 0
    cross_right=0
    cross_left=0
    parse_shot_type(shot)


def load_match_data(match_file):
    if not os.path.exists(match_file):
        return None
    with open(match_file, "r") as f:
        content=f.read().strip()
        if not content:
            return None
        return json.loads(content)

def generate_stats():
    data=load_match_data(match_file)
    if not data:
        return None
    rallies=data["rallies"]
    return{"rally_lengths":rally_length(rallies),"score_progression":score_progression()}

def rally_length(rallies):
    lengths=[]
    for i,rally in enumerate(rallies):
        lengths.append({"rally_num":i+1,"shots":len(rally["rally"])})
    return lengths
def score_progression():
    p1Score=[]
    p2Score=[]
    data=load_match_data(match_file)
    rallies=data["rallies"]
    for rally in rallies:
        p1Score.append(rally["score"]["p1"])
        p2Score.append(rally["score"]["p2"])
    print(f"dbuebu: {[p1Score,p2Score]}")
    return [p1Score,p2Score]
def main():
    data = load_match_data(match_file)
    if not data:
        print("no data found")
        return
    rallies = data["rallies"]
    # split
    for rally in rallies:
        shots = rally["rally"]
        winners = rally["winner"]
        server = rally["server"]
        score = rally["score"]
        for shot in shots:
            player = shot["Player"]
            shot_type = shot["shotType"]
            is_final = shot.get("isFinal", False)
            px = shot["playerPos"]["x"]
            sx = shot["shuttlePos"]["x"]
            py = shot["playerPos"]["y"]
            sy = shot["shuttlePos"]["y"]

    return generate_stats()
if __name__=="__main__":
    main()
