import time
from copy import deepcopy
import ctypes
import random

from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Lambda
from keras.layers import Input
from keras.layers import LeakyReLU
from keras.layers import Reshape
from keras.models import Model
from keras.models import load_model
from keras.utils.vis_utils import plot_model
import numpy as np
from numpy.ctypeslib import ndpointer
import tensorflow as tf

COLOR_WHITE: int = 1
COLOR_BLACK: int = 2

GPU_USAGE: bool = False

if len(tf.config.list_physical_devices('GPU')) == 0 or not GPU_USAGE:
    DEVICE: str = "/cpu:0"
else:
    DEVICE: str = "/gpu:0"

print(f"Using {DEVICE}")


def board_to_input(board: list[list[int]], color: int) -> np.array:
    return np.array([[1.0 if x == color else (0.5 if x == 0 else 0.0) for x in y] for y in board])


def noise(arr: np.array, alpha: float) -> np.array:
    return np.random.uniform(-alpha, alpha, arr.shape) + arr


def count_eval(board: np.array, color: int = COLOR_BLACK) -> float:
    t = np.count_nonzero(board != 0)
    p = np.count_nonzero(board == color)
    return p / t if t < 64 else (0 if p < 32 else 1)


class GlobalNetwork:
    def __init__(self,
                 device: str = DEVICE,
                 train: bool = False,
                 prob_random: float = 0.5,
                 count_evaluation: bool = False,
                 noise_alpha: float = 0.03):
        super().__init__()

        inputs = Input(shape=(8, 8, 1))

        x = Lambda(lambda val: val)(inputs)

        for i in range(7):
            x = self.residual_block(x)

        policy_out = self.policy_head(x)
        value_out = self.value_head(x)

        self.network = Model(inputs=inputs, outputs=[policy_out, value_out])

        # self.network.summary()

        self.network.compile(loss='mse', optimizer='adam', metrics=["accuracy", "mse"], run_eagerly=True)

        self.device: str = device
        self.train_mode: bool = train
        self.prob_random: float = prob_random
        self.noise_alpha: float = noise_alpha
        self.count_evaluation: bool = count_evaluation

    @staticmethod
    def residual_block(x):
        original = x
        x = Conv2D(filters=64,
                   kernel_size=(3, 3),
                   padding="same")(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Conv2D(filters=64,
                   kernel_size=(3, 3),
                   padding="same")(x)
        x = BatchNormalization()(x)

        x += original

        return LeakyReLU()(x)

    @staticmethod
    def policy_head(x):
        x = Conv2D(filters=2,
                   kernel_size=(1, 1),
                   padding="same")(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Dense(1)(x)

        x = Reshape((64,))(x)
        x = Activation("sigmoid")(x)

        return x

    @staticmethod
    def value_head(x):
        x = Conv2D(filters=1,
                   kernel_size=(1, 1),
                   padding="same")(x)
        x = BatchNormalization()(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(1)(x)
        x = Activation("sigmoid")(x)

        return x

    def __call__(self, board: np.array, color: int, *args, **kwargs) -> np.array:
        if not self.train_mode:

            b = noise(board_to_input(board, COLOR_BLACK), self.noise_alpha)

            with tf.device(self.device):
                policy, value = self.network(np.array([b]), *args, training=False, **kwargs)
                policy = policy[0].numpy()
                value = float(value[0][0])

            return policy, count_eval(board=board, color=color) if self.count_evaluation else value

        else:
            if random.random() < self.prob_random:
                return np.random.random((64,)), count_eval(board=board,
                                                           color=color) if self.count_evaluation else random.random()
            else:
                b = noise(board_to_input(board, COLOR_BLACK), self.noise_alpha)

                with tf.device(self.device):
                    policy, value = self.network(np.array([b]), *args, training=False, **kwargs)
                    policy = policy[0].numpy()
                    value = float(value[0][0])

                return policy, count_eval(board=board, color=color) if self.count_evaluation else value

    def save_model(self, path: str) -> None:
        self.network.save(path)

    def load_model(self, path: str) -> None:
        new = GlobalNetwork()
        new.network = load_model(path)
        self.network.set_weights(new.network.get_weights())

    def train(self, x, y, *args, device: str = DEVICE, **kwargs) -> None:
        with tf.device(device):
            self.network.fit(x, y, *args, **kwargs)


class TensorflowOthelloEngine:
    def __init__(self,
                 max_depth: int,
                 device: str = DEVICE,
                 train: bool = False,
                 rate_stop_exploration: float = 0.30,
                 prob_random: float = 0.5,
                 max_branch: int = 64,
                 max_search_time: float = 100.0,
                 count_evaluation: bool = False,
                 base_elo: float = 1000,
                 noise_alpha: float = 0.03):
        self.global_network: GlobalNetwork = GlobalNetwork(device=device,
                                                           train=train,
                                                           prob_random=prob_random,
                                                           noise_alpha=noise_alpha,
                                                           count_evaluation=count_evaluation)

        self.max_depth: int = max_depth
        self.max_branch: int = max_branch
        self.max_search_time: float = max_search_time
        self.count_evaluation: bool = count_evaluation
        self.rate_stop_exploration: float = rate_stop_exploration

        self.elo_score: float = base_elo

    @property
    def get_elo(self) -> float:
        return self.elo_score

    def evaluation(self, board) -> tuple[float, float]:
        _, value = self.global_network(board, COLOR_BLACK)
        return value, count_eval(board, COLOR_BLACK)

    def explore_node(self, board: np.array, depth: int) -> tuple[float, float]:
        if depth == self.max_depth:
            return self.evaluation(board)

        # opponent is playing
        if depth % 2 == 1:
            policy, value = self.global_network(board, COLOR_WHITE)

            if (1 - value) < self.rate_stop_exploration:
                return (1 - value), count_eval(board, COLOR_BLACK)
            else:
                mask = legal_moves_array(board, COLOR_WHITE).flatten()
                explore = mask * policy
                best_indices: int = int(np.argmax(explore))

                if explore[best_indices] == 0.0:
                    return self.evaluation(board)

                else:
                    new_board = place_piece(board, best_indices, COLOR_WHITE)
                    return self.explore_node(new_board, depth + 1)

        # engine is playing
        else:
            policy, value = self.global_network(board, COLOR_BLACK)

            if value < self.rate_stop_exploration:
                return value, count_eval(board, COLOR_BLACK)
            else:
                mask = legal_moves_array(board, COLOR_BLACK).flatten()
                explore = mask * policy
                best_indices: int = int(np.argmax(explore))

                if explore[best_indices] == 0.0:
                    return self.evaluation(board)

                else:
                    new_board = place_piece(board, best_indices, COLOR_BLACK)
                    return self.explore_node(new_board, depth + 1)

    def __call__(self,
                 board: list[list[int]],
                 engine_value: int,
                 *args,
                 return_reward: bool = False,
                 **kwargs) -> tuple[int, int] | tuple[int, int, float]:
        array_board = np.array(
            [[COLOR_BLACK if x == engine_value else (0 if x == 0 else COLOR_WHITE) for x in y] for y in board],
            dtype=np.int32)

        mask = legal_moves_array(array_board, COLOR_BLACK).flatten()
        policy, value = self.global_network(array_board, COLOR_BLACK)
        policy = policy * mask

        best_move = tf.argsort(mask.flatten(), direction='DESCENDING').numpy()[0]
        best_indices = tf.argsort(policy, direction='DESCENDING')
        max_return, max_c = 0.0, 0.0

        i: int = 0
        t0: float = time.time()

        while (i < self.max_branch) and (policy[best_indices[i]] > 0.0) and (time.time() - t0 < self.max_search_time):

            new_board = place_piece(array_board, best_indices[i], COLOR_BLACK)

            r, c = self.explore_node(new_board, 1)

            if r > max_return:
                best_move = best_indices.numpy()[i]
                max_return = r

            max_c = max(c, max_c)
            i += 1

        if return_reward:
            return int(best_move % 8), int(best_move // 8), max_c
        else:
            return int(best_move % 8), int(best_move // 8)


try:
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
    raise e


def place_piece(board: np.array, pos: int, value: int) -> np.array:
    arr: np.array = deepcopy(board)

    f_place_piece(arr, pos, value)

    return arr


def legal_moves_array(board: np.array, color: int) -> np.array:
    arr: np.array = deepcopy(board)

    if color == COLOR_BLACK:
        f_legal_moves_array(arr, True)
    else:
        f_legal_moves_array(arr, False)

    return arr


if __name__ == '__main__':
    a = GlobalNetwork()
    # Pour obtenir certaines images de diapositives
    plot_model(a.network, to_file='model_plot_global.jpg', show_shapes=True, show_layer_names=True)
