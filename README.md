# Flask Product CRUD

A simple Flask + SQLite CRUD app with Bootstrap UI.

## Local Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app app:create_app init-db
flask --app app:create_app run --host 0.0.0.0 --port 5050
```

## Deployment
- WSGI entrypoint: `wsgi:app`
- Procfile: `web: gunicorn --bind 0.0.0.0:$PORT wsgi:app`

### Render
- Create new Web Service from this repo
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`
- Environment: `PYTHON_VERSION=3.12`, optionally set `SECRET_KEY`

### GitHub Pages
Not applicable for Flask server apps. Use Render, Railway, Fly.io, or similar.

## License
MIT
# Two-tire-flask-app
