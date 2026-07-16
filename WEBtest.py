import cv2
import numpy as np
import pytesseract
from ultralytics import YOLO

# ===========================
# TESSERACT PATH
# ===========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ===========================
# LOAD YOLO MODEL
# ===========================
model = YOLO(r"C:\Users\hp\Downloads\best (1).pt")

# ===========================
# CLASS COLORS
# ===========================
CLASS_COLORS = {
    0: (255, 0, 0),   # id
    1: (0, 255, 0),   # name
    2: (0, 0, 255)    # roll
}

# ===========================
# OPEN CAMERA
# ===========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("❌ Webcam not found")

print("📷 Camera started... Show ID card")

# ===========================
# MAIN LOOP
# ===========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.6, classes=[0,1,2], verbose=False)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            label = model.names[cls_id]
            color = CLASS_COLORS.get(cls_id, (255,255,255))

            # Draw box
            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
            cv2.putText(frame,f"{label} {conf:.2f}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,color,2)

            # ===========================
            # OCR FOR ROLL NUMBER
            # ===========================
            if label.lower() == "roll":
                roi = frame[y1:y2, x1:x2]

                if roi.size > 0:
                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    thresh = cv2.threshold(gray, 0, 255,
                                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                    text = pytesseract.image_to_string(thresh, config="--psm 7")
                    roll = text.strip().replace(" ", "").replace("\n","")

                    if len(roll) > 3:
                        print("🆔 Extracted Roll Number:", roll)

                        cv2.putText(frame, roll,
                                    (x1, y2 + 30),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (0,255,0),2)

    cv2.imshow("Smart ID Detection + OCR", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ===========================
# CLEANUP
# ===========================
cap.release()
cv2.destroyAllWindows()
