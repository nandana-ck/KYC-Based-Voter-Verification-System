# KYC-Based Voter Verification System Using Facial Authentication and OCR-Based ID Verification

A Flask-based intelligent electronic voting system that verifies voter identity using **facial authentication** and **YOLO-based Optical Character Recognition (OCR)** before allowing a user to cast a vote. The system aims to improve the security and reliability of electronic voting by performing multi-stage identity verification.

---

## Project Overview

Traditional electronic voting systems often rely only on login credentials or manual verification, which may be vulnerable to impersonation or identity fraud.

This project introduces a two-stage voter verification process:

1. Facial Authentication using Face Recognition
2. ID Card Verification using YOLO Object Detection and OCR

Only voters who successfully pass both verification stages are allowed to vote.

---

## Features

- Secure voter authentication
- Face verification using Face Recognition
- ID card detection using YOLO
- Roll number extraction using Tesseract OCR
- Dual-factor identity verification
- Admin dashboard for voter monitoring
- Election result display
- SQLite database integration
- Flask-based web interface

---

## System Workflow

1. Voter enters their roll number.
2. Live face is captured through the webcam.
3. Face encoding is matched with the registered voter.
4. The voter shows their ID card.
5. YOLO detects the roll number region.
6. OCR extracts the roll number.
7. The extracted roll number is matched with the entered roll number.
8. If both verifications succeed, the voter can cast a vote.
9. The vote is securely recorded in the database.

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Face Recognition | face_recognition |
| Object Detection | YOLOv8 |
| OCR | Tesseract OCR |
| Image Processing | OpenCV |
| Numerical Computing | NumPy |
| Frontend | HTML, CSS |

---

## Project Structure

```text
KYC-Based-Voter-Verification-System/
│
├── app.py
├── create_db.py
├── database.py
├── face_test_live.py
├── WEBtest.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│
├── images/
│   ├── block_diagram.jpeg
│   ├── flowchart_voter.png
│   ├── confusion_matrix_facerecog.jpg
│   ├── confusion_matrix_ocr.jpg
│   └── roc_facerecog.jpg
│
└── models/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/KYC-Based-Voter-Verification-System.git
```

Move into the project folder:

```bash
cd KYC-Based-Voter-Verification-System
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the database setup:

```bash
python create_db.py
```

Start the Flask application:

```bash
python app.py
```

---

## Demo Credentials

Admin Login

```
Username: admin
Password: admin123
```

---

## Privacy Notice

The original dataset and database used during development are **not included** in this repository.

The repository does **not** contain:

- Face images of participants
- Personal ID card images
- Real voter database

These files have been removed to protect participant privacy.

Users can create their own dataset and database for testing.

---

## Results

The project achieved reliable performance for:

- Face Authentication
- ID Card Detection
- OCR-based Roll Number Recognition

Performance graphs such as the confusion matrix and ROC curve are included in the repository.

---

## Future Improvements

- Aadhaar QR verification
- Liveness detection
- Fingerprint authentication
- Face anti-spoofing
- Blockchain-based vote storage
- Cloud deployment

---

## Conference Publication

This project served as the basis for a research paper accepted at the **International Conference on Electronics, Computing, Communication and Control Technology (ICECCC 2026)**.

---

## License

This project is intended for educational and research purposes.

