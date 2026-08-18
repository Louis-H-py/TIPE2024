from copy import deepcopy
from multiprocessing import Manager
from multiprocessing import Process
import os
import random
from threading import Thread
import time

if __name__ != '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import numpy as np

from othello import Othello
from othello import COLOR_WHITE
from othello import COLOR_BLACK
from othello import SCORE_NOT_FINISH
from othello import SCORE_CANT_WHITE
from othello import SCORE_CANT_BLACK
from tensorflow_engine import board_to_input
from tensorflow_engine import TensorflowOthelloEngine

# Game properties
N_THREAD: int = 9
SAVE_DATA: bool = True

# Model properties
GAME_DEVICE: str = "/cpu:0"
PROB_RANDOM: float = 0.20  # CHANGE
MAX_DEPTH: int = 16  # CHANGE
MAX_BRANCH: int = 6  # CHANGE
TOTAL_GAME_PLAYED: int = 25514  # CHANGE
BASE_ELO: float = 4200  # CHANGE
LOAD_PREVIOUS_MODEL: bool = True  # CHANGE
COUNT_EVALUATION: bool = False
TRAIN_RATE_STOP_EXPLORATION: float = 0.10
MODEL_PATH: str = "C:/Users/Utilisateur/Documents/TIPE/tipe/global_net2.h5"

# Training properties
TRAIN_DEVICE: str = "/gpu:0"
VERBOSE: bool = False
N_EPOCHS: int = 15
N_STEPS: int = 10000
MEM_SIZE: int = 20

# Test properties
TEST_BLOCK_EVOLUTION: bool = True  # Change
TEST_DEVICE: str = "/cpu:0"
TEST_MAX_DEPTH: int = 16  # CHANGE
TEST_MAX_BRANCH: int = 6  # CHANGE
TEST_BASE_ELO: float = BASE_ELO  # CHANGE
TEST_COUNT_EVALUATION: bool = False  # CHANGE
TEST_RATE_STOP_EXPLORATION: float = 0.10

# Dashboard information
GAME_PER_LINE: int = 5
DASHBOARD_DATA: dict = {
    "train_statu": "Not started",
    "train_result": [[0.0, 0.0], [0.0, 0.0]],
    "test_statu": "Not tested",
}
EMPTY_BLOCK: str = " " * 80
NONE_BOARD = [[None for _ in range(8)] for _ in range(8)]


def pos_board(x, y):
    r = np.zeros((8, 8), dtype=np.float32)
    r[y][x] = 1.0
    return r


def new_elo_score(elo_player: float, elo_opponent: float, score) -> float:
    k: int = 20 if elo_player < 2400 else 10
    k = 20
    s: float = score
    ea: float = 1 / (1 + 10 ** ((elo_opponent - elo_player) / 400))

    return elo_player + k * (s - ea)


def dashboard():
    os.system("cls")
    while True:
        time.sleep(0.25)
        all_board = [test_board] + [v["board"] for v in m_thread_data]
        total = N_THREAD

        line_count = 0

        result = DASHBOARD_DATA["train_result"]
        print("------------------------------ [Training Status] ------------------------------")
        print(f"Training status: {DASHBOARD_DATA['train_statu']}{EMPTY_BLOCK}")
        print(f"Test status: {DASHBOARD_DATA['test_statu']}{EMPTY_BLOCK}")
        print(EMPTY_BLOCK, EMPTY_BLOCK)
        print(f"Results:        Loss:    Accuracy:  {EMPTY_BLOCK}")
        print(f"Network  {result[0][0]:.4f}   {result[0][1]:.4f}{EMPTY_BLOCK}")
        print(EMPTY_BLOCK, EMPTY_BLOCK)
        print("------------------------------   [Game Status]   ------------------------------")

        while total >= 0:

            for line in range(8):
                for g in range(GAME_PER_LINE):
                    if total - g < 0:
                        break
                    elif total - g == 0:
                        board = all_board[total - g][line]
                        print(" ".join(["T" if x == color_test else ("M" if x == color_train else ".") for x in board]),
                              end="    ")
                    else:
                        board = all_board[total - g][line]
                        print(" ".join(["B" if x == 2 else ("W" if x == 1 else ".") for x in board]), end="    ")
                print("\n", end="")

                line_count += 1
            print(EMPTY_BLOCK)
            line_count += 1

            total -= GAME_PER_LINE

        print(f"Session game played: {sum([v['game_played'] for v in m_thread_data[:-1]])}{EMPTY_BLOCK}")
        print(f"Total game played: {TOTAL_GAME_PLAYED}{EMPTY_BLOCK}")
        print(f"Elo score: {train_model.elo_score}{EMPTY_BLOCK}")

        print("\033[F" * (line_count + 12))


def game_thread(process_id, thread_data, load_previous_model):
    # create two models
    model = TensorflowOthelloEngine(max_depth=MAX_DEPTH,
                                    device=GAME_DEVICE,
                                    train=True,
                                    rate_stop_exploration=TRAIN_RATE_STOP_EXPLORATION,
                                    prob_random=PROB_RANDOM,
                                    max_branch=MAX_BRANCH,
                                    count_evaluation=COUNT_EVALUATION)

    if load_previous_model:
        print(f"{process_id} Loading models...")
        model.global_network.load_model(MODEL_PATH)

    while thread_data[process_id]["run"]:

        if thread_data[process_id]["new_model"]:
            try:
                model.global_network.load_model(MODEL_PATH)

            except:
                pass

            thread_data[process_id]["new_model"] = False

        game = Othello()

        x_train = []
        y_train = [[], []]

        error = 0

        while game.game_statu in [SCORE_NOT_FINISH, SCORE_CANT_WHITE, SCORE_CANT_BLACK]:
            board = deepcopy(game.get_board)

            thread_data[process_id]["board"] = deepcopy(board)

            x_train.append(board_to_input(board, game.who_plays))

            if game.who_plays == COLOR_BLACK:
                x, y, r = model(board, COLOR_BLACK, return_reward=True)

                y_train.append([r])

                game.place_piece(x, y)
                new_board = game.get_board

            else:
                x, y, r = model(board, COLOR_WHITE, return_reward=True)

                y_train.append([r])

                game.place_piece(x, y)
                new_board = game.get_board

            y_train[0].append(pos_board(x, y))
            y_train[1].append(r)

            # break if there is a problem with the board
            if board == new_board:
                error += 1
                if error > 3:
                    break

        # load every data in the manager list
        thread_data[process_id]["x_train"] += x_train
        thread_data[process_id]["y_train0"] += y_train[0]
        thread_data[process_id]["y_train1"] += y_train[1]

        # Add the 3 possible rotation
        for rot in range(1, 4):
            thread_data[process_id]["x_train"] += [np.rot90(b, k=rot) for b in x_train]
            thread_data[process_id]["y_train0"] += [np.rot90(b, k=rot) for b in y_train[0]]
            thread_data[process_id]["y_train1"] += y_train[1]

        thread_data[process_id]["game_played"] += 1


if __name__ == '__main__':
    manager = Manager()
    m_thread_data = manager.list()

    for i in range(N_THREAD):
        m_thread_data.append(manager.dict({
            "run": True,
            "new_model": False,
            "x_train": [],
            "y_train0": [],
            "y_train1": [],
            "game_played": 0,
            "board": NONE_BOARD
        }))

    for i in range(N_THREAD):
        Process(target=game_thread, args=(i, m_thread_data, LOAD_PREVIOUS_MODEL)).start()

    # stat training model
    train_model = TensorflowOthelloEngine(max_depth=TEST_MAX_DEPTH,
                                          device=TEST_DEVICE,
                                          train=False,
                                          rate_stop_exploration=TEST_RATE_STOP_EXPLORATION,
                                          count_evaluation=TEST_COUNT_EVALUATION,
                                          max_branch=TEST_MAX_BRANCH,
                                          base_elo=BASE_ELO)
    test_model = TensorflowOthelloEngine(max_depth=TEST_MAX_DEPTH,
                                         device=TEST_DEVICE,
                                         train=False,
                                         rate_stop_exploration=TEST_RATE_STOP_EXPLORATION,
                                         count_evaluation=TEST_COUNT_EVALUATION,
                                         max_branch=TEST_MAX_BRANCH,
                                         base_elo=TEST_BASE_ELO)
    color_test = 1
    color_train = 2
    test_board = NONE_BOARD

    if LOAD_PREVIOUS_MODEL:
        print(f"Loading training models...")
        train_model.global_network.load_model(MODEL_PATH)

        print(f"Loading test models...")
        test_model.global_network.load_model(MODEL_PATH)

    # Start dashboard
    Thread(target=dashboard).start()

    # Start the train loop
    for i in range(N_STEPS):
        # os.system("cls")

        while sum([v['game_played'] for v in m_thread_data]) < MEM_SIZE:
            time.sleep(0.25)

        TOTAL_GAME_PLAYED += sum([v["game_played"] for v in m_thread_data])

        # get every data in every manager list
        X_TRAIN = []
        Y_TRAIN = [[], []]

        for data in m_thread_data:
            X_TRAIN += list(data["x_train"])
            Y_TRAIN[0] += list(data["y_train0"])
            Y_TRAIN[1] += list(data["y_train1"])

            data["x_train"], data["y_train1"], data["y_train0"] = [], [], []
            data["game_played"] = 0

        Y_TRAIN[0] = np.array([np.array(b).flatten() for b in Y_TRAIN[0]])

        try:
            DASHBOARD_DATA['train_statu'] = "Training Model..."

            train_model.global_network.train(np.array(X_TRAIN),
                                             [np.array(Y_TRAIN[0]), np.array(Y_TRAIN[1])],
                                             device=TRAIN_DEVICE,
                                             batch_size=1024,
                                             epochs=N_EPOCHS,
                                             verbose=VERBOSE)

            DASHBOARD_DATA['train_statu'] = "Training finished"

            # Evaluate model
            rp = train_model.global_network.network.evaluate(np.array(X_TRAIN),
                                                             [np.array(Y_TRAIN[0]), np.array(Y_TRAIN[1])],
                                                             verbose=False)
            DASHBOARD_DATA['train_result'][0][0] = rp[0]
            DASHBOARD_DATA['train_result'][0][1] = rp[1]

            # save models
            train_model.global_network.save_model(MODEL_PATH)

            # Save data history
            train_history = open("train_history.txt", "a", encoding="utf-8")
            train_history.write(f"{TOTAL_GAME_PLAYED};{rp[0]:.4f};{rp[1]:.4f};")
            train_history.close()
            tran_history_saved = True

            # save dataset
            if SAVE_DATA:
                np.savez(f"dataset/epoch_{TOTAL_GAME_PLAYED}.npz",
                         x_train=np.array(X_TRAIN),
                         y_train0=np.array(Y_TRAIN[0]),
                         y_train1=np.array(Y_TRAIN[1]),
                         allow_pickle=True)

        except Exception as e:
            tran_history_saved = False
            """tran_history_saved = False

            for t in m_thread_data:
                t["run"] = False

            train_statu = f"Train error: {e}"
            raise Exception(f"{e}")"""

            pass

            # Save the model

        # Check if the model has a better score than previous version
        DASHBOARD_DATA['test_statu'] = "Testing..."

        test_game = Othello()
        color_test = random.choice([COLOR_BLACK, COLOR_WHITE])
        color_train = COLOR_BLACK if color_test == COLOR_WHITE else COLOR_WHITE

        while test_game.game_statu in [SCORE_NOT_FINISH, SCORE_CANT_WHITE, SCORE_CANT_BLACK]:
            test_board = deepcopy(test_game.get_board)
            who_plays = test_game.who_plays

            if who_plays == color_test:
                pos_x, pos_y = test_model(test_board, color_test)
                test_game.place_piece(pos_x, pos_y)
            else:
                pos_x, pos_y = train_model(test_board, color_train)
                test_game.place_piece(pos_x, pos_y)

        DASHBOARD_DATA['test_statu'] = "Test finished"

        # Calculate new Elo rating
        float_score = test_game.get_score

        if color_train == COLOR_BLACK:
            float_score = float_score[0] / (float_score[0] + float_score[1])
        else:
            float_score = float_score[1] / (float_score[0] + float_score[1])

        # if the trained model won load the model in every models
        if not TEST_BLOCK_EVOLUTION or float_score > 0.50:
            DASHBOARD_DATA['test_statu'] = "Trained model wins"
            new_network = train_model.global_network.network.get_weights()

            # load the model in every thread
            for data in m_thread_data:
                data["new_model"] = True

            # load in the test model
            test_model.global_network.network.set_weights(new_network)

            # update Elo rating
            elo_test, elo_train = test_model.get_elo, train_model.get_elo
            new_elo_train = round(new_elo_score(elo_train, elo_test, 1), 1)
            train_model.elo_score = new_elo_train

            # update test model Elo rating
            test_model.elo_score = train_model.get_elo

        else:
            DASHBOARD_DATA['test_statu'] = "Trained model loses"

        # Save score information
        if tran_history_saved:
            train_history = open("train_history.txt", "a", encoding="utf-8")
            train_history.write(f"{float_score};{train_model.get_elo}\n")
            train_history.close()
