# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez
# Brian Rojas

# This file allows you to run it as a cli application

from lib.game import Connect4
from lib.util import parse_score
import math


if __name__ == '__main__':
    game = Connect4()
    scores = {Connect4.player1: 0, Connect4.player2: 0}

    print("Welcome to Connect 4! Now with AI")
    print("-----------------------------------------")
    print("Instructions:")
    print("1. The game is played on a 6x6 grid.")
    print("2. Players take turns to drop their pieces (X or O) into one of the columns (0-5).")
    print("3. The first player to get four of their pieces in a row (vertically, horizontally, or diagonally) wins.")
    print("4. To make a move, press the corresponding number key (0-5) on your keyboard.")
    print("5. Press CTRL+C to exit the game at any time.")
    print("-----------------------------------------")

    try:
        while True:
            game.print_board()

            player = game.current_player

            # Suggest the next move
            # You can adjust the depth based on performance needs
            suggested_move, score, row_scores = game.minimax(
                True, float("-inf"), float("inf"))

            print([parse_score(i[1]) for i in row_scores], "\n\n")
            print(
                f"Suggested next move for Player {game.get_current_player()}: Column {suggested_move} (score: {score})")

            move_input = input(
                f"Player {game.get_current_player()}, enter your move: ")
            if not move_input.isdigit():
                print(f"Enter a number within 0 to {game.board_size-1}")
                continue
            move = int(move_input)
            if move < 0 or move >= game.board_size:
                print(
                    f"Choose a column that is within 0 to {game.board_size-1}")
                continue

            game.make_move(move)

            if game.check_if_winning()[0]:
                game.print_board()
                print(f"Player {player} wins!")

                if game.get_current_player() == Connect4.player1:
                    scores[Connect4.player2] += 1
                else:
                    scores[Connect4.player1] += 1

                print(
                    f"Score - Player {Connect4.player1}: {scores[Connect4.player1]} | Player {Connect4.player2}: {scores[Connect4.player2]}")

                play_again = input(
                    "Do you want to play again? (yes/no): ").lower()
                if play_again == 'yes':
                    game.reset_game()
                else:
                    break

            if len(game.open_locations()) == 0:
                game.print_board()
                print(f"Tie Game")

                print(
                    f"Score - Player {Connect4.player1}: {scores[Connect4.player1]} | Player {Connect4.player2}: {scores[Connect4.player2]}")

                play_again = input(
                    "Do you want to play again? (yes/no): ").lower()
                if play_again == 'yes':
                    game.reset_game()
                else:
                    break

        print("\n\nThanks for playing!")
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
