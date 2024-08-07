# COMP469
# Christian Walsh
# Kaylee Groves
# Jorge Torrez
# Brian Rojas

# This file allows you to run it as a lambda function on AWS (Vercel) for the web version

from flask import Flask, request
from lib.game import Connect4
from lib.util import parse_score
import json
import math

app = Flask(__name__)


@app.route('/api/suggest', methods=["POST"])
def assist():
    data = request.get_json(silent=True)

    game = Connect4()
    game.board = data['board']
    game.current_player = data['current_player']

    alpha = None
    beta = None
    if data["alpha_beta_prune"]:
        alpha = float("-inf")
        beta = float("inf")

    suggested_move, score, history = game.minimax(
        True, alpha=alpha, beta=beta, depth=int(data['max_depth']))

    response = json.dumps(
        {
            "top_suggestion": {
                "columns": suggested_move,
                "score": None if not math.isfinite(score) else score,
            },
            "column_scores": {str(j[0]): (parse_score(j[1])) for j in history},
        }).encode('utf-8')

    # lambda will store the game instance so we need to reset on
    # each request
    game.reset_game()

    return app.response_class(
        response=response,
        status=200,
        mimetype='application/json'
    )


@app.route('/api/move', methods=["POST"])
def make_move():
    data = request.get_json(silent=True)

    game = Connect4()
    game.board = data['board']
    game.current_player = data['current_player']

    game.make_move(int(data['column']))

    is_game_won, winner = game.check_if_winning()

    is_game_complete = is_game_won or len(game.open_locations()) == 0

    response = json.dumps(
        {
            "current_board": game.board,
            "open_locations": game.open_locations(),
            "board_state": {
                "is_game_complete": is_game_complete,
                "is_game_won": is_game_won,
                "is_tie": not is_game_won and len(game.open_locations()) == 0,
                "winner": winner,
            },
        }).encode('utf-8')

    # lambda will store the game instance so we need to reset on
    # each request
    game.reset_game()

    return app.response_class(
        response=response,
        status=200,
        mimetype='application/json'
    )
