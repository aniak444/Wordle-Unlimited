import customtkinter as ctk
from src.engine import GameEngine

class WordleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.game = GameEngine()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("Wordle Unlimited")
        self.geometry("450x700")
        
        # Zadanie #59: Blokada zmiany rozmiaru okna głównego
        self.resizable(False, False)
        
        self.header_label = ctk.CTkLabel(
            self,
            text="WORDLE",
            font=("Verdana", 36, "bold"),
            text_color="#80C17A"
        )
        self.header_label.pack(pady=(25, 0))
        
        self.subheader_label = ctk.CTkLabel(
            self,
            text="UNLIMITED",
            font=("Verdana", 24),
            text_color="#538D4E"
        )
        self.subheader_label.pack(pady=(0, 0))
        
        # Zadanie #91: Pływający dymek powiadomień (używany przy błędnym słowie)
        self.etykieta_powiadomienia = ctk.CTkLabel(
            self,
            text="",
            font=("Verdana", 14, "bold"),
            text_color="#FFFFFF",
            fg_color="#3A3A3C",
            corner_radius=6,
            height=35,
            padx=15
        )
        
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(expand=True, pady=(20, 20))
        
        self.hint_container = ctk.CTkFrame(self, fg_color="transparent")
        self.hint_container.pack(pady=(0, 20))
        
        self.hint_button = ctk.CTkButton(
            self.hint_container,
            text="PODPOWIEDŹ",
            font=("Verdana", 16),
            fg_color="#3A3A3C",     # ZADANIE #79: Startowy kolor zablokowanego przycisku (ciemnoszary)
            hover_color="#80C17A",
            text_color="#777777",   # ZADANIE #79: Startowy, zgaszony kolor tekstu
            width=150,
            height=40,
            corner_radius=8,
            state="disabled"        # ZADANIE #79: Przycisk jest domyślnie zablokowany na początku gry
        )
        self.hint_button.pack()
        
        self.tiles = []
        self.current_col = 0
        self.word_length = 5
        
        self.bind("<Key>", self.handle_keypress)

        # ======================================================================
        # INTEGRACJA SPRINT 2: Ekran menu startowego z wyborem trudności
        # ======================================================================
        self.stworz_menu_startowe()

    def stworz_menu_startowe(self):
        # Ramka przykrywająca widok gry na samym początku
        self.ramka_menu = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.ramka_menu.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        etykieta_tytul = ctk.CTkLabel(self.ramka_menu, text="WORDLE", font=("Verdana", 36, "bold"), text_color="#80C17A")
        etykieta_tytul.pack(pady=(150, 5))
        
        etykieta_podtytul = ctk.CTkLabel(self.ramka_menu, text="UNLIMITED", font=("Verdana", 24), text_color="#538D4E")
        etykieta_podtytul.pack(pady=(0, 40))
        
        etykieta_wybor = ctk.CTkLabel(self.ramka_menu, text="Wybierz poziom trudności:", font=("Verdana", 14), text_color="#FFFFFF")
        etykieta_wybor.pack(pady=10)
        
        # Rozwijana lista wyboru poziomu trudności
        self.wybor_trudnosci = ctk.CTkOptionMenu(
            self.ramka_menu, 
            values=["Łatwy", "Średni", "Trudny"],
            font=("Verdana", 14),
            fg_color="#538D4E",
            button_color="#3A3A3C",
            button_hover_color="#80C17A"
        )
        self.wybor_trudnosci.pack(pady=10)
        
        # Zadanie #62: Dodanie kursora 'hand2' (rączki) do przycisku START
        self.przycisk_start = ctk.CTkButton(
            self.ramka_menu,
            text="START",
            font=("Verdana", 16, "bold"),
            fg_color="#538D4E",
            hover_color="#80C17A",
            text_color="#FFFFFF",
            width=150,
            height=40,
            corner_radius=8,
            cursor="hand2",
            command=self.uruchom_gre
        )
        self.przycisk_start.pack(pady=30)
        
        # Zadanie #63: Bindowanie klawisza ENTER do akcji przycisku START w menu
        self.bind("<Return>", self.obsluga_enter_menu)

    def obsluga_enter_menu(self, zdarzenie):
        self.uruchom_gre()

    def uruchom_gre(self):
        # Zadanie #63: Odpięcie powiązania Entera z menu startowego
        self.unbind("<Return>")
        
        # Zadanie #64: Mapowanie polskich napisów z interfejsu na format tekstowy silnika (Enum)
        mapa_trudnosci = {
            "Łatwy": "EASY",
            "Średni": "MEDIUM",
            "Trudny": "HARD"
        }
        mapa_dlugosci = {
            "Łatwy": 4,
            "Średni": 5,
            "Trudny": 6
        }
        wybrany_tekst = self.wybor_trudnosci.get()
        self.word_length = mapa_dlugosci.get(wybrany_tekst, 5)
        kod_trudnosci = mapa_trudnosci.get(wybrany_tekst, "EASY")

        print(f"[DEBUG UI] Wybór z menu: '{wybrany_tekst}' -> Ustawiona długość: {self.word_length}")
        
        # Przekazanie zmapowanej wartości do silnika gry
        if hasattr(self.game, 'set_difficulty'):
            self.game.set_difficulty(kod_trudnosci)
        elif hasattr(self.game, 'difficulty'):
            self.game.difficulty = kod_trudnosci

        if hasattr(self.game, 'losuj_nowe_slowo'):
            self.game.losuj_nowe_slowo(word_length=self.word_length)
            
        self.create_game_grid()
        # Schowanie ramki menu, odsłaniające siatkę gry
        self.ramka_menu.place_forget()

    def pokaz_powiadomienie(self, komunikat, czas_trwania=2000, kolor_tekstu="#FFFFFF", kolor_tla="#3A3A3C", rely=0.13):
        self.etykieta_powiadomienia.configure(text=komunikat, text_color=kolor_tekstu, fg_color=kolor_tla)
        self.etykieta_powiadomienia.place(relx=0.5, rely=rely, anchor="center")
        self.etykieta_powiadomienia.lift()
        self.after(czas_trwania, self.etykieta_powiadomienia.place_forget)

    def create_game_grid(self):
        
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        self.tiles = []
        
        row_count = 6
        column_count = self.word_length
        
        for row_idx in range(row_count):
            current_row_tiles = []
            for col_idx in range(column_count):
                tile = ctk.CTkLabel(
                    self.grid_container,
                    text="",
                    width=60,
                    height=60,
                    fg_color="#2a2d32",
                    corner_radius=4,
                    font=("Verdana", 24, "bold")
                )
                tile.grid(row=row_idx, column=col_idx, padx=6, pady=6)
                current_row_tiles.append(tile)
                
            self.tiles.append(current_row_tiles)

    def handle_keypress(self, event):
        if self.game.status != "IN_PROGRESS":
            return

        aktualny_rzad = self.game.current_row

        if event.keysym == "Return":
            if self.current_col == self.word_length:
                self.check_current_row()
            return

        if event.keysym == "BackSpace":
            if self.current_col > 0:
                self.current_col -= 1
                self.tiles[aktualny_rzad][self.current_col].configure(text="")
            return

        char = event.char
        if char.isalpha() and len(char) == 1:
            char_upper = char.upper()
            if self.current_col < self.word_length:
                self.tiles[aktualny_rzad][self.current_col].configure(text=char_upper)
                self.current_col += 1

    def check_current_row(self):
        aktualny_rzad = self.game.current_row
        
        guess = ""
        for col in range(self.word_length):
            guess += self.tiles[aktualny_rzad][col].cget("text")

        colors = self.game.check_word(guess)

        # ======================================================================
        # Zadanie #91: Obsługa błędu 'INVALID_WORD' (brak słowa w bazie słownika)
        # ======================================================================
        if colors == ["INVALID_WORD"] or colors in ("INVALID_WORD", "INVALID", False, None):
            self.pokaz_powiadomienie(
                komunikat="Słowo niedopuszczalne w grach!",
                czas_trwania=2000,
                kolor_tekstu="#FF4D4D",
                kolor_tla="transparent",
                rely=0.78
                )
            return

        color_map = {
            "GREEN": "#538D4E",
            "YELLOW": "#B59F3B",
            "GRAY": "#3A3A3C"
        }

        liczba_kolorow = min(self.word_length, len(colors))
        for col in range(self.word_length):
            status = colors[col]
            self.tiles[aktualny_rzad][col].configure(fg_color=color_map[status])

        self.current_col = 0

        # ZADANIE #79: Dynamiczna aktywacja przycisku Podpowiedzi i zmiana kolorów
        if self.game.status == "IN_PROGRESS" and self.game.current_row >= 3:
            self.hint_button.configure(
                state="normal",
                fg_color="#538D4E",   # Zmiana na aktywny zielony
                text_color="#FFFFFF"  # Zmiana na aktywny biały tekst
            )

        # Wyświetlanie ekranu wygranej
        if self.game.status == "WIN":
            self.show_win_overlay()
        # Wyświetlanie ekranu przegranej
        if self.game.status == "LOSE":
            self.show_lose_overlay()

    # ======================================================================
    # ZADANIA #88, #89, #90, #92, #65: Logika pełnego twardego restartu gry
    # ======================================================================
    def restartuj_gre(self):
        def czyszczenie_i_powrot_do_menu():
            # Zadanie #88 & #65: Reset stanu silnika gry w backendzie
            self.game = GameEngine()
            
            self.current_col = 0
            
            if hasattr(self, 'tiles') and self.tiles:
                for rzad in self.tiles:
                    for kafelek in rzad:
                        try:
                            kafelek.destroy()
                        except Exception:
                            pass
                self.titles = []

            # ZADANIE #79: Ponowna blokada przycisku podpowiedzi na starcie nowej gry
            self.hint_button.configure(
                state="disabled",
                fg_color="#3A3A3C",   # Powrót do ciemnoszarego
                text_color="#777777"  # Powrót do zgaszonego tekstu
            )
            
            self.stworz_menu_startowe()

        if hasattr(self, 'overlay_frame') and self.overlay_frame.winfo_exists():
            self.animuj_chowanie_overlay(aktualne_rely=0.5, krok=0.06, callback=czyszczenie_i_powrot_do_menu)
        else:    
            czyszczenie_i_powrot_do_menu()
            
            
    def show_win_overlay(self):
        self.overlay_frame = ctk.CTkFrame(
            self,
            width=400,
            height=240,
            fg_color="#1e1e1e",
            border_width=2,
            border_color="#538D4E",
            corner_radius=24,
        )
        self.overlay_frame.pack_propagate(False)
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            self.overlay_frame,
            text="WYGRYWASZ :D",
            font=("Verdana", 28, "bold"),
            text_color="#538D4E"
        )
        title.pack(pady=(20, 5))
        
        desc = ctk.CTkLabel(
            self.overlay_frame,
            text=f"Udało Ci się odgadnąć hasło \"{self.game.target_word}!\"\nLiczba prób: {self.game.current_row}",
            font=("Verdana", 18),
            text_color="#80C17A"
        )
        desc.pack(pady=(10, 15))

        przycisk_restartu = ctk.CTkButton(
            self.overlay_frame,
            text="Graj Ponownie",
            font=("Verdana", 16, "bold"),
            fg_color="#538D4E",
            hover_color="#80C17A",
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.restartuj_gre
        )
        przycisk_restartu.pack(pady=(0, 15))

    def show_lose_overlay(self):
        self.overlay_frame = ctk.CTkFrame(
            self,
            width=400,
            height=240,
            fg_color="#1e1e1e",
            border_width=2,
            border_color="#B52A2A",
            corner_radius=24,
        )
        self.overlay_frame.pack_propagate(False)
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            self.overlay_frame,
            text="PRZEGRYWASZ :(",
            font=("Verdana", 28, "bold"),
            text_color="#B52A2A"
        )
        title.pack(pady=(20, 5))
        
        desc = ctk.CTkLabel(
            self.overlay_frame,
            text=f"Hasłem było: \"{self.game.target_word}\"\nSpróbuj ponownie!",
            font=("Verdana", 18),
            text_color="#F17979"
        )
        desc.pack(pady=(10, 15))

        przycisk_restartu = ctk.CTkButton(
            self.overlay_frame,
            text="Graj Ponownie",
            font=("Verdana", 16, "bold"),
            fg_color="#B52A2A",
            hover_color="#F17979",
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.restartuj_gre
        )
        przycisk_restartu.pack(pady=(0, 15))
    
    def animuj_chowanie_overlay(self, aktualne_rely=0.5, krok=0.05, callback=None):
        if hasattr(self, 'overlay_frame') and self.overlay_frame.winfo_exists():
            nowe_rely = aktualne_rely + krok
            
            if nowe_rely < 1.3:
                self.overlay_frame.place(relx=0.5, rely=nowe_rely, anchor="center")
                self.after(15, lambda: self.animuj_chowanie_overlay(nowe_rely, krok, callback))
            else:
                self.overlay_frame.place_forget()
                if callback:
                    callback()