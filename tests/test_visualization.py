import pytest

from src.visualization import (
    analyze_prices,
    build_dashboard_html,
    generate_html_report,
    generate_pdf_report,
)
from src.visualization.csv_data import parse_price_csv


def test_price_analysis_metrics():
    result = analyze_prices([100, 110, 99, 108], ["a", "b", "c", "d"], periods_per_year=3)
    assert result.timestamps == ("a", "b", "c", "d")
    assert result.returns == pytest.approx((0.1, -0.1, 108 / 99 - 1))
    assert result.total_return == pytest.approx(0.08)
    assert result.annualized_return == pytest.approx(0.08)
    assert result.max_drawdown == pytest.approx(0.1)


def test_dashboard_has_interactive_price_and_return_charts_and_safe_data():
    html = build_dashboard_html([10, 12, 11], ["x", "y", "</script>"])
    assert "plotly-2.35.2.min.js" in html
    assert "price-chart" in html and "return-chart" in html
    assert "\\u003c/script\\u003e" in html
    assert "Annualized volatility" in html


def test_reports_create_html_and_valid_pdf_and_write_files(tmp_path):
    html_path = tmp_path / "report.html"
    pdf_path = tmp_path / "report.pdf"
    report_html = generate_html_report([100, 102, 99], output_path=html_path)
    report_pdf = generate_pdf_report([100, 102, 99], output_path=pdf_path)
    assert "Report summary" in report_html
    assert html_path.read_text(encoding="utf-8") == report_html
    assert report_pdf.startswith(b"%PDF-1.4")
    assert b"xref" in report_pdf and b"%%EOF" in report_pdf
    assert pdf_path.read_bytes() == report_pdf


def test_csv_price_parser_accepts_date_and_price_headers():
    labels, prices = parse_price_csv("Date,Close\n2025-01-01,100\n2025-01-02,101\n")
    assert labels == ["2025-01-01", "2025-01-02"]
    assert prices == [100.0, 101.0]
    with pytest.raises(ValueError, match="column"):
        parse_price_csv("date,value\n2025-01-01,4\n")


@pytest.mark.parametrize(
    "prices,timestamps",
    [([100], None), ([100, 0], None), ([100, 101], ["only-one"])],
)
def test_dashboard_rejects_invalid_price_data(prices, timestamps):
    with pytest.raises(ValueError):
        analyze_prices(prices, timestamps)
