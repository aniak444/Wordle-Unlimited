from src.engine import GameEngine
from src.ui import WordleApp

if __name__ == "__main__":
    print("Test GameEngine \n")
    
    gra = GameEngine()
    print(f"Haslo: {gra.target_word}")
    print(f"Status poczatkowy: {gra.status}, aktualny rząd: {gra.current_row}\n")

    def kliknieto_enter(wpisane_slowo: str):
        if len(wpisane_slowo) == 5:
            wynik = gra.check_word(wpisane_slowo)
            print(f"Wynik analizy: {wynik}")
        else:
            print("Wyświetl komunikat na ekranie: Za mało liter!")

    def kliknieto_backspace(kafelki: list):
        if len(kafelki) > 0:
            usunieta = kafelki.pop()
            print(f"[BACKSPACE] Usunięto: '{usunieta}'. Aktualny stan rzędu: {kafelki}")
        else:
            print("[BACKSPACE] Blokada: Brak liter do usunięcia (indeks 0)!")

    print("--- TEST BACKSPACE ---")
    moje_kafelki = ["K", "O", "D"]
    print(f"Stan początkowy kafelków: {moje_kafelki}")
    
    kliknieto_backspace(moje_kafelki)
    kliknieto_backspace(moje_kafelki)
    kliknieto_backspace(moje_kafelki)
    kliknieto_backspace(moje_kafelki)
    print("---------------------\n")

    proba1 = "KOLOR"
    wynik1 = gra.check_word(proba1)
    print(f"Wpisane: {proba1} -> Wynik: {wynik1}")
    print(f"Status po próbie 1: {gra.status}, aktualny rząd: {gra.current_row}\n")

    proba2 = "DEROK"
    wynik2 = gra.check_word(proba2)
    print(f"Wpisane: {proba2} -> Wynik: {wynik2}")
    print(f"Status po próbie 2: {gra.status}, aktualny rząd: {gra.current_row}\n")

    proba3 = "KODER"
    wynik3 = gra.check_word(proba3)
    print(f"Wpisane: {proba3} -> Wynik: {wynik3}")
    print(f"Status po próbie 3: {gra.status}, aktualny rząd: {gra.current_row}\n")


    app = WordleApp()
    app.mainloop()