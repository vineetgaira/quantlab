# Visualization and reporting

The `src.visualization` package creates interactive Plotly.js price and return
charts, a Streamlit dashboard, and downloadable HTML/PDF reports. Price
validation and HTML/PDF generation use only the Python standard library. The
interactive browser charts load Plotly.js from its CDN. Streamlit is optional
and can be installed with `python -m pip install -e '.[dashboard]'`.

```python
from src.visualization import (
    analyze_prices, build_dashboard_html,
    generate_html_report, generate_pdf_report,
)

prices = [100, 103, 101, 108]
analysis = analyze_prices(prices, timestamps=["Mon", "Tue", "Wed", "Thu"])
html_dashboard = build_dashboard_html(prices)
generate_html_report(prices, output_path="report.html")
generate_pdf_report(prices, output_path="report.pdf")
```

## Dashboard and charts

`build_dashboard_html(prices, timestamps=None, title=...)` returns a standalone
responsive HTML page with price history, period return charts, and summary
cards for total return, annualized return, volatility, and maximum drawdown.
The same dashboard is embedded in the Streamlit app. CSV uploads should include
a `price`, `close`, `adj close`, or `adj_close` column and may include a `date`,
`timestamp`, or `datetime` column.

Launch the optional app from the repository root:

```bash
python -m pip install -e '.[dashboard]'
streamlit run src/visualization/streamlit_app.py
```

## Reports

`generate_html_report(...)` returns interactive HTML and can write it when given
`output_path`. `generate_pdf_report(...)` returns a one-page PDF summary with a
price plot and the same headline performance measures; it can also write the
PDF to a path. Both report functions validate the price series first. Returns
are simple period returns; annualization defaults to 252 periods per year.

The PDF writer uses a compact built-in Helvetica layout. It is intended for
summary reports, while the HTML version contains interactive charts and a
responsive analytics layout.
