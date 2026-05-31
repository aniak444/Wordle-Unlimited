import customtkinter as ctk

class WordleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("Wordle Unlimited")
        self.geometry("450x700")
        self.resizable(False, False)
        
        self.header_label = ctk.CTkLabel(
            self,
            text="WORDLE",
            font=("Arial", 36, "bold"),
            text_color="#45FF79"
        )
        self.header_label.pack(pady=(25, 0))
        
        self.subheader_label = ctk.CTkLabel(
            self,
            text="UNLIMITED",
            font=("Arial", 24),
            text_color="#2DBA55"
        )
        self.subheader_label.pack(pady=(0, 0))
        
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(expand=True, pady=(20, 20))
        
        self.tiles = []
        
        self.current_row = 0
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
        char = event.char
        if char.isalpha() and len(char) == 1:
            char_upper = char.upper()
            
            if self.current_col < 5:
                self.tiles[self.current_row][self.current_col].configure(text=char_upper)
                self.current_col += 1

    def color_row(self, row_idx, statuses):
        # Słownik z oryginalnymi kolorami Wordle (2: zielony, 1: żółty, 0: szary)
        color_map = {
            2: "#538d4e",
            1: "#b59f3b",
            0: "#3a3a3c"
        }
        
        for col_idx, status in enumerate(statuses):
            if col_idx < 5:
                kolor = color_map.get(status, "#3a3a3c")
                self.tiles[row_idx][col_idx].configure(fg_color=kolor)

if __name__ == "__main__":
    app = WordleApp()
    app.mainloop()