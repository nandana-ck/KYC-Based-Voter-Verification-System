import sqlite3
import face_recognition
import numpy as np
import cv2

# -------------------------------
# CONFIG
# -------------------------------
DB_PATH = "voting_system.db"
TEST_ROLL = "AMENU4ECE23148"   # change to any roll number
THRESHOLD = 0.48              # strict threshold

# -------------------------------
# Load face from database
# -------------------------------
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT face_encoding FROM voters WHERE roll_number=?", (TEST_ROLL,))
row = cur.fetchone()
conn.close()

if not row:
    print("❌ Roll number not found")
    exit()

db_face = np.frombuffer(row[0], dtype=np.float64)
print("✅ Loaded face for", TEST_ROLL)

# -------------------------------
# Open webcam
# -------------------------------
cap = cv2.VideoCapture(0)

print("\n📷 Look at the camera")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)

    if faces:
        live_enc = face_recognition.face_encodings(rgb, faces)[0]

        # Compute distance
        dist = face_recognition.face_distance([db_face], live_enc)[0]
        match = dist < THRESHOLD

        # Display result
        text = f"Distance: {dist:.3f} | {'MATCH' if match else 'NO MATCH'}"
        color = (0,255,0) if match else (0,0,255)

        top, right, bottom, left = faces[0]
        cv2.rectangle(frame,(left,top),(right,bottom),color,2)
        cv2.putText(frame, text, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Verification Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
