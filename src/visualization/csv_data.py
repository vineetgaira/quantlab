"""CSV parsing helpers for the optional dashboard application."""

import csv
import io


def parse_price_csv(content: str) -> tuple[list[str], list[float]]:
    """Read a CSV with a price/close column and optional date/timestamp column."""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("CSV content must not be empty")
    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        raise ValueError("CSV must include a header row")
    fields = {name.strip().lower(): name for name in reader.fieldnames if name}
    price_column = next((fields[key] for key in ("price", "close", "adj close", "adj_close") if key in fields), None)
    if price_column is None:
        raise ValueError("CSV must contain a price, close, adj close, or adj_close column")
    date_column = next((fields[key] for key in ("date", "timestamp", "datetime") if key in fields), None)
    labels, prices = [], []
    try:
        for index, row in enumerate(reader):
            prices.append(float(row[price_column]))
            labels.append(row[date_column] if date_column else str(index))
    except (TypeError, ValueError, KeyError, OverflowError) as exc:
        raise ValueError("CSV contains an invalid price row") from exc
    if not prices:
        raise ValueError("CSV contains no price rows")
    return labels, prices
