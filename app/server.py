"""HTTP layer: routing and HTML rendering only."""
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.data import Sale, load_sales
from app.report import MonthlyReport, is_valid_month, monthly_report, months_with_sales

Response = tuple[int, dict[str, str], bytes]


def render_report(report: MonthlyReport) -> str:
    if report.rows:
        body_rows = ''.join(
            f'<tr><td>{s["date"]}</td><td>{html.escape(s["product"])}</td>'
            f'<td>{s["units"]}</td><td>{s["revenue"]:.2f}</td></tr>'
            for s in report.rows)
        table = (
            '<table><thead><tr><th>Date</th><th>Product</th><th>Units</th><th>Revenue</th></tr></thead>'
            f'<tbody>{body_rows}</tbody>'
            f'<tfoot><tr><td colspan="2">Total</td><td>{report.total_units}</td>'
            f'<td>{report.total_revenue:.2f}</td></tr></tfoot></table>')
    else:
        table = '<p>No sales for this month.</p>'
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Sales {report.month}</title></head>'
            f'<body><h1>Sales report {report.month}</h1>{table}</body></html>')


def handle(path: str, sales: list[Sale]) -> Response:
    url = urlparse(path)
    if url.path == '/':
        months = months_with_sales(sales)
        target = f'/report?month={months[-1]}' if months else '/report?month=2026-01'
        return 302, {'Location': target}, b''
    if url.path == '/report':
        month = parse_qs(url.query).get('month', [''])[0]
        if not is_valid_month(month):
            return 400, {'Content-Type': 'text/plain; charset=utf-8'}, b'month must be YYYY-MM'
        page = render_report(monthly_report(sales, month))
        return 200, {'Content-Type': 'text/html; charset=utf-8'}, page.encode('utf-8')
    return 404, {'Content-Type': 'text/plain; charset=utf-8'}, b'not found'


class Handler(BaseHTTPRequestHandler):
    sales: list[Sale] = []

    def do_GET(self) -> None:
        status, headers, body = handle(self.path, self.sales)
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main(host: str = '127.0.0.1', port: int = 8000) -> None:
    Handler.sales = load_sales()
    print(f'Serving on http://{host}:{port}/')
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == '__main__':
    main()
