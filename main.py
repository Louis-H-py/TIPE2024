"""
Toutes les fonctions principles qui permettent de jouer à l'Othello
"""
from copy import deepcopy
import json
import time
import random
from uuid import uuid4

from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from flask import session
from flask import stream_with_context
import numpy as np

from othello import COLOR_BLACK
from othello import Othello
from cpp_engine import CppOthelloEngine
from tensorflow_engine import board_to_input
from tensorflow_engine import legal_moves_array
from tensorflow_engine import TensorflowOthelloEngine

ENGINE_NAME: str = "TF"  # CPP or TF

app = Flask(__name__)
app.secret_key = str(random.random()).replace(".", "")

GAMES: dict = {}  # Toutes les parties de chaque session
ENGINE_COLOR: dict = {}  # La couleur sur le plateau du model qui joue

CPP_ENGINE = CppOthelloEngine(n_thread=1,
                              logs=True,
                              max_depth=7)
TF_ENGINE = TensorflowOthelloEngine(max_depth=13,
                                    device="/cpu:0",
                                    train=False,
                                    max_branch=16,
                                    max_search_time=2.5,
                                    count_evaluation=False)
TF_ENGINE.global_network.load_model("global_net2.h5")

AI_STATS: bool = True


def ai_stats(board: list[list[int]], color: int) -> None:
    p = TF_ENGINE.global_network(board, 1)
    print(f"Probabilité of winning white: {p[1]}")
    p = TF_ENGINE.global_network(board, 2)
    print(f"Probabilité of winning black: {p[1]}")
    p = TF_ENGINE.global_network(board, color)

    print("Policy network prediction:")

    r = p[0]
    mask = legal_moves_array(np.array(board, dtype=np.int32), color).flatten() * r
    sm = np.array(mask / np.sum(mask))

    for y in range(8):
        for x in range(8):

            if sm[y * 8 + x] == 0.0:
                print(f" {'B' if board[y][x] == 2 else ('.' if board[y][x] == 0 else 'W')} ", end="")

            else:
                val = int(sm[y * 8 + x] * 100)
                sup = 3 - len(str(val))
                print(f" {val}{' ' * (sup - 1)}%", end="")

        print("\n")
    print("=================")


def reset_session():
    token: str = str(uuid4())
    session["token"]: str = token
    GAMES[token] = Othello()
    ENGINE_COLOR[token] = COLOR_BLACK


def game_stream():
    if "token" not in session or not session.get("token") in GAMES:
        reset_session()

    token = session["token"]
    session_game: Othello = GAMES[token]
    move_count: int = session_game.game_history.get_move_count - 1  # last player

    while True:

        session_game: Othello = GAMES[token]

        if move_count != session_game.game_history.get_move_count:
            if AI_STATS:
                try:
                    ai_stats(session_game.get_board, session_game.who_plays)
                except Exception as e:
                    print(e)

            move_count = session_game.game_history.get_move_count

            return_json: dict = {"board": session_game.get_board,
                                 "player": session_game.get_player}

            move_board = deepcopy(session_game.get_board)

            for m in session_game.get_possible_moves():
                move_board[m[1]][m[0]] = 5

            return_json["move_board"] = move_board

            score = session_game.get_score

            return_json["score_black"] = score[0]
            return_json["score_white"] = score[1]
            return_json["statu"] = session_game.game_statu

            # create a history
            return_json["history"] = {}
            i = 0
            for move in session_game.game_history:
                return_json["history"][str(i)] = {"move": move[1],
                                                  "board": move[0],
                                                  "score": [int(move[2][0]), int(move[2][1])],
                                                  "player": int(move[3])}
                i += 1

            yield f"data:{json.dumps(return_json)}\n\n"

        # engine move
        if session_game.get_player == ENGINE_COLOR[token]:
            if len(session_game.get_possible_moves()) > 0:
                engine_move(token, ENGINE_COLOR[token], ENGINE_NAME)

        time.sleep(0.01)


def engine_move(token: str, color: int, engine: str) -> None:
    if engine == "CPP":
        session_game: Othello = GAMES[token]

        x, y = CPP_ENGINE(board=deepcopy(session_game.get_board),
                          engine_value=color)

        if session_game.get_player == color:
            session_game.place_piece(x=x, y=y)

    elif engine == "TF":
        session_game: Othello = GAMES[token]

        x, y = TF_ENGINE(board=session_game.get_board,
                         engine_value=color)

        if session_game.get_player == color:
            session_game.place_piece(x=x, y=y)


@app.route("/api/move/", methods=["GET", "POST"])
def api_engine_move() -> str:
    if "token" not in session or not session.get("token") in GAMES:
        token: str = str(uuid4())
        session["token"]: str = token

        reset_session()

    # player move
    session_game: Othello = GAMES[session["token"]]

    if session_game.get_player != ENGINE_COLOR[session["token"]]:
        # get information given by the script
        data: dict = dict(request.get_json())

        x: int = data["x"]
        y: int = data["y"]

        session_game.place_piece(x=x, y=y)

    return ""


@app.route("/api/setting/", methods=["GET", "POST"])
def api_engine_setting() -> str:
    data: dict = dict(request.get_json())
    setting: str = data["setting"]

    token = session["token"]

    if setting == "change_engine_color":
        ENGINE_COLOR[token] = 1 if ENGINE_COLOR[token] == 2 else 2
        GAMES[token] = Othello()

    if setting == "restart":
        GAMES[token] = Othello()

    return ""


@app.route("/api/game-stream/", methods=["GET", "POST"])
def api_game_stream():
    return Response(stream_with_context(game_stream()), mimetype="text/event-stream")


@app.route("/", methods=["GET"])
def main() -> str:
    # generation des tokens pour la session
    if "token" not in session:
        reset_session()

    return render_template("index.html", ENGINE_BLACK=ENGINE_COLOR[session["token"]])


if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=4000,
        debug=True
    )
