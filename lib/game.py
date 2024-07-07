# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez
# Brian Rojas

board_size = 6
max_look_ahead = 4


class Connect4:
    player1 = 'X'
    player2 = 'O'
    current_player = player1  # this could be X or O
    board_size = board_size
    max_look_ahead = max_look_ahead

    def __init__(self):
        if board_size < 4:
            print("Board needs to be at least 4.")
            exit(1)
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(board_size)]
                      for _ in range(board_size)]
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
            if self.board[0][col] == ' ':  # if the top row is empty, then it's still open
                open_cols.append(col)
        return open_cols

    def make_move(self, column):
        for row in reversed(range(board_size)):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                break
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def score_move(self, move, player):
        # will change these scores/add more rules soon
        score = 0
        other_player = self.player1 if player == self.player2 else self.player2

        empty_count = move.count(' ')
        player_count = move.count(player)
        other_player_count = move.count(other_player)

        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 5
        elif player_count == 2 and empty_count == 2:
            score += 2
        if other_player_count == 3 and empty_count == 1:
            score -= 4
        return score

    # https://en.wikipedia.org/wiki/Minimax#Pseudocode
    def minimax(self, maximizingPlayer, depth=max_look_ahead):
        # get columns where i can make a move
        open_columns = self.open_locations()
        is_leaf_node = self.check_if_winning()[0] or len(open_columns) == 0
        if is_leaf_node or depth == 0:
            if is_leaf_node:
                # if either player wins at this stage, then return highest possible
                # score to indicate it's over, no need to run the rest of the code
                winning_player = self.check_if_winning()[1]
                if winning_player == self.player1:
                    return None, float('inf'), None  # player1 wins
                elif winning_player == self.player2:
                    return None, float('-inf'), None  # player2 wins
                else:
                    return None, 0, None  # Game is a tie
            # If we've reached the max depth, just assign the heuristic value to each possible move
            score = 0

            # rows
            for row in range(board_size):
                for offset in range(board_size - 3):
                    # rows
                    score += self.score_move(self.board[row]
                                             [offset:offset + 4], self.current_player)
                    # columns
                    score += self.score_move([item[offset]
                                              for item in self.board[row:row + 4]], self.current_player)

            # diagonals
            for row in range(board_size-3):
                for col in range(board_size-3):
                    # backwards
                    score += self.score_move([self.board[row + i][col + i]
                                              for i in range(4)], self.current_player)
                    # forward
                    score += self.score_move([self.board[row + 3 - i][col + i]
                                              for i in range(4)], self.current_player)

            return None, score, None

        # maximize or minimize the score for the current player
        value = float('-inf' if maximizingPlayer else 'inf')
        column = open_columns[0]
        history = []
        for col in open_columns:
            # borrow board from the current state and seek ahead
            for row in reversed(range(board_size)):
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.current_player
                    break
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            # recursively check and decrease depth to limit recursion
            _, new_score, _ = self.minimax(not maximizingPlayer, depth - 1)
            # reset the board to the original state
            self.board[row][col] = ' '
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            # if we get a better high score than previous best, then set new column
            # to be the best next move
            if maximizingPlayer:
                # maximize score
                if new_score > value:
                    value = max(value, new_score)
                    column = col
            else:
                # minimize score
                if new_score < value:
                    value = min(value, new_score)
                    column = col
            # keep track of columns as to not just return the best move
            history.append([col, new_score])
        return column, value, history

    def check_if_winning(self):
        winning_player = None

        # Check diagonals
        for row_offset in range(board_size - 3):
            for col_offset in range(board_size - 3):
                items = []
                for col in range(4):
                    # start from bottom left corner and check for 4 in a diagonal pattern, then shift to the right
                    # until it's board size - 4, example: 6 - (6 - 4) = check until 4th offset, then repeat for the
                    # columns so you offset it upwards from the bottom of the board upward
                    items.append(
                        self.board[board_size - 1 - (row_offset + col)][col + col_offset])
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        for row_offset in reversed(range(3, board_size)):
            for col_offset in reversed(range(3, board_size)):
                items = []
                for col in range(4):
                    items.append(
                        self.board[row_offset - col][col_offset - col])
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        # Check rows
        for row in range(board_size):
            for offset in range(board_size - 3):
                items = self.board[row][offset:offset + 4]
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        # Check columns
        for col in range(board_size):
            col_items = [item[col] for item in self.board]
            for offset in range(board_size - 3):
                items = col_items[offset:offset + 4]
                plays = set(items)
                if len(plays) == 1 and set(items) != {' '}:
                    winning_player = list(plays)[0]

        if winning_player:
            return [True, winning_player]
        else:
            return [False, None]
