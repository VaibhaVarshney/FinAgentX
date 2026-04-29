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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: #0e1117;
}

/* ── Header ── */
.header-wrap {
    background: linear-gradient(180deg, #0a0d14 0%, #0e1117 100%);
    border-bottom: 1px solid #1e2738;
    padding: 1.8rem 2rem 1.4rem 2rem;
    margin-bottom: 2rem;
}
.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}
.logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: 0.04em;
}
.logo span {
    color: #3b82f6;
}
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #64748b;
    background: #1e2738;
    border: 1px solid #2d3748;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    letter-spacing: 0.08em;
}
.tagline {
    font-size: 0.8rem;
    color: #475569;
    font-weight: 400;
    letter-spacing: 0.02em;
}

/* ── Disclaimer ── */
.disclaimer {
    background: #0f1923;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #3b82f6;
    border-radius: 6px;
    padding: 0.65rem 1rem;
    font-size: 0.72rem;
    color: #475569;
    margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Quick query buttons ── */
.query-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-bottom: 1.8rem;
}
.query-btn {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
}
.query-btn:hover {
    background: #1a2540;
    border-color: #3b82f6;
}
.query-btn-icon {
    font-size: 0.75rem;
    color: #3b82f6;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.15rem;
}
.query-btn-text {
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
}

/* ── Input area ── */
.input-wrap {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 2rem;
}
.stTextInput > div > div > input {
    background: #0e1117 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
    caret-color: #3b82f6 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #2d3748 !important;
}

/* ── Run button ── */
.stButton > button {
    background: #3b82f6 !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
}

/* ── Divider ── */
hr { border-color: #1e2738 !important; margin: 1.5rem 0 !important; }

/* ── Intent badge ── */
.intent-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #0f1f3d;
    border: 1px solid #1e3a5f;
    color: #3b82f6;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── Stat tiles ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    transition: border-color 0.15s;
}
.stat-card:hover { border-color: #2d4a7a; }
.stat-card-label {
    font-size: 0.6rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.stat-card-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
}
.stat-card-value.up { color: #22c55e; }
.stat-card-value.down { color: #ef4444; }
.stat-card-value.blue { color: #3b82f6; }

/* ── Result box ── */
.result-box {
    background: #0d1117;
    border: 1px solid #1e2738;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    line-height: 1.85;
    color: #94a3b8;
    margin-top: 1.2rem;
    white-space: pre-wrap;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1e2738 !important;
    gap: 0 !important;
    margin-bottom: 1rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    border-radius: 0 !important;
    padding: 0.5rem 1.2rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
}

/* Spinner */
.stSpinner { color: #3b82f6 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2d3748; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="header-top">
        <div class="logo">Fin<span>Agent</span>X</div>
        <div class="badge">EDUCATIONAL USE ONLY</div>
    </div>
    <div class="tagline">AI-powered stock analysis terminal · Groq · LangGraph · yfinance</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
⚠ This tool is for educational purposes only and does not constitute financial advice.
Do not make investment decisions based on its output.
</div>
""", unsafe_allow_html=True)

# ── Agent ─────────────────────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()


# ── Quick query buttons ───────────────────────────────────────────────────────
QUICK_QUERIES = [
    ("📈", "Analyze Apple"),
    ("📊", "Analyze Infosys"),
    ("⚡", "Analyze NVDA"),
    ("⚖️", "Compare Tesla and Apple"),
    ("🔍", "Compare Google and Microsoft"),
    ("📚", "What is the Sharpe Ratio?"),
    ("📉", "What is RSI?"),
    ("💡", "Explain PE ratio"),
    ("🌐", "Compare Infosys and TCS"),
]

st.markdown('<div class="section-label">Quick Queries</div>',
            unsafe_allow_html=True)

# Use columns for clickable buttons
cols = st.columns(3)
clicked_query = None
for i, (icon, label) in enumerate(QUICK_QUERIES):
    with cols[i % 3]:
        if st.button(f"{icon}  {label}", key=f"quick_{i}"):
            clicked_query = label

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1.5rem">Your Query</div>',
            unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input(
        label="query",
        value=clicked_query or "",
        placeholder="Type a company name, ticker, or financial concept...",
        label_visibility="collapsed",
        key="query_input",
    )
with col_btn:
    st.markdown("<div style='margin-top:0.1rem'></div>",
                unsafe_allow_html=True)
    submit = st.button("Analyze →", key="submit_btn")

# ── Helpers ───────────────────────────────────────────────────────────────────


def trend_cls(trend):
    return "up" if trend == "Uptrend" else "down" if trend == "Downtrend" else "blue"


def stat_card(label, value, cls=""):
    return f"""<div class="stat-card">
        <div class="stat-card-label">{label}</div>
        <div class="stat-card-value {cls}">{value}</div>
    </div>"""


# ── Run ───────────────────────────────────────────────────────────────────────
run_query = query.strip() if (submit or clicked_query) and query.strip() else None

if run_query:
    agent = load_agent()

    with st.spinner("Fetching market data and generating analysis..."):
        try:
            result = agent.invoke({"user_query": run_query})
            intent = result.get("intent", "unknown")
            output = result.get("final_output", "")

            st.markdown("---")
            st.markdown(
                f'<div class="intent-pill">● {intent.replace("_", " ")}</div>', unsafe_allow_html=True)

            # ── Stock Analysis ────────────────────────────────────────────────
            if intent == "stock_analysis":
                analysis = result.get("analysis_result", {})

                if analysis and "historical_data" in analysis:
                    ticker = analysis["ticker"]
                    tech = analysis["technical_analysis"]
                    risk = analysis["risk_analysis"]

                    price = f"${analysis['current_price']:,.2f}" if analysis.get(
                        'current_price') else "N/A"
                    pe = f"{analysis['pe_ratio']:.2f}" if analysis.get(
                        'pe_ratio') else "N/A"
                    rsi_v = tech.get('latest_rsi', 'N/A')
                    rsi_cls = "down" if rsi_v and rsi_v > 70 else "up" if rsi_v and rsi_v < 30 else "blue"
                    trend = tech.get('trend', 'N/A')

                    st.markdown(f"""
                    <div class="stat-grid">
                        {stat_card("Ticker", ticker, "blue")}
                        {stat_card("Price", price)}
                        {stat_card("Trend", trend, trend_cls(trend))}
                        {stat_card("RSI (14)", rsi_v, rsi_cls)}
                        {stat_card("Volatility", f"{risk['annual_volatility']*100:.1f}%", "down" if risk['annual_volatility'] > 0.3 else "")}
                        {stat_card("Sharpe Ratio", f"{risk['sharpe_ratio']:.3f}", "up" if risk['sharpe_ratio'] > 1 else "")}
                        {stat_card("Max Drawdown", f"{risk['max_drawdown']*100:.1f}%", "down")}
                        {stat_card("P/E Ratio", pe)}
                    </div>
                    """, unsafe_allow_html=True)

                    tab1, tab2 = st.tabs(
                        ["📈  Price & Indicators", "⚠️  Risk Metrics"])
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
                tickers = resolve_tickers(run_query, needed=2)
                if len(tickers) >= 2:
                    with st.spinner(f"Loading {tickers[0]} vs {tickers[1]} charts..."):
                        try:
                            a1 = run_full_stock_analysis(tickers[0])
                            a2 = run_full_stock_analysis(tickers[1])

                            # Side-by-side stat cards
                            col1, col2 = st.columns(2)
                            for col, a in [(col1, a1), (col2, a2)]:
                                with col:
                                    t = a["ticker"]
                                    r = a["risk_analysis"]
                                    tech = a["technical_analysis"]
                                    st.markdown(f"""
                                    <div class="stat-grid" style="grid-template-columns: repeat(2,1fr)">
                                        {stat_card("Ticker", t, "blue")}
                                        {stat_card("Trend", tech['trend'], trend_cls(tech['trend']))}
                                        {stat_card("RSI", tech['latest_rsi'], "blue")}
                                        {stat_card("Sharpe", f"{r['sharpe_ratio']:.3f}", "up" if r['sharpe_ratio'] > 1 else "")}
                                        {stat_card("Volatility", f"{r['annual_volatility']*100:.1f}%", "down" if r['annual_volatility'] > 0.3 else "")}
                                        {stat_card("Drawdown", f"{r['max_drawdown']*100:.1f}%", "down")}
                                    </div>
                                    """, unsafe_allow_html=True)

                            fig_price, fig_risk = plot_comparison_chart(a1, a2)
                            tab1, tab2 = st.tabs(
                                ["📊  Price Comparison", "⚖️  Risk Comparison"])
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
                            st.warning(f"Charts unavailable: {e}")

                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Concept ───────────────────────────────────────────────────────
            else:
                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
