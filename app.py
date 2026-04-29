from tools.ticker_resolver import resolve_tickers
from tools.charts import plot_price_chart, plot_risk_chart, plot_comparison_chart
from agent.analysis_engine import run_full_stock_analysis
from agent.graph import build_graph
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="FinAgentX", page_icon="📈", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background-color: #0a0a0f; color: #e8e8e8; }
h1,h2,h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

.hero-title {
    font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800;
    background: linear-gradient(135deg, #00ff88 0%, #00ccff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.hero-sub {
    font-family: 'Space Mono', monospace; font-size: 0.8rem; color: #555;
    letter-spacing: 0.15em; text-transform: uppercase; margin-top: 0.2rem;
}
.disclaimer {
    background: #111118; border-left: 3px solid #ff4444;
    padding: 0.75rem 1rem; border-radius: 4px;
    font-size: 0.8rem; color: #888; font-family: 'Space Mono', monospace; margin: 1rem 0;
}
.example-chip {
    display: inline-block; background: #111118; border: 1px solid #222;
    border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.78rem;
    color: #00ff88; font-family: 'Space Mono', monospace; margin: 0.2rem;
}
.result-box {
    background: #0d0d15; border: 1px solid #1a1a2e; border-radius: 8px;
    padding: 1.5rem; font-family: 'Space Mono', monospace; font-size: 0.85rem;
    line-height: 1.8; color: #ccc; white-space: pre-wrap;
}
.intent-badge {
    display: inline-block; background: #001a0d; border: 1px solid #00ff88;
    color: #00ff88; font-family: 'Space Mono', monospace; font-size: 0.7rem;
    padding: 0.2rem 0.6rem; border-radius: 12px; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 1rem;
}
.stTextInput > div > div > input {
    background: #0d0d15 !important; border: 1px solid #222 !important;
    border-radius: 6px !important; color: #e8e8e8 !important;
    font-family: 'Space Mono', monospace !important; font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00ff88 !important; box-shadow: 0 0 0 1px #00ff88 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00ff88, #00ccff) !important;
    color: #000 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 6px !important; padding: 0.5rem 2rem !important;
    font-size: 0.95rem !important;
}
hr { border-color: #1a1a2e !important; }
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

st.markdown("**Try asking:**")
st.markdown("""
<span class="example-chip">Analyze Apple</span>
<span class="example-chip">Compare Tesla and Nvidia</span>
<span class="example-chip">Analyse Infosys</span>
<span class="example-chip">What is RSI?</span>
<span class="example-chip">Analyze $MSFT</span>
""", unsafe_allow_html=True)

st.markdown("")

# ── Agent (cached) ────────────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()


# ── Input ─────────────────────────────────────────────────────────────────────
query = st.text_input(
    label="Your question",
    placeholder="e.g. Analyze Apple  |  Compare Infosys and TCS  |  What is Sharpe Ratio?",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 5])
with col1:
    submit = st.button("Ask →")

# ── Run ───────────────────────────────────────────────────────────────────────
if submit and query.strip():
    agent = load_agent()

    with st.spinner("Fetching data & generating analysis..."):
        try:
            result = agent.invoke({"user_query": query.strip()})
            intent = result.get("intent", "unknown")
            output = result.get("final_output", "No response generated.")

            st.markdown("---")
            st.markdown(
                f'<div class="intent-badge">Intent: {intent}</div>', unsafe_allow_html=True)

            # ── Stock Analysis ────────────────────────────────────────────────
            if intent == "stock_analysis":
                analysis = result.get("analysis_result", {})

                if analysis and "historical_data" in analysis:
                    ticker = analysis["ticker"]

                    # Charts
                    tab1, tab2 = st.tabs(
                        ["📈 Price & Indicators", "⚠️ Risk Metrics"])
                    with tab1:
                        st.plotly_chart(
                            plot_price_chart(
                                analysis["historical_data"], ticker),
                            use_container_width=True,
                        )
                    with tab2:
                        st.plotly_chart(
                            plot_risk_chart(analysis["risk_analysis"], ticker),
                            use_container_width=True,
                        )

                # LLM explanation
                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Comparison ────────────────────────────────────────────────────
            elif intent == "comparison":
                tickers = resolve_tickers(query.strip(), needed=2)
                if len(tickers) >= 2:
                    with st.spinner("Loading comparison charts..."):
                        try:
                            a1 = run_full_stock_analysis(tickers[0])
                            a2 = run_full_stock_analysis(tickers[1])

                            fig_price, fig_risk = plot_comparison_chart(a1, a2)

                            tab1, tab2 = st.tabs(
                                ["📊 Price Comparison", "⚖️ Risk Comparison"])
                            with tab1:
                                st.plotly_chart(
                                    fig_price, use_container_width=True)

                                # Individual price charts
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.plotly_chart(
                                        plot_price_chart(
                                            a1["historical_data"], tickers[0]),
                                        use_container_width=True,
                                    )
                                with c2:
                                    st.plotly_chart(
                                        plot_price_chart(
                                            a2["historical_data"], tickers[1]),
                                        use_container_width=True,
                                    )

                            with tab2:
                                st.plotly_chart(
                                    fig_risk, use_container_width=True)

                        except Exception as e:
                            st.warning(f"Charts unavailable: {e}")

                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Concept Explanation ───────────────────────────────────────────
            else:
                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

elif submit and not query.strip():
    st.warning("Please enter a question first.")
