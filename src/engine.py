class GameEngine:
    def __init__(self):
        self.target_word = "KODER"
        self.max_rows = 6
        self.current_row = 0
        self.status = "IN_PROGRESS"

    def check_word(self, guess: str) -> list:
        guess = guess.upper()
        target = self.target_word.upper()
        
        result = ["GRAY"] * 5
        target_letters = list(target)

        for i in range(5):
            if guess[i] == target[i]:
                result[i] = "GREEN"
                target_letters[i] = None

        for i in range(5):
            if result[i] == "GREEN":
                continue
                
            if guess[i] in target_letters:
                result[i] = "YELLOW"
                index_to_remove = target_letters.index(guess[i])
                target_letters[index_to_remove] = None

        self.current_row += 1
        
        if result == ["GREEN", "GREEN", "GREEN", "GREEN", "GREEN"]:
            self.status = "WIN"
            
        elif self.current_row >= self.max_rows:
            self.status = "LOSE"

        return result