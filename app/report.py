"""Monthly report logic."""
import re
from dataclasses import dataclass
from decimal import Decimal

from app.data import Sale

MONTH = re.compile(r'^\d{4}-(0[1-9]|1[0-2])$')


@dataclass
class MonthlyReport:
    month: str
    rows: list[Sale]
    total_units: int
    total_revenue: Decimal


def is_valid_month(month: str) -> bool:
    return bool(MONTH.match(month))


def months_with_sales(sales: list[Sale]) -> list[str]:
    return sorted({s['date'][:7] for s in sales})


def monthly_report(sales: list[Sale], month: str) -> MonthlyReport:
    if not is_valid_month(month):
        raise ValueError(f'invalid month: {month!r}')
    rows = sorted((s for s in sales if s['date'].startswith(month + '-')),
                  key=lambda s: (s['date'], s['product']))
    return MonthlyReport(
        month=month,
        rows=rows,
        total_units=sum(s['units'] for s in rows),
        total_revenue=sum((s['revenue'] for s in rows), Decimal('0.00')),
    )
