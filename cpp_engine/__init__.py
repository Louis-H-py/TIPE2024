from copy import deepcopy
import ctypes
from multiprocessing import Manager
from multiprocessing import Process

import numpy as np
from numpy.ctypeslib import ndpointer

COLOR_WHITE: int = 1
COLOR_BLACK: int = 2


class CppOthelloEngine:
    def __init__(self, max_depth: int, n_thread: int = 1, logs: bool = True) -> None:
        self.n_thread: int = n_thread
        self.logs: bool = logs
        self.max_depth: int = max_depth

    @staticmethod
    def board_to_bitboard(board: list[list[int]]) -> tuple:

        white_board: int = 0
        black_board: int = 0

        for y, line in enumerate(board):
            for x, val in enumerate(line):

                if val == COLOR_WHITE:
                    white_board += (2 ** ((7 - y) * 8 + (7 - x)))

                elif val == COLOR_BLACK:
                    black_board += (2 ** ((7 - y) * 8 + (7 - x)))

        return white_board, black_board

    def thread_search(self, board: np.array, thread_id: int, available: list[int], reward: list[int], engine_white: bool):
        white_board, black_board = self.board_to_bitboard(board)

        stats = ctypes.c_int(0)
        r: int = get_move_reward(ctypes.c_ulonglong(white_board),
                                 ctypes.c_ulonglong(black_board),
                                 ctypes.c_bool(not engine_white),  # Black becomes white
                                 ctypes.c_int32(self.max_depth),
                                 stats)

        reward[thread_id] = r

        # end
        available[0] += 1

    def __call__(self, board: list[list[int]], engine_value: int, **kwargs) -> tuple:

        white_board, black_board = self.board_to_bitboard(board)

        engine_white = True if engine_value == COLOR_WHITE else False

        if self.n_thread == 1:
            stats = ctypes.c_int(0)
            r: int = get_best_move(ctypes.c_ulonglong(white_board),
                                   ctypes.c_ulonglong(black_board),
                                   ctypes.c_bool(engine_white),
                                   ctypes.c_int32(self.max_depth),
                                   stats)

            if self.logs:
                print(f"Move calculated: {stats.value:,}")

            # x, y
            return r % 8, r // 8

        else:

            manager = Manager()
            reward = manager.dict()
            available_thread = manager.list([self.n_thread, ])

            list_process = []

            # Simulate every possible move
            b = np.array(board, dtype=np.int32)

            for i, v in enumerate(legal_moves_array(b, engine_value).flatten()):
                if v == 1:
                    new_board = place_piece(b, i, engine_value)

                    while available_thread[0] <= 0:
                        pass

                    available_thread[0] -= 1

                    list_process.append(
                        Process(target=self.thread_search,
                                args=(new_board, i, available_thread, reward, engine_white,)
                                )
                    )
                    list_process[-1].start()

            for p in list_process:
                p.join()

            # cherche best move
            min_reward = 100
            min_pos = -1

            for pos in reward:
                if reward[pos] < min_reward:
                    min_reward = reward[pos]
                    min_pos = pos

            return min_pos % 8, min_pos // 8


try:
    lib = ctypes.cdll.LoadLibrary(__file__.replace("__init__.py", "OthelloEngine.so"))

    get_best_move = lib.cpp_get_best_move
    get_best_move.restype = ctypes.c_int32
    get_best_move.argtypes = [ctypes.c_ulonglong,  # white board
                              ctypes.c_ulonglong,  # black board
                              ctypes.c_bool,  # white engine
                              ctypes.c_int32,  # max depth
                              ctypes.POINTER(ctypes.c_int32)  # stats
                              ]

    get_move_reward = lib.cpp_get_move_reward
    get_move_reward.restype = ctypes.c_int32
    get_move_reward.argtypes = [ctypes.c_ulonglong,  # white board
                                ctypes.c_ulonglong,  # black board
                                ctypes.c_bool,  # white engine
                                ctypes.c_int32,  # max depth
                                ctypes.POINTER(ctypes.c_int32)  # stats
                                ]
    lib = ctypes.cdll.LoadLibrary(__file__.replace("__init__.py", "accelerator.so"))

    f_place_piece = lib.cpp_place_piece
    f_place_piece.argtypes = [ndpointer(ctypes.c_int32, flags="C_CONTIGUOUS"),  # **board
                              ctypes.c_int32,  # pos
                              ctypes.c_int32,  # value
                              ]

    f_legal_moves_array = lib.cpp_legal_moves_array
    f_legal_moves_array.argtypes = [ndpointer(ctypes.c_int32, flags="C_CONTIGUOUS"),  # **board
                                    ctypes.c_bool,  # reversed
                                    ]

except Exception as e:
    print(e)


def place_piece(board: np.array, pos: int, value: int) -> np.array:
    arr: np.array = deepcopy(board)
    f_place_piece(arr, pos, value)
    return arr


def legal_moves_array(board: np.array, color: int) -> np.array:
    return f_legal_moves_array(deepcopy(board), True if color == COLOR_BLACK else False)
