# COMP469
# Christian Walsh

class Connect4:
    player1 = 'X'
    player2 = 'O'
    current_player = player1 # this could be X or O
    
    def __init__(self):
        self.board = [[' ' for _ in range(4)] for _ in range(4)]
    
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
    
if __name__ == '__main__':
    game = Connect4()
    game.make_move(0) # X
    game.print_board()
    game.make_move(0) # O
    game.print_board()
    game.make_move(0) # X
    game.print_board()
    game.make_move(3) # O
    game.print_board()
    game.make_move(3) # X
    game.print_board()
    game.make_move(2) # O
    game.print_board()
    
    
    