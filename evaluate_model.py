import random
from copy import deepcopy
import os

if __name__ != '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import numpy as np

from cpp_engine import CppOthelloEngine
from othello import Othello
from othello import COLOR_WHITE
from othello import COLOR_BLACK
from othello import SCORE_NOT_FINISH
from othello import SCORE_CANT_WHITE
from othello import SCORE_CANT_BLACK
from tensorflow_engine import board_to_input
from tensorflow_engine import legal_moves_array
from tensorflow_engine import TensorflowOthelloEngine

MAX_DEPTH: int = 16

GAME_DEVICE: str = "/cpu:0"
LOAD_PREVIOUS_MODEL: bool = True
VERBOSE: bool = False

CPP: bool = True
NAME: str = "CPPEngine" if CPP else "TensorflowEngine 2"


def print_board(b: list[list[int]]):
    for line in b:
        for case in line:
            print(". " if case == 0 else ("W " if case == COLOR_WHITE else "B "), end="")
        print("\n", end="")
    print()


def softmax(b: np.array):
    total = np.sum(b)
    return b / total


def print_prob(b: list[list[int]], color: int) -> None:

    p = model1.global_network(b, 1)
    print(f"Probabilité of winning white: {p[1]}")
    p = model1.global_network(b, 2)
    print(f"Probabilité of winning black: {p[1]}")
    p = model1.global_network(b, color)
    print("Policy network prediction:")

    r = p[0]
    mask = legal_moves_array(np.array(b, dtype=np.int32), color).flatten() * r
    sm = np.array(mask / np.sum(mask))

    for y in range(8):
        for x in range(8):

            if sm[y * 8 + x] == 0.0:
                print(f" {'B' if b[y][x] == 2 else ('.' if b[y][x] == 0 else 'W')} ", end="")

            else:
                val = int(sm[y * 8 + x] * 100)
                sup = 3 - len(str(val))
                print(f" {val}{' ' * (sup - 1)}%", end="")

        print("\n")
    print("==================================")


if __name__ == '__main__':
    model1 = TensorflowOthelloEngine(max_depth=MAX_DEPTH,
                                     device=GAME_DEVICE,
                                     count_evaluation=False )
    model1.global_network.load_model("global_net2.h5")

    if CPP:
        model2 = CppOthelloEngine(7, logs=False)
    else:
        model2 = TensorflowOthelloEngine(max_depth=MAX_DEPTH,
                                         device=GAME_DEVICE,
                                         count_evaluation=False,
                                         rate_stop_exploration=0.30)
        model2.global_network.load_model("global_net.h5")

    game = Othello()
    model1_color = random.choice([COLOR_BLACK, COLOR_WHITE])
    model2_color = COLOR_BLACK if model1_color == COLOR_WHITE else COLOR_WHITE

    print(f"TensorflowEngine: {'W' if model1_color == COLOR_WHITE else 'B'}")
    print(f"{NAME}: {'B' if model2_color == COLOR_BLACK else 'W'}")

    while game.game_statu in [SCORE_NOT_FINISH, SCORE_CANT_WHITE, SCORE_CANT_BLACK]:
        print("==================================")
        board = deepcopy(game.get_board)
        who_plays = game.who_plays

        print_board(board)
        s = game.get_score
        if model1_color == COLOR_WHITE:
            print(f"TensorflowEngine (W): {s[1]}   |   {NAME} (B): {s[0]}")
        else:
            print(f"TensorflowEngine (B): {s[0]}   |   {NAME} (W): {s[1]}")

        print_prob(board, who_plays)

        print(f"{'TensorflowEngine' if model1_color == who_plays else NAME} is playing...")

        if who_plays == model1_color:
            x, y = model1(board, model1_color)
            game.place_piece(x, y)

        else:
            x, y = model2(board, model2_color)
            game.place_piece(x, y)

    print("Final board:")
    print_board(game.get_board)

    print("Final score:")
    s = game.get_score
    if model1_color == COLOR_WHITE:
        print(f"TensorflowEngine (W): {s[1]}")
        print(f"{NAME} (B):        {s[0]}")
    else:
        print(f"TensorflowEngine (B): {s[0]}")
        print(f"{NAME} (W):        {s[1]}")
