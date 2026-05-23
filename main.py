from src.engine import GameEngine

if __name__ == "__main__":
    print("Test GameEngine \n")
    
    gra = GameEngine()
    print(f"Haslo: {gra.target_word}")
    print(f"Status poczatkowy: {gra.status}, aktualny rząd: {gra.current_row}\n")

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