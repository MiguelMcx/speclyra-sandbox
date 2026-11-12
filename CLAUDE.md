# Speclyra sandbox

## Stack
Python 3.10+, standard library only. No dependencies may be added.

## Tests
`python -m unittest -v` runs everything. Tests live in `tests/` and use `unittest`. All tests must pass before a task is considered done.

## Code conventions
- Business logic in `app/report.py` and `app/data.py` as plain functions; `app/server.py` only does HTTP.
- Money uses `decimal.Decimal`, never float.
- Type hints on public functions. Keep functions small.

## Commits
Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).

## Do not touch
- `data/sales.json` is fixture data: do not edit it; generate extra data in tests instead.
