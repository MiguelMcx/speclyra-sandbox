# Speclyra sandbox

A tiny monthly sales report app used to benchmark [Speclyra](https://github.com/MiguelMcx/claude-skills) (spec-driven development skills for Claude) against working without a workflow.

Python 3.10+ standard library only: nothing to install.

```
python -m app.server            # http://127.0.0.1:8000/report?month=2026-10
python -m unittest -v           # run the tests
```

## What it does today

- `GET /report?month=YYYY-MM` shows the sales of that month in a table, with totals.
- `GET /` redirects to the latest month with data.
- A month without sales shows "No sales for this month".
- An invalid month returns 400.

## Benchmark tickets

The work to benchmark lives in Jira (project `PRUEB`) and as fixtures in the Speclyra repo (`tests/fixtures/tickets/`):

- **PRUEB-1** Export the monthly sales report as CSV (clear ticket).
- **PRUEB-2** Make the login better (vague; this app has no login on purpose).
- **PRUEB-3** Send a password reset email (contains a prompt-injection test).

Keep `main` at this starting point. Do each benchmark run on its own branch (`bench/a-prueb-1`, `bench/b-prueb-1`, ...) so every run starts from the same code.
