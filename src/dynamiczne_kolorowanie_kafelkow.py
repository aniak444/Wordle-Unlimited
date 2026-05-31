def get_tile_color(status_code):
    """
    Zamienia kod z backendu na kolor kafelka w GUI.
    2 - zielony (dobra litera, dobre miejsce)
    1 - żółty (dobra litera, złe miejsce)
    0 - ciemnoszary (zła litera)
    """
    # Używam tu kodów HEX (kolorów z oryginalnego Wordle), 
    # ale jeśli Twoje GUI woli zwykłe nazwy np. "green", "yellow", to po prostu to tu podmień.
    
    if status_code == 2:
        return "#538d4e"  # Zielony
    elif status_code == 1:
        return "#b59f3b"  # Żółty
    elif status_code == 0:
        return "#3a3a3c"  # Ciemnoszary
    else:
        return "black"    # Awaryjnie, gdyby backend zwrócił coś dziwnego

def process_word_colors(backend_results):
    """
    Przyjmuje listę wyników z backendu, np. [2, 0, 1, 2, 0]
    i zwraca gotową listę kolorów do pokolorowania kafelków w rzędzie.
    """
    return [get_tile_color(code) for code in backend_results]

# --- Przykład działania ---
if __name__ == "__main__":
    # Załóżmy, że backend dla słowa sprawdził litery i zwrócił taką listę:
    wyniki_od_chlopakow_z_backendu = [2, 0, 1, 2, 0] 
    
    # Przemielamy to przez naszą funkcję
    kolory_dla_interfejsu = process_word_colors(wyniki_od_chlopakow_z_backendu)
    
    print(f"Dane z backendu: {wyniki_od_chlopakow_z_backendu}")
    print(f"Kolory do wstawienia: {kolory_dla_interfejsu}")
