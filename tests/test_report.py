import unittest
from decimal import Decimal

from app.data import Sale, load_sales
from app.report import monthly_report, months_with_sales
from app.server import handle


def sale(date: str, product: str, units: int, revenue: str) -> Sale:
    return Sale(date=date, product=product, units=units, revenue=Decimal(revenue))


SAMPLE = [
    sale('2026-10-02', 'Hand grinder', 1, '39.90'),
    sale('2026-10-01', 'Coffee beans 1kg', 2, '37.00'),
    sale('2026-09-30', 'Coffee beans 1kg', 1, '18.50'),
]


class ReportTests(unittest.TestCase):
    def test_rows_of_the_month_sorted_by_date(self):
        r = monthly_report(SAMPLE, '2026-10')
        self.assertEqual([s['date'] for s in r.rows], ['2026-10-01', '2026-10-02'])
        self.assertEqual(r.total_units, 3)
        self.assertEqual(r.total_revenue, Decimal('76.90'))

    def test_month_without_sales_is_empty(self):
        r = monthly_report(SAMPLE, '2026-11')
        self.assertEqual(r.rows, [])
        self.assertEqual(r.total_revenue, Decimal('0.00'))

    def test_invalid_month_raises(self):
        with self.assertRaises(ValueError):
            monthly_report(SAMPLE, '2026-13')

    def test_fixture_data_loads(self):
        sales = load_sales()
        self.assertEqual(months_with_sales(sales), ['2026-09', '2026-10'])
        self.assertTrue(all(isinstance(s['revenue'], Decimal) for s in sales))


class ServerTests(unittest.TestCase):
    def test_report_page(self):
        status, headers, body = handle('/report?month=2026-10', SAMPLE)
        self.assertEqual(status, 200)
        self.assertIn(b'Hand grinder', body)
        self.assertIn(b'76.90', body)

    def test_empty_month_message(self):
        status, _, body = handle('/report?month=2026-11', SAMPLE)
        self.assertEqual(status, 200)
        self.assertIn(b'No sales for this month', body)

    def test_invalid_month_is_400(self):
        self.assertEqual(handle('/report?month=oct', SAMPLE)[0], 400)

    def test_root_redirects_to_latest_month(self):
        status, headers, _ = handle('/', SAMPLE)
        self.assertEqual(status, 302)
        self.assertEqual(headers['Location'], '/report?month=2026-10')

    def test_unknown_path_is_404(self):
        self.assertEqual(handle('/nope', SAMPLE)[0], 404)


if __name__ == '__main__':
    unittest.main()
