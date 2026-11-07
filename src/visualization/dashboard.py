"""Interactive Plotly.js dashboard generation using standard-library inputs."""

import html
import json
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class PriceAnalysis:
    """Validated price series and common annualized performance measures."""

    timestamps: tuple[str, ...]
    prices: tuple[float, ...]
    returns: tuple[float, ...]
    total_return: float
    annualized_return: float
    annualized_volatility: float
    max_drawdown: float


def analyze_prices(
    prices: Iterable[float], timestamps: Sequence[object] | None = None,
    periods_per_year: int = 252,
) -> PriceAnalysis:
    """Validate prices and calculate returns, CAGR, volatility, and drawdown."""
    try:
        values = [float(value) for value in prices]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("prices must contain finite positive numbers") from exc
    if len(values) < 2 or any(not math.isfinite(value) or value <= 0 for value in values):
        raise ValueError("prices must contain at least two finite positive numbers")
    if isinstance(periods_per_year, bool) or not isinstance(periods_per_year, int) or periods_per_year < 1:
        raise ValueError("periods_per_year must be a positive integer")
    if timestamps is None:
        labels = [str(index) for index in range(len(values))]
    else:
        labels = [str(value) for value in timestamps]
        if len(labels) != len(values):
            raise ValueError("timestamps and prices must have equal lengths")
    returns = [values[i] / values[i - 1] - 1.0 for i in range(1, len(values))]
    if any(not math.isfinite(value) for value in returns):
        raise ValueError("prices produce non-finite returns")
    total_return = values[-1] / values[0] - 1.0
    years = (len(values) - 1) / periods_per_year
    annualized_return = (values[-1] / values[0]) ** (1.0 / years) - 1.0
    average = math.fsum(returns) / len(returns)
    variance = (
        math.fsum((value - average) ** 2 for value in returns) / (len(returns) - 1)
        if len(returns) > 1 else 0.0
    )
    volatility = math.sqrt(variance * periods_per_year)
    peak, max_drawdown = values[0], 0.0
    for value in values:
        peak = max(peak, value)
        max_drawdown = max(max_drawdown, (peak - value) / peak)
    return PriceAnalysis(
        tuple(labels), tuple(values), tuple(returns), total_return,
        annualized_return, volatility, max_drawdown,
    )


def build_dashboard_html(
    prices: Iterable[float], timestamps: Sequence[object] | None = None,
    title: str = "QuantLab Analytics Dashboard",
) -> str:
    """Return a standalone HTML dashboard with interactive Plotly.js charts."""
    data = analyze_prices(prices, timestamps)
    safe_title = html.escape(str(title))
    # Escape HTML-sensitive characters so data cannot terminate the script tag.
    payload = json.dumps(
        {"dates": data.timestamps, "prices": data.prices, "returns": data.returns},
        allow_nan=False,
    ).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    stats = [
        ("Total return", f"{data.total_return:.2%}"),
        ("Annualized return", f"{data.annualized_return:.2%}"),
        ("Annualized volatility", f"{data.annualized_volatility:.2%}"),
        ("Maximum drawdown", f"{data.max_drawdown:.2%}"),
    ]
    cards = "\n".join(
        f'<article class="card"><span>{label}</span><strong>{value}</strong></article>'
        for label, value in stats
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
body{{font:16px system-ui,sans-serif;margin:0;background:#f4f6fa;color:#172033}}main{{max-width:1100px;margin:auto;padding:28px}}
h1{{margin:0 0 20px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}}
.card{{background:white;padding:18px;border-radius:10px;box-shadow:0 1px 5px #18243a14}}.card span{{display:block;color:#637087;font-size:13px}}
.card strong{{display:block;margin-top:7px;font-size:23px}}.chart{{background:white;border-radius:10px;margin-top:18px;padding:8px}}
</style></head><body><main><h1>{safe_title}</h1><section class="cards">{cards}</section>
<section class="chart"><div id="price-chart" aria-label="Interactive price chart"></div></section>
<section class="chart"><div id="return-chart" aria-label="Interactive return chart"></div></section></main>
<script>const qdata={payload};
Plotly.newPlot('price-chart',[{{x:qdata.dates,y:qdata.prices,type:'scatter',mode:'lines',name:'Price',line:{{color:'#2563eb',width:2}}}}],
{{title:'Price history',xaxis:{{title:'Date'}},yaxis:{{title:'Price'}},margin:{{t:48,l:58,r:20,b:48}},paper_bgcolor:'white',plot_bgcolor:'white'}},{{responsive:true,displaylogo:false}});
Plotly.newPlot('return-chart',[{{x:qdata.dates.slice(1),y:qdata.returns.map(v=>v*100),type:'bar',name:'Return',marker:{{color:'#0f9f77'}}}}],
{{title:'Period returns',xaxis:{{title:'Date'}},yaxis:{{title:'Return (%)'}},margin:{{t:48,l:58,r:20,b:48}},paper_bgcolor:'white',plot_bgcolor:'white'}},{{responsive:true,displaylogo:false}});
</script></body></html>"""
