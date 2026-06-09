import sqlite3
import json
import os
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import quote

# dodanie zmiennych konfiguracyjnych
DB_PATH = os.path.join(os.getcwd(), "wordle.db")
TABLE_NAME = "words"

def init_db():
    # tworzy tabele w bazie danych jesli jeszcze nei istnieje
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            length INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            hint TEXT DEFAULT 'Brak podpowiedzi'
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_database(json_path="words.json"):
    # wczytuje słowa z pliku JSON do bazy, zapobiega duplikatom
    if not os.path.exists(json_path):
        print(f"Plik {json_path} nie istnieje")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
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
        hint = entry.get("hint", "Brak podpowiedzi")
        
        cursor.execute(f'''
            INSERT OR IGNORE INTO {TABLE_NAME} (word, length, difficulty, hint)
            VALUES (?, ?, ?, ?)
        ''', (word, length, difficulty, hint))
        
    conn.commit()
    conn.close()
    print(f"Pomyślnie dodano {len(words_data)} słów do bazy danych")


def get_random_word(length: int, difficulty: str) -> tuple:
    # wyciaga losowe slowo z bazy danych dopasowane do parametrow z menu
    difficulty = difficulty.upper()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        SELECT word, hint FROM {TABLE_NAME} 
        WHERE length = ? AND difficulty = ? 
        ORDER BY RANDOM() LIMIT 1
    ''', (length, difficulty))
    
    result = cursor.fetchone()
    
    if result is None:
        print(f"Brak w bazie słowa ({length} liter, {difficulty}). Fallback")
        cursor.execute(f'''
            SELECT word, hint FROM {TABLE_NAME} 
            WHERE length = ? 
            ORDER BY RANDOM() LIMIT 1
        ''', (length,))
        result = cursor.fetchone()

    conn.close()
    
    if result:
        return result[0], result[1]
    else:
        return "ERROR", "Brak podpowiedzi"
    

def is_word_valid(word: str) -> bool:
    # walidacja slowa przez slownik jezyka polskiego
    word_lower = word.lower()
    safe_word = quote(word_lower)
    url = f"https://sjp.pl/{safe_word}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=2) as response:
            html = response.read().decode('utf-8')
            
            if "dopuszczalne w grach" in html:
                return True
            else:
                return False
                
    except HTTPError as e:
        if e.code == 404:
            return False
        return True
        
    except URLError:
        print(f"Brak internetu/blad api, slowo zostalo zaakceptowane")
        return True