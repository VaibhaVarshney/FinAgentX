import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

C = {
    "bg":     "#0e1117",
    "panel":  "#131929",
    "border": "#1e2d45",
    "grid":   "#1a2235",
    "blue":   "#3b82f6",
    "blue2":  "#60a5fa",
    "green":  "#22c55e",
    "red":    "#ef4444",
    "yellow": "#f59e0b",
    "text":   "#94a3b8",
    "muted":  "#2d3748",
    "white":  "#e2e8f0",
}
FONT = "JetBrains Mono, monospace"


def _base(height=500, title="", **kw):
    return dict(
        paper_bgcolor=C["bg"], plot_bgcolor=C["panel"],
        font=dict(family=FONT, color=C["text"], size=10),
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        title=dict(text=title, font=dict(size=12, color=C["white"]), x=0.01),
        **kw,
    )


def _xaxis(**kw):
    base = dict(gridcolor=C["grid"], zeroline=False,
                tickfont=dict(color=C["muted"], size=9), linecolor=C["border"])
    base.update(kw)
    return base


def _yaxis(**kw):
    base = dict(gridcolor=C["grid"], zeroline=False,
                tickfont=dict(color=C["muted"], size=9), linecolor=C["border"])
    base.update(kw)
    return base


def plot_price_chart(historical_df: pd.DataFrame, ticker: str):
    df = historical_df.copy()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).ewm(com=13, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(com=13, adjust=False).mean()
    df["RSI"] = 100 - (100 / (1 + gain / loss))

    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.55, 0.25, 0.20],
        vertical_spacing=0.06,
        subplot_titles=(f"{ticker} · Price & Moving Averages",
                        "RSI (14)", "Volume"),
    )

    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Price",
                             line=dict(color=C["blue"], width=1.8)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA 50",
                             line=dict(color=C["yellow"], width=1.2, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA200"], name="MA 200",
                             line=dict(color=C["blue2"], width=1.2, dash="dash")), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"],
                             line=dict(color=C["blue"], width=1.5), showlegend=False), row=2, col=1)
    fig.add_hline(y=70, line=dict(
        color=C["red"], dash="dot", width=1), row=2, col=1)
    fig.add_hline(y=30, line=dict(
        color=C["green"], dash="dot", width=1), row=2, col=1)
    fig.add_hrect(
        y0=30, y1=70, fillcolor=C["muted"], opacity=0.08, row=2, col=1)

    bar_colors = [C["green"] if c >= o else C["red"]
                  for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"],
                         marker_color=bar_colors, showlegend=False, marker_line_width=0), row=3, col=1)

    fig.update_layout(**_base(580, f"{ticker} · Technical Analysis",
                              legend=dict(bgcolor=C["panel"], bordercolor=C["border"], borderwidth=1,
                                          orientation="h", y=1.03, font=dict(size=9)),
                              hovermode="x unified"))

    for row in [1, 2, 3]:
        fig.update_xaxes(row=row, col=1, **_xaxis())
        fig.update_yaxes(row=row, col=1, **_yaxis())

    for ann in fig.layout.annotations:
        ann.font.color = C["text"]
        ann.font.size = 9

    return fig


def plot_risk_chart(risk_data: dict, ticker: str):
    metrics = ["Annual Volatility", "Sharpe Ratio", "Max Drawdown"]
    values = [risk_data["annual_volatility"],
              risk_data["sharpe_ratio"], risk_data["max_drawdown"]]
    colors = [C["yellow"], C["green"], C["red"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics, y=values, marker_color=colors, marker_line_width=0,
        text=[f"{v:.4f}" for v in values], textposition="outside",
        textfont=dict(color=C["white"], size=10),
    ))

    fig.update_layout(
        **_base(310, f"{ticker} · Risk Metrics", showlegend=False))
    fig.update_xaxes(**_xaxis())
    fig.update_yaxes(**_yaxis(zeroline=True, zerolinecolor=C["border"]))
    return fig


def plot_comparison_chart(analysis1: dict, analysis2: dict):
    t1, t2 = analysis1["ticker"], analysis2["ticker"]

    df1 = analysis1["historical_data"].copy()
    df2 = analysis2["historical_data"].copy()
    df1["N"] = (df1["Close"] / df1["Close"].iloc[0]) * 100
    df2["N"] = (df2["Close"] / df2["Close"].iloc[0]) * 100

    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter(x=df1.index, y=df1["N"], name=t1,
                               line=dict(color=C["blue"], width=2)))
    fig_p.add_trace(go.Scatter(x=df2.index, y=df2["N"], name=t2,
                               line=dict(color=C["yellow"], width=2)))
    fig_p.add_hline(y=100, line=dict(color=C["muted"], dash="dot", width=1))

    fig_p.update_layout(**_base(340, f"{t1} vs {t2} · Normalized Price (Base 100)",
                                legend=dict(
                                    bgcolor=C["panel"], bordercolor=C["border"], borderwidth=1, font=dict(size=9)),
                                hovermode="x unified"))
    fig_p.update_xaxes(**_xaxis())
    fig_p.update_yaxes(**_yaxis())

    metrics = ["Volatility", "Sharpe Ratio", "Max Drawdown"]
    v1 = [analysis1["risk_analysis"]["annual_volatility"],
          analysis1["risk_analysis"]["sharpe_ratio"],
          analysis1["risk_analysis"]["max_drawdown"]]
    v2 = [analysis2["risk_analysis"]["annual_volatility"],
          analysis2["risk_analysis"]["sharpe_ratio"],
          analysis2["risk_analysis"]["max_drawdown"]]

    fig_r = go.Figure()
    fig_r.add_trace(go.Bar(name=t1, x=metrics, y=v1, marker_color=C["blue"],
                           marker_line_width=0, text=[f"{v:.3f}" for v in v1],
                           textposition="outside", textfont=dict(color=C["white"], size=9)))
    fig_r.add_trace(go.Bar(name=t2, x=metrics, y=v2, marker_color=C["yellow"],
                           marker_line_width=0, text=[f"{v:.3f}" for v in v2],
                           textposition="outside", textfont=dict(color=C["white"], size=9)))

    fig_r.update_layout(**_base(310, f"{t1} vs {t2} · Risk Comparison",
                                barmode="group",
                                legend=dict(bgcolor=C["panel"], bordercolor=C["border"], borderwidth=1, font=dict(size=9))))
    fig_r.update_xaxes(**_xaxis())
    fig_r.update_yaxes(**_yaxis(zeroline=True, zerolinecolor=C["border"]))

    return fig_p, fig_r
