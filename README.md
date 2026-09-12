# notekeep

Learning project: clean Flask API with tests

Built for my own use; public in case it helps someone.

## Usage

```bash
curl -X POST localhost:5000/notes \
  -H 'content-type: application/json' \
  -d '{"title": "first", "body": "hello"}'
```

## Installation

```bash
pip install -r requirements.txt
flask --app app run --debug
```

## Highlights

- pytest coverage for the happy paths
- CRUD endpoints for notes
- SQLite storage via sqlite3 stdlib
- Request validation and consistent error shape

## Project structure

```text
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   └── configuration.md
├── tests/
│   └── test_api.py
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── app.py
└── requirements.txt
```

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

## License

MIT - see [LICENSE](LICENSE).
