import numpy as np

ROWS = 6
COLUMNS = 7

class Connect4:
    def __init__(self):
        self.board = np.zeros((ROWS, COLUMNS))
        self.current_player = 1  # Player 1 is represented by 1, Player 2 by 2

    def print_board(self):
        print(np.flip(self.board, 0))

    def is_valid_location(self, col):
        return self.board[ROWS-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROWS):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLUMNS-3):
            for r in range(ROWS):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMNS-3):
            for r in range(ROWS-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMNS-3):
            for r in range(3, ROWS):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
        return False

    def change_turn(self):
        self.current_player = 1 if self.current_player == 2 else 2

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMNS):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def is_terminal_node(self):
        return self.winning_move(1) or self.winning_move(2) or len(self.get_valid_locations()) == 0
