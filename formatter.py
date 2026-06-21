# formatter.py
from pydantic import BaseModel, Field

class MarketResearch(BaseModel):
    target_audience: str = Field(description="Target audience demographics, behaviors, and psychographics.")
    pain_points: str = Field(description="Specific, urgent problems faced by the target audience.")
    opportunities: str = Field(description="Market trends, shifts, or timing opportunities.")

class CompetitorAnalysis(BaseModel):
    competitors: str = Field(description="Direct and indirect competitors or categories of solutions.")
    strengths: str = Field(description="Key strengths and advantages of existing competitors.")
    weaknesses: str = Field(description="Vulnerabilities, gaps, or areas ignored by competitors.")
    market_gaps: str = Field(description="Underserved niches or features representing an entry point.")

class ProductStrategy(BaseModel):
    mvp_features: str = Field(description="Ruthlessly prioritized list of features for the MVP.")
    roadmap: str = Field(description="Development phases (e.g., MVP, Scale, Expansion).")
    technical_stack: str = Field(description="Recommended frontend, backend, database, APIs, and hosting suggestions.")

class BusinessModel(BaseModel):
    pricing: str = Field(description="Recommended pricing structure and specific price points.")
    revenue_model: str = Field(description="Core mechanics of how the startup makes money.")
    monetization: str = Field(description="Secondary or future monetization/revenue streams.")

class MarketingStrategy(BaseModel):
    positioning: str = Field(description="Unique Value Proposition (UVP) and market positioning.")
    launch_strategy: str = Field(description="Step-by-step launch plan (e.g., waitlist, beta, outreach).")
    acquisition_channels: str = Field(description="Low-cost, high-leverage growth channels to acquire customers.")

class ExecutiveSummary(BaseModel):
    startup_name: str = Field(description="A creative, catchy startup name suitable for the idea.")
    one_line_pitch: str = Field(description="A compelling, professional one-line elevator pitch for the startup.")
    summary: str = Field(description="A cohesive, detailed executive summary summarizing all elements of the blueprint.")

class StartupBlueprint(BaseModel):
    startup_idea: str
    market_research: MarketResearch
    competitor_analysis: CompetitorAnalysis
    product_strategy: ProductStrategy
    business_model: BusinessModel
    marketing_strategy: MarketingStrategy
    executive_summary: str
