import os
from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required
from collections import defaultdict

app = Flask(__name__)

# Configura sessões
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configura banco de dados
db = SQL("sqlite:///diario.db")

# Configura pasta para uploads
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@login_required
def index():
    entries = db.execute(
        "SELECT emotion, thought, timestamp, image FROM entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10",
        session["user_id"]
    )
    return render_template("index.html", entries=entries)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            flash("Preencha todos os campos.")
            return render_template("register.html")

        if password != confirmation:
            flash("As senhas não coincidem.")
            return render_template("register.html")

        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            flash("Usuário já existe.")
            return render_template("register.html")

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Usuário ou senha inválidos.")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/new", methods=["GET", "POST"])
@login_required
def new_entry():
    if request.method == "POST":
        emotion = request.form.get("emotion")
        intensity = request.form.get("intensity")
        thought = request.form.get("thought")

        # Verifica se o arquivo foi enviado
        file = request.files.get("image")
        filename = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
        elif file and file.filename != "":
            flash("Formato de arquivo não permitido.")
            return render_template("new_entry.html")

        if not emotion or not intensity:
            flash("Preencha todos os campos obrigatórios.")
            return render_template("new_entry.html")

        db.execute("""
            INSERT INTO entries (user_id, emotion, intensity, thought, image)
            VALUES (?, ?, ?, ?, ?)
        """, session["user_id"], emotion, intensity, thought, filename)

        return redirect("/")

    return render_template("new_entry.html")

@app.route("/history")
@login_required
def history():
    entries = db.execute(
        "SELECT emotion, intensity, thought, timestamp, image FROM entries WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )
    return render_template("history.html", entries=entries)

@app.route("/dashboard")
@login_required
def dashboard():
    rows = db.execute(
        "SELECT emotion, intensity, thought, timestamp FROM entries WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )

    emotions_count = {}
    emotions_list = [row['emotion'] for row in rows]
    for emotion in set(emotions_list):
        emotions_count[emotion] = emotions_list.count(emotion)

    daily_intensity = defaultdict(list)
    for row in rows:
        date = row['timestamp'].split(' ')[0]
        daily_intensity[date].append(int(row['intensity']))

    dates = sorted(daily_intensity.keys())
    avg_intensities = [sum(vals) / len(vals) for vals in [daily_intensity[date] for date in dates]]

    emotions_labels = list(emotions_count.keys())
    emotions_data = list(emotions_count.values())

    # Envie as entradas para o template
    return render_template("dashboard.html",
                           emotions_labels=emotions_labels,
                           emotions_data=emotions_data,
                           dates=dates,
                           avg_intensities=avg_intensities,
                           entries=rows)

if __name__ == "__main__":
    app.run(debug=True)
