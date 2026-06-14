from src.ui import WordleApp
from src.database import init_db, seed_database
import ctypes
import platform

if __name__ == "__main__":

    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(f"[DEBUG] Nie udało się skonfigurować DPI Awareness: {e}")

    # inicjalizacja bazy danych
    init_db()
    seed_database()

    # odpalenie aplikacji
    app = WordleApp()
    app.mainloop()