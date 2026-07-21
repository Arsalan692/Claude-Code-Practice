# Spec: Profile Page

## Overview
This step replaces the placeholder `/profile` view ("Profile page — coming in Step 4") with a real, read-only profile page for signed-in users. It shows the user's account details (name, email, member since), a quick summary of their expense activity (total expenses logged, total amount spent), a spending-by-category breakdown, and a recent-expenses table — all pulled from the `expenses` table. This gives users a home base to land on after login before expense CRUD (add/edit/delete) is built out in later steps. Editing profile details (name/email/password) and full expense CRUD remain out of scope for this step — this page is display-only, aside from linking to the existing `/expenses/add` placeholder from the empty state.

**Note:** this was extended beyond the original spec (which only covered the header card + the two summary tiles) at the user's request, to also include a category breakdown chart, a recent-expenses table, and a zero-state. This document has been updated after the fact to describe what was actually built.

## Depends on
- Step 1 — Database setup (`.claude/specs/01-database-setup.md`), already complete. Requires `get_db()` and the `users` / `expenses` tables to exist.
- Step 3 — Login and Logout (`.claude/specs/03-login-logout.md`), already complete. Requires the `login_required` decorator and an active `session["user_id"]` to identify the current user.

## Routes
- `GET /profile` — already existed as a placeholder; now renders the full profile view (account details, expense summary, category breakdown, recent expenses) — logged-in

## Database changes
No database changes. Uses the existing `users` table (`id`, `name`, `email`, `created_at`) and `expenses` table (`user_id`, `amount`, `category`, `date`, `description`) as defined in `database/db.py`. The view runs three read queries against `expenses` for the current `user_id`:
- `COUNT(*)` / `COALESCE(SUM(amount), 0)` — total expenses logged and total spent (`NULL` on zero rows coalesced to `0`)
- `SELECT category, SUM(amount) AS total ... GROUP BY category ORDER BY total DESC` — category breakdown, used to compute each category's percentage of total spend
- `SELECT amount, category, date, description ... ORDER BY date DESC, id DESC LIMIT 10` — the 10 most recent expenses

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; renders:
  - A header card: avatar (initials), name, email, member-since date
  - Two summary tiles: total expenses logged, total amount spent (reusing `.mock-label`/`.mock-total`)
  - A "Spending by Category" card — reuses the existing `.mock-card-header`/`.mock-bars`/`.mock-bar-row`/`.mock-cat`/`.mock-bar-track`/`.mock-bar`/`.mock-amt` classes from the landing-page hero mock, with real per-category totals and bar widths driven by each category's share of total spend
  - A "Recent Expenses" table (date, category badge, description, right-aligned amount) capped at the 10 most recent, with a "showing N of M" note when there are more
  - A zero-state card (icon, heading, supporting copy, CTA to `/expenses/add`) shown instead of the category card/table when the user has no expenses
- **Modify:**
  - `templates/base.html` — wrap the existing `Hi, {{ session.name }}` greeting in `.nav-links` with a link to `{{ url_for('profile') }}` so signed-in users have a way to reach the profile page from the navbar

## Files to change
- `app.py`:
  - `profile` view (already decorated with `@login_required`) now queries the user row, expense stats, per-category totals, and the 10 most recent expenses; computes initials, formatted member-since date, per-category percentages/bar-color classes, and formatted recent-expense rows; renders `profile.html` with all of it
- `templates/base.html`:
  - Navbar greeting is now a link to `/profile`
- `static/css/style.css`:
  - New "Profile page" section: header card, avatar, summary tiles, category card, expenses table, category badge, empty-state card, and responsive rules at `900px`/`600px` (table collapses to stacked cards on mobile)
  - Added `.mock-bar-5` through `.mock-bar-8` as translucent tints of the existing four data-series colors, to extend the bar-chart palette to more than 4 categories per the frontend-design skill's guidance ("desaturate/lighten these four rather than introducing a hue outside this warm-muted family")

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (not touched in this step — no password display or editing)
- Use CSS variables — never hardcode hex values (the `.mock-bar-5`–`.mock-bar-8` tints use `rgba()` derived from the existing accent/accent-2/blue/plum hex values, since CSS custom properties can't be alpha-blended without `color-mix()`)
- All templates extend `base.html`
- Do not expose `password_hash` to the template context
- Handle the zero-expenses case cleanly: dedicated empty-state card, and "0"/"Rs 0.00" in the summary tiles rather than `None`/`null`
- Currency is displayed with the `Rs` prefix (Pakistani Rupee), matching the rest of the app (`landing.html`, footer tagline) — not `$` or `₹`

## Definition of done
- [x] Visiting `/profile` while signed out redirects to `/login` (unchanged behavior from Step 3)
- [x] Visiting `/profile` while signed in renders the full profile page instead of the placeholder string
- [x] The profile page shows the correct name, email, and member-since date for the logged-in user
- [x] The profile page shows the correct total expense count and total amount spent (verified against the seeded demo user's 8 expenses, Rs 383.74)
- [x] The category breakdown shows each distinct category with a correctly proportioned bar and correct Rs total (verified: 7 categories for the demo user, bar widths summing proportionally to 100%)
- [x] The recent-expenses table shows up to 10 rows, most recent first, with a "showing N of M" note only when there are more than 10
- [x] A newly registered user with no expenses sees the empty-state card (not "0 expenses"/"Rs 0.00" summary tiles with an otherwise-empty category/table section)
- [x] The navbar greeting links to `/profile` from any page when signed in
- [x] The expenses table collapses to a stacked, labeled layout at the `600px` breakpoint instead of overflowing horizontally
- [x] App starts and runs with no errors via `python app.py`
