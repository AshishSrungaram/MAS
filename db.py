import sqlite3
from datetime import datetime
# Database setup


def setup_database():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        dob DATE NOT NULL,
                        medical_history TEXT,
                        contact TEXT,
                        last_visit DATE
                      )''')
    conn.commit()
    conn.close()
# Add a patient


def add_patient(name, dob, medical_history, contact):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO patients (name, dob, medical_history, contact, last_visit) VALUES (?, ?, ?, ?, ?)',
                   (name, dob, medical_history, contact, datetime.now().date()))
    conn.commit()
    conn.close()

# Fetch patient by name and DOB


def fetch_patient(name, dob):
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM patients WHERE name = ? AND dob = ?', (name, dob))
    patient = cursor.fetchone()
    conn.close()
    return patient
