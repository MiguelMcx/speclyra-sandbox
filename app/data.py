"""Loading the sales data."""
import json
from decimal import Decimal
from pathlib import Path
from typing import TypedDict

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'sales.json'


class Sale(TypedDict):
    date: str          # ISO 8601, e.g. 2026-10-05
    product: str
    units: int
    revenue: Decimal


def load_sales(path: Path = DATA_FILE) -> list[Sale]:
    with open(path, encoding='utf-8') as f:
        raw = json.load(f)
    return [Sale(date=r['date'], product=r['product'], units=int(r['units']),
                 revenue=Decimal(r['revenue'])) for r in raw]
