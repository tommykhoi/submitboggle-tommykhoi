import random
from typing import List, Optional, Tuple, Set
from py_boggle.boggle_game import BoggleGame
from py_boggle.boggle_dictionary import BoggleDictionary

SHORT = 3  # Minimum word length to score
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`"""

    def __init__(self):
        self.board: List[List[str]] = []  # current game board
        self.size: int = 0  # board size
        self.words: List[str] = []  # player's current words
        self.dictionary: BoggleDictionary = None  # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] = None  # position of the last added word

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """Start a new game with the given board size and dictionary"""
        with open(cubefile, 'r') as infile:
            faces = [line.strip().lower() for line in infile]
        cubes = [f for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size * size:
            raise ValueError("ERROR: Invalid Dimensions (size, cubes)")
        random.shuffle(cubes)
        self.board = [[random.choice(cubes[r * size + c]) for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None

    def get_board(self) -> List[List[str]]:
        """Return the current game board"""
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """
        Helper method called by add_word()
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word().
        If `word` is not present on the board, return None.
        """
        word = word.lower()

        def dfs(row: int, col: int, index: int, path: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
            # Check if we have found the whole word
            if index == len(word):
                return path
            # If out of bounds or already visited
            if row < 0 or row >= self.size or col < 0 or col >= self.size or (row, col) in path:
                return None
            # If the letter does not match
            if self.board[row][col] != word[index]:
                return None
            # Valid letter found, proceed to the next letter
            path.append((row, col))
            for dRow, dCol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                result = dfs(row + dRow, col + dCol, index + 1, path)
                if result:
                    return result
            path.pop()  # Backtrack if no valid path
            return None

        # Start searching from every position on the board
        for row in range(self.size):
            for col in range(self.size):
                result = dfs(row, col, 0, [])
                if result:
                    return result
        return None

    def add_word(self, word: str) -> int:
        """Add a word to the game if valid, and return the score"""
        word = word.lower()
        if len(word) > SHORT and word not in self.words and self.dictionary.contains(word):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """Return the positions of the last added word, or None if no word was added"""
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """Set the current game board manually for testing"""
        self.board = [[c.lower() for c in row] for row in board]
        self.size = len(board)

    def get_score(self) -> int:
        """Calculate and return the current game score"""
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """
        Find all words using a dictionary-driven search.
        The dictionary-driven search explores every possible path on the board
        and checks whether the path forms a valid word in the dictionary.
        """
        found_words = set()

        def dfs(row: int, col: int, current_string: str, visited: Set[Tuple[int, int]]):
            # Stop if the current string is not a valid prefix
            if not self.dictionary.is_prefix(current_string):
                return

            # If the current string is a valid word, add it to the found words
            if len(current_string) > SHORT and self.dictionary.contains(current_string):
                found_words.add(current_string)

            # Explore neighbors (up, down, left, right, diagonals)
            for dRow, dCol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = row + dRow, col + dCol
                if 0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) not in visited:
                    dfs(nr, nc, current_string + self.board[nr][nc], visited | {(nr, nc)})

        # Start the DFS from every position on the board
        for row in range(self.size):
            for col in range(self.size):
                dfs(row, col, self.board[row][col], {(row, col)})

        return found_words

    def board_driven_search(self) -> Set[str]:
        """
        Find all words using a board-driven search.
        This approach explores every possible path on the board and checks whether the path forms a valid word.
        """
        found_words = set()

        def dfs(row: int, col: int, current_string: str, visited: Set[Tuple[int, int]]) -> None:
            if len(current_string) > SHORT and self.dictionary.contains(current_string):
                found_words.add(current_string)
            if len(current_string) > self.size * self.size:  # Early exit for long strings
                return
            for dRow, dCol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = row + dRow, col + dCol
                if 0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) not in visited:
                    dfs(nr, nc, current_string + self.board[nr][nc], visited | {(nr, nc)})

        # Start the DFS from every position on the board
        for row in range(self.size):
            for col in range(self.size):
                dfs(row, col, self.board[row][col], {(row, col)})

        return found_words
