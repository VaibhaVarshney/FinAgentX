from tools.ticker_resolver import resolve_tickers
from tools.charts import plot_price_chart, plot_risk_chart, plot_comparison_chart
from agent.analysis_engine import run_full_stock_analysis
from agent.graph import build_graph
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


st.set_page_config(page_title="FinAgentX", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #0e1117; }

/* Hide default sidebar toggle and sidebar */
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Topbar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 2rem; height: 56px;
    background: #0a0d14;
    border-bottom: 0.5px solid #1e2738;
    margin-bottom: 2rem;
    position: sticky; top: 0; z-index: 999;
}
.topbar-left { display: flex; align-items: center; gap: 2.5rem; }
.logo { font-size: 18px; font-weight: 600; color: #e2e8f0; letter-spacing: -0.01em; text-decoration: none; }
.logo em { font-style: normal; color: #3b82f6; }
.topbar-nav { display: flex; align-items: center; gap: 0; }
.nav-link {
    font-size: 0.8rem; font-weight: 500; color: #475569;
    padding: 0.35rem 1rem; border-radius: 6px;
    text-decoration: none; transition: color 0.15s, background 0.15s;
    cursor: pointer;
}
.nav-link:hover { color: #e2e8f0; background: #131929; }
.nav-link.active { color: #3b82f6; background: #0f1f3d; }
.topbar-right { display: flex; align-items: center; gap: 0.75rem; }
.nav-badge {
    font-size: 11px; color: #3b82f6; background: #0f1f3d;
    border: 0.5px solid #1e3a5f; padding: 3px 12px;
    border-radius: 20px; font-family: 'JetBrains Mono', monospace;
}
.gh-btn {
    font-size: 0.78rem; color: #64748b; background: #131929;
    border: 0.5px solid #1e2d45; padding: 4px 12px;
    border-radius: 6px; text-decoration: none;
    transition: color 0.15s, border-color 0.15s;
}
.gh-btn:hover { color: #e2e8f0; border-color: #3b82f6; }

/* ── Page content ── */
.page-wrap { padding: 0 2rem; }

.disclaimer {
    padding: 0.6rem 1rem; border-left: 3px solid #3b82f6;
    background: #0f1923; font-size: 12px; color: #475569;
    border-radius: 0 6px 6px 0; margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
}
.section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #475569; margin-bottom: 0.7rem;
}

/* Quick query buttons */
[data-testid="column"] .stButton > button {
    background: #131929 !important; border: 0.5px solid #1e2d45 !important;
    border-radius: 8px !important; color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.82rem !important;
    font-weight: 500 !important; text-align: left !important;
    padding: 0.75rem 1rem !important; width: 100% !important;
    height: auto !important; line-height: 1.4 !important;
    transition: border-color 0.15s, background 0.15s !important;
    white-space: normal !important;
}
[data-testid="column"] .stButton > button:hover {
    background: #1a2540 !important; border-color: #3b82f6 !important; color: #e2e8f0 !important;
}

/* Input */
.stTextInput > div > div > input {
    background: #131929 !important; border: 0.5px solid #1e2d45 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important; padding: 0.65rem 1rem !important;
    caret-color: #3b82f6 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #2d3748 !important; }

/* Analyze button — last column */
[data-testid="column"]:last-child {
    display: flex !important; flex-direction: column !important; justify-content: flex-end !important;
}
[data-testid="column"]:last-child .stButton > button {
    background: #3b82f6 !important; color: #fff !important;
    font-weight: 600 !important; border: none !important;
    font-size: 0.85rem !important; text-align: center !important;
    padding: 0.65rem 1rem !important;
}
[data-testid="column"]:last-child .stButton > button:hover { background: #2563eb !important; }

hr { border-color: #1e2738 !important; margin: 1.8rem 0 !important; }

.intent-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0f1f3d; border: 0.5px solid #1e3a5f;
    color: #3b82f6; font-family: 'JetBrains Mono', monospace;
    font-size: 10px; padding: 3px 12px; border-radius: 20px;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.2rem;
}
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 1.6rem; }
.stat-card { background: #131929; border: 0.5px solid #1e2d45; border-radius: 8px; padding: 0.8rem 1rem; }
.stat-label { font-size: 10px; font-weight: 600; color: #475569; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px; }
.stat-val { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 500; color: #e2e8f0; }
.stat-val.up { color: #22c55e; }
.stat-val.down { color: #ef4444; }
.stat-val.blue { color: #3b82f6; }
.result-box {
    background: #0d1117; border: 0.5px solid #1e2738; border-radius: 10px;
    padding: 1.4rem 1.6rem; font-size: 0.84rem; line-height: 1.85;
    color: #94a3b8; margin-top: 1.4rem; white-space: pre-wrap;
}
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 0.5px solid #1e2738 !important; gap: 0 !important; margin-bottom: 1rem !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #475569 !important; font-family: 'Inter', sans-serif !important; font-size: 0.78rem !important; font-weight: 500 !important; border-radius: 0 !important; padding: 0.45rem 1.1rem !important; border-bottom: 2px solid transparent !important; }
.stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }
[data-testid="stPlotlyChart"] { margin-bottom: 1.5rem !important; padding-bottom: 1rem !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Topbar ────────────────────────────────────────────────────────────────────
page = st.query_params.get("page", "home")

st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <a class="logo" href="?page=home">Fin<em>Agent</em>X</a>
        <nav class="topbar-nav">
            <a class="nav-link {'active' if page == 'home' else ''}" href="?page=home">Terminal</a>
            <a class="nav-link {'active' if page == 'about' else ''}" href="?page=about">About</a>
        </nav>
    </div>
    <div class="topbar-right">
        <a class="gh-btn" href="https://github.com/VaibhaVarshney/FinAgentX" target="_blank">⭐ GitHub</a>
        <span class="nav-badge">educational use only</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# ── Agent ─────────────────────────────────────────────────────────────────────


@st.cache_resource
def load_agent():
    return build_graph()


# ══════════════════════════════════════════════════════════════════════════════
# ABOUT PAGE
# ══════════════════════════════════════════════════════════════════════════════
if page == "about":
    st.markdown("""
    <style>
    .hero { background: #0f1923; border: 0.5px solid #1e2d45; border-radius: 12px; padding: 2.5rem; margin-bottom: 2rem; }
    .hero-title { font-size: 2rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem; letter-spacing: -0.02em; }
    .hero-title em { font-style: normal; color: #3b82f6; }
    .hero-sub { font-size: 0.95rem; color: #64748b; line-height: 1.7; max-width: 680px; }
    .card { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.4rem 1.6rem; height: 100%; }
    .card-title { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem; }
    .card-body { font-size: 0.82rem; color: #64748b; line-height: 1.75; }
    .flow-wrap { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.8rem 2rem; margin-bottom: 2rem; }
    .flow { display: flex; align-items: center; flex-wrap: wrap; justify-content: center; gap: 0; }
    .flow-step { background: #0e1117; border: 0.5px solid #1e2d45; border-radius: 8px; padding: 0.7rem 1.1rem; text-align: center; min-width: 110px; }
    .flow-step-icon { font-size: 1.2rem; margin-bottom: 0.2rem; }
    .flow-step-label { font-size: 0.72rem; color: #e2e8f0; font-weight: 500; }
    .flow-step-sub { font-size: 0.65rem; color: #475569; margin-top: 2px; font-family: 'JetBrains Mono', monospace; }
    .flow-arrow { color: #2d3748; font-size: 1.2rem; padding: 0 0.5rem; }
    .tech-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 2rem; }
    .tech-pill { background: #131929; border: 0.5px solid #1e2d45; border-radius: 8px; padding: 0.7rem 1rem; display: flex; align-items: flex-start; gap: 0.7rem; }
    .tech-name { font-size: 0.82rem; font-weight: 500; color: #e2e8f0; }
    .tech-desc { font-size: 0.72rem; color: #475569; margin-top: 1px; }
    .lim-list { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.4rem 1.6rem; margin-bottom: 2rem; }
    .lim-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 0.5px solid #1a2235; font-size: 0.82rem; color: #64748b; line-height: 1.6; }
    .lim-item:last-child { border-bottom: none; }
    .lim-dot { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; margin-top: 6px; flex-shrink: 0; }
    .lim-strong { color: #94a3b8; font-weight: 500; }
    .about-disclaimer { padding: 0.65rem 1rem; border-left: 3px solid #3b82f6; background: #0f1923; font-size: 12px; color: #475569; border-radius: 0 6px 6px 0; font-family: 'JetBrains Mono', monospace; }
    </style>

    <div class="hero">
        <div class="hero-title">About <em>FinAgentX</em></div>
        <div class="hero-sub">
            FinAgentX is a free, open-source AI-powered financial education terminal.
            It combines a locally-routed AI agent with real-time market data to help
            beginners understand stocks, risk metrics, and financial concepts —
            without any paid APIs or cloud infrastructure.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">What it does</div>',
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.markdown("""<div class="card"><div class="card-title">📈 Stock Analysis</div><div class="card-body">Fetches real-time data for any stock using yfinance. Computes RSI, MA50, MA200, trend direction, annual volatility, Sharpe Ratio, and Max Drawdown — then explains each metric in plain language.</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card"><div class="card-title">⚖️ Stock Comparison</div><div class="card-body">Compares two stocks side by side using normalized price charts and grouped risk metric bars. Supports company names like "Compare Infosys and TCS" — no need to know the ticker.</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card"><div class="card-title">💡 Concept Explanation</div><div class="card-body">Ask about any financial term — RSI, Sharpe Ratio, PE ratio, moving averages — and get a beginner-friendly explanation with a real-world example.</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:2rem'></div>",
                unsafe_allow_html=True)
    st.markdown('<div class="section-label">How it works</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="flow-wrap"><div class="flow">
        <div class="flow-step"><div class="flow-step-icon">💬</div><div class="flow-step-label">User Query</div><div class="flow-step-sub">Natural language</div></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="flow-step-icon">🧠</div><div class="flow-step-label">Intent Classifier</div><div class="flow-step-sub">Groq LLM</div></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="flow-step-icon">🔀</div><div class="flow-step-label">LangGraph Router</div><div class="flow-step-sub">3 routes</div></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="flow-step-icon">🔧</div><div class="flow-step-label">Tool Execution</div><div class="flow-step-sub">yfinance + numpy</div></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="flow-step-icon">✍️</div><div class="flow-step-label">LLM Explanation</div><div class="flow-step-sub">Groq llama3</div></div>
        <div class="flow-arrow">→</div>
        <div class="flow-step"><div class="flow-step-icon">📊</div><div class="flow-step-label">Charts + Output</div><div class="flow-step-sub">Plotly + Streamlit</div></div>
    </div></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Tech stack</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-grid">
        <div class="tech-pill"><div>⚡</div><div><div class="tech-name">Groq — llama-3.1-8b-instant</div><div class="tech-desc">Free LLM API · intent classification + explanations</div></div></div>
        <div class="tech-pill"><div>🔀</div><div><div class="tech-name">LangGraph + LangChain</div><div class="tech-desc">Agent routing · stateful graph execution</div></div></div>
        <div class="tech-pill"><div>📈</div><div><div class="tech-name">yfinance</div><div class="tech-desc">Real-time & historical stock data · free</div></div></div>
        <div class="tech-pill"><div>🔢</div><div><div class="tech-name">pandas + numpy</div><div class="tech-desc">RSI · moving averages · risk metrics</div></div></div>
        <div class="tech-pill"><div>📊</div><div><div class="tech-name">Plotly</div><div class="tech-desc">Interactive charts · price · RSI · volume</div></div></div>
        <div class="tech-pill"><div>🌐</div><div><div class="tech-name">Streamlit</div><div class="tech-desc">Web UI · free cloud hosting</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Known limitations</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="lim-list">
        <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Stateless</span> — no memory between queries. Each question is treated independently.</div></div>
        <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Rate limiting</span> — yfinance can get rate-limited on cloud servers. If a query fails, wait 30 seconds and retry.</div></div>
        <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Small LLM</span> — llama-3.1-8b may give generic explanations. All numbers always come from yfinance, never the LLM.</div></div>
        <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Ticker coverage</span> — works best with major US-listed stocks. Some international stocks may lack data.</div></div>
        <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">No predictions</span> — explains historical data only. Cannot predict future prices.</div></div>
    </div>
    <div class="about-disclaimer">⚠ FinAgentX is for educational purposes only. Nothing here constitutes financial advice or trading signals.</div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME / TERMINAL PAGE
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="disclaimer">
        ⚠ This tool is for educational purposes only and does not constitute financial advice.
        Do not make investment decisions based on its output.
    </div>
    """, unsafe_allow_html=True)

    QUERIES = [
        ("Analyze Apple"),
        ("Analyze Infosys"),
        ("Analyze NVDA"),
        ("Compare Tesla and Apple"),
        ("Compare Google and Microsoft"),
        ("Compare Infosys and TCS"),
        ("What is Sharpe Ratio?"),
        ("What is RSI?"),
        ("Explain PE ratio"),
    ]

    st.markdown('<div class="section-label">Quick queries</div>',
                unsafe_allow_html=True)
    clicked = None
    c1, c2, c3 = st.columns(3, gap="small")
    for i, label in enumerate(QUERIES):
        col = [c1, c2, c3][i % 3]
        with col:
            if st.button(label, key=f"q{i}"):
                clicked = label

    st.markdown('<div class="section-label" style="margin-top:1.6rem">Your query</div>',
                unsafe_allow_html=True)
    col_in, col_btn = st.columns([5, 1], gap="small")
    with col_in:
        query = st.text_input("query", value=clicked or "",
                              placeholder="Type a company name, ticker, or financial concept...",
                              label_visibility="collapsed")
    with col_btn:
        submit = st.button("Analyze →", key="main_submit")

    def trend_cls(
        t): return "up" if t == "Uptrend" else "down" if t == "Downtrend" else "blue"

    def stat_card(label, value, cls=""):
        return f'<div class="stat-card"><div class="stat-label">{label}</div><div class="stat-val {cls}">{value}</div></div>'

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
                        st.markdown(f"""<div class="stat-grid">
                            {stat_card("Ticker", ticker, "blue")}
                            {stat_card("Price", price)}
                            {stat_card("Trend", trend, trend_cls(trend))}
                            {stat_card("RSI (14)", rsi_v, rsi_c)}
                            {stat_card("Volatility", f"{risk['annual_volatility']*100:.1f}%", "down" if risk['annual_volatility'] > 0.3 else "")}
                            {stat_card("Sharpe Ratio", f"{risk['sharpe_ratio']:.3f}", "up" if risk['sharpe_ratio'] > 1 else "")}
                            {stat_card("Max Drawdown", f"{risk['max_drawdown']*100:.1f}%", "down")}
                            {stat_card("P/E Ratio", pe)}
                        </div>""", unsafe_allow_html=True)
                        tab1, tab2 = st.tabs(
                            ["📈  Price & Indicators", "⚠️  Risk Metrics"])
                        with tab1:
                            st.plotly_chart(plot_price_chart(
                                analysis["historical_data"], ticker), width="stretch")
                        with tab2:
                            st.plotly_chart(plot_risk_chart(
                                risk, ticker), width="stretch")
                    st.markdown(
                        f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

                elif intent == "comparison":
                    comparison_data = result.get("comparison_results", [])
                    if len(comparison_data) == 2:
                        a1, a2 = comparison_data[0], comparison_data[1]
                        cc1, cc2 = st.columns(2, gap="medium")
                        for col, a in [(cc1, a1), (cc2, a2)]:
                            with col:
                                r = a["risk_analysis"]
                                tech = a["technical_analysis"]
                                st.markdown(f"""<div class="stat-grid" style="grid-template-columns:repeat(2,1fr)">
                                    {stat_card("Ticker", a['ticker'], "blue")}
                                    {stat_card("Trend", tech['trend'], trend_cls(tech['trend']))}
                                    {stat_card("RSI", tech['latest_rsi'], "blue")}
                                    {stat_card("Sharpe", f"{r['sharpe_ratio']:.3f}", "up" if r['sharpe_ratio'] > 1 else "")}
                                    {stat_card("Volatility", f"{r['annual_volatility']*100:.1f}%", "down" if r['annual_volatility'] > 0.3 else "")}
                                    {stat_card("Drawdown", f"{r['max_drawdown']*100:.1f}%", "down")}
                                </div>""", unsafe_allow_html=True)
                        try:
                            fig_p, fig_r = plot_comparison_chart(a1, a2)
                            tab1, tab2 = st.tabs(
                                ["📊  Price Comparison", "⚖️  Risk Comparison"])
                            with tab1:
                                st.plotly_chart(fig_p, width="stretch")
                                st.markdown(
                                    "<div style='height:0.8rem'></div>", unsafe_allow_html=True)
                                pc1, pc2 = st.columns(2, gap="medium")
                                with pc1:
                                    st.plotly_chart(plot_price_chart(
                                        a1["historical_data"], a1["ticker"]), width="stretch")
                                with pc2:
                                    st.plotly_chart(plot_price_chart(
                                        a2["historical_data"], a2["ticker"]), width="stretch")
                            with tab2:
                                st.plotly_chart(fig_r, width="stretch")
                        except Exception as e:
                            st.warning(f"Charts unavailable: {e}")
                    st.markdown(
                        f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

                else:
                    st.markdown(
                        f'<div class="result-box">{output}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
