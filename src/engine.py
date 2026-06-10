from src.database import is_word_valid, get_random_word

class GameEngine:
    def __init__(self, length=5, difficulty="MEDIUM"):
        self.length = length
        self.difficulty = difficulty
        
        self._target_word, self._hint = get_random_word(self.length, self.difficulty)
        
        self.max_rows = 6
        self.current_row = 0
        self.status = "IN_PROGRESS"
        
        self.hint_used = False
        print(f"Wylosowano hasło: {self._target_word}")

    def get_target_word(self) -> str:
        return self._target_word

    def reset_state(self, length=None, difficulty=None):
        if length is not None:
            self.length = length
        if difficulty is not None:
            self.difficulty = difficulty
            
        self._target_word, self._hint = get_random_word(self.length, self.difficulty)
        self.current_row = 0
        self.status = "IN_PROGRESS"
        self.hint_used = False
        print(f"RESET Nowe hasło: {self._target_word}")

    def is_hint_available(self) -> bool:
        return self.current_row >= 3 and not self.hint_used

    def get_hint(self) -> str:
        if self.is_hint_available():
            self.hint_used = True
            return self._hint
        return ""

    def check_word(self, guess: str) -> list:
        guess = guess.upper()

        if not is_word_valid(guess):
            return ["INVALID_WORD"]

        target = self._target_word.upper()
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
