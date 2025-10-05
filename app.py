#!/usr/bin/env python3
"""
Phishing Awareness Demo - educational only.
Run locally. Do NOT deploy to public internet.
"""

import os
import sqlite3
import secrets
import json
import datetime
from flask import Flask, g, render_template, request, redirect, url_for, Response, send_file

DB_PATH = "phish_demo.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key")

# ---------- DB helpers ----------
def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS recipients (
      id INTEGER PRIMARY KEY,
      name TEXT,
      email TEXT,
      token TEXT UNIQUE
    )""")
    db.execute("""
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY,
      token TEXT,
      event_type TEXT,
      meta TEXT,
      ts TEXT
    )""")
    db.commit()

with app.app_context():
    init_db()

@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

# ---------- Routes ----------
@app.route("/")
def index():
    db = get_db()
    cur = db.execute("SELECT * FROM recipients ORDER BY id DESC")
    recipients = cur.fetchall()
    host = request.host_url.rstrip("/")
    return render_template("index.html", recipients=recipients, host=host)

@app.route("/add_recipient", methods=["POST"])
def add_recipient():
    name = request.form.get("name", "Test User").strip()
    email = request.form.get("email", "test@example.com").strip()
    token = secrets.token_urlsafe(8)
    db = get_db()
    db.execute("INSERT INTO recipients (name,email,token) VALUES (?,?,?)", (name,email,token))
    db.commit()
    return redirect(url_for("index"))

@app.route("/p/<token>", methods=["GET"])
def phish(token):
    db = get_db()
    cur = db.execute("SELECT * FROM recipients WHERE token=?", (token,))
    rec = cur.fetchone()
    if not rec:
        return "Invalid token", 404
    # Render the demo phishing page (explicitly educational)
    return render_template("phish.html", recipient=rec, token=token)

@app.route("/submit/<token>", methods=["POST"])
def submit(token):
    consent = request.form.get("consent")
    email_sub = request.form.get("email","").strip()
    password_sub = request.form.get("password","")
    if consent != "on":
        return "Consent required for this demo. Check the consent box.", 400

    meta = {
        "ip": request.remote_addr,
        "ua": request.headers.get("User-Agent"),
        "submitted_email": email_sub,
        # we do NOT store raw password; store only masked info
        "password_mask": f"<redacted length={len(password_sub)}>"
    }
    db = get_db()
    db.execute("INSERT INTO events (token,event_type,meta,ts) VALUES (?,?,?,?)",
               (token, "submit", json.dumps(meta), datetime.datetime.utcnow().isoformat()))
    db.commit()
    return render_template("phish_submitted.html", token=token)

@app.route("/click/<token>")
def click(token):
    # log the click and redirect to landing page for demo
    meta = {"ip": request.remote_addr, "ua": request.headers.get("User-Agent")}
    db = get_db()
    db.execute("INSERT INTO events (token,event_type,meta,ts) VALUES (?,?,?,?)",
               (token, "click", json.dumps(meta), datetime.datetime.utcnow().isoformat()))
    db.commit()
    return redirect(url_for("phish", token=token))

@app.route("/pixel/<token>.gif")
def pixel(token):
    # 1x1 transparent GIF bytes
    gif = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
           b"\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,"
           b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
    meta = {"ip": request.remote_addr, "ua": request.headers.get("User-Agent")}
    db = get_db()
    db.execute("INSERT INTO events (token,event_type,meta,ts) VALUES (?,?,?,?)",
               (token, "open", json.dumps(meta), datetime.datetime.utcnow().isoformat()))
    db.commit()
    return Response(gif, mimetype="image/gif")

@app.route("/dashboard")
def dashboard():
    db = get_db()
    recs = db.execute("SELECT * FROM recipients ORDER BY id DESC").fetchall()
    data = []
    for r in recs:
        cur = db.execute("SELECT event_type, COUNT(*) AS cnt FROM events WHERE token=? GROUP BY event_type", (r["token"],))
        counts = {row["event_type"]: row["cnt"] for row in cur.fetchall()}
        events = db.execute("SELECT * FROM events WHERE token=? ORDER BY ts DESC LIMIT 100", (r["token"],)).fetchall()
        data.append({"recipient": r, "counts": counts, "events": events})
    return render_template("dashboard.html", data=data)

@app.route("/export.csv")
def export_csv():
    import csv, io
    db = get_db()
    rows = db.execute("SELECT * FROM events ORDER BY ts").fetchall()
    si = io.StringIO()
    w = csv.writer(si)
    w.writerow(["id","token","event_type","meta","ts"])
    for r in rows:
        w.writerow([r["id"], r["token"], r["event_type"], r["meta"], r["ts"]])
    output = si.getvalue()
    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=events.csv"})

# ---------- Run ----------
if __name__ == "__main__":
    # safe default: do not use debug=True on shared networks
    app.run(host="127.0.0.1", port=5000)
