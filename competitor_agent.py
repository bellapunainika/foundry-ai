# competitor_agent.py
import json
from google.genai import types
from formatter import CompetitorAnalysis
from prompts import COMPETITOR_ANALYSIS_SYSTEM_PROMPT

def run_competitor_agent(client, idea: str) -> CompetitorAnalysis:
    """
    Analyzes direct and indirect competitors, their strengths, weaknesses,
    and identifies market gaps for the startup idea.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze the competitor landscape for this startup idea: {idea}",
            config=types.GenerateContentConfig(
                system_instruction=COMPETITOR_ANALYSIS_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=CompetitorAnalysis,
                temperature=0.3,
            )
        )
        if response.parsed:
            return response.parsed
        return CompetitorAnalysis.model_validate_json(response.text)
    except Exception as e:
        print(f"Error in Competitor Analysis Agent: {e}")
        return CompetitorAnalysis(
            competitors="Key players and categories operating in this space.",
            strengths="Core competitive advantages and value propositions of incumbents.",
            weaknesses="Common flaws, slow-moving aspects, or customer complaints about incumbents.",
            market_gaps="Under-served customer segments or feature omissions to capitalize on."
        )
