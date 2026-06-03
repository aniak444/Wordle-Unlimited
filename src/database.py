import sqlite3
import json
import os

DB_PATH = "wordle.db"

def init_db():
    #Tworzy tabele w bazie danych jesli jeszcze nei istnieje
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            length INTEGER NOT NULL,
            difficulty TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_database(json_path="words.json"):
    #wczytuje słowa z pliku JSON do bazy, zapobiega duplikatom
    if not os.path.exists(json_path):
        print(f"Plik {json_path} nie istnieje")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM words")
    count = cursor.fetchone()[0]
    
    if count > 0:
        # baza danych juz zasilona, zamykamy polaczenie
        conn.close()
        return
        
    # jesli baza jest pusta
    with open(json_path, 'r', encoding='utf-8') as file:
        try:
            words_data = json.load(file)
        except json.JSONDecodeError:
            print("Blad odczytu pliku")
            conn.close()
            return

    # insert or ignore chroni przed duplikatami
    for entry in words_data:
        word = entry.get("word", "").upper()
        length = entry.get("length", len(word))
        difficulty = entry.get("difficulty", "MEDIUM").upper()
        
        cursor.execute('''
            INSERT OR IGNORE INTO words (word, length, difficulty)
            VALUES (?, ?, ?)
        ''', (word, length, difficulty))
        
    conn.commit()
    conn.close()
    print(f"Pomyślnie dodano {len(words_data)} słów do bazy danych")