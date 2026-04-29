from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import random
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "aceest_secret_key_2024"

DB_NAME = "aceest_fitness.db"

PROGRAM_TEMPLATES = {
    "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
    "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"]
}

WORKOUT_PLANS = {
    "Fat Loss": {
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "Breakfast: 3 Egg Whites + Oats Idli\nLunch: Grilled Chicken + Brown Rice\nDinner: Fish Curry + Millet Roti\nTarget: 2,000 kcal"
    },
    "Muscle Gain": {
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "Breakfast: 4 Eggs + PB Oats\nLunch: Chicken Biryani (250g Chicken)\nDinner: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal"
    },
    "Beginner": {
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati\nProtein: 120g/day"
    }
}


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            height REAL,
            weight REAL,
            program TEXT,
            calories INTEGER,
            target_weight REAL,
            target_adherence INTEGER,
            membership_status TEXT DEFAULT 'Active',
            membership_end TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            date TEXT,
            workout_type TEXT,
            duration_min INTEGER,
            notes TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            date TEXT,
            weight REAL,
            waist REAL,
            bodyfat REAL
        )
    """)
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin','admin','Admin')")
    conn.commit()
    conn.close()


# ---------- AUTH ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        conn.close()
        if row:
            session["user"] = username
            session["role"] = row["role"]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    clients = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
    total_clients = len(clients)
    active = sum(1 for c in clients if c["membership_status"] == "Active")
    conn.close()
    return render_template("dashboard.html", clients=clients,
                           total=total_clients, active=active,
                           user=session["user"], role=session["role"])


# ---------- CLIENTS ----------
@app.route("/clients/add", methods=["POST"])
def add_client():
    if "user" not in session:
        return redirect(url_for("login"))
    name = request.form.get("name", "").strip()
    age = request.form.get("age", 0)
    height = request.form.get("height", 0)
    weight = request.form.get("weight", 0)
    program = request.form.get("program", "Beginner")
    calories = request.form.get("calories", 2000)
    membership_end = request.form.get("membership_end", "")
    if name:
        conn = get_db()
        conn.execute("""
            INSERT OR IGNORE INTO clients
            (name, age, height, weight, program, calories, membership_status, membership_end)
            VALUES (?, ?, ?, ?, ?, ?, 'Active', ?)
        """, (name, age, height, weight, program, calories, membership_end))
        conn.commit()
        conn.close()
    return redirect(url_for("dashboard"))


@app.route("/client/<name>")
def client_detail(name):
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    client = conn.execute("SELECT * FROM clients WHERE name=?", (name,)).fetchone()
    workouts = conn.execute(
        "SELECT * FROM workouts WHERE client_name=? ORDER BY date DESC", (name,)
    ).fetchall()
    progress = conn.execute(
        "SELECT * FROM progress WHERE client_name=? ORDER BY id", (name,)
    ).fetchall()
    metrics = conn.execute(
        "SELECT * FROM metrics WHERE client_name=? ORDER BY date DESC", (name,)
    ).fetchall()
    conn.close()
    if not client:
        return redirect(url_for("dashboard"))
    plan = WORKOUT_PLANS.get(client["program"], WORKOUT_PLANS["Beginner"])
    return render_template("client.html", client=client, workouts=workouts,
                           progress=progress, metrics=metrics, plan=plan,
                           user=session["user"], role=session["role"])


@app.route("/client/<name>/generate_program")
def generate_program(name):
    if "user" not in session:
        return redirect(url_for("login"))
    program_type = random.choice(list(PROGRAM_TEMPLATES.keys()))
    conn = get_db()
    conn.execute("UPDATE clients SET program=? WHERE name=?", (program_type, name))
    conn.commit()
    conn.close()
    return redirect(url_for("client_detail", name=name))


@app.route("/client/<name>/add_workout", methods=["POST"])
def add_workout(name):
    if "user" not in session:
        return redirect(url_for("login"))
    workout_date = request.form.get("date", date.today().isoformat())
    workout_type = request.form.get("type", "")
    duration = request.form.get("duration", 60)
    notes = request.form.get("notes", "")
    conn = get_db()
    conn.execute("""
        INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (name, workout_date, workout_type, duration, notes))
    conn.commit()
    conn.close()
    return redirect(url_for("client_detail", name=name))


@app.route("/client/<name>/add_metric", methods=["POST"])
def add_metric(name):
    if "user" not in session:
        return redirect(url_for("login"))
    metric_date = request.form.get("date", date.today().isoformat())
    weight = request.form.get("weight", 0)
    waist = request.form.get("waist", 0)
    bodyfat = request.form.get("bodyfat", 0)
    conn = get_db()
    conn.execute("""
        INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
        VALUES (?, ?, ?, ?, ?)
    """, (name, metric_date, weight, waist, bodyfat))
    conn.commit()
    conn.close()
    return redirect(url_for("client_detail", name=name))


# ---------- API FOR CHARTS ----------
@app.route("/api/progress/<name>")
def api_progress(name):
    conn = get_db()
    rows = conn.execute(
        "SELECT week, adherence FROM progress WHERE client_name=? ORDER BY id", (name,)
    ).fetchall()
    metrics = conn.execute(
        "SELECT date, weight FROM metrics WHERE client_name=? ORDER BY date", (name,)
    ).fetchall()
    conn.close()
    return jsonify({
        "weeks": [r["week"] for r in rows],
        "adherence": [r["adherence"] for r in rows],
        "metric_dates": [m["date"] for m in metrics],
        "weights": [m["weight"] for m in metrics]
    })


# ---------- HEALTH CHECK (for K8s) ----------
@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "3.2.4"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
