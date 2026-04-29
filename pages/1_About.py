import streamlit as st

st.set_page_config(page_title="About — FinAgentX",
                   page_icon="📖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #0e1117; }
.topnav { display: flex; align-items: center; justify-content: space-between; padding: 1.2rem 0 1rem 0; border-bottom: 0.5px solid #1e2738; margin-bottom: 2rem; }
.logo { font-size: 20px; font-weight: 600; color: #e2e8f0; }
.logo em { font-style: normal; color: #3b82f6; }
.nav-badge { font-size: 11px; color: #3b82f6; background: #0f1f3d; border: 0.5px solid #1e3a5f; padding: 3px 12px; border-radius: 20px; font-family: 'JetBrains Mono', monospace; }
.hero { background: #0f1923; border: 0.5px solid #1e2d45; border-radius: 12px; padding: 2.5rem; margin-bottom: 2rem; }
.hero-title { font-size: 2rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem; letter-spacing: -0.02em; }
.hero-title em { font-style: normal; color: #3b82f6; }
.hero-sub { font-size: 0.95rem; color: #64748b; line-height: 1.7; max-width: 680px; }
.section-label { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #475569; margin-bottom: 0.8rem; }
.card { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.4rem 1.6rem; height: 100%; }
.card-title { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem; }
.card-body { font-size: 0.82rem; color: #64748b; line-height: 1.75; }
.flow-wrap { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.8rem 2rem; margin-bottom: 2rem; }
.flow { display: flex; align-items: center; flex-wrap: wrap; justify-content: center; }
.flow-step { background: #0e1117; border: 0.5px solid #1e2d45; border-radius: 8px; padding: 0.7rem 1.1rem; text-align: center; min-width: 110px; }
.flow-step-icon { font-size: 1.2rem; margin-bottom: 0.2rem; }
.flow-step-label { font-size: 0.72rem; color: #e2e8f0; font-weight: 500; }
.flow-step-sub { font-size: 0.65rem; color: #475569; margin-top: 2px; font-family: 'JetBrains Mono', monospace; }
.flow-arrow { color: #2d3748; font-size: 1.2rem; padding: 0 0.5rem; }
.tech-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 2rem; }
.tech-pill { background: #131929; border: 0.5px solid #1e2d45; border-radius: 8px; padding: 0.7rem 1rem; display: flex; align-items: flex-start; gap: 0.7rem; }
.tech-icon { font-size: 1rem; margin-top: 1px; }
.tech-name { font-size: 0.82rem; font-weight: 500; color: #e2e8f0; }
.tech-desc { font-size: 0.72rem; color: #475569; margin-top: 1px; }
.lim-list { background: #131929; border: 0.5px solid #1e2d45; border-radius: 10px; padding: 1.4rem 1.6rem; margin-bottom: 2rem; }
.lim-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 0.5px solid #1a2235; font-size: 0.82rem; color: #64748b; line-height: 1.6; }
.lim-item:last-child { border-bottom: none; }
.lim-dot { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; margin-top: 6px; flex-shrink: 0; }
.lim-strong { color: #94a3b8; font-weight: 500; }
.disclaimer { padding: 0.65rem 1rem; border-left: 3px solid #3b82f6; background: #0f1923; font-size: 12px; color: #475569; border-radius: 0 6px 6px 0; font-family: 'JetBrains Mono', monospace; }
hr { border-color: #1e2738 !important; margin: 2rem 0 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0e1117; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topnav">
    <div class="logo">Fin<em>Agent</em>X</div>
    <span class="nav-badge">educational use only</span>
</div>
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

# ── What it does ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">What it does</div>',
            unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="small")
with c1:
    st.markdown("""<div class="card">
        <div class="card-title">📈 Stock Analysis</div>
        <div class="card-body">Fetches real-time data for any stock using yfinance. Computes RSI, MA50, MA200, trend direction, annual volatility, Sharpe Ratio, and Max Drawdown — then explains what each metric means in plain language.</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="card">
        <div class="card-title">⚖️ Stock Comparison</div>
        <div class="card-body">Compares two stocks side by side using normalized price charts and grouped risk metric bars. Supports company names like "Compare Infosys and TCS" — no need to know the ticker symbol.</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="card">
        <div class="card-title">💡 Concept Explanation</div>
        <div class="card-body">Ask about any financial term — RSI, Sharpe Ratio, PE ratio, moving averages, volatility — and get a beginner-friendly explanation with a real-world example. No jargon.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:2rem'></div>", unsafe_allow_html=True)

# ── Architecture ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">How it works</div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="flow-wrap">
    <div class="flow">
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
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tech stack ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Tech stack</div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="tech-grid">
    <div class="tech-pill"><div class="tech-icon">⚡</div><div><div class="tech-name">Groq — llama-3.1-8b-instant</div><div class="tech-desc">Free LLM API · intent classification + explanations</div></div></div>
    <div class="tech-pill"><div class="tech-icon">🔀</div><div><div class="tech-name">LangGraph + LangChain</div><div class="tech-desc">Agent routing · stateful graph execution</div></div></div>
    <div class="tech-pill"><div class="tech-icon">📈</div><div><div class="tech-name">yfinance</div><div class="tech-desc">Real-time & historical stock data · free</div></div></div>
    <div class="tech-pill"><div class="tech-icon">🔢</div><div><div class="tech-name">pandas + numpy</div><div class="tech-desc">RSI · moving averages · risk metrics</div></div></div>
    <div class="tech-pill"><div class="tech-icon">📊</div><div><div class="tech-name">Plotly</div><div class="tech-desc">Interactive charts · price · RSI · volume</div></div></div>
    <div class="tech-pill"><div class="tech-icon">🌐</div><div><div class="tech-name">Streamlit</div><div class="tech-desc">Web UI · free cloud hosting</div></div></div>
</div>
""", unsafe_allow_html=True)

# ── Limitations ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Known limitations</div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="lim-list">
    <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Stateless</span> — the agent has no memory between queries. Each question is treated independently with no conversation history.</div></div>
    <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Rate limiting</span> — yfinance can get rate-limited by Yahoo Finance on cloud servers. If a query fails, wait 30 seconds and try again.</div></div>
    <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Small LLM</span> — llama-3.1-8b is a compact model and may occasionally give generic explanations. All numbers always come directly from yfinance, never from the LLM.</div></div>
    <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">Ticker coverage</span> — works best with major US-listed stocks. Some international or OTC stocks may not have sufficient data.</div></div>
    <div class="lim-item"><div class="lim-dot"></div><div><span class="lim-strong">No predictions</span> — this tool explains historical data only. It cannot predict future prices or guarantee any outcome.</div></div>
</div>
""", unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚠ FinAgentX is built for learning purposes only. Nothing on this platform constitutes financial advice,
    investment recommendations, or trading signals. Always consult a qualified financial advisor before
    making any investment decisions.
</div>
""", unsafe_allow_html=True)
