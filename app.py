import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

with app.app_context():
    init_db()
    seed_db()


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id") is not None:
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return render_template(
                "register.html",
                error="All fields are required.",
                name=name,
                email=email,
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters.",
                name=name,
                email=email,
            )

        password_hash = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="An account with that email already exists.",
                name=name,
                email=email,
            )
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id") is not None:
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        try:
            user = conn.execute(
                "SELECT id, name, password_hash FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        finally:
            conn.close()

        if (
            not email
            or not password
            or user is None
            or not check_password_hash(user["password_hash"], password)
        ):
            return render_template("login.html", error="Invalid email or password")

        session["user_id"] = user["id"]
        session["name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
@login_required
def profile():
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()
        stats = conn.execute(
            "SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total "
            "FROM expenses WHERE user_id = ?",
            (session["user_id"],),
        ).fetchone()
        category_rows = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses "
            "WHERE user_id = ? GROUP BY category ORDER BY total DESC",
            (session["user_id"],),
        ).fetchall()
        expense_rows = conn.execute(
            "SELECT amount, category, date, description FROM expenses "
            "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 10",
            (session["user_id"],),
        ).fetchall()
    finally:
        conn.close()

    initials = "".join(part[0].upper() for part in user["name"].split()[:2])
    member_since = datetime.strptime(
        user["created_at"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%B %Y")

    total_spent = stats["total"]
    category_breakdown = []
    for i, row in enumerate(category_rows):
        percent = (row["total"] / total_spent * 100) if total_spent else 0
        cycle = i % 8
        category_breakdown.append({
            "name": row["category"],
            "total": row["total"],
            "percent": round(percent, 1),
            "bar_class": "" if cycle == 0 else f"mock-bar-{cycle + 1}",
        })

    recent_expenses = [
        {
            "date_display": datetime.strptime(row["date"], "%Y-%m-%d").strftime("%b %d, %Y"),
            "category": row["category"],
            "description": row["description"],
            "amount": row["amount"],
        }
        for row in expense_rows
    ]
    has_more = stats["count"] > len(recent_expenses)

    return render_template(
        "profile.html",
        user=user,
        initials=initials,
        member_since=member_since,
        expense_count=stats["count"],
        total_spent=total_spent,
        category_breakdown=category_breakdown,
        recent_expenses=recent_expenses,
        has_more=has_more,
    )


@app.route("/expenses/add")
@login_required
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
@login_required
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
@login_required
def delete_expense(id):
    return "Delete expense — coming in Step 9"


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
