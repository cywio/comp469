# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez
# Brian Rojas

import keyboard


class Connect4:
    player1 = 'X'
    player2 = 'O'
    current_player = player1  # this could be X or O

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = self.player1

    def print_board(self):
        print("\n")
        for row in self.board:
            print(row)
        print("\n")

    def get_current_player(self):
        return self.current_player

    def make_move(self, column):
        rowToInsertInto = 3
        for i in range(4):
            if self.board[i][column] != ' ':
                rowToInsertInto -= 1
        self.board[rowToInsertInto][column] = self.current_player
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def check_if_winning(self):
        winning_player = None

        # Check diagonals
        for r in range(3):
            for c in range(4):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] != ' ':
                    winning_player = self.board[r][c]
                if self.board[r+3][c] == self.board[r+2][c+1] == self.board[r+1][c+2] == self.board[r][c+3] != ' ':
                    winning_player = self.board[r+3][c]

        # Check rows
        for row in self.board:
            for col in range(4):
                if row[col] == row[col+1] == row[col+2] == row[col+3] != ' ':
                    winning_player = row[col]

        # check columns
        for col in range(7):
            for row in range(3):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != ' ':
                    winning_player = self.board[row][col]

        if winning_player:
            print(f"Player {winning_player} wins!")
            return True
        else:
            return False


def evaluate_window(window, piece):
    score = 0
    opp_piece = 'O' if piece == 'X' else 'X'

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(' ') == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [row[3] for row in board]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for row in board:
        for c in range(7 - 3):
            window = row[c:c + 4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(7):
        col_array = [row[c] for row in board]
        for r in range(6 - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(6 - 3):
        for c in range(7 - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(6 - 3):
        for c in range(7 - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


if __name__ == '__main__':
    game = Connect4()
    # Initialize scores outside the class
    score = {Connect4.player1: 0, Connect4.player2: 0}

    print("Welcome to Connect 4! Now with AI")
    print("-----------------------------------------")
    print("Instructions:")
    print("1. The game is played on a 4x4 grid.")
    print("2. Players take turns to drop their pieces (X or O) into one of the columns (0-3).")
    print("3. The first player to get four of their pieces in a row (vertically, horizontally, or diagonally) wins.")
    print("4. To make a move, press the corresponding number key (0-6) on your keyboard.")
    print("5. Press 'esc' to exit the game at any time.")
    print("-----------------------------------------")

    while True:
        game.print_board()
        print(f"Current turn: Player {game.get_current_player()}")
        move = None
        while move is None:
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name in ['0', '1', '2', '3', '4', '5', '6']:
                    move = int(key.name)
                elif key.name == 'esc':
                    break

        if move is not None:
            game.make_move(move)
            if game.check_if_winning():
                if game.get_current_player() == Connect4.player1:
                    score[Connect4.player2] += 1
                else:
                    score[Connect4.player1] += 1

                game.print_board()
                print(
                    f"Score - Player {Connect4.player1}: {score[Connect4.player1]} | Player {Connect4.player2}: {score[Connect4.player2]}")

                play_again = input(
                    "Do you want to play again? (yes/no): ").lower()
                if play_again == 'yes':
                    game.reset_game()
                else:
                    break
        else:
            break

    print("Thanks for playing!")

    # game.make_move(move)  # X
    # game.print_board()
    # game.make_move(0) # O
    # game.print_board()
    # game.make_move(0) # X
    # game.print_board()
    # game.make_move(3) # O
    # game.print_board()
    # game.make_move(3) # X
    # game.print_board()
    # game.make_move(2) # O
    # game.print_board()
    # game.check_if_winning() # should be false
    # game.make_move(1) # X
    # game.make_move(0) # O
    # game.make_move(1) # X
    # game.make_move(3) # O
    # game.make_move(1) # X
    # game.make_move(3) # O
    # game.make_move(1) # X
    # game.print_board()
    # game.check_if_winning() # should be player X because we have 4 in column 1
