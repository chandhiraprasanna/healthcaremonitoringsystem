from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

alerts = []

USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        return "Invalid credentials", 403
    return render_template("login.html")

@socketio.on("send_alert")
def handle_send_alert(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = {
        "patient": data["patient"],
        "message": data["message"],
        "severity": data["severity"],
        "time": timestamp
    }
    alerts.append((datetime.now(), alert))
    emit("receive_alert", alert, broadcast=True)

def clear_old_alerts():
    while True:
        now = datetime.now()
        alerts[:] = [(t, a) for (t, a) in alerts if now - t < timedelta(hours=1)]
        time.sleep(60)

threading.Thread(target=clear_old_alerts, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, debug=True)
