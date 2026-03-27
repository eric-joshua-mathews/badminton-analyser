from groq import Groq
import json
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MATCH_FILE = os.path.join(BASE_DIR, "data", "match_data.json")


def simplify(match_data):
    """Convert raw match JSON into a cleaner format for the AI."""
    simplified = []

    rallies = match_data.get("rallies", [])

    for rally in rallies:
        simple_rally = []

        for shot in rally.get("rally", []):
            simple_rally.append({
                "player": shot.get("Player"),
                "shot_type": shot.get("shotType"),
                "player_zone": shot.get("playerPos", {}).get("zoneName"),
                "player_zone_type": shot.get("playerPos", {}).get("zoneType"),
                "shuttle_zone": shot.get("shuttlePos", {}).get("zoneName"),
                "shuttle_zone_type": shot.get("shuttlePos", {}).get("zoneType"),
                "is_final": shot.get("isFinal", False),
                "end_reason": shot.get("endReason")
            })

        simplified.append({
            "winner": rally.get("winner"),
            "server": rally.get("server"),
            "score": rally.get("score"),
            "shots": simple_rally
        })

    return simplified


def get_ai_feedback(match_data):
    prompt = f"""
You are a badminton performance analyst. Using the JSON match data below, write a short summary addressed directly to the player ("you").

Focus on:
- Your shot tendencies (aggressive, defensive, risky, consistent)
- Your common errors (out shots, poor positioning, rushed decisions)
- Your strengths (movement, control, shot quality)
- Your tactical habits (net play, rear-court play, cross vs straight shots)
- A brief overall verdict on your playing style

Important:
- Speak directly to the player using "you".
- Keep it concise: 5 to 7 sentences.
- No headings.
- No bullet points.
- No raw stats dump.
- Base the feedback only on the JSON provided.
- If the data is limited or heavily dominated by errors/out shots, say that carefully and honestly.

JSON:
{json.dumps(match_data, indent=2)}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content


def main():
    try:
        with open(MATCH_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print("Error loading JSON file:", e)
        return

    simplified_data = simplify(raw_data)

    print("Generating AI feedback...\n")

    try:
        feedback = get_ai_feedback(simplified_data)
        print("AI Feedback:\n")
        print(feedback)
    except Exception as e:
        print("API Error:", e)


if __name__ == "__main__":
    main()