# Wordle Unlimited - Aplikacja Desktopowa

Projekt realizowany w ramach przedmiotu **Narzędzia Pracy Grupowej (NPG)**.

---

## Opis produktu

**Wordle Unlimited** to nowoczesna, samodzielna aplikacja desktopowa inspirowana grą internetową "Wordle", tworzoną przez NYT. Nasza wersja usuwa największą wadę oryginału – ograniczenie do jednej rozgrywki dziennie – i wprowadza szereg ulepszeń, które transformują prostą minigrę w rozbudowaną aplikację.

Gra opiera się na aplikacji okienkowej (system desktopowy), eliminując potrzebę uruchamiania przeglądarki internetowej czy instalowania ciężkich środowisk kontenerowych przez użytkownika końcowego.

### Kluczowe mechaniki i dodatkowe funkcjonalności projektu:
* **Tryb Nieskończony (Endless Mode):** Po zakończeniu rozgrywki (wygranej lub przegranej) użytkownik może natychmiast rozpocząć nową partię z nowym, losowym hasłem.
* **Inteligentny System Podpowiedzi (Hint System):** Jeśli gracz ma problem z odgadnięciem słowa, po 3. nieudanej próbie aplikacja odblokowuje podpowiedź.
* **Wybór długości słowa:** Użytkownik przed startem decyduje, czy chce zgadywać słowa 4-, 5-, lub 6-literowe. Plansza gry dynamicznie dostosowuje swój rozmiar.
* **Poziomy trudności haseł:** Słowa w bazie są kategoryzowane według stopnia zaawansowania (od prostych słów codziennych po rzadkie terminy).

---

## Zasady gry

1. Celem gracza jest odgadnięcie ukrytego słowa w maksymalnie **6 próbach**.
2. Każde wpisane słowo musi mieć poprawną długość (zgodną z wybranym ustawieniem) i istnieć w słowniku gry.
3. Po zatwierdzeniu słowa, kafelki zmieniają kolor, udzielając graczowi informacji zwrotnej:
    * 🟩 **Zielony:** Litera znajduje się w słowie i jest na poprawnej pozycji.
    * 🟨 **Żółty:** Litera znajduje się w słowie, ale na innej pozycji.
    * ⬛ **Szary:** Litera w ogóle nie występuje w ukrytym słowie.
4. Od 4. próby gracz może skorzystać z unikalnej podpowiedzi tekstowej.

---

## Architektura i kod

Aplikacja została zaprojektowana zgodnie z dobrymi praktykami inżynierii oprogramowania. Wyraźnie oddzielono warstwę logiki gry (operacje na słowach, weryfikacja i baza danych) od warstwy widoku/UI. Dzięki temu kod jest przejrzysty, łatwiejszy w utrzymaniu i gotowy do dalszego skalowania.

---

## Tech Stack

* **Frontend / UI:** Python + `CustomTkinter`
* **Logika / API:** Python 3.x
* **Baza danych:** `SQLite` (lokalna baza danych generowana w AppData)
* **Dystrybucja:** `PyInstaller` 

---

## Jak uruchomić grę

**Opcja 1: Uruchomienie gotowej gry**
Wystarczy pobrać wygenerowany plik `WordleUnlimited.exe` i uruchomić go dwukrotnym kliknięciem. Gra działa natychmiast, nie wymaga instalacji żadnych dodatkowych programów ani środowiska Python na Twoim komputerze.

**Opcja 2: Uruchomienie z kodu źródłowego**
1. Zainstaluj wymagane biblioteki poleceniem w terminalu: `pip install -r requirements.txt`
2. Uruchom grę wpisując: `python main.py`

**Opcja 3: Kompilacja własnego pliku wykonywalnego (Zalecane)**
1. Zainstaluj wymagane biblioteki poleceniem w terminalu: `pip install -r requirements.txt`
2. Zbuduj plik .exe za pomocą komendy:
    ```bash
        pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --add-data "words.json;." --add-data "icon.ico;." --collect-all customtkinter "main.py"
    ```
3. W nowo utworzonym folderze dist/ znajdziesz plik wykonywalny main.exe

---
> **Status projektu:** Zakończony
---

## Licencja

Udostępniany jest na licencji **MIT**.
