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
        
        # Zadanie #91: Pływający dymek powiadomień
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
            fg_color="#3A3A3C",
            hover_color="#80C17A",
            text_color="#777777",
            width=150,
            height=40,
            corner_radius=8,
            state="disabled",
            command=self.pokaz_podpowiedz
        )
        self.hint_button.pack()
        
        # ZADANIE #80: Konstrukcja dymka informacyjnego
        self.hint_popup_frame = ctk.CTkFrame(
            self,
            width=350,
            height=80,
            fg_color="#1e1e1e",
            border_width=2,
            border_color="#B59F3B",
            corner_radius=12
        )
        self.hint_popup_frame.pack_propagate(False)
        
        self.hint_popup_label = ctk.CTkLabel(
            self.hint_popup_frame,
            text="Placeholder (powinno być tekstem z bazy)...",
            font=("Verdana", 14),
            text_color="#FFFFFF",
            wraplength=320
        )
        self.hint_popup_label.pack(expand=True, padx=10, pady=10)
        
        self.tiles = []
        self.current_col = 0
        
        self.create_game_grid()
        self.bind("<Key>", self.handle_keypress)

        # Wywołanie menu startowego
        self.stworz_menu_startowe()

    def stworz_menu_startowe(self):
        # Ramka przykrywająca widok gry na samym początku
        self.ramka_menu = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.ramka_menu.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        etykieta_tytul = ctk.CTkLabel(self.ramka_menu, text="WORDLE", font=("Verdana", 36, "bold"), text_color="#80C17A")
        etykieta_tytul.pack(pady=(80, 5))
        
        etykieta_podtytul = ctk.CTkLabel(self.ramka_menu, text="UNLIMITED", font=("Verdana", 24), text_color="#538D4E")
        etykieta_podtytul.pack(pady=(0, 20))
        
        # ======================================================================
        # ZADANIE #36: Komponent wyboru długości słowa (Segmented Button)
        # ======================================================================
        etykieta_dlugosc = ctk.CTkLabel(self.ramka_menu, text="Wybierz długość słowa:", font=("Verdana", 14), text_color="#FFFFFF")
        etykieta_dlugosc.pack(pady=(10, 5))
        
        self.wybor_dlugosci = ctk.CTkSegmentedButton(
            self.ramka_menu,
            values=["4", "5", "6"],
            font=("Verdana", 14),
            selected_color="#538D4E",
            selected_hover_color="#80C17A",
            unselected_color="#3A3A3C",
            unselected_hover_color="#4A4A4C"
        )
        self.wybor_dlugosci.pack(pady=5)
        self.wybor_dlugosci.set("5")  # Ustawienie 5 jako wartości domyślnej

        # ======================================================================
        # INTEGRACJA SPRINT 2: Wybór poziomu trudności
        # ======================================================================
        etykieta_wybor = ctk.CTkLabel(self.ramka_menu, text="Wybierz poziom trudności:", font=("Verdana", 14), text_color="#FFFFFF")
        etykieta_wybor.pack(pady=(10, 5))
        
        self.wybor_trudnosci = ctk.CTkOptionMenu(
            self.ramka_menu, 
            values=["Łatwy", "Średni", "Trudny"],
            font=("Verdana", 14),
            fg_color="#538D4E",
            button_color="#3A3A3C",
            button_hover_color="#80C17A"
        )
        self.wybor_trudnosci.pack(pady=5)
        
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
        self.przycisk_start.pack(pady=25)
        
        # Zadanie #63: Bindowanie klawisza ENTER do akcji przycisku START w menu
        self.bind("<Return>", self.obsluga_enter_menu)

    def obsluga_enter_menu(self, zdarzenie):
        self.uruchom_gre()

    def uruchom_gre(self):
        # Zadanie #63: Odpięcie powiązania Entera z menu startowego
        self.unbind("<Return>")
        
        # Mapowanie polskich napisów z interfejsu na format tekstowy silnika (Enum)
        mapa_trudnosci = {
            "Łatwy": "EASY",
            "Średni": "MEDIUM",
            "Trudny": "HARD"
        }
        wybrany_tekst = self.wybor_trudnosci.get()
        kod_trudnosci = mapa_trudnosci.get(wybrany_tekst, "EASY")
        
        # Pobranie wybranej długości słowa (Zadanie #36)
        wybrana_dlugosc = int(self.wybor_dlugosci.get())
        
        # Przekazanie zmapowanych wartości do silnika gry
        if hasattr(self.game, 'reset_state'):
            self.game.reset_state(length=wybrana_dlugosc, difficulty=kod_trudnosci)
        else:
            if hasattr(self.game, 'difficulty'):
                self.game.difficulty = kod_trudnosci
            if hasattr(self.game, 'length'):
                self.game.length = wybrana_dlugosc
            
        # Schowanie ramki menu, odsłaniające siatkę gry
        self.ramka_menu.place_forget()

    # ZADANIE #80: Funkcja wyświetlająca dymek po kliknięciu
    def pokaz_podpowiedz(self):
        self.hint_popup_frame.place(relx=0.5, rely=0.76, anchor="center")

    def pokaz_powiadomienie(self, komunikat, czas_trwania=2000):
        self.etykieta_powiadomienia.configure(text=komunikat)
        self.etykieta_powiadomienia.place(relx=0.5, rely=0.13, anchor="center")
        self.after(czas_trwania, self.etykieta_powiadomienia.place_forget)

    def create_game_grid(self):
        row_count = 6
        column_count = 5 # Tutaj zostaje 5 dla wizualnego maksymalnego grida, gra zarządza logiką użycia
        
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
            if self.current_col == self.game.length:
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
            if self.current_col < self.game.length:
                self.tiles[aktualny_rzad][self.current_col].configure(text=char_upper)
                self.current_col += 1

    def check_current_row(self):
        aktualny_rzad = self.game.current_row
        
        guess = ""
        for col in range(self.game.length):
            guess += self.tiles[aktualny_rzad][col].cget("text")

        colors = self.game.check_word(guess)

        # ======================================================================
        # Zadanie #91: Obsługa błędu 'INVALID_WORD'
        # ======================================================================
        if colors == ["INVALID_WORD"] or colors == "INVALID_WORD":
            self.pokaz_powiadomienie("Słowo niedopuszczalne w grach!")
            return

        color_map = {
            "GREEN": "#538D4E",
            "YELLOW": "#B59F3B",
            "GRAY": "#3A3A3C"
        }

        for col in range(self.game.length):
            status = colors[col]
            self.tiles[aktualny_rzad][col].configure(fg_color=color_map[status])

        self.current_col = 0

        # ZADANIE #79: Dynamiczna aktywacja przycisku Podpowiedzi i zmiana kolorów
        if self.game.status == "IN_PROGRESS" and self.game.current_row >= 3:
            self.hint_button.configure(
                state="normal",
                fg_color="#538D4E",
                text_color="#FFFFFF"
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
        # Reset stanu silnika gry w backendzie
        self.game.reset_state()
        
        # Reset lokalnego wskaźnika kolumn we Frontendzie
        self.current_col = 0
        
        # Ponowna blokada przycisku podpowiedzi na starcie nowej gry
        self.hint_button.configure(
            state="disabled",
            fg_color="#3A3A3C",
            text_color="#777777"
        )
        
        # Ukrycie dymka podpowiedzi, jeśli był otwarty
        self.hint_popup_frame.place_forget()
        
        # Wizualny reset siatki
        for rzad_kafelkow in self.tiles:
            for pojedynczy_kafelek in rzad_kafelkow:
                pojedynczy_kafelek.configure(
                    text="",             
                    fg_color="#2a2d32"    
                )
        
        # Ukrycie nakładki końcowej
        self.overlay_frame.place_forget()

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
            text=f"Udało Ci się odgadnąć hasło \"{self.game.get_target_word()}!\"\nLiczba prób: {self.game.current_row}",
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
            text=f"Hasłem było: \"{self.game.get_target_word()}\"\nSpróbuj ponownie!",
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
