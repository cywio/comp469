# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez
# Brian Rojas

import keyboard

board_size = 6

class Connect4:
    player1 = 'X'
    player2 = 'O'
    current_player = player1  # this could be X or O

    def __init__(self):
        if board_size < 4:
            print("Board needs to be at least 4.")
            exit(1)
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = self.player1

    def print_board(self):
        print("\n")
        for row in self.board:
            print(row)
        print("\n")

    def get_current_player(self):
        return self.current_player

    def open_locations(self):
        open_cols = []
        for col in range(board_size):
            if self.board[0][col] == ' ':
                open_cols.append(col)
        return open_cols

    def make_move(self, column):
        for row in reversed(range(board_size)):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                break
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def is_ending_move(self):
        return self.check_if_winning()[0] or len(self.open_locations()) == 0

    def minimax(self, depth, maximizingPlayer):
        open_columns = self.open_locations()
        is_terminal = self.is_ending_move()
        if is_terminal or depth == 0:
            if is_terminal:
                if self.check_if_winning()[1] == self.player1:
                    return (None, float('inf'))  # player1 wins
                elif self.check_if_winning()[1] == self.player2:
                    return (None, float('-inf'))  # player2 wins
                else:
                    return (None, 0)  # Game is a tie
            return (None, 0)  # Depth is zero

        if maximizingPlayer:
            value = float('-inf')
            column = open_columns[0]
            for col in open_columns:
                for row in reversed(range(board_size)):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = self.current_player
                        break
                self.current_player = self.player2
                new_score = self.minimax(depth - 1, False)[1]
                self.board[row][col] = ' '
                self.current_player = self.player1
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
        else:
            value = float('inf')
            column = open_columns[0]
            for col in open_columns:
                for row in reversed(range(board_size)):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = self.current_player
                        break
                self.current_player = self.player1
                new_score = self.minimax(depth - 1, True)[1]
                self.board[row][col] = ' '
                self.current_player = self.player2
                if new_score < value:
                    value = new_score
                    column = col
            return column, value
         
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
        for row_offset in range(board_size-3):
            for col_offset in range(board_size-3):
                items = []
                for col in range(4):
                    # start from bottom left corner and check for 4 in a diagonal pattern, then shift to the right
                    # until it's board size - 4, example: 6 - (6 - 4) = check until 4th offset, then repeat for the
                    # columns so you offset it upwards from the bottom of the board upward
                    items.append(self.board[board_size-1-(row_offset+col)][col+col_offset])
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        # Check rows
        for row in range(board_size):
            for offset in range(board_size-3):
                items = self.board[row][offset:offset+4]
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        # Check columns
        for col in range(board_size):
            col_items = [item[col] for item in self.board]
            for offset in range(board_size-3):
                items = col_items[offset:offset+4]
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        if winning_player:
            print(f"Player {winning_player} wins!")
            return [True, winning_player]
        else:
            return [False, None]


if __name__ == '__main__':
    game = Connect4()
    score = {Connect4.player1: 0, Connect4.player2: 0}

    print("Welcome to Connect 4! Now with AI")
    print("-----------------------------------------")
    print("Instructions:")
    print("1. The game is played on a 6x7 grid.")
    print("2. Players take turns to drop their pieces (X or O) into one of the columns (0-6).")
    print("3. The first player to get four of their pieces in a row (vertically, horizontally, or diagonally) wins.")
    print("4. To make a move, press the corresponding number key (0-6) on your keyboard.")
    print("5. Press 'esc' to exit the game at any time.")
    print("-----------------------------------------")

    while True:
        game.print_board()
     
        if keyboard.read_key() == "esc":
            break

        move = int(input(f"Player {game.get_current_player()}, enter your move: "))
        if(move >= board_size):
            print(f"Choose a row that is within 0 to {board_size-1}")
            continue

        game.make_move(move)

        # Suggest the next move
        suggested_move, _ = game.minimax(3, game.current_player == game.player1)  # You can adjust the depth based on performance needs
        print(f"Suggested next move for Player {game.get_current_player()}: Column {suggested_move}")

        if game.check_if_winning()[0]:
            game.print_board()
            if game.get_current_player() == Connect4.player1:
                score[Connect4.player2] += 1
            else:
                score[Connect4.player1] += 1

            print(f"Score - Player {Connect4.player1}: {score[Connect4.player1]} | Player {Connect4.player2}: {score[Connect4.player2]}")

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again == 'yes':
                game.reset_game()
            else:
                break

    print("Thanks for playing!")
