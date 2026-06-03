from src.ui import WordleApp
from src.database import init_db, seed_database

if __name__ == "__main__":
    # inicjalizacja bazy danych
    init_db()
    seed_database()

    # odpalenie aplikacji
    app = WordleApp()
    app.mainloop()