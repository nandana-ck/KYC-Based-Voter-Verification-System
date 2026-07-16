from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import os
import base64
import cv2
import numpy as np
import face_recognition
from ultralytics import YOLO
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


ID_MODEL = YOLO(r"C:\Users\hp\Downloads\best (1).pt")
import re
FACE_THRESHOLD = 0.48
def normalize_roll(text):
    if not text:
        return None
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]", "", text)   # remove dots, spaces, symbols
    return text


app = Flask(__name__)
app.secret_key = "secure_voting_key"

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "voting_system.db")
IMAGE_DIR = os.path.join(BASE_DIR, "images", "voters")

def get_db():
    return sqlite3.connect(DB_PATH)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")

# ---------------- ADMIN DASHBOARD ----------------


@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, roll_number, has_voted, image_path FROM voters")
    voters = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", voters=voters)
# ---------------- RESULTS ----------------
@app.route("/results")
def results():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name, votes FROM candidates")
    data = cur.fetchall()

    cur.execute("SELECT name FROM candidates ORDER BY votes DESC LIMIT 1")
    winner = cur.fetchone()

    conn.close()

    return render_template("results.html", data=data, winner=winner[0])


# ---------------- SERVE VOTER IMAGES ----------------
@app.route("/voter_image/<filename>")
def voter_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

# ---------------- VOTER LOGIN ----------------
@app.route("/vote", methods=["GET", "POST"])
def vote_login():
    if request.method == "POST":
        roll = request.form.get("roll")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT has_voted FROM voters WHERE roll_number=?", (roll,))
        voter = cur.fetchone()
        conn.close()

        if not voter:
            return render_template("vote_login.html", error="Invalid Roll Number")

        if voter[0] == 1:
            return render_template("vote_login.html", error="You have already voted")

        session["voter_roll"] = roll
        return redirect(url_for("camera_page"))


    return render_template("vote_login.html")
# ---------------- CAMERA PAGE ----------------
@app.route("/camera")
def camera_page():
    if "voter_roll" not in session:
        return redirect(url_for("vote_login"))
    return render_template("camera.html")
# ---------------- VERIFY FACE ----------------
@app.route("/verify_face", methods=["POST"])
def verify_face():
    if "voter_roll" not in session:
        return {"status":"fail","message":"Session expired"}

    data = request.json
    image_data = data["image"]

    img_bytes = base64.b64decode(image_data.split(",")[1])
    np_img = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    faces = face_recognition.face_locations(frame)
    if not faces:
        return {"status":"fail","message":"No face detected"}

    live_face = face_recognition.face_encodings(frame, faces)[0]

    # Load DB face for TYPED roll number
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT face_encoding FROM voters WHERE roll_number=?", (session["voter_roll"],))
    row = cur.fetchone()
    conn.close()

    if not row:
        return {"status":"fail","message":"Roll not found in DB"}

    db_face = np.frombuffer(row[0], dtype=np.float64)

    dist = face_recognition.face_distance([db_face], live_face)[0]
    print("👤 Face distance:", dist)

    if dist > FACE_THRESHOLD:
        return {"status":"fail","message":"Face does not match roll number"}

    return {"status":"success"}


# ---------------- VERIFY ID CARD ----------------
@app.route("/verify_id", methods=["POST"])
def verify_id():
    if "voter_roll" not in session:
        return {"status":"fail","message":"Session expired","detected":""}

    data = request.json
    image_data = data["image"]

    img_bytes = base64.b64decode(image_data.split(",")[1])
    np_img = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # OCR from ID card (your existing YOLO + OCR)
    results = ID_MODEL(frame, conf=0.6, classes=[2], verbose=False)[0]

    detected_text = None

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        roi = frame[y1:y2, x1:x2]

        if roi.size > 0:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            thresh = cv2.threshold(gray, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            text = pytesseract.image_to_string(thresh, config="--psm 7")
            detected_text = normalize_roll(text)

    print("🆔 OCR Roll:", detected_text)

    if not detected_text:
        return {"status":"fail","message":"ID not detected","detected":""}

    if detected_text != session["voter_roll"]:
        return {
            "status":"fail",
            "message":"ID does not match entered roll number",
            "detected": detected_text
        }

    return {"status":"success","detected":detected_text}

# ---------------- VOTING PAGE ----------------
@app.route("/vote_page", methods=["GET", "POST"])
def vote_page():
    if "voter_roll" not in session:
        return redirect(url_for("vote_login"))

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        candidate = request.form.get("candidate")
        roll = session["voter_roll"]

        cur.execute("UPDATE voters SET has_voted=1 WHERE roll_number=?", (roll,))
        cur.execute("UPDATE candidates SET votes = votes + 1 WHERE name=?", (candidate,))
        conn.commit()
        conn.close()

        session.pop("voter_roll")
        return render_template("vote_success.html")

    cur.execute("SELECT name FROM candidates")
    candidates = cur.fetchall()
    conn.close()

    return render_template("vote_page.html", candidates=candidates)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_login"))

# ---------------- RUN APP (ALWAYS LAST) ----------------
if __name__ == "__main__":
    app.run(debug=True)
