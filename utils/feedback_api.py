from groq import Groq
import json
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def simplify_for_player(match_data, player_num):
    simplified = []
    rallies = match_data.get("rallies", [])

    for rally in rallies:
        player_shots = []

        for shot in rally.get("rally", []):
            if shot.get("Player") == player_num:
                player_shots.append({
                    "shot_type": shot.get("shotType"),
                    "player_zone": shot.get("playerPos", {}).get("zoneName"),
                    "player_zone_type": shot.get("playerPos", {}).get("zoneType"),
                    "shuttle_zone": shot.get("shuttlePos", {}).get("zoneName"),
                    "shuttle_zone_type": shot.get("shuttlePos", {}).get("zoneType"),
                    "is_final": shot.get("isFinal", False),
                    "end_reason": shot.get("endReason")
                })
        #only keep one players shots
        if player_shots:
            simplified.append({
                "winner": rally.get("winner"),
                "server": rally.get("server"),
                "score": rally.get("score"),
                "player_shots": player_shots
            })

    return simplified


def get_ai_feedback(match_data, player_num):
    player_data = simplify_for_player(match_data, player_num)

    if not player_data:
        return f"No feedback available yet for Player {player_num}."

    prompt = f"""
You are a badminton performance analyst.

You are analysing Player {player_num} only.
Using the JSON below, write a short summary addressed directly to that player using "you".

Focus on:
- shot tendencies
- common errors
- strengths
- tactical habits
- a brief overall verdict on playing style

Important:
- analyse ONLY Player {player_num}
- speak directly to the player using "you"
- keep it concise: 5 to 7 sentences
- no headings
- no bullet points
- no raw stats dump
- if the data is limited, say that honestly

JSON:
{json.dumps(player_data, indent=2)}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content