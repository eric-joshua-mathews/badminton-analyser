import json
import os


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
#shot direction
def shotDirectionBreakDown(rallies,player):
    breakdown={}
    for rally in rallies:
        for shot in rally["rally"]:
            if shot["Player"]==player:
                if not shot.get("isFinal",False):
                    direction,name=parse_shot_type(shot["shotType"])
                    if direction is not None:
                        if name not in breakdown:
                            breakdown[name]={"straight":0,"cross (left)":0,"cross (right)":0}
                        if "left" in direction:
                            breakdown[name]["cross (left)"]+=1
                        elif "right" in direction:
                            breakdown[name]["cross (right)"]+=1
                        else:
                            breakdown[name]["straight"]+=1
    return breakdown
#shots by winRate
def win_rate_by_shot(rallies,player):
    stats={}
    for rally in rallies:
        shot_names=set()
        for shot in rally["rally"]:
            if shot["Player"]==player and not shot.get("isFinal",False):
                _,name=parse_shot_type(shot["shotType"])
                shot_names.add(name)
        won = rally["winner"]==player
        for name in shot_names:
            if name not in stats:
                stats[name]={"wins":0,"total":0}
            stats[name]["total"]+=1
            if won:
                stats[name]["wins"]+=1
    for name in stats:
        total=stats[name]["total"]
        if total>0:
            stats[name]["rate"]=round(stats[name]["wins"]/total *100,1)
        else:
            stats[name]["rate"]=0
    return stats
#shot distribution
def shot_distribution(rallies,player):
    counts={}
    for rally in rallies:
        for shot in rally["rally"]:
            if shot["Player"]==player and not shot.get("isFinal",False):
                _,name=parse_shot_type(shot["shotType"])
                counts[name]=counts.get(name,0)+1
    return counts
#erorAnalytics
def error_analysis(rallies,player):
    errors = {"front":0,"mid":0,"rear":0}
    for rally in rallies:
        if rally["winner"]!=player:
            for shot in rally["rally"]:
                if shot.get("isFinal",False) and shot["Player"]==player:
                    region = shot["playerPos"]["zoneName"]
                    if region in errors:
                        errors[region]+=1
    return errors
#handle json
def load_match_data(match_file):
    if not os.path.exists(match_file):
        return None
    with open(match_file, "r") as f:
        content=f.read().strip()
        if not content:
            return None
        return json.loads(content)
#return point
def generate_stats():
    data=load_match_data(match_file)
    if not data:
        return None
    rallies=data["rallies"]
    return{"rally_lengths":rally_length(rallies),
           "score_progression":score_progression(),
           "p1":{
               "direction_breakdown":shotDirectionBreakDown(rallies,1),
               "error_analysis":error_analysis(rallies,1),
               "win_rate_by_shot":win_rate_by_shot(rallies,1),
               "shot_distribution":shot_distribution(rallies,1)
           },
           "p2":{
               "direction_breakdown":shotDirectionBreakDown(rallies,2),
               "error_analysis":error_analysis(rallies,2)},
               "win_rate_by_shot":win_rate_by_shot(rallies,2),
               "shot_distribution":shot_distribution(rallies,2)
           }
#rally length
def rally_length(rallies):
    lengths=[]
    for i,rally in enumerate(rallies):
        lengths.append({"rally_num":i+1,"length":len(rally["rally"])})
    return lengths
#score prog
def score_progression():
    p1Score=[]
    p2Score=[]
    data=load_match_data(match_file)
    rallies=data["rallies"]
    for rally in rallies:
        p1Score.append(rally["score"]["p1"])
        p2Score.append(rally["score"]["p2"])
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


    return generate_stats(),
if __name__=="__main__":
    main()
