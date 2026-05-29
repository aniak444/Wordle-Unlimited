import customtkinter as ctk

class WordleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wordle Unlimited")
        self.geometry("450x700")
        self.resizable(False, False)
        

if __name__ == "__main__":
    app = WordleApp()
    app.mainloop()