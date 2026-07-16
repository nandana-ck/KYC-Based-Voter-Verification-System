import sqlite3
import face_recognition

def add_voter(name, roll_number, image_path):
    conn = sqlite3.connect("voting_system.db")
    cursor = conn.cursor()

    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            face_blob = encodings[0].tobytes()
            print(f"Face detected for {roll_number}")
        else:
            face_blob = None
            print(f"No face detected for {roll_number}, inserting without encoding")

    except Exception as e:
        face_blob = None
        print(f"Error processing {image_path}: {e}")

    cursor.execute("""
        INSERT OR IGNORE INTO voters (name, roll_number, face_encoding, image_path, has_voted)
        VALUES (?, ?, ?, ?, 0)
    """, (name, roll_number, face_blob, image_path))

    conn.commit()
    conn.close()
    print(f"Voter {name} added successfully")

if __name__ == "__main__":
    add_voter("Student 108", "AMENU4ECE23108", "images/voters/108.jpg")
    add_voter("Student 111", "AMENU4ECE23111", "images/voters/111.jpg")
    add_voter("Student 112", "AMENU4ECE23112", "images/voters/112.jpg")
    add_voter("Student 115", "AMENU4ECE23115", "images/voters/115.jpg")
    add_voter("Student 120", "AMENU4ECE23120", "images/voters/120.jpg")
    add_voter("Student 126", "AMENU4ECE23126", "images/voters/126.jpg")
    add_voter("Student 134", "AMENU4ECE23134", "images/voters/134.jpg")
    add_voter("Student 136", "AMENU4ECE23136", "images/voters/136.jpg")
    add_voter("Student 138", "AMENU4ECE23138", "images/voters/138.jpg")
    add_voter("Student 139", "AMENU4ECE23139", "images/voters/139.jpg")
    add_voter("Student 142", "AMENU4ECE23142", "images/voters/142.jpg")
    add_voter("Student 145", "AMENU4ECE23145", "images/voters/145.jpg")
    add_voter("Student 148", "AMENU4ECE23148", "images/voters/148.jpg")
    add_voter("Student 150", "AMENU4ECE23150", "images/voters/150.jpg")
    add_voter("Student 151", "AMENU4ECE23151", "images/voters/151.jpg")
    add_voter("Student 161", "AMENU4ECE23161", "images/voters/161.jpg")
    add_voter("Student 164", "AMENU4ECE23164", "images/voters/164.jpg")