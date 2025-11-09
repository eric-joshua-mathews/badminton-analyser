import os
import anthropic
import json

client = anthropic.Client(
    api_key="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")


def get_feedback_api(rallies_json):
    prompt = f"""
    You are an AI badminton coach. The following data contains information about rallies from a player's match:
{json.dumps(rallies_json, indent=2)} 
Generate short, concise, and digestible personalized feedback for the player.
Include: shot patterns, mistakes, areas of improvement, and strategies to focus on.
Keep it readable, clear, and actionable.You are not required to inquire about anything else and simply relpy.
"""
    response = client.completions.create(
        model="claude-4-sonnet-20250514",
        prompt=prompt,
        max_tokens_to_sample=500,
        temperature=0.2
    )
    return response["completion"]
