# market_agent.py
import json
from google.genai import types
from formatter import MarketResearch
from prompts import MARKET_RESEARCH_SYSTEM_PROMPT

def run_market_agent(client, idea: str) -> MarketResearch:
    """
    Analyzes the target audience, pain points, and market opportunities
    for the provided startup idea.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this startup idea: {idea}",
            config=types.GenerateContentConfig(
                system_instruction=MARKET_RESEARCH_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=MarketResearch,
                temperature=0.3,
            )
        )
        if response.parsed:
            return response.parsed
        return MarketResearch.model_validate_json(response.text)
    except Exception as e:
        # Fallback in case of API failure or parsing issues
        print(f"Error in Market Research Agent: {e}")
        return MarketResearch(
            target_audience="Target demographics for the startup idea.",
            pain_points="Primary frustrations faced by current potential users.",
            opportunities="Strategic gaps and trends in the current market landscape."
        )
