# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez 
# Brian Rojas

import keyboard

class Connect4:
    player1 = 'X'
    player2 = 'O' #AI
    current_player = player1  # this could be X or O

    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def print_board(self):
        print("\n")
        for row in self.board:
            print(row)
        print("\n")

    def get_current_player(self):
        return self.current_player

    def open_locations(self):
        open_cols = []
        for col in range(6):
            if self.board[0][col] == ' ':
                open_cols.append(col)

        return open_cols  # these are open columns (if top row is open, then apiece can be placed there)

    def make_move(self, column):
        rowToInsertInto = 3
        for i in range(4):
            if self.board[i][column] != ' ':
                rowToInsertInto -= 1
        self.board[rowToInsertInto][column] = self.current_player
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def is_ending_move(self):
        return self.check_if_winning()[0] or len(self.open_locations()) == 0

    def minimax(self, depth, maximizingPlayer):
        open_columns = self.open_locations()

        if self.is_ending_move or depth == 0:
            if self.is_ending_move():
                winning_player = self.check_if_winning()[1]
                print(winning_player)
                if winning_player is "X":
                    return (None,-10000000000000) #X will be player we dont want to win
                elif winning_player is "O":
                    return (None, 10000000000000)

            else: #depth of 0
                return (None, 0)

        if maximizingPlayer:
            pass
        else: #minimizingPlayer
            pass

    #Pseudocode template
    # minimax(node, depth, maximizingPlayer) is
    #     if depth = 0 or node is a terminal node then
    #     return the
    #     heuristic
    #     value
    #     of
    #     node
    #
    #     if maximizingPlayer then
    #     value := −∞
    #     for each child of node do
    #     value := max(value, minimax(child, depth − 1, FALSE))
    #     return value
    #     else (*minimizing player *)
    #     value := +∞
    #     for each child of node do
    #     value := min(value, minimax(child, depth − 1, TRUE))
    #     return value

    def check_if_winning(self):
        winning_player = None

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3] != ' ':
            winning_player = self.board[0][0]
        if self.board[3][0] == self.board[2][1] == self.board[1][2] == self.board[0][3] != ' ':
            winning_player = self.board[3][0]

        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] == row[3] != ' ':
                winning_player = row[0]

        # check columns
        for col in range(4):
            items = [item[col] for item in self.board]
            plays = set(items)
            if len(plays) == 1 and set(items) != {' '}:
                winning_player = list(plays)[0]

        if winning_player:
            print(f"Player {winning_player} wins!")

            return [True, winning_player]
        else:
            return False


if __name__ == '__main__':
    game = Connect4()
    print("Welcome to Connect 4! Now with AI")
    print("-----------------------------------------")
    print("Instructions:")
    print("1. The game is played on a 4x4 grid.")
    print("2. Players take turns to drop their pieces (X or O) into one of the columns (0-3).")
    print("3. The first player to get four of their pieces in a row (vertically, horizontally, or diagonally) wins.")
    print("4. To make a move, enter the column number (0-3) when prompted.")
    print("5. Press 'esc' to exit the game at any time.")
    print("-----------------------------------------")
    while True:

        game.print_board()
        move = int(input(f"Player {game.get_current_player()}, enter your move: "))
        game.make_move(move)
        if keyboard.read_key() == "esc" or game.check_if_winning()[0]:
            break

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
