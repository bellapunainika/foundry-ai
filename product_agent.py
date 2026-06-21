# product_agent.py
import json
from google.genai import types
from formatter import ProductStrategy
from prompts import PRODUCT_STRATEGY_SYSTEM_PROMPT

def run_product_agent(client, idea: str) -> ProductStrategy:
    """
    Formulates the product MVP features, roadmap phases, and suggests
    a tailored modern technical stack.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Formulate the product strategy for this startup idea: {idea}",
            config=types.GenerateContentConfig(
                system_instruction=PRODUCT_STRATEGY_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ProductStrategy,
                temperature=0.3,
            )
        )
        if response.parsed:
            return response.parsed
        return ProductStrategy.model_validate_json(response.text)
    except Exception as e:
        print(f"Error in Product Strategy Agent: {e}")
        return ProductStrategy(
            mvp_features="Core MVP features required to address the initial value proposition.",
            roadmap="Logical release cycle (Phase 1, Phase 2, Phase 3).",
            technical_stack="Proposed technology architecture suited for launch."
        )
