"""Optional Streamlit dashboard entry point.

Run from the repository root with ``streamlit run src/visualization/streamlit_app.py``.
Install the dashboard extra first: ``pip install -e '.[dashboard]'``.
"""

from src.visualization.csv_data import parse_price_csv
from src.visualization.dashboard import analyze_prices, build_dashboard_html
from src.visualization.reports import generate_html_report, generate_pdf_report


def main() -> None:
    try:
        import streamlit as st
    except ImportError as exc:
        raise SystemExit(
            "Streamlit is optional. Install it with: pip install -e '.[dashboard]'"
        ) from exc

    st.set_page_config(page_title="QuantLab", layout="wide")
    st.title("QuantLab Analytics Dashboard")
    uploaded = st.file_uploader("Upload a CSV with Date and Close/Price columns", type=["csv"])
    if uploaded is None:
        st.info("Upload a price history CSV to view interactive charts and analytics.")
        return
    try:
        labels, prices = parse_price_csv(uploaded.getvalue().decode("utf-8-sig"))
        analysis = analyze_prices(prices, labels)
    except (UnicodeDecodeError, ValueError) as exc:
        st.error(str(exc))
        return
    cols = st.columns(4)
    for column, label, value in zip(
        cols,
        ("Total return", "Annualized return", "Annualized volatility", "Maximum drawdown"),
        (analysis.total_return, analysis.annualized_return, analysis.annualized_volatility, analysis.max_drawdown),
    ):
        column.metric(label, f"{value:.2%}")
    st.components.v1.html(build_dashboard_html(prices, labels), height=900, scrolling=True)
    st.download_button(
        "Download HTML report", generate_html_report(prices, labels),
        file_name="quantlab_report.html", mime="text/html",
    )
    st.download_button(
        "Download PDF report", generate_pdf_report(prices, labels),
        file_name="quantlab_report.pdf", mime="application/pdf",
    )


if __name__ == "__main__":
    main()
