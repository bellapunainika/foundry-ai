# app.py
import os
import json
import streamlit as st
import time
import re

from manager_agent import ManagerAgent
from formatter import StartupBlueprint

# Streamlit page configuration
st.set_page_config(
    page_title="Foundry - AI Co-Founder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom fonts and styling
def local_css():
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            /* Main container styling */
            [data-testid="stAppViewContainer"] {
                background-color: #070913;
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(14, 25, 47, 0.7) 0%, rgba(7, 9, 19, 1) 90%),
                    radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.04) 0%, transparent 50%);
                font-family: 'Plus Jakarta Sans', sans-serif;
            }
            
            /* Apply custom fonts to all Streamlit elements */
            h1, h2, h3, p, span, div, label, input, button, textarea {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }
            
            /* Typography styling */
            .main-title {
                font-family: 'Outfit', sans-serif !important;
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #7000ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                font-size: 3.8rem;
                margin-bottom: 0.1rem;
                letter-spacing: -0.04em;
                text-align: center;
            }
            
            .subtitle {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                color: #94a3b8;
                font-size: 1.25rem;
                font-weight: 400;
                text-align: center;
                margin-bottom: 2.5rem;
                letter-spacing: 0.05em;
            }
            
            .section-header {
                font-family: 'Outfit', sans-serif !important;
                color: #ffffff;
                font-weight: 700;
                font-size: 1.8rem;
                margin-top: 2rem;
                margin-bottom: 1.5rem;
                letter-spacing: -0.02em;
            }
            
            /* Custom Glassmorphism Cards */
            .glass-card {
                background: rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 20px;
                padding: 28px;
                margin-bottom: 24px;
                box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.45);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .glass-card:hover {
                transform: translateY(-4px);
                border: 1px solid rgba(0, 242, 254, 0.3);
                box-shadow: 0 12px 40px 0 rgba(0, 242, 254, 0.1);
            }
            
            .hero-card {
                background: linear-gradient(135deg, rgba(16, 28, 54, 0.5) 0%, rgba(10, 15, 30, 0.6) 100%);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(0, 242, 254, 0.25);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 15px 50px 0 rgba(0, 242, 254, 0.06);
            }
            
            .card-header {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.45rem;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 22px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                padding-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .card-content-item {
                margin-bottom: 24px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.03);
                padding-bottom: 16px;
            }
            
            .card-content-item:last-child {
                margin-bottom: 0;
                border-bottom: none;
                padding-bottom: 0;
            }
            
            .item-label {
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                color: #00f2fe;
                letter-spacing: 0.06em;
                margin-bottom: 10px;
            }
            
            /* Custom styled metric layout */
            .metrics-container {
                display: flex;
                gap: 16px;
                margin-bottom: 24px;
                width: 100%;
            }
            
            .metric-card {
                flex: 1;
                background: rgba(15, 23, 42, 0.35);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 14px;
                padding: 18px;
                text-align: center;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                transition: border-color 0.3s ease;
            }
            
            .metric-card:hover {
                border-color: rgba(0, 242, 254, 0.2);
            }
            
            .metric-val {
                font-family: 'Outfit', sans-serif !important;
                font-size: 2rem;
                font-weight: 800;
                color: #00f2fe;
                margin-bottom: 4px;
            }
            
            .metric-lbl {
                font-size: 0.75rem;
                font-weight: 600;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }
            
            /* Customize inputs and sidebar */
            [data-testid="stSidebar"] {
                background-color: #05070f !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
            }
            
            /* Text area overrides */
            div[data-baseweb="textarea"] {
                background-color: rgba(15, 23, 42, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 12px !important;
                color: #ffffff !important;
                transition: border-color 0.2s ease !important;
            }
            
            div[data-baseweb="textarea"]:focus-within {
                border-color: #00f2fe !important;
            }
            
            /* Button styling */
            div.stButton > button {
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
                color: #05070f !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                border: none !important;
                padding: 14px 28px !important;
                border-radius: 30px !important;
                box-shadow: 0 4px 20px rgba(0, 242, 254, 0.35) !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                cursor: pointer !important;
                width: 100%;
            }
            
            div.stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(0, 242, 254, 0.45) !important;
                color: #05070f !important;
            }
            
            /* Sidebar button overrides */
            section[data-testid="stSidebar"] div.stButton > button {
                background: rgba(255, 255, 255, 0.03) !important;
                color: #cbd5e1 !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                padding: 8px 16px !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
                border-radius: 8px !important;
                box-shadow: none !important;
                text-align: left !important;
            }
            
            section[data-testid="stSidebar"] div.stButton > button:hover {
                background: rgba(0, 242, 254, 0.08) !important;
                border-color: rgba(0, 242, 254, 0.3) !important;
                color: #ffffff !important;
                transform: none !important;
            }
            
            /* Custom Tab Styling */
            button[data-baseweb="tab"] {
                background-color: transparent !important;
                border-bottom: 2px solid transparent !important;
                color: #94a3b8 !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                padding: 10px 20px !important;
                transition: all 0.3s ease !important;
            }
            
            button[data-baseweb="tab"]:hover {
                color: #00f2fe !important;
            }
            
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #ffffff !important;
                border-bottom: 2px solid #00f2fe !important;
                background: rgba(0, 242, 254, 0.04) !important;
                border-top-left-radius: 8px !important;
                border-top-right-radius: 8px !important;
            }
            
            /* Sidebar status items styling */
            .agent-status-container {
                padding: 10px 14px;
                border-radius: 8px;
                margin-bottom: 8px;
                background-color: rgba(255, 255, 255, 0.03);
                border-left: 3px solid rgba(255, 255, 255, 0.1);
            }
            
            .agent-status-active {
                border-left: 3px solid #00f2fe;
                background-color: rgba(0, 242, 254, 0.05);
            }
            
            .agent-status-done {
                border-left: 3px solid #10b981;
                background-color: rgba(16, 185, 129, 0.05);
            }
            
            /* Footer style */
            .footer {
                text-align: center;
                padding: 40px 0 20px 0;
                color: #475569;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)

# Helper function to convert markdown text blocks into clean HTML elements inside the glassmorphic card container
def format_text_to_html(text):
    if not text:
        return ""
    lines = text.split("\n")
    formatted_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match markdown list items: "- item" or "* item"
        if line.startswith("- ") or line.startswith("* "):
            if not in_list:
                formatted_lines.append('<ul style="margin-left: 20px; color: #cbd5e1; line-height: 1.6; margin-bottom: 12px;">')
                in_list = True
            item_text = line[2:]
            # Replace bold markdown: **text** -> <strong>text</strong>
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            # Replace inline code/quotes if any
            item_text = re.sub(r'`(.*?)`', r'<code style="background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px;">\1</code>', item_text)
            formatted_lines.append(f'<li style="margin-bottom: 8px;">{item_text}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            
            # Match subheadings
            if line.startswith("### "):
                formatted_lines.append(f'<h4 style="color: #00f2fe; margin-top: 18px; margin-bottom: 8px; font-weight: 600; font-family: \'Outfit\', sans-serif;">{line[4:]}</h4>')
            elif line.startswith("## "):
                formatted_lines.append(f'<h3 style="color: #ffffff; margin-top: 22px; margin-bottom: 10px; font-weight: 700; font-family: \'Outfit\', sans-serif;">{line[3:]}</h3>')
            elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. "):
                item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line[3:])
                formatted_lines.append(f'<p style="margin-left: 20px; color: #cbd5e1; line-height: 1.6; margin-bottom: 8px;"><strong>{line[:3]}</strong>{item_text}</p>')
            else:
                line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                line = re.sub(r'`(.*?)`', r'<code style="background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px;">\1</code>', line)
                formatted_lines.append(f'<p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 12px;">{line}</p>')
                
    if in_list:
        formatted_lines.append('</ul>')
        
    return "".join(formatted_lines)

# Helper function to render a clean glassmorphic card for a section
def render_section_card(title, emoji, sections_dict):
    html = f"""
    <div class="glass-card">
        <div class="card-header">
            <span>{emoji}</span> {title}
        </div>
    """
    for label, content in sections_dict.items():
        formatted_content = format_text_to_html(content)
        html += f"""
        <div class="card-content-item">
            <div class="item-label">{label}</div>
            <div style="margin-top: 6px;">{formatted_content}</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# Helper to build a downloadable markdown report
def generate_markdown_report(blueprint: StartupBlueprint) -> str:
    return f"""# 🚀 {blueprint.executive_summary.startup_name} - Actionable Startup Blueprint
**One-Line Pitch**: *{blueprint.executive_summary.one_line_pitch}*

---

## 👑 Executive Summary
{blueprint.executive_summary.summary}

---

## 📈 Market Research
### Target Audience
{blueprint.market_research.target_audience}

### Pain Points
{blueprint.market_research.pain_points}

### Market Opportunities
{blueprint.market_research.opportunities}

---

## 🔍 Competitor Analysis
### Existing Competitors
{blueprint.competitor_analysis.competitors}

### Competitor Strengths
{blueprint.competitor_analysis.strengths}

### Competitor Weaknesses
{blueprint.competitor_analysis.weaknesses}

### Market Gaps
{blueprint.competitor_analysis.market_gaps}

---

## 🛠️ Product Strategy
### MVP Feature Set
{blueprint.product_strategy.mvp_features}

### Product Roadmap
{blueprint.product_strategy.roadmap}

### Technical Stack
{blueprint.product_strategy.technical_stack}

---

## 💎 Business Model
### Pricing Structure
{blueprint.business_model.pricing}

### Revenue Model
{blueprint.business_model.revenue_model}

### Secondary Monetization
{blueprint.business_model.monetization}

---

## 📣 Marketing Strategy
### Unique Positioning (UVP)
{blueprint.marketing_strategy.positioning}

### Product Launch Strategy
{blueprint.marketing_strategy.launch_strategy}

### Customer Acquisition Channels
{blueprint.marketing_strategy.acquisition_channels}

---
*Generated by Foundry AI Co-Founder*
"""

# Initialize app styling
local_css()

# Header Section
st.markdown('<div class="main-title">Foundry</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An AI Co-Founder for Entrepreneurs</div>', unsafe_allow_html=True)

# Sidebar setup
st.sidebar.markdown("### ⚙️ Settings")
api_key = st.sidebar.text_input(
    "🔑 Enter Gemini API Key", 
    value="", 
    type="password", 
    help="Paste your Google Gemini API Key here to enable generation."
)

st.sidebar.markdown("---")

# Session state initialization for text box
if "startup_idea_input" not in st.session_state:
    st.session_state["startup_idea_input"] = ""

st.sidebar.markdown("### 💡 Example Startup Ideas")
examples = {
    "⚖️ AI SaaS for Lawyers": "An AI-powered software-as-a-service (SaaS) that automates contract analysis, clause comparison, and regulatory compliance risk assessment for boutique law firms.",
    "🎒 Student Productivity App": "A gamified student productivity mobile application that syncs with university course syllabi, schedules study blocks, and rewards focus sessions with virtual rewards.",
    "🏋️ Fitness Coaching Platform": "A fitness coaching platform that connects local personal trainers with clients for hybrid (online/offline) training sessions and personalized nutrition plans.",
    "🐶 Eco-Friendly Pet Toys": "A direct-to-consumer circular subscription service providing 100% biodegradable, chew-resistant dog toys made from agricultural waste.",
    "✏️ Local Tutor Marketplace": "A peer-to-peer marketplace that matches university student tutors with high school students for in-person, subject-specific tutoring and college application prep."
}

# Example buttons click logic
for label, desc in examples.items():
    if st.sidebar.button(label, use_container_width=True):
        st.session_state["startup_idea_input"] = desc
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Agent Network Status")
status_placeholder = st.sidebar.empty()

# Main page setup
st.markdown("### 💡 What are you building?")
startup_idea = st.text_area(
    label="Describe your startup idea in detail:",
    key="startup_idea_input",
    placeholder="e.g., A subscription-based platform that rents high-quality baby clothes, allowing parents to return them for the next size up as their baby grows...",
    height=120,
    label_visibility="collapsed"
)

# Render locked button or active button based on API key entry
if not api_key:
    st.sidebar.warning("⚠️ Please enter a Gemini API Key to enable generation.")
    generate_button = st.button("Generate Blueprint", disabled=True)
else:
    generate_button = st.button("Generate Blueprint")

# Execution flow
if generate_button:
    if not startup_idea.strip():
        st.error("💡 Please describe your startup idea before generating.")
    else:
        # Dictionary representing progress status
        agent_statuses = {
            "market": {"status": "Pending", "msg": "Waiting..."},
            "competitor": {"status": "Pending", "msg": "Waiting..."},
            "product": {"status": "Pending", "msg": "Waiting..."},
            "business": {"status": "Pending", "msg": "Waiting..."},
            "marketing": {"status": "Pending", "msg": "Waiting..."},
            "summary": {"status": "Pending", "msg": "Waiting..."}
        }

        # Unified callback to update status on-screen and in sidebar
        def update_status(agent_key, msg):
            if msg == "Done.":
                agent_statuses[agent_key] = {"status": "Done", "msg": "Completed successfully."}
            elif "Completed" in msg or "Done" in msg:
                agent_statuses[agent_key] = {"status": "Done", "msg": msg}
            else:
                agent_statuses[agent_key] = {"status": "Active", "msg": msg}
            
            # Generate status HTML
            status_html = '<div class="glass-card" style="border: 1px solid rgba(0, 242, 254, 0.25);">'
            status_html += '<div class="card-header" style="font-size: 1.15rem; margin-bottom: 12px; padding-bottom: 6px;">⚡ Agent Network Collaboration</div>'
            
            sidebar_status_html = ""
            for key, val in agent_statuses.items():
                label_name = {
                    "market": "📈 Market Research Agent",
                    "competitor": "🔍 Competitor Agent",
                    "product": "🛠️ Product Agent",
                    "business": "💎 Business Agent",
                    "marketing": "📣 Marketing Agent",
                    "summary": "👑 Manager Agent"
                }[key]
                
                status_symbol = "⏳" if val["status"] == "Pending" else ("⚙️" if val["status"] == "Active" else "✅")
                color = "#94a3b8" if val["status"] == "Pending" else ("#00f2fe" if val["status"] == "Active" else "#10b981")
                
                # Main panel list item
                status_html += f"""
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.04); color: {color}; font-size: 0.95rem;">
                    <span style="font-weight: 600;">{label_name}</span>
                    <span>{status_symbol} {val["msg"]}</span>
                </div>
                """
                
                # Sidebar status list item
                s_cls = "agent-status-container"
                if val["status"] == "Active":
                    s_cls += " agent-status-active"
                elif val["status"] == "Done":
                    s_cls += " agent-status-done"
                sidebar_status_html += f"""
                <div class="{s_cls}">
                    <div style="font-weight: 700; color: #fff; font-size: 0.85rem;">{status_symbol} {label_name.split(' ', 1)[1]}</div>
                    <div style="color: #94a3b8; font-size: 0.75rem; margin-top: 2px;">{val["msg"]}</div>
                </div>
                """
                
            status_html += '</div>'
            status_box.markdown(status_html, unsafe_allow_html=True)
            status_placeholder.markdown(sidebar_status_html, unsafe_allow_html=True)

        status_box = st.empty()
        
        with st.spinner("Foundry agent network is analyzing your startup idea..."):
            try:
                start_time = time.time()
                # Initialize and run Manager Agent
                manager = ManagerAgent(api_key=api_key)
                blueprint = manager.run(startup_idea, progress_callback=update_status)
                generation_time = time.time() - start_time
                
                # Store results in session state
                st.session_state["blueprint"] = blueprint
                st.session_state["generation_time"] = generation_time
                
                # Clear status box from screen
                status_box.empty()
            except Exception as e:
                status_box.empty()
                err_msg = str(e)
                if "API key" in err_msg or "INVALID_ARGUMENT" in err_msg or "400" in err_msg or "key" in err_msg.lower():
                    st.error("🔑 Invalid Gemini API Key. Please check your key in Google AI Studio and try again.")
                elif "quota" in err_msg.lower() or "exhausted" in err_msg.lower():
                    st.error("⚠️ Gemini API Rate Limit Exceeded. Please wait a moment before trying again.")
                else:
                    st.error(f"📡 Gemini API Connection Failure: {err_msg}")
                st.info("Ensure your API Key is correct and has access to Gemini 2.5 Flash.")

# Render generated output tabs
if "blueprint" in st.session_state:
    blueprint: StartupBlueprint = st.session_state["blueprint"]
    gen_time = st.session_state.get("generation_time", 0.0)
    
    st.markdown('<div class="section-header">🚀 Actionable Startup Blueprint</div>', unsafe_allow_html=True)
    
    # Organize into Tabs
    tab_overview, tab_market, tab_competitors, tab_product, tab_business, tab_marketing = st.tabs([
        "✨ Overview", 
        "📊 Market", 
        "🔍 Competitors", 
        "🛠️ Product", 
        "💎 Business", 
        "📣 Marketing"
    ])
    
    # 1. OVERVIEW TAB
    with tab_overview:
        # Custom Metrics Grid (glowing HTML cards)
        metrics_html = f"""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-val">6</div>
                <div class="metric-lbl">🤖 Agents Used</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">6</div>
                <div class="metric-lbl">📋 Sections Generated</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{gen_time:.2f}s</div>
                <div class="metric-lbl">⚡ Generation Time</div>
            </div>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)
        
        # Hero Card: Executive Summary
        summary_sections = {
            "Startup Name": f"### {blueprint.executive_summary.startup_name}",
            "One-line Pitch": f"*{blueprint.executive_summary.one_line_pitch}*",
            "Executive Summary": blueprint.executive_summary.summary
        }
        render_section_card(
            title="Executive Summary",
            emoji="🔥",
            sections_dict=summary_sections
        )
        
        # Download block in columns
        st.markdown("### 💾 Export Blueprint")
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            report_md = generate_markdown_report(blueprint)
            st.download_button(
                label="📝 Download Markdown Report",
                data=report_md,
                file_name=f"{blueprint.executive_summary.startup_name.lower().replace(' ', '_')}_report.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with col_dl2:
            blueprint_json = json.dumps(blueprint.model_dump(), indent=2)
            st.download_button(
                label="📥 Download JSON Blueprint",
                data=blueprint_json,
                file_name=f"{blueprint.executive_summary.startup_name.lower().replace(' ', '_')}_blueprint.json",
                mime="application/json",
                use_container_width=True
            )
            
    # 2. MARKET TAB
    with tab_market:
        render_section_card(
            title="Market Research",
            emoji="🔍",
            sections_dict={
                "Target Audience": blueprint.market_research.target_audience,
                "Pain Points": blueprint.market_research.pain_points,
                "Opportunities & Trends": blueprint.market_research.opportunities
            }
        )
        
    # 3. COMPETITORS TAB
    with tab_competitors:
        render_section_card(
            title="Competitor Analysis",
            emoji="🏆",
            sections_dict={
                "Existing Competitors": blueprint.competitor_analysis.competitors,
                "Competitor Strengths": blueprint.competitor_analysis.strengths,
                "Competitor Weaknesses": blueprint.competitor_analysis.weaknesses,
                "Market Gaps": blueprint.competitor_analysis.market_gaps
            }
        )
        
    # 4. PRODUCT TAB
    with tab_product:
        render_section_card(
            title="Product Strategy",
            emoji="🚀",
            sections_dict={
                "MVP Features": blueprint.product_strategy.mvp_features,
                "Product Roadmap": blueprint.product_strategy.roadmap,
                "Technical Suggestions": blueprint.product_strategy.technical_stack
            }
        )
        
    # 5. BUSINESS TAB
    with tab_business:
        render_section_card(
            title="Business Model",
            emoji="💰",
            sections_dict={
                "Pricing Structure": blueprint.business_model.pricing,
                "Revenue Model": blueprint.business_model.revenue_model,
                "Monetization Channels": blueprint.business_model.monetization
            }
        )
        
    # 6. MARKETING TAB
    with tab_marketing:
        render_section_card(
            title="Marketing Strategy",
            emoji="📢",
            sections_dict={
                "Positioning (UVP)": blueprint.marketing_strategy.positioning,
                "Launch Strategy": blueprint.marketing_strategy.launch_strategy,
                "Customer Acquisition Channels": blueprint.marketing_strategy.acquisition_channels
            }
        )

# Footer
st.markdown("""
<div class="footer">
    Foundry AI Co-Founder • Built with Google Gemini 2.5 Flash & Streamlit
</div>
""", unsafe_allow_html=True)
