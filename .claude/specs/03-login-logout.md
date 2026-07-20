# Spec: Login and Logout

## Overview
This step implements session-based authentication for Spendly. `/login` currently only renders `login.html` on GET — the form posts to `/login` but there is no handler for it, and `/logout` is a placeholder that returns a plain string. This step wires up the `POST /login` handler to verify credentials against the `users` table and start a Flask session, adds a real `/logout` that clears the session, and introduces a `login_required` decorator to protect the pages that only make sense for a signed-in user (`/profile` and the `/expenses/*` placeholder routes). The navbar in `base.html` is also updated to reflect signed-in vs signed-out state. This builds directly on Step 2 (Registration), which creates the `users` rows this step authenticates against.

## Depends on
- Step 1 — Database setup (`.claude/specs/01-database-setup.md`), already complete. Requires `get_db()` and the `users` table to exist.
- Step 2 — Registration (`.claude/specs/02-registration.md`), already complete. Requires `POST /register` to create rows in `users` with hashed passwords.

## Routes
- `GET /login` — render the empty login form — public (already exists, unchanged)
- `POST /login` — validate credentials, start a session, redirect to `/profile` on success or re-render the form with an error — public
- `GET /logout` — clear the session and redirect to `/login` — logged-in
- `GET /profile` — protected by `login_required`; view stays a placeholder string for this step ("Profile page — coming in Step 4"), only the access control changes — logged-in
- `GET /expenses/add` — protected by `login_required`, otherwise unchanged placeholder — logged-in
- `GET /expenses/<int:id>/edit` — protected by `login_required`, otherwise unchanged placeholder — logged-in
- `GET /expenses/<int:id>/delete` — protected by `login_required`, otherwise unchanged placeholder — logged-in

## Database changes
No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports authentication as defined in `database/db.py`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — no structural changes needed; it already posts to `/login` and can render `{{ error }}` the same way `register.html` does. Only touch it if `{% if error %}` markup for the error banner is missing (check the `auth-error` block used in `register.html` and mirror it here if absent).
  - `templates/base.html` — update `.nav-links` to show "Sign in" / "Get started" when no user is in the session, and a user's name plus a "Log out" link (`{{ url_for('logout') }}`) when one is. Gate this with `{% if session.user_id %}` / `{% else %}`.

## Files to change
- `app.py`:
  - Set `app.secret_key` (read from an environment variable, e.g. `os.environ.get("SECRET_KEY", "dev")`, since there's no config layer yet)
  - Add a `login_required` decorator (using `functools.wraps`) that checks `session.get("user_id")` and redirects to `/login` if absent
  - Update the `login` view to accept `GET` and `POST`: on POST, look up the user by email, verify the password with `check_password_hash`, store `user_id` and `name` in the session on success, and redirect to `/profile`; on failure, re-render `login.html` with a generic "Invalid email or password" error (do not reveal whether the email exists)
  - Replace the placeholder `logout` view with one that calls `session.clear()` and redirects to `/login`
  - Apply `@login_required` to `profile`, `add_expense`, `edit_expense`, `delete_expense`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` pairs with the `generate_password_hash` already used in `database/db.py` and `app.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with werkzeug (`check_password_hash`) — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only non-sensitive identifiers in the session (`user_id`, `name`) — never the password or password hash
- Use a generic error message for failed login ("Invalid email or password") so the response doesn't disclose whether the email is registered
- `login_required` must redirect unauthenticated users to `/login`, not raise or 403

## Definition of done
- [ ] Submitting `/login` with a valid, registered email and correct password redirects to `/profile` and the navbar shows the signed-in state
- [ ] Submitting `/login` with a correct email and wrong password re-renders `login.html` with an "Invalid email or password" error and does not start a session
- [ ] Submitting `/login` with an email that isn't registered re-renders `login.html` with the same generic error (no distinct message)
- [ ] Visiting `/logout` while signed in clears the session and redirects to `/login`; the navbar reverts to the signed-out state
- [ ] Visiting `/profile`, `/expenses/add`, `/expenses/<id>/edit`, or `/expenses/<id>/delete` while signed out redirects to `/login` instead of showing the placeholder text
- [ ] Visiting those same routes while signed in shows the existing placeholder text as before
- [ ] `GET /login` still renders the empty form with no errors
- [ ] App starts and runs with no errors via `python app.py`
