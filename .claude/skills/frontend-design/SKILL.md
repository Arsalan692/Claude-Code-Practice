---
name: spendly-frontend-design
description: Design and build frontend pages, screens, and UI components for the Spendly expense-tracking web app, following Spendly's warm-editorial design system (warm paper backgrounds, forest-green + amber accents, DM Serif Display headings with DM Sans body text, vanilla HTML/CSS + Flask/Jinja templates). Use whenever the user asks to design, redesign, build, or improve any Spendly page or component — dashboards, auth pages, landing/marketing pages, settings, forms, tables, modals, empty states, alerts, badges, pagination, charts, or any new screen. Also trigger for improving UI/UX, layout, spacing, typography, color usage, responsiveness, or visual hierarchy on an existing page, or keeping a new screen visually consistent with the rest of the product. Trigger even without the word "design" — e.g. "add a transactions page," "make settings nicer," "build a modal for X," "add a status badge."
---

# Spendly Frontend Design

Spendly's identity is **warm editorial**, not generic SaaS-blue: warm paper
background, deep forest green + amber accents, a serif display face for
headings paired with a clean sans body face. Every page must read as if it
shipped from the same design file as the rest of the product — nothing here
should be designed in a vacuum.

Stack: vanilla HTML/CSS, Flask + Jinja2 templates (`{% extends "base.html" %}`),
no framework, no component library.

## Design identity, locked in

- **Fixed, don't drift toward generic SaaS defaults.** Resist the pull toward
  indigo/blue primary colors, Inter/system-ui-only type, or flat 8px-corner
  "modern SaaS" defaults — those are exactly what this system deliberately
  avoids. The forest green (`--accent`), amber (`--accent-2`), warm paper
  background, and serif display headings are the whole point.
- **Reuse before inventing.** For components that already exist (buttons,
  cards, forms, nav, modal), reuse the existing classes/patterns verbatim.
  For genuinely new component types, follow the "Extending into uncovered
  territory" section below — those extensions are derived directly from the
  tokens already in use, so following them keeps new work indistinguishable
  in spirit from the original.
- **Headings are always the display serif**, body/UI text is always DM Sans.
  Don't introduce a third typeface or use the serif for body copy or the sans
  for headings.

## Before doing anything

1. Check the **canonical stylesheet** and **canonical page shell** at the
   bottom of this file (Appendix A and B) — never guess at colors, radii,
   spacing, or fonts; every one of them already exists as a CSS custom
   property or an established value there.
2. Skim the **token reference** below for the full table (colors, type
   scale, spacing values in use, radius scale, shadow levels, breakpoints).
3. If the request touches something not yet in the codebase (a table,
   dashboard tile, badge, alert, empty state, pagination, chart, or dark
   mode), use the locked-in extension pattern in "Extending into uncovered
   territory" before inventing your own.

---

## Design Tokens (canonical)

This is the single source of truth for Spendly's visual identity, extracted
directly from the live stylesheet (Appendix A — always diff new work against
it, don't reinvent tokens from memory).

### Color

| Token | Value | Use |
|---|---|---|
| `--ink` | `#0f0f0f` | Primary text, primary button fill, footer bg |
| `--ink-soft` | `#2d2d2d` | Secondary headings, label text on light bg |
| `--ink-muted` | `#6b6b6b` | Body copy, subtitles, nav links |
| `--ink-faint` | `#a0a0a0` | Placeholder text, timestamps, least-important copy |
| `--paper` | `#f7f6f3` | Page background, primary button text (on ink) |
| `--paper-warm` | `#f0ede6` | Section background for contrast bands, modal-close bg |
| `--paper-card` | `#ffffff` | Card/panel surfaces sitting on `--paper` |
| `--accent` | `#1a472a` (deep forest green) | Primary brand accent — links, hover states, active bars, focus border |
| `--accent-light` | `#e8f0eb` | Accent-tinted backgrounds (badges, subtle highlights) |
| `--accent-2` | `#c17f24` (amber/gold) | Secondary accent — second data series, alternate highlights |
| `--accent-2-light` | `#fdf3e3` | Amber-tinted backgrounds |
| `--danger` | `#c0392b` | Errors, destructive actions |
| `--danger-light` | `#fdecea` | Error banner backgrounds |
| `--border` | `#e4e1da` | Default hairline borders on cards, inputs, dividers |
| `--border-soft` | `#eeebe4` | Lighter internal dividers (inside cards) |

**Extended data-series colors** (used in the landing hero mock chart, extend
this palette for any chart/graph work rather than inventing new hues):
`--accent` (green) → `--accent-2` (amber) → `#5b7fa6` (muted blue) → `#8b5e83`
(muted plum). If a 5th+ series is ever needed, desaturate/lighten these four
rather than introducing a hue outside this warm-muted family.

### Typography

| Token | Value |
|---|---|
| `--font-display` | `'DM Serif Display', Georgia, serif` — all headings (h1–h3, card titles, brand moments) |
| `--font-body` | `'DM Sans', system-ui, sans-serif` — body copy, UI labels, buttons, nav |

Loaded via Google Fonts: `DM+Serif+Display:ital@0;1` and `DM+Sans:wght@300;400;500;600`.
Only these two families and these weights exist in the system — don't add new
weights or families without a strong reason.

**Scale in use** (approximate, derived from existing pages):
- Hero/display: `clamp(2.5rem, 5vw, 4rem)`, line-height 1.1, letter-spacing -0.02em
- Section title (CTA, legal): `clamp(1.75rem, 3vw, 2.75rem)`
- Auth title: `2rem`
- Card/feature title: `1.2rem`
- Modal title: `1.3rem`
- Body: `1rem` / `0.9rem–0.95rem` for secondary copy
- Micro labels (badges, mock labels, uppercase eyebrow text): `0.75rem–0.85rem`,
  often `text-transform: uppercase; letter-spacing: 0.06em–0.08em; font-weight: 600`
- Base line-height: `1.6` (body), `1.7–1.75` for longer-form copy (feature/legal body)

### Spacing & Radius

| Token | Value |
|---|---|
| `--radius-sm` | `6px` — buttons, inputs, small controls |
| `--radius-md` | `12px` — cards (feature/auth/legal cards) |
| `--radius-lg` | `20px` — hero mock card, modal box |
| pill | `999px` — badges, progress-bar tracks, avatar/icon circles |

Spacing is rem-based and loosely follows an 8px-derived rhythm, but isn't a
strict single-unit grid — common values in use: `0.4rem, 0.5rem, 0.6rem,
0.65rem, 0.75rem, 0.875rem, 1rem, 1.25rem, 1.5rem, 1.75rem, 2rem, 2.5rem, 3rem,
4rem, 5rem, 6rem`. Prefer values from this existing list over inventing new
ones. Section vertical padding tends to be generous (`4rem–6rem` top/bottom on
desktop); card internal padding is `2rem` (or `2.5rem` for legal cards).

### Layout

| Token | Value |
|---|---|
| `--max-width` | `1200px` — main content max-width, centered |
| `--auth-width` | `440px` — auth forms (narrow, focused) |
| Legal container | `760px` — long-form reading content |

### Elevation / Shadow

No `--shadow` custom properties exist yet, but two concrete values are in use —
treat these as the two elevation levels until more are needed:
- Card resting elevation (hero mock card): `0 8px 40px rgba(0,0,0,0.06)` — subtle, soft
- Overlay/modal elevation: `0 20px 60px rgba(0,0,0,0.3)` — pronounced, for content floating above a scrim

### Motion

Transitions are short and purposeful, never decorative: `0.2s` for
color/background/border changes on hover/focus, `0.6s ease` for the one
data-driven animation in the system (bar-chart width fill). Don't add spring
physics, bounce, or long (>300ms) transitions for simple state changes.

### Breakpoints

- `900px` — hero collapses to single column, features grid collapses to 1 column, hero visual hides
- `600px` — nav links collapse (keep CTA + logout only), hero padding tightens

Design mobile-first in spirit even though the CSS is written desktop-first
with max-width media queries — always check both breakpoints when building
new layouts.

---

## Extending into uncovered territory

The current codebase only has: navbar, footer, hero, feature cards, CTA
section, auth forms, a modal, and legal pages. Real product work will need
components that don't exist yet — dashboards, tables, badges, alerts, empty
states, pagination, dark mode, etc. This gives locked-in extensions for those
gaps, built strictly from the tokens above so they feel native to the system
rather than bolted on.

**Rule of thumb**: before inventing a new pattern, check Appendix A for
something close (a card, a badge-like pill, a bar) and adapt it. Only use the
patterns below when nothing close exists.

### Data tables (transaction lists, expense history)

- Row height generous enough for touch: ~52–56px
- Header row: `--paper-warm` background, `--ink-soft` text, `0.8rem`,
  `font-weight: 600`, `text-transform: uppercase`, `letter-spacing: 0.06em` —
  matches the `.mock-label` treatment already in the system
- Row borders: `1px solid var(--border-soft)` between rows, no vertical
  borders (this system never uses vertical table rules)
- Row hover: background shifts to `--paper-warm`, `0.2s` transition
- Numeric columns (amounts): right-aligned, `--font-body`, `font-weight: 500`,
  same treatment as `.mock-amt`
- Wrap tables in a card: `--paper-card` background, `--radius-md`, `1px solid
  var(--border)`, matching `.feature-card`/`.auth-card`
- On mobile (≤600px), collapse rows into stacked blocks (hide `<thead>`,
  stack each cell full-width) rather than allowing horizontal scroll

### Badges / tags / status pills

Base on the existing `.hero-badge` pattern (pill radius `999px`, uppercase,
`0.75rem`, `font-weight: 600`, `letter-spacing: 0.08em`, generous horizontal
padding ~`0.85rem`, tight vertical padding ~`0.35rem`). Vary only the color pair:

- Success / positive: `--accent` on `--accent-light`
- Warning / attention: `--accent-2` on `--accent-2-light`
- Danger / overdue: `--danger` on `--danger-light`
- Neutral / default: `--ink-muted` on `--paper-warm`

### Alerts / inline banners

Extend `.auth-error` (already exists: `--danger-light` bg, `--danger` text,
`--radius-sm`, `1px solid #f5c6c2`, `0.75rem 1rem` padding). Build the sibling
success/info variants the same way, swapping in the accent-light/accent pair
for success and a neutral `--paper-warm`/`--ink-soft` pair for info.

### Empty states

Center-aligned within a card (`--paper-card`, `--radius-md`, generous padding
~`3rem 2rem`). Use an oversized icon or glyph in `--ink-faint`, a
`--font-display` short headline (`1.2rem`, matching `.feature-title`), a
`--ink-muted` supporting line, and a `.btn-primary` or `.btn-ghost` call to
action — reuse those button classes verbatim.

### Pagination / step controls

Small pill or square buttons, `--radius-sm`, `1px solid var(--border)`,
`--ink-soft` text, hover matches `.btn-ghost` hover (`border-color: var(--ink)`,
`color: var(--ink)`). Active/current page: `--ink` background, `--paper` text —
mirrors the `.btn-primary` / `.nav-cta` solid treatment.

### Toasts / notifications

Float above content like the modal (`box-shadow: 0 20px 60px rgba(0,0,0,0.3)`,
`--radius-md`), `--paper-card` background, slide/fade in over `0.2s`. Never
exceed the system's existing transition speed — no bounce.

### Dashboard summary cards (KPI tiles)

Follow the hero `.mock-card` pattern directly: `--paper-card`, `1px solid
var(--border)`, `--radius-lg`, header row with an uppercase `--ink-muted`
label and a large `--font-display` number, divided from any body content by
`1px solid var(--border-soft)`.

### Charts / graphs

Use the bar-chart pattern already established (`.mock-bar-track` /
`.mock-bar`): track is `--border-soft` at `999px` radius, filled bar uses the
data-series palette above in order (green → amber → muted blue → muted
plum). For line/area charts not yet in the codebase, use the same palette and
keep fills semi-transparent tints of the same colors (don't introduce a
separate chart-only palette).

### Dark mode (not yet implemented — only build if explicitly asked)

If dark mode is requested, invert the ink/paper relationship rather than
switching to a generic dark-SaaS gray/blue theme:
- Background → a near-black warm charcoal (not pure black, keep the "paper"
  warmth, e.g. `#1a1917`), cards a shade lighter (`#232220`)
- Text → the current `--paper` (`#f7f6f3`) becomes the primary text color
- Keep `--accent` and `--accent-2` as-is but consider lightening slightly for
  contrast (test against the dark card background, don't guess)
- Borders lighten to a low-opacity white rather than the current warm grays
Flag this as a proposal to the user rather than assuming exact hex values —
dark mode wasn't part of the original system and deserves a quick sanity check.

### Naming & code conventions to preserve

- Class names: lowercase, hyphen-separated, component-prefixed
  (`.feature-card`, `.feature-icon`, `.feature-title`, `.feature-body` — not
  BEM double-underscores)
- All colors/radii/fonts referenced via the existing CSS custom properties,
  never hardcoded hex values in new component CSS
- New component styles get appended to `style.css` in their own clearly
  commented section (matching the `/* --- Section --- */` divider style
  already used throughout the file), not split into new files, unless the
  page is large enough to warrant its own stylesheet (ask the user first)
- Markup uses Jinja2 templating (`{% extends "base.html" %}`, `{% block
  content %}`) consistent with the existing Flask app — new pages always
  extend `base.html`, never duplicate the `<nav>`/`<footer>`

---

## Workflow

1. **Clarify scope** if ambiguous — which page, what data/content goes on it,
   logged-in vs logged-out, any specific user actions it needs to support.
   Don't over-ask if the request is already concrete; default to a reasonable
   structure and state the assumption.
2. **Reuse before inventing.** Map the requested screen to what already
   exists: is this basically a card grid (→ `.feature-card` pattern), a
   focused form (→ `.auth-card` pattern), a long-form page (→ `.legal-card`
   pattern), or something new (→ "Extending into uncovered territory" above)?
3. **Build the structure first**, then layer in details: page section →
   layout grid/flex → components → spacing → color/type refinements. Keep
   visual hierarchy explicit — one clear primary action per screen, secondary
   actions styled with `.btn-ghost`, never two competing `.btn-primary`s
   fighting for attention.
4. **Responsive pass.** Every new layout needs to work at the two existing
   breakpoints (`900px`, `600px`) — collapse multi-column grids to single
   column, hide/simplify decorative elements (like the hero visual does),
   and check nav/touch-target sizing on narrow screens.
5. **Output as real files** matching the existing project shape: a Jinja
   template in `templates/` extending `base.html`, plus new CSS appended to
   `style.css` in its own clearly commented section (or a new stylesheet only
   if the page is large enough to justify one — ask first). Don't hand back
   a one-off HTML file with inline `<style>` unless explicitly asked for a
   quick mockup.
6. **Sanity check before delivering:**
   - Every color, font, radius, and spacing value traces back to the token
     table above or an approved extension — no stray hex codes or ad hoc
     pixel values.
   - Headings use `--font-display`, body/UI uses `--font-body`.
   - One clear primary action, hierarchy is unambiguous at a glance.
   - Layout holds up at both breakpoints.
   - New class names are lowercase-hyphenated and component-prefixed, matching
     the existing convention.
   - If you introduced something not covered above (a genuinely new
     pattern), briefly explain the design decision so the user can sanity
     check it — don't silently invent and move on.

---

## Appendix A: Canonical stylesheet (`static/css/style.css`)

Ground truth for every token, class, and pattern referenced above.

```css
/* ------------------------------------------------------------------ */
/* Variables                                                           */
/* ------------------------------------------------------------------ */

:root {
    --ink: #0f0f0f;
    --ink-soft: #2d2d2d;
    --ink-muted: #6b6b6b;
    --ink-faint: #a0a0a0;
    --paper: #f7f6f3;
    --paper-warm: #f0ede6;
    --paper-card: #ffffff;
    --accent: #1a472a;
    --accent-light: #e8f0eb;
    --accent-2: #c17f24;
    --accent-2-light: #fdf3e3;
    --danger: #c0392b;
    --danger-light: #fdecea;
    --border: #e4e1da;
    --border-soft: #eeebe4;

    --font-display: 'DM Serif Display', Georgia, serif;
    --font-body: 'DM Sans', system-ui, sans-serif;

    --max-width: 1200px;
    --auth-width: 440px;

    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 20px;
}

/* ------------------------------------------------------------------ */
/* Reset                                                               */
/* ------------------------------------------------------------------ */

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html { font-size: 16px; scroll-behavior: smooth; }

body {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 1rem;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

a { color: inherit; text-decoration: none; }

/* ------------------------------------------------------------------ */
/* Navbar                                                              */
/* ------------------------------------------------------------------ */

.navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--paper);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
}

.nav-inner {
    max-width: var(--max-width);
    margin: 0 auto;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--ink);
}

.brand-icon {
    color: var(--accent);
    font-size: 1.3rem;
}

.brand-name { color: var(--ink); }

.nav-links {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    font-size: 0.9rem;
    font-weight: 500;
}

.nav-links a { color: var(--ink-muted); transition: color 0.2s; }
.nav-links a:hover { color: var(--ink); }

.nav-greeting { color: var(--ink-muted); }

.nav-cta {
    background: var(--ink) !important;
    color: var(--paper) !important;
    padding: 0.45rem 1.1rem;
    border-radius: var(--radius-sm);
    transition: background 0.2s !important;
}

.nav-cta:hover { background: var(--accent) !important; }

/* ------------------------------------------------------------------ */
/* Main                                                                */
/* ------------------------------------------------------------------ */

.main-content { min-height: calc(100vh - 60px - 100px); }

/* ------------------------------------------------------------------ */
/* Hero                                                                */
/* ------------------------------------------------------------------ */

.hero {
    padding: 5rem 2rem 4rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    max-width: var(--max-width);
    margin: 0 auto;
}

.hero-badge {
    display: inline-block;
    background: var(--accent-light);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 5vw, 4rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin-bottom: 1.25rem;
}

.hero-title em {
    font-style: italic;
    color: var(--accent);
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--ink-muted);
    line-height: 1.7;
    max-width: 460px;
    margin-bottom: 2rem;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
}

/* ------------------------------------------------------------------ */
/* Mock card (hero visual)                                             */
/* ------------------------------------------------------------------ */

.hero-visual {
    display: flex;
    justify-content: center;
}

.mock-card {
    background: var(--paper-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    width: 100%;
    max-width: 380px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.06);
}

.mock-card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.75rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-soft);
}

.mock-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--ink-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.mock-total {
    font-family: var(--font-display);
    font-size: 1.75rem;
    color: var(--ink);
}

.mock-bars { display: flex; flex-direction: column; gap: 1rem; }

.mock-bar-row {
    display: grid;
    grid-template-columns: 80px 1fr 60px;
    align-items: center;
    gap: 0.75rem;
}

.mock-cat {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--ink-soft);
}

.mock-bar-track {
    height: 6px;
    background: var(--border-soft);
    border-radius: 999px;
    overflow: hidden;
}

.mock-bar {
    height: 100%;
    background: var(--accent);
    border-radius: 999px;
    transition: width 0.6s ease;
}

.mock-bar-2 { background: var(--accent-2); }
.mock-bar-3 { background: #5b7fa6; }
.mock-bar-4 { background: #8b5e83; }

.mock-amt {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--ink-muted);
    text-align: right;
}

/* ------------------------------------------------------------------ */
/* Buttons                                                             */
/* ------------------------------------------------------------------ */

.btn-primary {
    display: inline-block;
    background: var(--ink);
    color: var(--paper);
    padding: 0.65rem 1.5rem;
    border-radius: var(--radius-sm);
    font-family: var(--font-body);
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: background 0.2s;
    text-decoration: none;
}

.btn-primary:hover { background: var(--accent); }

.btn-ghost {
    display: inline-block;
    background: transparent;
    color: var(--ink-soft);
    padding: 0.65rem 1.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid var(--border);
    transition: all 0.2s;
    text-decoration: none;
}

.btn-ghost:hover {
    border-color: var(--ink);
    color: var(--ink);
}

/* ------------------------------------------------------------------ */
/* Features section                                                    */
/* ------------------------------------------------------------------ */

.features {
    background: var(--paper-warm);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 5rem 2rem;
}

.features-inner {
    max-width: var(--max-width);
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
}

.feature-card {
    background: var(--paper-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 2rem;
}

.feature-icon {
    font-size: 1.5rem;
    color: var(--accent);
    margin-bottom: 1rem;
    font-weight: 700;
}

.feature-title {
    font-family: var(--font-display);
    font-size: 1.2rem;
    color: var(--ink);
    margin-bottom: 0.75rem;
}

.feature-body {
    font-size: 0.9rem;
    color: var(--ink-muted);
    line-height: 1.7;
}

/* ------------------------------------------------------------------ */
/* CTA section                                                         */
/* ------------------------------------------------------------------ */

.cta-section {
    padding: 6rem 2rem;
    text-align: center;
}

.cta-inner {
    max-width: 560px;
    margin: 0 auto;
}

.cta-title {
    font-family: var(--font-display);
    font-size: clamp(1.75rem, 3vw, 2.5rem);
    color: var(--ink);
    margin-bottom: 1rem;
}

.cta-body {
    font-size: 1rem;
    color: var(--ink-muted);
    margin-bottom: 2rem;
}

/* ------------------------------------------------------------------ */
/* Auth pages                                                          */
/* ------------------------------------------------------------------ */

.auth-section {
    min-height: calc(100vh - 60px - 100px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
}

.auth-container {
    width: 100%;
    max-width: var(--auth-width);
}

.auth-header {
    text-align: center;
    margin-bottom: 2rem;
}

.auth-title {
    font-family: var(--font-display);
    font-size: 2rem;
    color: var(--ink);
    margin-bottom: 0.5rem;
}

.auth-subtitle {
    font-size: 0.9rem;
    color: var(--ink-muted);
}

.auth-card {
    background: var(--paper-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.auth-error {
    background: var(--danger-light);
    color: var(--danger);
    border: 1px solid #f5c6c2;
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    margin-bottom: 1.25rem;
}

.form-group { margin-bottom: 1.25rem; }

.form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--ink-soft);
    margin-bottom: 0.4rem;
}

.form-input {
    width: 100%;
    padding: 0.6rem 0.875rem;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--ink);
    background: var(--paper);
    outline: none;
    transition: border-color 0.2s;
}

.form-input:focus { border-color: var(--accent); }

.form-input::placeholder { color: var(--ink-faint); }

.btn-submit {
    width: 100%;
    padding: 0.7rem;
    background: var(--ink);
    color: var(--paper);
    border: none;
    border-radius: var(--radius-sm);
    font-family: var(--font-body);
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
    margin-top: 0.5rem;
}

.btn-submit:hover { background: var(--accent); }

.auth-switch {
    text-align: center;
    font-size: 0.875rem;
    color: var(--ink-muted);
}

.auth-switch a {
    color: var(--accent);
    font-weight: 500;
}

.auth-switch a:hover { text-decoration: underline; }

/* ------------------------------------------------------------------ */
/* How it works button                                                 */
/* ------------------------------------------------------------------ */

.btn-how-it-works {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-body);
    cursor: pointer;
}

.play-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.4rem;
    height: 1.4rem;
    background: var(--accent);
    color: var(--paper);
    border-radius: 50%;
    font-size: 0.6rem;
}

/* ------------------------------------------------------------------ */
/* Modal                                                               */
/* ------------------------------------------------------------------ */

.modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(15, 15, 15, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.modal-overlay[hidden] { display: none; }

.modal-box {
    position: relative;
    width: 100%;
    max-width: 720px;
    background: var(--paper-card);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-title {
    font-family: var(--font-display);
    font-size: 1.3rem;
    color: var(--ink);
    margin-bottom: 1.25rem;
    padding-right: 2rem;
}

.modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 2rem;
    height: 2rem;
    border: none;
    background: var(--paper-warm);
    color: var(--ink-soft);
    border-radius: 50%;
    font-size: 1.1rem;
    line-height: 1;
    cursor: pointer;
    transition: background 0.2s;
}

.modal-close:hover { background: var(--border); }

.modal-video {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: var(--ink);
    border-radius: var(--radius-md);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-video iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
}

.modal-placeholder-text {
    color: var(--ink-faint);
    font-size: 0.9rem;
}

/* ------------------------------------------------------------------ */
/* Legal pages                                                         */
/* ------------------------------------------------------------------ */

.legal-section {
    min-height: calc(100vh - 60px - 100px);
    padding: 4rem 2rem 5rem;
}

.legal-container {
    max-width: 760px;
    margin: 0 auto;
}

.legal-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.legal-title {
    font-family: var(--font-display);
    font-size: clamp(2rem, 4vw, 2.75rem);
    color: var(--ink);
    margin-bottom: 0.5rem;
}

.legal-updated {
    font-size: 0.85rem;
    color: var(--ink-faint);
}

.legal-card {
    background: var(--paper-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 2.5rem;
}

.legal-card h2 {
    font-family: var(--font-display);
    font-size: 1.2rem;
    color: var(--ink);
    margin-bottom: 0.6rem;
}

.legal-card h2:not(:first-child) {
    margin-top: 1.75rem;
}

.legal-card p {
    font-size: 0.925rem;
    color: var(--ink-muted);
    line-height: 1.75;
}

/* ------------------------------------------------------------------ */
/* Footer                                                              */
/* ------------------------------------------------------------------ */

.footer {
    background: var(--ink);
    color: var(--paper);
    padding: 2.5rem 2rem;
    text-align: center;
}

.footer-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}

.footer .brand-icon { color: var(--accent-2); font-size: 1.5rem; }

.footer-name {
    font-weight: 600;
    font-size: 1rem;
}

.footer-copy {
    font-size: 0.8rem;
    color: var(--ink-faint);
}

.footer-links {
    display: flex;
    gap: 1.25rem;
    margin-top: 0.5rem;
}

.footer-links a {
    font-size: 0.8rem;
    color: var(--ink-faint);
    text-decoration: none;
}

.footer-links a:hover {
    color: var(--paper);
    text-decoration: underline;
}

/* ------------------------------------------------------------------ */
/* Responsive                                                          */
/* ------------------------------------------------------------------ */

@media (max-width: 900px) {
    .hero {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .hero-subtitle { max-width: 100%; }
    .hero-actions { justify-content: center; }
    .hero-visual { display: none; }

    .features-inner { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
    .nav-links a:not(.nav-cta):not(.nav-logout) { display: none; }
    .nav-greeting { display: none; }
    .hero { padding: 3rem 1rem 2rem; }
}
```

---

## Appendix B: Canonical page shell (`templates/base.html`)

Every new template extends this — never duplicate the `<nav>` or `<footer>`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Spendly{% endblock %}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block head %}{% endblock %}
</head>
<body>

    <nav class="navbar">
        <div class="nav-inner">
            <a href="{{ url_for('landing') }}" class="nav-brand">
                <span class="brand-icon">◈</span>
                <span class="brand-name">Spendly</span>
            </a>
            <div class="nav-links">
                {% if session.user_id %}
                <span class="nav-greeting">Hi, {{ session.name }}</span>
                <a href="{{ url_for('logout') }}" class="nav-logout">Log out</a>
                {% else %}
                <a href="{{ url_for('login') }}">Sign in</a>
                <a href="{{ url_for('register') }}" class="nav-cta">Get started</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="footer-inner">
            <span class="brand-icon">◈</span>
            <span class="footer-name">Spendly</span>
            <p class="footer-copy">Track every rupee. Own your finances.</p>
            <div class="footer-links">
                <a href="{{ url_for('terms') }}">Terms and Conditions</a>
                <a href="{{ url_for('privacy') }}">Privacy Policy</a>
            </div>
        </div>
    </footer>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```
