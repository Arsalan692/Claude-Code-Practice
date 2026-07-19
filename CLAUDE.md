# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask expense tracker built incrementally as a **step-by-step learning project**. Routes and modules are deliberately left as stubs until the corresponding lesson step is reached — do not "complete" unimplemented features unless the user asks you to build that specific step. Comments like `# Students will write this file in Step 1` or `Placeholder routes — students will implement these` mark intentional scaffolding, not oversights.

## Commands

- Run the dev server: `python app.py` (serves on `http://localhost:5001`, `debug=True`)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest` (test suite not yet written — `pytest` and `pytest-flask` are listed in requirements.txt for when it is)

There is no build step, linter, or frontend toolchain — templates and static assets are served directly by Flask.

## Folder structure

```
expense-tracker/
├── app.py                  # Flask app entrypoint — all routes live here
├── requirements.txt        # flask, werkzeug, pytest, pytest-flask
├── database/
│   ├── __init__.py         # empty
│   └── db.py                # stub — get_db()/init_db()/seed_db() not yet implemented
├── templates/               # Jinja2 templates (all extend base.html)
│   ├── base.html            # shared layout: navbar, footer, content block
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── terms.html
│   └── privacy.html
├── static/
│   ├── css/
│   │   └── style.css        # single global stylesheet
│   └── js/
│       └── main.js          # single global script (landing page video modal)
└── venv/                    # local virtualenv, gitignored
```

Notes:
- `expense_tracker.db` (SQLite file) will be created at the project root once `db.py` is implemented; it's gitignored.
- No `tests/` directory exists yet despite `pytest`/`pytest-flask` being in requirements.txt.

## Architecture

- `app.py` — single Flask app with all routes. No blueprints; new routes are added directly here as steps are implemented.
- `database/db.py` — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables via `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample data). Currently a stub — implement per the comments in that file when asked.
- `templates/` — Jinja2 templates. `base.html` is the shared layout (navbar, footer, `{% block content %}`) that all pages extend; page-specific templates only fill in blocks.
- `static/css/style.css` — single global stylesheet for the whole site.
- `static/js/main.js` — single global script; currently just powers the "How it works" video modal on the landing page (set `HOW_IT_WORKS_VIDEO_URL` there to enable it).
- The SQLite database file (`expense_tracker.db`) is gitignored and created locally via `init_db()`/`seed_db()` once implemented.

## Conventions

- Keep everything in the existing single-file structure (one `app.py`, one `db.py`, one `style.css`, one `main.js`) unless the user directs otherwise — this mirrors the tutorial's step progression and splitting things up prematurely will conflict with later steps.
- New pages should extend `base.html` and follow the existing block structure (`title`, `head`, `content`, `scripts`).
