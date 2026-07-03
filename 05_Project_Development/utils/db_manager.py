import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("database", "hdi_history.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the prediction history database and table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            country TEXT,
            life_expectancy REAL NOT NULL,
            expected_schooling REAL NOT NULL,
            mean_schooling REAL NOT NULL,
            gni_per_capita REAL NOT NULL,
            predicted_category TEXT NOT NULL,
            prediction_confidence REAL NOT NULL,
            hdi_score REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_prediction(country, life_expectancy, expected_schooling, mean_schooling, gni_per_capita, predicted_category, prediction_confidence, hdi_score):
    """Inserts a prediction entry into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO predictions (
            timestamp, country, life_expectancy, expected_schooling, mean_schooling, gni_per_capita, predicted_category, prediction_confidence, hdi_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, country or "Custom", life_expectancy, expected_schooling, mean_schooling, gni_per_capita, predicted_category, prediction_confidence, hdi_score))
    conn.commit()
    conn.close()

def get_history(search=None, category=None, sort_by='date_desc'):
    """Retrieves prediction history with optional searching, filtering, and sorting."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM predictions WHERE 1=1"
    params = []
    
    if search:
        query += " AND country LIKE ?"
        params.append(f"%{search}%")
        
    if category:
        query += " AND predicted_category = ?"
        params.append(category)
        
    # Sort order
    if sort_by == 'date_asc':
        query += " ORDER BY timestamp ASC"
    elif sort_by == 'score_desc':
        query += " ORDER BY hdi_score DESC"
    elif sort_by == 'score_asc':
        query += " ORDER BY hdi_score ASC"
    else:  # default 'date_desc'
        query += " ORDER BY timestamp DESC"
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_prediction(pred_id):
    """Deletes a specific prediction entry by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    conn.commit()
    conn.close()

def clear_history():
    """Clears all records from prediction history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()

# Initialize when imported
init_db()
