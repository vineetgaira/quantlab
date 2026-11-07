"""HTML and minimal vector PDF report generation."""

import html
from pathlib import Path
from collections.abc import Iterable, Sequence

from .dashboard import analyze_prices, build_dashboard_html


def generate_html_report(
    prices: Iterable[float], timestamps: Sequence[object] | None = None,
    title: str = "QuantLab Performance Report", output_path: str | Path | None = None,
) -> str:
    """Create an interactive HTML report; optionally write it to a file."""
    values = list(prices)
    labels = list(timestamps) if timestamps is not None else None
    dashboard = build_dashboard_html(values, labels, title)
    analysis = analyze_prices(values, labels)
    table_rows = "".join(
        f"<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>"
        for label, value in (
            ("Observations", str(len(analysis.prices))),
            ("First price", f"{analysis.prices[0]:.6g}"),
            ("Last price", f"{analysis.prices[-1]:.6g}"),
            ("Total return", f"{analysis.total_return:.2%}"),
            ("Annualized return", f"{analysis.annualized_return:.2%}"),
            ("Annualized volatility", f"{analysis.annualized_volatility:.2%}"),
            ("Maximum drawdown", f"{analysis.max_drawdown:.2%}"),
        )
    )
    report = dashboard.replace(
        "</main>",
        f'<section class="chart"><h2>Report summary</h2><table>{table_rows}</table></section></main>',
    ).replace(
        "</style>",
        "table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:9px;border-bottom:1px solid #e5e9f0}th{color:#637087}</style>",
    )
    if output_path is not None:
        Path(output_path).write_text(report, encoding="utf-8")
    return report


def generate_pdf_report(
    prices: Iterable[float], timestamps: Sequence[object] | None = None,
    title: str = "QuantLab Performance Report", output_path: str | Path | None = None,
) -> bytes:
    """Create a one-page PDF summary and price chart without extra dependencies."""
    data = analyze_prices(prices, timestamps)
    commands = ["0.12 0.16 0.24 rg"]

    def text(x: float, y: float, value: str, size: int = 11) -> None:
        plain = value.encode("latin-1", "replace").decode("latin-1")
        plain = " ".join(plain.split())
        escaped = plain.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        commands.append(f"BT /F1 {size} Tf {x:.2f} {y:.2f} Td ({escaped}) Tj ET")

    text(48, 748, title, 20)
    text(48, 718, f"Observations: {len(data.prices)}    First: {data.prices[0]:.6g}    Last: {data.prices[-1]:.6g}")
    text(48, 696, f"Total return: {data.total_return:.2%}    Annualized return: {data.annualized_return:.2%}")
    text(48, 674, f"Annualized volatility: {data.annualized_volatility:.2%}    Maximum drawdown: {data.max_drawdown:.2%}")
    left, bottom, width, height = 52.0, 400.0, 508.0, 220.0
    low, high = min(data.prices), max(data.prices)
    span = high - low or 1.0
    points = [
        (left + width * i / (len(data.prices) - 1), bottom + height * (value - low) / span)
        for i, value in enumerate(data.prices)
    ]
    commands.extend(["0.15 0.40 0.86 RG", "1.8 w"])
    commands.append(f"{points[0][0]:.2f} {points[0][1]:.2f} m")
    commands.extend(f"{x:.2f} {y:.2f} l" for x, y in points[1:])
    commands.extend(["S", "0.55 0.60 0.68 RG", "0.6 w", f"{left} {bottom} m {left + width} {bottom} l S"])
    text(48, 370, f"Period return observations: {len(data.returns)}", 10)
    content = "\n".join(commands).encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    result = bytes(pdf)
    if output_path is not None:
        Path(output_path).write_bytes(result)
    return result
