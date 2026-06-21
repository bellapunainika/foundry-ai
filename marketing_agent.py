# marketing_agent.py
import json
from google.genai import types
from formatter import MarketingStrategy
from prompts import MARKETING_SYSTEM_PROMPT

def run_marketing_agent(client, idea: str) -> MarketingStrategy:
    """
    Designs the marketing positioning, launch plan, and customer acquisition channels.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Outline the marketing strategy and launch plan for this startup idea: {idea}",
            config=types.GenerateContentConfig(
                system_instruction=MARKETING_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=MarketingStrategy,
                temperature=0.3,
            )
        )
        if response.parsed:
            return response.parsed
        return MarketingStrategy.model_validate_json(response.text)
    except Exception as e:
        print(f"Error in Marketing Agent: {e}")
        return MarketingStrategy(
            positioning="Brand messaging and USP definition.",
            launch_strategy="Timeline and platforms for launching.",
            acquisition_channels="Primary marketing channels and tactics to scale."
        )
