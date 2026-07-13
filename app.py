import streamlit as st
import pandas as pd
import json
import os
import sys
import io
import time
import plotly.express as px
from finance_crew import run_crew

# Set up page config
st.set_page_config(page_title="FinSight", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS matching the Stitch MCP UI requirements
# Colors: Olive green (#6B7A4F), Off-white (#F5F3EE), Warm grey (#D9D6CE), Charcoal (#2B2B26), Muted gold (#B8A369)
# Typography: Serif headings (Fraunces/Playfair), sans-serif body (Inter).
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;600;700&display=swap');

    :root {
        --primary: #6B7A4F;
        --background: #F5F3EE;
        --surface: #D9D6CE;
        --text: #2B2B26;
        --accent: #B8A369;
    }

    /* Overall Background and Typography */
    .stApp {
        background-color: var(--background) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: var(--text) !important;
    }

    /* Sidebar */
    .stSidebar {
        background-color: var(--surface) !important;
    }

    /* Search Bar and Inputs */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid var(--surface) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 10px -2px rgba(43, 43, 38, 0.05) !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
        box-shadow: 0 2px 10px -2px rgba(43, 43, 38, 0.08) !important;
    }
    .stButton>button:hover {
        background-color: var(--accent) !important;
        color: #FFFFFF !important;
    }

    /* Expander / Accordion */
    .streamlit-expanderHeader {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border-radius: 8px !important;
        border: none !important;
    }
    
    /* Metrics Cards */
    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--primary) !important;
    }
    [data-testid="stMetricDelta"] > div > svg {
        fill: var(--primary) !important;
    }
    
    /* Card Layout for Metrics */
    div[data-testid="metric-container"] {
        background-color: var(--surface) !important;
        padding: 24px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px -2px rgba(43, 43, 38, 0.05) !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; margin-top: 40px; margin-bottom: 40px; font-size: 48px;'>FinSight</h1>", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.markdown("### Settings")
    timeframe = st.selectbox("Timeframe (Override)", ["", "1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"])
    symbol_override = st.text_input("Symbol Override (e.g. RELIANCE.NS)")
    st.markdown("---")
    st.markdown("Quiet Luxury Financial Intelligence.")

# Main search bar
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("Search Stock", placeholder="e.g. Analyze Reliance stock for the past year", label_visibility="collapsed")
    analyze_btn = st.button("Analyze", use_container_width=True)

class CapturingOutput(io.StringIO):
    def __init__(self, st_container):
        super().__init__()
        self.st_container = st_container
        self.full_log = ""
        self.stages = {
            "query": False,
            "code_writer": False,
            "execution": False
        }

    def write(self, text):
        super().write(text)
        self.full_log += text
        
        # Parse logs for our custom stepper
        if "Stock Data Analyst" in self.full_log and not self.stages["query"]:
            self.stages["query"] = True
            self.update_stepper()
        if "Senior Python Developer" in self.full_log and not self.stages["code_writer"]:
            self.stages["code_writer"] = True
            self.update_stepper()
        if "Senior Code Execution Expert" in self.full_log and not self.stages["execution"]:
            self.stages["execution"] = True
            self.update_stepper()
            
    def update_stepper(self):
        # We can update a placeholder with our custom HTML stepper
        html = f"""
        <div style="background-color: #D9D6CE; padding: 24px; border-radius: 12px; margin-top: 20px;">
            <h4 style="margin-top: 0;">Agent Progress</h4>
            <div style="margin: 10px 0;">{'🟢' if self.stages['query'] else '⚪'} Analyzing Query...</div>
            <div style="margin: 10px 0;">{'🟢' if self.stages['code_writer'] else '⚪'} Fetching Data (Python Dev)...</div>
            <div style="margin: 10px 0;">{'🟢' if self.stages['execution'] else '⚪'} Generating Visualization (Exec Expert)...</div>
        </div>
        """
        self.st_container.markdown(html, unsafe_allow_html=True)

if analyze_btn and query:
    # Append overrides to the query if provided
    final_query = query
    if symbol_override:
        final_query += f" Use symbol {symbol_override}."
    if timeframe:
        final_query += f" Use timeframe {timeframe}."

    # Remove old files if they exist to prevent stale data
    if os.path.exists("data.csv"): os.remove("data.csv")
    if os.path.exists("stats.json"): os.remove("stats.json")

    st.markdown("---")
    
    # Progress Stepper Placeholder
    stepper_placeholder = st.empty()
    stepper_placeholder.markdown("""
    <div style="background-color: #D9D6CE; padding: 24px; border-radius: 12px; margin-top: 20px;">
        <h4 style="margin-top: 0;">Agent Progress</h4>
        <div style="margin: 10px 0;">🟡 Initializing...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Raw log expander
    with st.expander("Raw Agent Logs", expanded=False):
        log_placeholder = st.empty()

    # Capture stdout
    old_stdout = sys.stdout
    captured = CapturingOutput(stepper_placeholder)
    sys.stdout = captured

    with st.spinner("CrewAI is analyzing your request..."):
        try:
            run_crew(final_query)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            sys.stdout = old_stdout
    
    # Update raw logs one last time
    log_placeholder.text(captured.full_log)
    
    # Mark stepper complete
    stepper_placeholder.markdown("""
    <div style="background-color: #D9D6CE; padding: 24px; border-radius: 12px; margin-top: 20px; border: 1px solid #6B7A4F;">
        <h4 style="margin-top: 0;">Agent Progress</h4>
        <div style="margin: 10px 0;">✅ Analyzing Query</div>
        <div style="margin: 10px 0;">✅ Fetching Data</div>
        <div style="margin: 10px 0;">✅ Generating Visualization</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Read the output files generated by the agent
    if os.path.exists("data.csv") and os.path.exists("stats.json"):
        df = pd.read_csv("data.csv")
        with open("stats.json", "r") as f:
            stats = json.load(f)
            
        # Format the Plotly Chart
        # Convert date column if necessary
        date_col = df.columns[0]
        if 'Date' in df.columns:
            date_col = 'Date'
        
        # Assume 'Close' is the primary metric
        if 'Close' in df.columns:
            fig = px.line(df, x=date_col, y='Close', title="Stock Price")
            # Apply gradient fill aesthetic (Olive green #6B7A4F to Gold #B8A369)
            fig.update_traces(line_color='#6B7A4F', fill='tozeroy', fillcolor='rgba(184, 163, 105, 0.2)')
            fig.update_layout(
                plot_bgcolor='#F5F3EE',
                paper_bgcolor='#F5F3EE',
                font_family='Inter',
                font_color='#2B2B26',
                title_font_family='Playfair Display',
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Metric Cards
        cols = st.columns(4)
        cols[0].metric("Current Price", f"{stats.get('current_price', stats.get('Current Price', 'N/A'))}")
        cols[1].metric("% Change", f"{stats.get('%_change', stats.get('% Change', 'N/A'))}")
        cols[2].metric("Mean", f"{stats.get('mean', stats.get('Mean', 'N/A'))}")
        cols[3].metric("Std Dev", f"{stats.get('std_dev', stats.get('Std Dev', 'N/A'))}")
        
        # Raw Data Accordion
        with st.expander("Historical Data Table", expanded=False):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("The agents completed the analysis but didn't generate the expected data.csv and stats.json files. Please try rephrasing your query.")
