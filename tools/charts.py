import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


COLORS = {
    "bg": "#0a0800",
    "panel": "#0f0c00",
    "border": "#331a00",
    "amber": "#ff9900",
    "orange": "#ff6600",
    "green": "#00cc44",
    "red": "#ff3300",
    "yellow": "#ffcc00",
    "text": "#cc8800",
    "muted": "#332200",
    "grid": "#1a0f00",
}


def _base_layout(**kwargs):
    layout = dict(
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["panel"],
        font=dict(family="IBM Plex Mono, monospace",
                  color=COLORS["text"], size=10),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    layout.update(kwargs)
    return layout


def plot_price_chart(historical_df: pd.DataFrame, ticker: str):
    df = historical_df.copy()

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
        vertical_spacing=0.025,
        subplot_titles=(f"{ticker} · PRICE & MOVING AVERAGES",
                        "RSI (14)", "VOLUME"),
    )

    # Price + MAs
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="PRICE",
                             line=dict(color=COLORS["amber"], width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA50",
                             line=dict(color=COLORS["yellow"], width=1, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA200"], name="MA200",
                             line=dict(color=COLORS["orange"], width=1, dash="dash")), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
                             line=dict(color=COLORS["amber"], width=1.5), showlegend=False), row=2, col=1)
    fig.add_hline(y=70, line=dict(
        color=COLORS["red"], dash="dot", width=1), row=2, col=1)
    fig.add_hline(y=30, line=dict(
        color=COLORS["green"], dash="dot", width=1), row=2, col=1)
    fig.add_hrect(
        y0=30, y1=70, fillcolor=COLORS["muted"], opacity=0.1, row=2, col=1)

    # Volume
    bar_colors = [COLORS["green"] if c >= o else COLORS["red"]
                  for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="VOLUME",
                         marker_color=bar_colors, showlegend=False), row=3, col=1)

    fig.update_layout(_base_layout(
        height=580,
        title=dict(text=f"■ {ticker} · TECHNICAL ANALYSIS CHART",
                   font=dict(size=12, color=COLORS["amber"])),
        legend=dict(bgcolor=COLORS["panel"], bordercolor=COLORS["border"],
                    borderwidth=1, orientation="h", y=1.02,
                    font=dict(size=9)),
        hovermode="x unified",
    ))

    for row in [1, 2, 3]:
        fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"],
                         zeroline=False, row=row, col=1,
                         tickfont=dict(color=COLORS["muted"], size=9))
        fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"],
                         zeroline=False, row=row, col=1,
                         tickfont=dict(color=COLORS["muted"], size=9))

    # Style subplot titles
    for ann in fig.layout.annotations:
        ann.font.color = COLORS["text"]
        ann.font.size = 10

    return fig


def plot_risk_chart(risk_data: dict, ticker: str):
    metrics = ["ANNUAL VOLATILITY", "SHARPE RATIO", "MAX DRAWDOWN"]
    values = [
        risk_data["annual_volatility"],
        risk_data["sharpe_ratio"],
        risk_data["max_drawdown"],
    ]
    bar_colors = [COLORS["orange"], COLORS["green"], COLORS["red"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics, y=values,
        marker_color=bar_colors,
        marker_line=dict(color=COLORS["border"], width=1),
        text=[f"{v:.4f}" for v in values],
        textposition="outside",
        textfont=dict(color=COLORS["amber"], size=10),
    ))

    fig.update_layout(_base_layout(
        height=320,
        title=dict(text=f"■ {ticker} · RISK METRICS",
                   font=dict(size=12, color=COLORS["amber"])),
        showlegend=False,
    ))
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"],
                     zeroline=True, zerolinecolor=COLORS["orange"],
                     tickfont=dict(color=COLORS["muted"], size=9))
    fig.update_xaxes(showgrid=False,
                     tickfont=dict(color=COLORS["text"], size=9))
    return fig


def plot_comparison_chart(analysis1: dict, analysis2: dict):
    t1 = analysis1["ticker"]
    t2 = analysis2["ticker"]

    df1 = analysis1["historical_data"].copy()
    df2 = analysis2["historical_data"].copy()
    df1["Normalized"] = (df1["Close"] / df1["Close"].iloc[0]) * 100
    df2["Normalized"] = (df2["Close"] / df2["Close"].iloc[0]) * 100

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=df1.index, y=df1["Normalized"], name=t1,
                                   line=dict(color=COLORS["amber"], width=2)))
    fig_price.add_trace(go.Scatter(x=df2.index, y=df2["Normalized"], name=t2,
                                   line=dict(color=COLORS["orange"], width=2, dash="dash")))
    fig_price.add_hline(y=100, line=dict(
        color=COLORS["muted"], dash="dot", width=1))

    fig_price.update_layout(_base_layout(
        height=350,
        title=dict(text=f"■ {t1} vs {t2} · NORMALIZED PRICE (BASE 100)",
                   font=dict(size=12, color=COLORS["amber"])),
        legend=dict(bgcolor=COLORS["panel"], bordercolor=COLORS["border"],
                    borderwidth=1, font=dict(size=9)),
        hovermode="x unified",
    ))
    fig_price.update_xaxes(showgrid=True, gridcolor=COLORS["grid"],
                           tickfont=dict(color=COLORS["muted"], size=9))
    fig_price.update_yaxes(showgrid=True, gridcolor=COLORS["grid"],
                           tickfont=dict(color=COLORS["muted"], size=9))

    # Risk comparison
    metrics = ["VOLATILITY", "SHARPE RATIO", "MAX DRAWDOWN"]
    v1 = [analysis1["risk_analysis"]["annual_volatility"],
          analysis1["risk_analysis"]["sharpe_ratio"],
          analysis1["risk_analysis"]["max_drawdown"]]
    v2 = [analysis2["risk_analysis"]["annual_volatility"],
          analysis2["risk_analysis"]["sharpe_ratio"],
          analysis2["risk_analysis"]["max_drawdown"]]

    fig_risk = go.Figure()
    fig_risk.add_trace(go.Bar(name=t1, x=metrics, y=v1,
                              marker_color=COLORS["amber"],
                              marker_line=dict(
                                  color=COLORS["border"], width=1),
                              text=[f"{v:.3f}" for v in v1], textposition="outside",
                              textfont=dict(color=COLORS["amber"], size=9)))
    fig_risk.add_trace(go.Bar(name=t2, x=metrics, y=v2,
                              marker_color=COLORS["orange"],
                              marker_line=dict(
                                  color=COLORS["border"], width=1),
                              text=[f"{v:.3f}" for v in v2], textposition="outside",
                              textfont=dict(color=COLORS["orange"], size=9)))

    fig_risk.update_layout(_base_layout(
        height=320,
        barmode="group",
        title=dict(text=f"■ {t1} vs {t2} · RISK COMPARISON",
                   font=dict(size=12, color=COLORS["amber"])),
        legend=dict(bgcolor=COLORS["panel"], bordercolor=COLORS["border"],
                    borderwidth=1, font=dict(size=9)),
    ))
    fig_risk.update_yaxes(showgrid=True, gridcolor=COLORS["grid"],
                          zeroline=True, zerolinecolor=COLORS["orange"],
                          tickfont=dict(color=COLORS["muted"], size=9))
    fig_risk.update_xaxes(showgrid=False,
                          tickfont=dict(color=COLORS["text"], size=9))

    return fig_price, fig_risk
