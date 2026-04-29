<div align="center">

# FellTrack
### Mental Health Diary & Emotion Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Security](https://img.shields.io/badge/Security-PBKDF2--SHA256-01696f?style=flat-square)](#security)
[![License](https://img.shields.io/badge/License-MIT-30363d?style=flat-square)](LICENSE)

*A full-stack Python/Flask application for daily mood journaling with a Chart.js analytics dashboard — built with production security standards.*

</div>

---

## The Problem It Solves

Most people don't track their emotional patterns systematically — which means they can't see the correlation between daily events, mood swings, and long-term mental health trends. FellTrack gives users a structured, private space to log emotions with intensity ratings, add written reflections, and then **visualize those patterns over time** through an interactive dashboard.

The result: users go from "I feel bad sometimes" to "my average intensity drops every Monday and peaks on Thursday" — actionable self-knowledge from their own data.

---

## Technical Highlights

### Architecture
FellTrack follows a clean **MVC pattern** inside Flask:
- **Model** — SQLite via cs50's parameterized SQL wrapper; schema managed manually to keep dependencies lean
- **View** — Jinja2 templates with a Chart.js dashboard for client-side visualization
- **Controller** — Flask route handlers with a `login_required` decorator that guards all authenticated endpoints

The `login_required` decorator was implemented from scratch (see `helpers.py`) rather than using Flask-Login, demonstrating understanding of session management primitives.

### Security Decisions

Every security decision has a rationale:

| Threat | Mitigation | Why |
|---|---|---|
| Password theft via DB leak | PBKDF2-SHA256 via `werkzeug.security` | Industry-standard adaptive hashing; resistant to rainbow tables |
| SQL injection | Parameterized queries (cs50 SQL wrapper) | Zero raw string interpolation in any query |
| Malicious file uploads | Extension allowlist + `secure_filename()` | Prevents path traversal and executable uploads |
| Session hijacking | Server-side sessions via `flask-session` | Session tokens stored server-side; client only holds an opaque ID |
| Secret exposure | `.env` gitignored; `.env.example` as template | Secret keys never committed to version control |
| Exposed database | `*.db` gitignored; removed from git history | No real user data ever lives in the repository |

### Data Flow

```
User submits entry
    ↓
 Flask validates form (emotion, intensity, thought, optional image)
    ↓
File validated (allowlist) → secure_filename() → saved to static/uploads/
    ↓
Parameterized INSERT → SQLite (entries table)
    ↓
Dashboard query aggregates: emotion counts + daily avg intensity
    ↓
Chart.js renders pie (emotion frequency) + line (intensity over time)
```

---

## Features

- **Secure registration & login** — PBKDF2-SHA256 hashing, server-side session management
- **Structured journal entries** — emotion type, intensity scale (1–10), free-text reflection, optional image
- **Full history view** — reverse-chronological feed of all entries with timestamps
- **Analytics dashboard** — emotion frequency (pie chart) + daily intensity trend (line chart)
- **Image upload** — type-validated, sanitized, stored in a dedicated static folder
- **One-click logout** — full session clear on `/logout`

---

## Tech Stack

| Layer | Technology | Decision Rationale |
|---|---|---|
| Backend framework | Python 3.11, Flask 3.0 | Lightweight, explicit routing, minimal magic |
| Database | SQLite + cs50 SQL | Zero-config persistence; sufficient for single-user scope |
| Auth | Werkzeug PBKDF2-SHA256 | Battle-tested; avoids rolling custom crypto |
| Templates | Jinja2 | Native Flask integration; logic-light views |
| Charts | Chart.js (CDN) | No build step; client-side rendering keeps server lean |
| Sessions | flask-session (filesystem) | Server-side; more secure than signed cookies for sensitive apps |

---

## Getting Started

```bash
# Clone and enter the project
git clone https://github.com/MarcosCF1/Di-rio-Mental-Felltrack.git
cd Di-rio-Mental-Felltrack

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Open .env and set a strong SECRET_KEY:
# python -c "import secrets; print(secrets.token_hex(32))"

# Run the app (auto-creates DB tables on first launch)
cd diario_mental
flask run
```

Visit [http://localhost:5000](http://localhost:5000) → register → start logging.

---

## Project Structure

```
Di-rio-Mental-Felltrack/
├── diario_mental/
│   ├── app.py              # Route handlers + application config
│   ├── helpers.py          # login_required decorator (custom, not Flask-Login)
│   ├── static/
│   │   └── uploads/        # User images — gitignored, never committed
│   └── templates/          # Jinja2 HTML: login, register, index, history, dashboard
├── .env.example            # Template for required environment variables
├── .gitignore              # Excludes: *.db, flask_session/, .env, uploads/
├── requirements.txt        # Pinned Python dependencies
└── README.md
```

---

## What I Learned Building This

- Implementing session-based auth **without a library** forces a deep understanding of how Flask sessions, secret keys, and server-side token storage actually work — knowledge that makes debugging auth issues in any framework much faster.
- Writing every SQL query with parameterized inputs becomes muscle memory quickly and prevents entire categories of security bugs.
- Separating the analytics logic (aggregation in SQL, rendering in Chart.js) from the entry logic keeps each route small and testable.

---

## Author

**Marcos Pires** — Full Stack Developer & AI Integration Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-marcos--pires--dev-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/marcos-pires-dev)
[![GitHub](https://img.shields.io/badge/GitHub-MarcosCF1-181717?style=flat-square&logo=github)](https://github.com/MarcosCF1)
[![Portfolio](https://img.shields.io/badge/More%20Projects-github.com%2FMarcosCF1-01696f?style=flat-square)](https://github.com/MarcosCF1)

---

<sub>MIT License — built as a CS50x capstone project, extended with production security hardening.</sub>
