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
        # if the top row is empty, then it's still open
        return list(filter(lambda x: self.board[0][x] == ' ', range(board_size)))

    def make_move(self, column):
        for row in reversed(range(board_size)):
            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                break
        self.current_player = self.get_opponent(self.current_player)

    def score_move(self, move, player):
        # will change these scores/add more rules soon
        score = 0
        other_player = self.player1 if player == self.player2 else self.player2

        empty_count = move.count(' ')
        player_count = move.count(player)
        other_player_count = move.count(other_player)

        '''
            • 0 - column is full or other player wins on the next move
            • 100 - next move is winning move
            • 50 - otherwise
        '''

        # winning/neutral moves
        if player_count == 4:
            score += 100
        elif other_player == 4:
            score -= 100
        elif empty_count == 4:
            score += 50

        # with empties in row organized by strength
        # 3 curr, 1 empty
        elif player_count == 3 and empty_count == 1:
            score += 52
        # 2 curr, 2 empty
        elif player_count == 2 and empty_count == 2:
            score += 51
        # 1 curr, 3 empty
        elif player_count == 1 and empty_count == 3:
            score += 50

        # 3 enemy, 1 empty
        elif other_player_count == 3 and empty_count == 1:
            score -= 50
        # 2 enemy, 2 empty
        elif other_player_count == 2 and empty_count == 2:
            score -= 49
        # 1 enemy, 3 empty
        elif other_player_count == 1 and empty_count == 3:
            score -= 48

        # with enemy in row organized by strength — these are worse than empty
        # 3 curr, 1 enemy
        elif player_count == 3 and other_player_count == 1:
            score -= 51
        # 2 curr, 2 enemy
        elif player_count == 2 and other_player_count == 2:
            score -= 52
        # 3 enemy, 1 curr
        elif player_count == 1 and other_player_count == 3:
            score -= 53

        return score // 50

    def get_opponent(self, player):
        return self.player1 if player == self.player2 else self.player2

    # https://en.wikipedia.org/wiki/Minimax#Pseudocode
    # https://canvas.csun.edu/courses/157708/files/24943298 pg 25 - 27
    def minimax(self, maximizingPlayer, alpha=None, beta=None, depth=max_look_ahead):
        # get columns where i can make a move
        open_columns = self.open_locations()
        is_game_won, winning_player = self.check_if_winning()
        is_leaf_node = is_game_won or len(open_columns) == 0
        if is_leaf_node:
            # if either player wins at this stage, then return highest possible
            # score to indicate it's over, no need to run the rest of the code
            if winning_player == self.current_player:
                return [], float('inf'), []  # current wins
            elif winning_player == self.get_opponent(self.current_player):
                return [], float('-inf'), []  # opponent wins
            else:
                return [], 0, []  # Game is a tie
        # If we've reached the max depth, just assign the heuristic value to each possible move
        if depth == 0:
            score = 0

            # rows
            for row in range(board_size):
                for offset in range(board_size - 3):
                    # rows
                    base_score = self.score_move(self.board[row]
                                                 [offset:offset + 4], self.current_player)
                    # give bonus points to the rows towards the bottom since those have a higher change of winning
                    lower_row_bonus = board_size - row
                    score += base_score + lower_row_bonus
                    # columns
                    score += self.score_move([item[row]
                                              for item in self.board[offset:offset + 4]], self.current_player)

            # diagonals
            for row in range(board_size-3):
                for col in range(board_size-3):
                    # backwards
                    score += self.score_move([self.board[row + i][col + i]
                                              for i in range(4)], self.current_player)
                    # forward
                    score += self.score_move([self.board[row + 3 - i][col + i]
                                              for i in range(4)], self.current_player)

            return [], score, []

        # maximize or minimize the score for the current player
        value = float('-inf' if maximizingPlayer else 'inf')
        columns_and_scores = []
        for col in open_columns:
            # borrow board from the current state and seek ahead
            for row in reversed(range(board_size)):
                if self.board[row][col] == ' ':
                    # if we are maximizing then we want to maximize the current player, otherwise if we are
                    # minimizing, then we want to minimize the other player
                    self.board[row][col] = self.current_player if maximizingPlayer else self.get_opponent(
                        self.current_player)
                    break
            # recursively check and decrease depth to limit recursion
            _, new_score, _ = self.minimax(
                not maximizingPlayer, alpha, beta, depth - 1)
            # reset the board to the original state
            self.board[row][col] = ' '
            # keep track of columns as to not just return the best move
            columns_and_scores.append([col, new_score])
            # if we get a better high score than previous best, then set new column
            # to be the best next move, use alpha beta pruning to reduce the search space
            if maximizingPlayer:
                # maximize score
                value = max(value, new_score)
                if alpha:
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break  # beta prune
            else:
                # minimize score
                value = min(value, new_score)
                if beta:
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # alpha prune
        top_columns = list(map(lambda x: x[0], filter(
            lambda x: x[1] == value, columns_and_scores)))
        return top_columns, value, columns_and_scores

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
