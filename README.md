# Phishing Awareness Demo

A fully functional **phishing simulation project** built with Python and Flask to demonstrate how phishing campaigns track user interactions — including **opens**, **clicks**, and **credential submissions** — in a **safe, local, and educational environment**.

> ⚠️ This tool is intended for **training, awareness, and demonstration purposes only.**  
> Do **NOT** use it against real users or systems without explicit permission.

---

## Overview

This project simulates the lifecycle of a phishing attack, allowing you to see exactly how attackers:

- Send unique phishing links
- Track email **opens** (via invisible tracking pixels)
- Log **clicks** when users visit the malicious site
- Record **credential submissions** (with passwords masked)
- Display all captured events in a real-time **dashboard**

It’s perfect for cybersecurity students, red-team learners, and awareness trainers who want a hands-on demonstration of phishing behavior.

---

## Features

✅ **Unique tracking links** – Each recipient gets a personalized phishing link.
✅ **Open tracking** – Detect when the email was opened.
✅ **Click tracking** – Log when a victim clicks the phishing link.
✅ **Credential submission logging** – Record demo login attempts (with masked passwords).
✅ **Dashboard & Analytics** – See all opens, clicks, and submissions with timestamps, IPs, and user agents.
✅ **CSV Export** – Download event logs for reporting and training.


---

## Installation & Setup

### 1 Clone the Repository
git clone https://github.com/Nitindasapalli/phish-awareness-demo.git
cd phish-awareness-demo

### 2 Install Dependencies
Make sure Python 3.8+ is installed, then:

pip install -r requirements.txt
Or install manually:
pip install flask tqdm

### 3 Run the App
python app.py
You should see:
* Running on http://127.0.0.1:5000

## Usage Guide
 Step 1: Generate a Phishing Link
Visit http://127.0.0.1:5000 and create a new recipient (e.g., a test email).

 Step 2: Open the Phishing Page
Use the generated link (e.g., http://127.0.0.1:5000/click/<token>) — either open it in a browser or with curl:

curl -L http://127.0.0.1:5000/click/<token>

 Step 3: Submit Demo Credentials
Fill in the form with dummy data (never real passwords):

Email: test@example.com
Password: demo123

 Step 4: View the Dashboard
Go to:

http://127.0.0.1:5000/dashboard
Here you'll see detailed logs of:

Opens (email tracking pixel triggered)
Clicks (link visited)
Submissions (login form posted)

Example Output
Here’s an example of the dashboard you’ll see:

<img width="1120" height="736" alt="Screenshot 2025-10-05 at 4 41 00 PM" src="https://github.com/user-attachments/assets/35986cd2-4bbe-4621-af45-66fcaceb5bd5" />

It shows:
Total Opens, Clicks, and Submits per recipient
IP addresses and User-Agents
Timestamp of each event
Masked password data for privacy

How It Works (Flow)

[Generate Phishing Link] 
        │
        ▼
[Send to Recipient / Simulate Email]
        │
        ▼
[Open Tracking Pixel Loaded] ──> Logs "open"
        │
        ▼
[User Clicks Link] ─────────────> Logs "click"
        │
        ▼
[Fake Login Page]
        │
        ▼
[User Submits Credentials] ────> Logs "submit"
        │
        ▼
[Dashboard + CSV Export]

## Technologies Used
 Python 3
 Flask – lightweight web framework
 SQLite – simple event storage
 HTML/CSS – frontend templates
 (Optional) Docker – for containerized deployment

## Ethical Disclaimer
This project is built only for ethical, educational, and awareness purposes.
Using phishing techniques on real users or networks without consent is illegal and punishable by law.

Use this tool only in controlled labs, classrooms, or authorized environments.

