import customtkinter as ctk

class WordleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("Wordle Unlimited")
        self.geometry("450x700")
        self.resizable(False, False)
        
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(expand=True, pady=(20, 20))
        
        # Triggering the grid rendering
        self.create_game_grid()

    def create_game_grid(self):
        row_count = 6
        column_count = 5
        
        for row_idx in range(row_count):
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

if __name__ == "__main__":
    app = WordleApp()
    app.mainloop()