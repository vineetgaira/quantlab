"""Interactive analytics dashboards and HTML/PDF reports."""

from .dashboard import PriceAnalysis, analyze_prices, build_dashboard_html
from .reports import generate_html_report, generate_pdf_report

__all__ = [
    "PriceAnalysis", "analyze_prices", "build_dashboard_html",
    "generate_html_report", "generate_pdf_report",
]
