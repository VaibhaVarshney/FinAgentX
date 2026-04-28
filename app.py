from agent.graph import build_graph
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinAgentX",
    page_icon="📈",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background-color: #0a0a0f;
    color: #e8e8e8;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00ff88 0%, #00ccff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #555;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

.disclaimer {
    background: #111118;
    border-left: 3px solid #ff4444;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #888;
    font-family: 'Space Mono', monospace;
    margin: 1rem 0;
}

.example-chip {
    display: inline-block;
    background: #111118;
    border: 1px solid #222;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.78rem;
    color: #00ff88;
    font-family: 'Space Mono', monospace;
    margin: 0.2rem;
}

.result-box {
    background: #0d0d15;
    border: 1px solid #1a1a2e;
    border-radius: 8px;
    padding: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.8;
    color: #ccc;
    white-space: pre-wrap;
}

.intent-badge {
    display: inline-block;
    background: #001a0d;
    border: 1px solid #00ff88;
    color: #00ff88;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}

.stTextInput > div > div > input {
    background: #0d0d15 !important;
    border: 1px solid #222 !important;
    border-radius: 6px !important;
    color: #e8e8e8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 1px #00ff88 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00ff88, #00ccff) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 2rem !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

.stSpinner > div {
    border-top-color: #00ff88 !important;
}

hr {
    border-color: #1a1a2e !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">FinAgentX</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">⚡ Powered by Groq · LangGraph · yfinance</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
⚠️ EDUCATIONAL PURPOSES ONLY — This tool does not provide financial advice.
Do not make investment decisions based on its output.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Examples ──────────────────────────────────────────────────────────────────
st.markdown("**Try asking:**")
st.markdown("""
<span class="example-chip">Analyze AAPL</span>
<span class="example-chip">Compare TSLA and NVDA</span>
<span class="example-chip">What is RSI?</span>
<span class="example-chip">Explain Sharpe Ratio</span>
<span class="example-chip">Analyze $MSFT</span>
""", unsafe_allow_html=True)

st.markdown("")

# ── Agent init (cached) ───────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()


# ── Input ─────────────────────────────────────────────────────────────────────
query = st.text_input(
    label="Your question",
    placeholder="e.g. Analyze AAPL  |  Compare MSFT and GOOGL  |  What is PE ratio?",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 5])
with col1:
    submit = st.button("Ask →")

# ── Run agent ─────────────────────────────────────────────────────────────────
if submit and query.strip():
    agent = load_agent()

    with st.spinner("Thinking..."):
        try:
            result = agent.invoke({"user_query": query.strip()})
            intent = result.get("intent", "unknown")
            output = result.get("final_output", "No response generated.")

            st.markdown("---")
            st.markdown(
                f'<div class="intent-badge">Intent: {intent}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submit and not query.strip():
    st.warning("Please enter a question first.")
