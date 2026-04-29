# FellTrack — Mental Health Diary

> A web application for daily mood tracking and mental wellness journaling, built with Python/Flask and an interactive analytics dashboard.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-01696f?style=flat-square)](LICENSE)

---

## Overview

FellTrack is a personal mental health journal that allows users to log their daily emotions, intensity levels, and written reflections. It includes a visual analytics dashboard powered by Chart.js to help users identify emotional patterns over time.

Built as a capstone project following the CS50x curriculum, this app demonstrates a full MVC architecture in Flask with secure authentication and file upload support.

---

## Features

- **Secure authentication** — User registration and login with `werkzeug` password hashing (PBKDF2-SHA256)
- **Daily journal entries** — Log emotion type, intensity (1–10 scale), written thoughts, and optional image attachments
- **History view** — Paginated list of all past entries with timestamps
- **Analytics dashboard** — Pie chart of emotion frequency + line chart of daily intensity averages (Chart.js)
- **Image uploads** — Validated file type checking (`png`, `jpg`, `jpeg`, `gif`) with `secure_filename`
- **Session management** — Server-side sessions with `flask-session`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite via cs50 SQL |
| Auth | Werkzeug (PBKDF2-SHA256 hashing) |
| Frontend | Jinja2 templates, Chart.js |
| Sessions | flask-session (server-side) |
| File Uploads | Werkzeug `secure_filename` |

---

## Security Notes

This project follows secure development practices:

- All passwords are hashed with **PBKDF2-SHA256** via `werkzeug.security` — never stored as plain text
- Database files (`*.db`) and session folders (`flask_session/`) are excluded via `.gitignore`
- File uploads are validated against an allowlist of extensions and sanitized with `secure_filename`
- Secret keys are loaded from environment variables (see `.env.example`)
- SQL queries use **parameterized statements** via the cs50 SQL wrapper — no raw string interpolation

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MarcosCF1/Di-rio-Mental-Felltrack.git
cd Di-rio-Mental-Felltrack

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 5. Initialize the database
# The app creates tables automatically on first run

# 6. Run the development server
cd diario_mental
flask run
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Project Structure

```
Di-rio-Mental-Felltrack/
├── diario_mental/
│   ├── app.py              # Application factory and route handlers
│   ├── helpers.py          # login_required decorator
│   ├── static/
│   │   └── uploads/        # User-uploaded images (gitignored)
│   └── templates/          # Jinja2 HTML templates
├── .env.example            # Environment variable template
├── .gitignore              # Excludes .db, flask_session/, .env
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Dashboard Preview

The analytics dashboard provides:
- **Emotion frequency chart** (pie/doughnut) — which emotions appear most often
- **Daily intensity trend** (line chart) — average emotional intensity per day

---

## Author

**Marcos Pires** — Full Stack Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-marcos--pires--dev-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/marcos-pires-dev)
[![GitHub](https://img.shields.io/badge/GitHub-MarcosCF1-181717?style=flat-square&logo=github)](https://github.com/MarcosCF1)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
