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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp { background: #0e1117; }

.topnav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0 1rem 0;
    border-bottom: 0.5px solid #1e2738;
    margin-bottom: 1.5rem;
}
.logo { font-size: 20px; font-weight: 600; color: #e2e8f0; letter-spacing: -0.01em; }
.logo em { font-style: normal; color: #3b82f6; }
.nav-badge {
    font-size: 11px; color: #3b82f6;
    background: #0f1f3d;
    border: 0.5px solid #1e3a5f;
    padding: 3px 10px; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
}

.disclaimer {
    padding: 0.6rem 1rem;
    border-left: 3px solid #3b82f6;
    background: #0f1923;
    font-size: 12px; color: #475569;
    border-radius: 0 6px 6px 0;
    margin-bottom: 1.8rem;
    font-family: 'JetBrains Mono', monospace;
}

.section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #475569; margin-bottom: 0.6rem;
}

.query-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;
    margin-bottom: 1.6rem;
}
.qbtn {
    background: #131929; border: 0.5px solid #1e2d45;
    border-radius: 8px; padding: 0.65rem 0.9rem;
    cursor: pointer; text-align: left;
    transition: border-color 0.15s, background 0.15s;
    width: 100%;
}
.qbtn:hover { border-color: #3b82f6; background: #1a2540; }
.qbtn-cat { font-size: 10px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; margin-bottom: 3px; }
.qbtn-text { font-size: 12px; color: #94a3b8; font-weight: 500; }

.stTextInput > div > div > input {
    background: #131929 !important; border: 0.5px solid #1e2d45 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.88rem !important;
    padding: 0.65rem 1rem !important; caret-color: #3b82f6 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #2d3748 !important; }

.stButton > button {
    background: #3b82f6 !important; color: #fff !important;
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
    border: none !important; border-radius: 8px !important;
    padding: 0.6rem 1.6rem !important; font-size: 0.85rem !important;
    width: 100% !important; transition: background 0.15s !important;
}
.stButton > button:hover { background: #2563eb !important; }

hr { border-color: #1e2738 !important; margin: 1.5rem 0 !important; }

.intent-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0f1f3d; border: 0.5px solid #1e3a5f;
    color: #3b82f6; font-family: 'JetBrains Mono', monospace;
    font-size: 10px; padding: 3px 12px; border-radius: 20px;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.2rem;
}

.stat-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
    margin-bottom: 1.4rem;
}
.stat-card {
    background: #131929; border: 0.5px solid #1e2d45;
    border-radius: 8px; padding: 0.8rem 1rem;
}
.stat-label {
    font-size: 10px; font-weight: 600; color: #475569;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px;
}
.stat-val { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 500; color: #e2e8f0; }
.stat-val.up { color: #22c55e; }
.stat-val.down { color: #ef4444; }
.stat-val.blue { color: #3b82f6; }

.result-box {
    background: #0d1117; border: 0.5px solid #1e2738;
    border-radius: 10px; padding: 1.4rem 1.6rem;
    font-size: 0.84rem; line-height: 1.85; color: #94a3b8;
    margin-top: 1.2rem; white-space: pre-wrap;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 0.5px solid #1e2738 !important;
    gap: 0 !important; margin-bottom: 1rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #475569 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.78rem !important;
    font-weight: 500 !important; border-radius: 0 !important;
    padding: 0.45rem 1.1rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav">
    <div class="logo">Fin<em>Agent</em>X</div>
    <span class="nav-badge">educational use only</span>
</div>
<div class="disclaimer">
    This tool is for educational purposes only and does not constitute financial advice. Do not make investment decisions based on its output.
</div>
""", unsafe_allow_html=True)

# ── Agent ─────────────────────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()


# ── Quick query buttons ───────────────────────────────────────────────────────
QUERIES = [
    ("analysis",   "Analyze Apple"),
    ("analysis",   "Analyze Infosys"),
    ("analysis",   "Analyze NVDA"),
    ("comparison", "Compare Tesla and Apple"),
    ("comparison", "Compare Google and Microsoft"),
    ("comparison", "Compare Infosys and TCS"),
    ("concept",    "What is Sharpe Ratio?"),
    ("concept",    "What is RSI?"),
    ("concept",    "Explain PE ratio"),
]

st.markdown('<div class="section-label">Quick queries</div>',
            unsafe_allow_html=True)

clicked = None
cols = st.columns(3)
for i, (cat, label) in enumerate(QUERIES):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="qbtn" onclick="void(0)">
            <div class="qbtn-cat">{cat}</div>
            <div class="qbtn-text">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"q{i}", help=f"Run: {label}"):
            clicked = label

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1.4rem">Your query</div>',
            unsafe_allow_html=True)

col_in, col_btn = st.columns([5, 1])
with col_in:
    query = st.text_input(
        "query", value=clicked or "",
        placeholder="Type a company name, ticker, or financial concept...",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    submit = st.button("Analyze →", key="main_submit")

# ── Helpers ───────────────────────────────────────────────────────────────────


def trend_cls(
    t): return "up" if t == "Uptrend" else "down" if t == "Downtrend" else "blue"


def stat_card(label, value, cls=""):
    return f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-val {cls}">{value}</div></div>'


# ── Run ───────────────────────────────────────────────────────────────────────
run = query.strip() if (submit or clicked) and query.strip() else None

if run:
    agent = load_agent()
    with st.spinner("Fetching market data..."):
        try:
            result = agent.invoke({"user_query": run})
            intent = result.get("intent", "unknown")
            output = result.get("final_output", "")

            st.markdown("---")
            st.markdown(
                f'<div class="intent-pill">● {intent.replace("_", " ")}</div>', unsafe_allow_html=True)

            # ── Stock analysis ────────────────────────────────────────────────
            if intent == "stock_analysis":
                analysis = result.get("analysis_result", {})
                if analysis and "historical_data" in analysis:
                    ticker = analysis["ticker"]
                    tech = analysis["technical_analysis"]
                    risk = analysis["risk_analysis"]
                    price = f"${analysis['current_price']:,.2f}" if analysis.get(
                        "current_price") else "N/A"
                    pe = f"{analysis['pe_ratio']:.2f}" if analysis.get(
                        "pe_ratio") else "N/A"
                    rsi_v = tech.get("latest_rsi", "N/A")
                    rsi_c = "down" if rsi_v and rsi_v > 70 else "up" if rsi_v and rsi_v < 30 else "blue"
                    trend = tech.get("trend", "N/A")

                    st.markdown(f"""
                    <div class="stat-grid">
                        {stat_card("Ticker", ticker, "blue")}
                        {stat_card("Price", price)}
                        {stat_card("Trend", trend, trend_cls(trend))}
                        {stat_card("RSI (14)", rsi_v, rsi_c)}
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
                            risk, ticker), use_container_width=True)

                st.markdown(
                    f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            # ── Comparison ────────────────────────────────────────────────────
            elif intent == "comparison":
                tickers = resolve_tickers(run, needed=2)
                if len(tickers) >= 2:
                    with st.spinner(f"Loading {tickers[0]} vs {tickers[1]}..."):
                        try:
                            a1 = run_full_stock_analysis(tickers[0])
                            a2 = run_full_stock_analysis(tickers[1])

                            c1, c2 = st.columns(2)
                            for col, a in [(c1, a1), (c2, a2)]:
                                with col:
                                    r = a["risk_analysis"]
                                    tech = a["technical_analysis"]
                                    st.markdown(f"""
                                    <div class="stat-grid" style="grid-template-columns:repeat(2,1fr)">
                                        {stat_card("Ticker", a['ticker'], "blue")}
                                        {stat_card("Trend", tech['trend'], trend_cls(tech['trend']))}
                                        {stat_card("RSI", tech['latest_rsi'], "blue")}
                                        {stat_card("Sharpe", f"{r['sharpe_ratio']:.3f}", "up" if r['sharpe_ratio'] > 1 else "")}
                                        {stat_card("Volatility", f"{r['annual_volatility']*100:.1f}%", "down" if r['annual_volatility'] > 0.3 else "")}
                                        {stat_card("Drawdown", f"{r['max_drawdown']*100:.1f}%", "down")}
                                    </div>
                                    """, unsafe_allow_html=True)

                            fig_p, fig_r = plot_comparison_chart(a1, a2)
                            tab1, tab2 = st.tabs(
                                ["📊  Price Comparison", "⚖️  Risk Comparison"])
                            with tab1:
                                st.plotly_chart(
                                    fig_p, use_container_width=True)
                                cc1, cc2 = st.columns(2)
                                with cc1:
                                    st.plotly_chart(plot_price_chart(
                                        a1["historical_data"], tickers[0]), use_container_width=True)
                                with cc2:
                                    st.plotly_chart(plot_price_chart(
                                        a2["historical_data"], tickers[1]), use_container_width=True)
                            with tab2:
                                st.plotly_chart(
                                    fig_r, use_container_width=True)
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
