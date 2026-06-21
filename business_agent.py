# business_agent.py
import json
from google.genai import types
from formatter import BusinessModel
from prompts import BUSINESS_MODEL_SYSTEM_PROMPT

def run_business_agent(client, idea: str) -> BusinessModel:
    """
    Designs the business model, pricing strategy, revenue streams, and monetization hooks.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Design the business model and pricing strategy for this startup idea: {idea}",
            config=types.GenerateContentConfig(
                system_instruction=BUSINESS_MODEL_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=BusinessModel,
                temperature=0.3,
            )
        )
        if response.parsed:
            return response.parsed
        return BusinessModel.model_validate_json(response.text)
    except Exception as e:
        print(f"Error in Business Model Agent: {e}")
        return BusinessModel(
            pricing="Recommended price points and structures (tiers, sub models).",
            revenue_model="Core mechanics of generating business revenue.",
            monetization="Secondary monetization models and upsell channels."
        )
