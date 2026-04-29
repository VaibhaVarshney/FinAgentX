from tools.ticker_resolver import resolve_tickers
from tools.charts import plot_price_chart, plot_risk_chart, plot_comparison_chart
from agent.analysis_engine import run_full_stock_analysis
from agent.graph import build_graph
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


st.set_page_config(page_title="FinAgentX", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
    background-color: #0a0800;
    color: #ff9900;
}

.stApp { background-color: #0a0800; }

/* Top bar */
.topbar {
    background: #0f0c00;
    border-bottom: 1px solid #ff6600;
    padding: 0.6rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #ff6600;
    letter-spacing: 0.08em;
    margin-bottom: 1.2rem;
}

.topbar-logo {
    font-size: 1rem;
    font-weight: 700;
    color: #ff9900;
    letter-spacing: 0.2em;
}

.topbar-tag {
    color: #664400;
    font-size: 0.65rem;
}

/* Hero */
.hero-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ff9900;
    letter-spacing: 0.12em;
    text-shadow: 0 0 30px rgba(255,153,0,0.3);
    margin-bottom: 0.1rem;
}

.hero-sub {
    font-size: 0.7rem;
    color: #664400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* Disclaimer */
.disclaimer {
    background: #0f0c00;
    border: 1px solid #ff6600;
    border-left: 4px solid #ff3300;
    padding: 0.6rem 1rem;
    border-radius: 2px;
    font-size: 0.72rem;
    color: #cc4400;
    letter-spacing: 0.05em;
    margin: 1rem 0;
}

/* Chips */
.chip-row { margin: 0.5rem 0 1rem 0; }
.chip {
    display: inline-block;
    background: #0f0c00;
    border: 1px solid #663300;
    border-radius: 2px;
    padding: 0.25rem 0.7rem;
    font-size: 0.7rem;
    color: #ff9900;
    font-family: 'IBM Plex Mono', monospace;
    margin: 0.15rem;
    letter-spacing: 0.05em;
}

/* Intent badge */
.intent-badge {
    display: inline-block;
    background: #0f0c00;
    border: 1px solid #ff6600;
    color: #ff9900;
    font-size: 0.65rem;
    padding: 0.15rem 0.6rem;
    border-radius: 2px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Result box */
.result-box {
    background: #0a0800;
    border: 1px solid #332200;
    border-left: 3px solid #ff6600;
    border-radius: 2px;
    padding: 1.2rem 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.9;
    color: #cc8800;
    white-space: pre-wrap;
    margin-top: 1rem;
}

/* Divider */
.bbg-divider {
    border: none;
    border-top: 1px solid #331a00;
    margin: 1rem 0;
}

/* Stat tiles */
.stat-row {
    display: flex;
    gap: 0.6rem;
    margin: 0.8rem 0;
    flex-wrap: wrap;
}
.stat-tile {
    background: #0f0c00;
    border: 1px solid #332200;
    padding: 0.6rem 1rem;
    border-radius: 2px;
    min-width: 140px;
    flex: 1;
}
.stat-label {
    font-size: 0.6rem;
    color: #664400;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.stat-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ff9900;
    margin-top: 0.1rem;
}
.stat-value.up { color: #00cc44; }
.stat-value.down { color: #ff3300; }
.stat-value.neutral { color: #ff9900; }

/* Input */
.stTextInput > div > div > input {
    background: #0f0c00 !important;
    border: 1px solid #663300 !important;
    border-radius: 2px !important;
    color: #ff9900 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.85rem !important;
    caret-color: #ff9900 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff9900 !important;
    box-shadow: 0 0 0 1px #ff6600 !important;
}
.stTextInput > div > div > input::placeholder { color: #443300 !important; }

/* Button */
.stButton > button {
    background: #ff6600 !important;
    color: #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.45rem 1.8rem !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
}
.stButton > button:hover { background: #ff9900 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0c00 !important;
    border-bottom: 1px solid #332200 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #664400 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 0 !important;
    padding: 0.4rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: #1a0f00 !important;
    color: #ff9900 !important;
    border-bottom: 2px solid #ff6600 !important;
}

hr { border-color: #221100 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0800; }
::-webkit-scrollbar-thumb { background: #663300; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <span class="topbar-logo">FINAGENTX</span>
    <span>EQUITY ANALYSIS TERMINAL</span>
    <span class="topbar-tag">EDUCATIONAL USE ONLY</span>
    <span class="topbar-tag">POWERED BY GROQ · LANGGRAPH · YFINANCE</span>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown('<div class="hero-title">FINAGENTX</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI-Powered Stock Analysis · Educational Terminal</div>',
                unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
▶ DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY. THIS TOOL DOES NOT CONSTITUTE FINANCIAL ADVICE.
DO NOT MAKE INVESTMENT DECISIONS BASED ON ITS OUTPUT.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="bbg-divider">', unsafe_allow_html=True)

# ── Example chips ─────────────────────────────────────────────────────────────
st.markdown('<div style="font-size:0.65rem;color:#664400;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.4rem;">QUICK QUERIES</div>', unsafe_allow_html=True)
st.markdown("""
<div class="chip-row">
    <span class="chip">▶ ANALYZE APPLE</span>
    <span class="chip">▶ COMPARE TESLA AND NVIDIA</span>
    <span class="chip">▶ ANALYSE INFOSYS</span>
    <span class="chip">▶ WHAT IS RSI?</span>
    <span class="chip">▶ ANALYZE $MSFT</span>
    <span class="chip">▶ COMPARE GOOGLE AND META</span>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
query = st.text_input(
    label="query",
    placeholder="ENTER TICKER, COMPANY NAME, OR FINANCIAL CONCEPT...",
    label_visibility="collapsed",
)
col_btn, _ = st.columns([1, 6])
with col_btn:
    submit = st.button("EXECUTE ▶")

# ── Agent ─────────────────────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()

# ── Helpers ───────────────────────────────────────────────────────────────────


def trend_color(trend: str) -> str:
    if trend == "Uptrend":
        return "up"
    if trend == "Downtrend":
        return "down"
    return "neutral"


def stat_tile(label, value, cls="neutral"):
    return f"""<div class="stat-tile">
        <div class="stat-label">{label}</div>
        <div class="stat-value {cls}">{value}</div>
    </div>"""


# ── Run ───────────────────────────────────────────────────────────────────────
if submit and query.strip():
    agent = load_agent()

    with st.spinner("FETCHING MARKET DATA..."):
        try:
            result = agent.invoke({"user_query": query.strip()})
            intent = result.get("intent", "unknown")
            output = result.get("final_output", "")

            st.markdown('<hr class="bbg-divider">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="intent-badge">■ INTENT: {intent.upper()}</div>', unsafe_allow_html=True)

            # ── Stock Analysis ────────────────────────────────────────────────
            if intent == "stock_analysis":
                analysis = result.get("analysis_result", {})

                if analysis and "historical_data" in analysis:
                    ticker = analysis["ticker"]
                    tech = analysis["technical_analysis"]
                    risk = analysis["risk_analysis"]

                    # Stat tiles row
                    price = f"${analysis['current_price']:,.2f}" if analysis.get(
                        'current_price') else "N/A"
                    pe = f"{analysis['pe_ratio']:.2f}" if analysis.get(
                        'pe_ratio') else "N/A"
                    rsi_val = tech.get('latest_rsi', 'N/A')
                    rsi_cls = "down" if rsi_val and rsi_val > 70 else "up" if rsi_val and rsi_val < 30 else "neutral"
                    vol_pct = f"{risk['annual_volatility']*100:.1f}%"
                    sharpe = f"{risk['sharpe_ratio']:.3f}"
                    drawdown = f"{risk['max_drawdown']*100:.1f}%"
                    trend = tech.get('trend', 'N/A')

                    st.markdown(f"""
                    <div class="stat-row">
                        {stat_tile("TICKER", ticker, "neutral")}
                        {stat_tile("PRICE", price, "neutral")}
                        {stat_tile("TREND", trend, trend_color(trend))}
                        {stat_tile("RSI (14)", rsi_val, rsi_cls)}
                        {stat_tile("VOLATILITY", vol_pct, "down" if risk['annual_volatility'] > 0.3 else "neutral")}
                        {stat_tile("SHARPE RATIO", sharpe, "up" if risk['sharpe_ratio'] > 1 else "neutral")}
                        {stat_tile("MAX DRAWDOWN", drawdown, "down")}
                        {stat_tile("P/E RATIO", pe, "neutral")}
                    </div>
                    """, unsafe_allow_html=True)

                    # Charts
                    tab1, tab2 = st.tabs(
                        ["▶ PRICE & INDICATORS", "▶ RISK METRICS"])
                    with tab1:
                        st.plotly_chart(plot_price_chart(
                            analysis["historical_data"], ticker), use_container_width=True)
                    with tab2:
                        st.plotly_chart(plot_risk_chart(
                            analysis["risk_analysis"], ticker), use_container_width=True)

                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Comparison ────────────────────────────────────────────────────
            elif intent == "comparison":
                tickers = resolve_tickers(query.strip(), needed=2)
                if len(tickers) >= 2:
                    with st.spinner(f"LOADING {tickers[0]} VS {tickers[1]}..."):
                        try:
                            a1 = run_full_stock_analysis(tickers[0])
                            a2 = run_full_stock_analysis(tickers[1])

                            # Comparison stat tiles
                            def cmp_tiles(a, color_class):
                                t = a["ticker"]
                                r = a["risk_analysis"]
                                tech = a["technical_analysis"]
                                return f"""
                                <div style="flex:1">
                                    <div style="font-size:0.65rem;color:#664400;letter-spacing:0.15em;margin-bottom:0.4rem">{t}</div>
                                    <div class="stat-row">
                                        {stat_tile("TREND", tech['trend'], trend_color(tech['trend']))}
                                        {stat_tile("RSI", tech['latest_rsi'], "neutral")}
                                        {stat_tile("VOLATILITY", f"{r['annual_volatility']*100:.1f}%", "neutral")}
                                        {stat_tile("SHARPE", f"{r['sharpe_ratio']:.3f}", "up" if r['sharpe_ratio'] > 1 else "neutral")}
                                    </div>
                                </div>"""

                            st.markdown(f"""
                            <div style="display:flex;gap:1rem;margin:0.5rem 0">
                                {cmp_tiles(a1, "green")}
                                {cmp_tiles(a2, "blue")}
                            </div>
                            """, unsafe_allow_html=True)

                            fig_price, fig_risk = plot_comparison_chart(a1, a2)
                            tab1, tab2 = st.tabs(
                                ["▶ PRICE COMPARISON", "▶ RISK COMPARISON"])
                            with tab1:
                                st.plotly_chart(
                                    fig_price, use_container_width=True)
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.plotly_chart(plot_price_chart(
                                        a1["historical_data"], tickers[0]), use_container_width=True)
                                with c2:
                                    st.plotly_chart(plot_price_chart(
                                        a2["historical_data"], tickers[1]), use_container_width=True)
                            with tab2:
                                st.plotly_chart(
                                    fig_risk, use_container_width=True)

                        except Exception as e:
                            st.warning(f"CHARTS UNAVAILABLE: {e}")

                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Concept Explanation ───────────────────────────────────────────
            else:
                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"TERMINAL ERROR: {str(e)}")

elif submit and not query.strip():
    st.warning("ENTER A QUERY TO PROCEED.")
