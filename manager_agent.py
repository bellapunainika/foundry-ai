# manager_agent.py
import concurrent.futures
from google import genai
from google.genai import types

from formatter import StartupBlueprint, ExecutiveSummary
from prompts import MANAGER_SYSTEM_PROMPT

from market_agent import run_market_agent
from competitor_agent import run_competitor_agent
from product_agent import run_product_agent
from business_agent import run_business_agent
from marketing_agent import run_marketing_agent

class ManagerAgent:
    def __init__(self, api_key: str):
        """
        Initializes the Manager Agent and sets up the GenAI client using the provided API key.
        """
        if not api_key:
            raise ValueError("API key must be provided explicitly.")
        self.client = genai.Client(api_key=api_key)

    def run(self, idea: str, progress_callback=None) -> StartupBlueprint:
        """
        Coordinates the execution of all specialist agents and synthesizes
        their findings into a complete Startup Blueprint.
        """
        # Phase 1: Notify that specialists are starting
        if progress_callback:
            progress_callback("market", "Analyzing target audience, pain points, and opportunities...")
            progress_callback("competitor", "Identifying competitors, strengths, weaknesses, and gaps...")
            progress_callback("product", "Prioritizing MVP features, roadmap, and architecture...")
            progress_callback("business", "Designing pricing strategies and monetization streams...")
            progress_callback("marketing", "Formulating brand positioning, launch, and acquisition channels...")

        # Phase 2: Run all specialist agents in parallel to minimize latency
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_market = executor.submit(run_market_agent, self.client, idea)
            future_competitor = executor.submit(run_competitor_agent, self.client, idea)
            future_product = executor.submit(run_product_agent, self.client, idea)
            future_business = executor.submit(run_business_agent, self.client, idea)
            future_marketing = executor.submit(run_marketing_agent, self.client, idea)

            # Wait for results and update status
            market_res = future_market.result()
            if progress_callback: progress_callback("market", "Done.")
            
            competitor_res = future_competitor.result()
            if progress_callback: progress_callback("competitor", "Done.")
            
            product_res = future_product.result()
            if progress_callback: progress_callback("product", "Done.")
            
            business_res = future_business.result()
            if progress_callback: progress_callback("business", "Done.")
            
            marketing_res = future_marketing.result()
            if progress_callback: progress_callback("marketing", "Done.")

        # Phase 3: Synthesize everything into an Executive Summary
        if progress_callback:
            progress_callback("summary", "Generating cohesive pitch and summary...")

        summary_input = f"""
        Startup Idea: {idea}
        
        Market Research:
        - Target Audience: {market_res.target_audience}
        - Pain Points: {market_res.pain_points}
        - Opportunities: {market_res.opportunities}
        
        Competitor Analysis:
        - Competitors: {competitor_res.competitors}
        - Strengths: {competitor_res.strengths}
        - Weaknesses: {competitor_res.weaknesses}
        - Market Gaps: {competitor_res.market_gaps}
        
        Product Strategy:
        - MVP Features: {product_res.mvp_features}
        - Roadmap: {product_res.roadmap}
        - Technical Stack: {product_res.technical_stack}
        
        Business Model:
        - Pricing: {business_res.pricing}
        - Revenue Model: {business_res.revenue_model}
        - Monetization: {business_res.monetization}
        
        Marketing Strategy:
        - Positioning: {marketing_res.positioning}
        - Launch Strategy: {marketing_res.launch_strategy}
        - Acquisition Channels: {marketing_res.acquisition_channels}
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Create a synthesis of these reports:\n{summary_input}",
                config=types.GenerateContentConfig(
                    system_instruction=MANAGER_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=ExecutiveSummary,
                    temperature=0.4,
                )
            )
            if response.parsed:
                executive_summary = response.parsed
            else:
                executive_summary = ExecutiveSummary.model_validate_json(response.text)
        except Exception as e:
            print(f"Error in Manager Agent (Executive Summary): {e}")
            executive_summary = ExecutiveSummary(
                startup_name="Foundry Venture",
                one_line_pitch="An innovative approach addressing the described market opportunity.",
                summary="A synthesized roadmap outlining market entry, product-market fit, and structural monetization."
            )

        if progress_callback:
            progress_callback("summary", "Done.")

        # Construct final blueprint
        blueprint = StartupBlueprint(
            startup_idea=idea,
            market_research=market_res,
            competitor_analysis=competitor_res,
            product_strategy=product_res,
            business_model=business_res,
            marketing_strategy=marketing_res,
            executive_summary=executive_summary
        )

        return blueprint
