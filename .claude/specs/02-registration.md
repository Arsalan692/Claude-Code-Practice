# Spec: Registration

## Overview
This step implements user registration for Spendly. Currently `/register` only renders `register.html` on GET — the form posts to `/register` but there is no handler for it. This step wires up the POST handler so a visitor can create an account: validate the submitted name/email/password, hash the password with werkzeug, insert a new row into `users`, and redirect to the login page so they can sign in. This is the first "real" feature step built on top of the database layer from Step 1, and it does not introduce sessions — that's Step 3 (Login and Logout).

## Depends on
- Step 1 — Database setup (`.claude/specs/01-database-setup.md`), already complete. Requires `get_db()` and the `users` table to exist.

## Routes
- `GET /register` — render the empty registration form — public (already exists, unchanged)
- `POST /register` — validate input, create the user, redirect to login on success or re-render the form with an error — public

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports registration as defined in `database/db.py`.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — no structural changes needed; it already posts to `/register` and renders `{{ error }}` via the existing `auth-error` block, so validation/duplicate-email errors from the new POST handler will display automatically. Only touch it if a field needs to keep its submitted value after a failed submit (e.g. re-populate `name`/`email` with `value="{{ name or '' }}"`).

## Files to change
- `app.py` — update the `register` view to accept `GET` and `POST`, validate form input, hash the password, insert the user, and redirect to `/login` on success

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already used in `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate required fields (`name`, `email`, `password`) are non-empty before inserting
- Enforce a minimum password length of 8 characters (matches the placeholder text already in `register.html`)
- Catch the `sqlite3.IntegrityError` from the `email UNIQUE` constraint and re-render the form with a friendly "email already registered" error instead of a 500
- Never store or log plaintext passwords

## Definition of done
- [ ] Submitting the registration form with valid, unique data creates a row in `users` with a hashed (not plaintext) password
- [ ] After successful registration, the browser is redirected to `/login`
- [ ] Submitting with an email that already exists re-renders `register.html` with an error message and does not create a duplicate row
- [ ] Submitting with a missing name, email, or password re-renders `register.html` with an error message and does not hit the database
- [ ] Submitting with a password under 8 characters re-renders `register.html` with an error message
- [ ] `GET /register` still renders the empty form with no errors
- [ ] App starts and runs with no errors via `python app.py`
