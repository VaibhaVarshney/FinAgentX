import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


COLORS = {
    "bg": "#0a0a0f",
    "panel": "#0d0d15",
    "border": "#1a1a2e",
    "green": "#00ff88",
    "blue": "#00ccff",
    "red": "#ff4444",
    "yellow": "#ffd700",
    "text": "#e8e8e8",
    "muted": "#555577",
}


def _base_layout(**kwargs):
    """Returns a base layout dict merged with any overrides."""
    layout = dict(
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["panel"],
        font=dict(family="Space Mono, monospace",
                  color=COLORS["text"], size=11),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    layout.update(kwargs)
    return layout


def plot_price_chart(historical_df: pd.DataFrame, ticker: str):
    """3-panel chart: Price + MA50/MA200 | RSI | Volume"""
    df = historical_df.copy()

    # Compute indicators
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).ewm(com=13, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(com=13, adjust=False).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.55, 0.25, 0.20],
        vertical_spacing=0.03,
        subplot_titles=(f"{ticker} Price & Moving Averages",
                        "RSI (14)", "Volume"),
    )

    # Panel 1: Price + MAs
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Price",
                             line=dict(color=COLORS["green"], width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA50",
                             line=dict(color=COLORS["yellow"], width=1, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA200"], name="MA200",
                             line=dict(color=COLORS["blue"], width=1, dash="dash")), row=1, col=1)

    # Panel 2: RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
                             line=dict(color=COLORS["blue"], width=1.5), showlegend=False), row=2, col=1)
    fig.add_hline(y=70, line=dict(
        color=COLORS["red"], dash="dot", width=1), row=2, col=1)
    fig.add_hline(y=30, line=dict(
        color=COLORS["green"], dash="dot", width=1), row=2, col=1)
    fig.add_hrect(
        y0=30, y1=70, fillcolor=COLORS["muted"], opacity=0.07, row=2, col=1)

    # Panel 3: Volume
    bar_colors = [COLORS["green"] if c >= o else COLORS["red"]
                  for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
                         marker_color=bar_colors, showlegend=False), row=3, col=1)

    fig.update_layout(_base_layout(
        height=600,
        title=dict(text=f"📈 {ticker} — Technical Chart",
                   font=dict(size=14, color=COLORS["green"])),
        legend=dict(bgcolor=COLORS["panel"], bordercolor=COLORS["border"],
                    borderwidth=1, orientation="h", y=1.02),
        hovermode="x unified",
    ))

    for row in [1, 2, 3]:
        fig.update_xaxes(
            showgrid=True, gridcolor=COLORS["border"], row=row, col=1)
        fig.update_yaxes(
            showgrid=True, gridcolor=COLORS["border"], row=row, col=1)

    return fig


def plot_risk_chart(risk_data: dict, ticker: str):
    """Bar chart for risk metrics."""
    metrics = ["Annual Volatility", "Sharpe Ratio", "Max Drawdown"]
    values = [
        risk_data["annual_volatility"],
        risk_data["sharpe_ratio"],
        risk_data["max_drawdown"],
    ]
    bar_colors = [COLORS["yellow"], COLORS["green"], COLORS["red"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics, y=values,
        marker_color=bar_colors,
        text=[f"{v:.4f}" for v in values],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=11),
    ))

    fig.update_layout(_base_layout(
        height=320,
        title=dict(text=f"⚠️ {ticker} — Risk Metrics",
                   font=dict(size=14, color=COLORS["green"])),
        showlegend=False,
    ))
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"],
                     zeroline=True, zerolinecolor=COLORS["muted"])
    fig.update_xaxes(showgrid=False)

    return fig


def plot_comparison_chart(analysis1: dict, analysis2: dict):
    """Normalized price comparison + side-by-side risk metrics."""
    t1 = analysis1["ticker"]
    t2 = analysis2["ticker"]

    # Normalized price chart
    df1 = analysis1["historical_data"].copy()
    df2 = analysis2["historical_data"].copy()
    df1["Normalized"] = (df1["Close"] / df1["Close"].iloc[0]) * 100
    df2["Normalized"] = (df2["Close"] / df2["Close"].iloc[0]) * 100

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=df1.index, y=df1["Normalized"], name=t1,
                                   line=dict(color=COLORS["green"], width=2)))
    fig_price.add_trace(go.Scatter(x=df2.index, y=df2["Normalized"], name=t2,
                                   line=dict(color=COLORS["blue"], width=2)))

    fig_price.update_layout(_base_layout(
        height=350,
        title=dict(text=f"📊 {t1} vs {t2} — Normalized Price (Base 100)",
                   font=dict(size=13, color=COLORS["green"])),
        legend=dict(bgcolor=COLORS["panel"],
                    bordercolor=COLORS["border"], borderwidth=1),
        hovermode="x unified",
    ))
    fig_price.update_xaxes(showgrid=True, gridcolor=COLORS["border"])
    fig_price.update_yaxes(showgrid=True, gridcolor=COLORS["border"])

    # Side-by-side risk metrics
    metrics = ["Volatility", "Sharpe Ratio", "Max Drawdown"]
    v1 = [analysis1["risk_analysis"]["annual_volatility"],
          analysis1["risk_analysis"]["sharpe_ratio"],
          analysis1["risk_analysis"]["max_drawdown"]]
    v2 = [analysis2["risk_analysis"]["annual_volatility"],
          analysis2["risk_analysis"]["sharpe_ratio"],
          analysis2["risk_analysis"]["max_drawdown"]]

    fig_risk = go.Figure()
    fig_risk.add_trace(go.Bar(name=t1, x=metrics, y=v1,
                              marker_color=COLORS["green"],
                              text=[f"{v:.3f}" for v in v1], textposition="outside"))
    fig_risk.add_trace(go.Bar(name=t2, x=metrics, y=v2,
                              marker_color=COLORS["blue"],
                              text=[f"{v:.3f}" for v in v2], textposition="outside"))

    fig_risk.update_layout(_base_layout(
        height=320,
        barmode="group",
        title=dict(text=f"⚖️ {t1} vs {t2} — Risk Comparison",
                   font=dict(size=13, color=COLORS["green"])),
        legend=dict(bgcolor=COLORS["panel"],
                    bordercolor=COLORS["border"], borderwidth=1),
    ))
    fig_risk.update_yaxes(showgrid=True, gridcolor=COLORS["border"],
                          zeroline=True, zerolinecolor=COLORS["muted"])
    fig_risk.update_xaxes(showgrid=False)

    return fig_price, fig_risk
