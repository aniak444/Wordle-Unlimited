from src.database import is_word_valid

class GameEngine:
    def __init__(self):
        self.target_word = "KODER"
        self.max_rows = 6
        self.current_row = 0
        self.status = "IN_PROGRESS"

    def set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    def check_word(self, guess: str) -> list:
        guess = guess.upper()

        if not is_word_valid(guess):
            return ["INVALID_WORD"]

        target = self.target_word.upper()
        word_length = len(target)
        
        result = ["GRAY"] * word_length
        target_letters = list(target)

        for i in range(word_length):
            if guess[i] == target[i]:
                result[i] = "GREEN"
                target_letters[i] = None

        for i in range(word_length):
            if result[i] == "GREEN":
                continue
                
            if guess[i] in target_letters:
                result[i] = "YELLOW"
                index_to_remove = target_letters.index(guess[i])
                target_letters[index_to_remove] = None

        self.current_row += 1
        
        if result == ["GREEN"] * word_length:
            self.status = "WIN"
            
        elif self.current_row >= self.max_rows:
            self.status = "LOSE"

        return result

    def losuj_nowe_slowo(self, word_length: int):
        slowa_testowe = {
            4: "KOTY",
            5: "KODER",
            6: "PYTHON"
        }
        
        self.target_word = slowa_testowe.get(word_length, "KODER").upper()
        
        print(f"[DEBUG ENGINE] Wylosowano hasło testowe: '{self.target_word}' (długość: {word_length})")
        
        # Resetujemy stan rundy
        self.current_row = 0
        self.status = "IN_PROGRESS"