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
    
    def check_if_winning(self):
        winning_player = None
        
        # check diagnals
        # @todo
        
        # check rows
        #@todo
        
        # check columns
        for col in range(4):
            items = [item[col] for item in self.board]
            plays = set(items)
            if len(plays) == 1 and set(items) != {' '}:
                winning_player = list(plays)[0]
                
        if winning_player:
            print(f"Player {winning_player} wins!")
            
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
    game.check_if_winning() # should be false
    game.make_move(1) # X
    game.make_move(0) # O
    game.make_move(1) # X
    game.make_move(3) # O
    game.make_move(1) # X
    game.make_move(3) # O
    game.make_move(1) # X
    game.print_board()
    game.check_if_winning() # should be player X because we have 4 in column 1
    
    
    
    