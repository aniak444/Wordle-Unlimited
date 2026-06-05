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
        self.resizable(False, False)
        
        self.header_label = ctk.CTkLabel(
            self,
            text="WORDLE",
            font=("Arial", 36, "bold"),
            text_color="#80C17A"
        )
        self.header_label.pack(pady=(25, 0))
        
        self.subheader_label = ctk.CTkLabel(
            self,
            text="UNLIMITED",
            font=("Arial", 24),
            text_color="#538D4E"
        )
        self.subheader_label.pack(pady=(0, 0))
        
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(expand=True, pady=(20, 20))
        
        self.hint_container = ctk.CTkFrame(self, fg_color="transparent")
        self.hint_container.pack(pady=(0, 20)) 
        
        self.hint_button = ctk.CTkButton(
            self.hint_container,
            text="PODPOWIEDŹ",
            font=("Arial", 16, "bold"),
            fg_color="#538D4E",
            hover_color="#80C17A",
            text_color="#FFFFFF",
            width=150,
            height=40,
            corner_radius=8
        )
        self.hint_button.pack()
        
        self.tiles = []
        self.current_col = 0 
        
        self.create_game_grid()
        self.bind("<Key>", self.handle_keypress)

    def create_game_grid(self):
        row_count = 6
        column_count = 5
        
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
                    font=("Arial", 24, "bold")
                )
                tile.grid(row=row_idx, column=col_idx, padx=6, pady=6)
                current_row_tiles.append(tile)
                
            self.tiles.append(current_row_tiles)

    def handle_keypress(self, event):
        if self.game.status != "IN_PROGRESS":
            return

        aktualny_rzad = self.game.current_row

        if event.keysym == "Return":
            if self.current_col == 5:
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
            if self.current_col < 5:
                self.tiles[aktualny_rzad][self.current_col].configure(text=char_upper)
                self.current_col += 1

    def check_current_row(self):
        aktualny_rzad = self.game.current_row
        
        guess = ""
        for col in range(5):
            guess += self.tiles[aktualny_rzad][col].cget("text")

        colors = self.game.check_word(guess)

        color_map = {
            "GREEN": "#538D4E",
            "YELLOW": "#B59F3B",
            "GRAY": "#3A3A3C"
        }

        for col in range(5):
            status = colors[col]
            self.tiles[aktualny_rzad][col].configure(fg_color=color_map[status])

        self.current_col = 0

        # Wyświetlanie ekranu wygranej
        if self.game.status == "WIN":
            self.show_win_overlay()
        # Wyświetlanie ekranu przegranej
        if self.game.status == "LOSE":
            self.show_lose_overlay()

    def show_win_overlay(self):
        self.overlay_frame = ctk.CTkFrame(
            self, 
            width=400, 
            height=180, 
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
            font=("Arial", 28, "bold"), 
            text_color="#80C17A"
        )
        title.pack(pady=(30, 10))
        
        desc = ctk.CTkLabel(
            self.overlay_frame, 
            text=f"Udało Ci się odgadnąć hasło \"{self.game.target_word}!\"\nLiczba prób: {self.game.current_row}", 
            font=("Arial", 18),
            text_color="#5AA054"
        )
        desc.pack(pady=(30, 30))

    def show_lose_overlay(self):
        self.overlay_frame = ctk.CTkFrame(
            self, 
            width=400, 
            height=180, 
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
            font=("Arial", 28, "bold"), 
            text_color="#E55B5B"
        )
        title.pack(pady=(30, 10))
        
        desc = ctk.CTkLabel(
            self.overlay_frame, 
            text=f"Hasłem było: \"{self.game.target_word}\"\nSpróbuj ponownie!",
            font=("Arial", 18),
            text_color="#CC4C4C"
        )
        desc.pack(pady=(15, 30))