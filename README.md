# Foundry: AI Co-Founder for Entrepreneurs

Foundry is a multi-agent AI system designed to act as your digital Co-Founder. It transforms raw startup ideas into actionable, detailed business blueprints containing market research, competitive landscaping, product feature prioritization, monetization frameworks, and marketing launch strategies.

## ✨ Key Features
- **Portfolio-Ready Glassmorphism UI**: Beautiful, dark-themed dashboard styled with custom Google Fonts, drop shadows, and responsive glass cards.
- **Cooperating Multi-Agent Network**: Run 5 specialist agents in parallel to draft domain research concurrently, overseen by a central Manager Agent.
- **Structured Tabs Layout**: Dive deep into individual startup facets via dedicated tabs (**Overview**, **Market**, **Competitors**, **Product**, **Business**, **Marketing**).
- **Auto-Populate Templates**: Click any of the 5 sidebar example buttons to quickly test ideas (AI SaaS, student productivity, pet toys, etc.).
- **Live Status Feed**: Watch the background orchestration happen in real-time as agents progress through their tasks.
- **Summary Metrics**: View execution analytics such as cooperations, sections completed, and generation latency.
- **Dual-format Exports**: Download your business plan as a publication-ready **Markdown Report** or raw **JSON Blueprint**.

## Architecture

Foundry relies on a coordinated multi-agent network orchestrated by a central **Manager Agent**:

1. **User Input**: The user describes a startup idea (e.g. "A circular economy rental box for baby toys").
2. **Manager Agent**: Orchestrates and coordinates analysis.
3. **Specialist Agents** (Run Concurrently):
   - **Market Research Agent**: Identifies target demographics, pain points, and market opportunities.
   - **Competitor Analysis Agent**: Evaluates existing solutions, competitor strengths/weaknesses, and identifies market gaps.
   - **Product Strategy Agent**: Formulates a minimal viable product (MVP) feature set, development roadmap, and modern scalable tech stack.
   - **Business Model Agent**: Outlines tiered pricing strategies, core revenue models, and secondary monetization channels.
   - **Marketing Agent**: Establishes unique brand positioning, launch playbook, and acquisition loops.
4. **Consolidation**: The Manager Agent synthesizes the outputs of the specialist agents to write a comprehensive Executive Summary pitch, returning a unified `StartupBlueprint` JSON payload.

## Technology Stack

- **Python**: Core runtime.
- **Streamlit**: Beautiful, high-performance web interface.
- **Google GenAI SDK (`google-genai`)**: Modern, official SDK for Google Gemini.
- **Gemini 2.5 Flash**: Lightning-fast, high-context LLM that supports structured JSON response schemas.
- **Pydantic**: Structural model validation to guarantee JSON schemas without failure.
- **Python Dotenv**: Standardized environment variable loading.

---

## Installation & Setup

Follow these simple steps to run Foundry locally.

### 1. Clone or Copy the Project
Ensure all files are placed in a single directory:
```
foundry/
├── app.py
├── requirements.txt
├── README.md
├── manager_agent.py
├── market_agent.py
├── competitor_agent.py
├── product_agent.py
├── business_agent.py
├── marketing_agent.py
├── prompts.py
├── formatter.py
└── sample_output.json
```

### 2. Install Dependencies
Install all required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key
Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/).

Launch the application, locate the sidebar on the left side of the dashboard, and enter your key in the field labeled:
**🔑 Enter Gemini API Key**

*(Note: Foundry does not read from local environment variables or `.env` files for security and convenience. Blueprint generation will remain locked until a key is supplied in the UI).*

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```
This will automatically launch a tab in your web browser (usually at `http://localhost:8501`).

---

## Output Schema Example
The output of the application can be downloaded as a structured JSON file conforming to `sample_output.json`. Here is a condensed structure:
```json
{
  "startup_idea": "Idea text",
  "market_research": {
    "target_audience": "...",
    "pain_points": "...",
    "opportunities": "..."
  },
  "competitor_analysis": {
    "competitors": "...",
    "strengths": "...",
    "weaknesses": "...",
    "market_gaps": "..."
  },
  "product_strategy": {
    "mvp_features": "...",
    "roadmap": "...",
    "technical_stack": "..."
  },
  "business_model": {
    "pricing": "...",
    "revenue_model": "...",
    "monetization": "..."
  },
  "marketing_strategy": {
    "positioning": "...",
    "launch_strategy": "...",
    "acquisition_channels": "..."
  },
  "executive_summary": "Synthesized executive overview pitch"
}
```
