from copy import deepcopy

COLOR_WHITE: int = 1
COLOR_BLACK: int = 2

SCORE_WIN_W: int = COLOR_WHITE
SCORE_WIN_B: int = COLOR_BLACK
SCORE_NOT_FINISH: int = 0
SCORE_TIE: int = 3
SCORE_CANT_WHITE: int = 11
SCORE_CANT_BLACK: int = 22


class Othello:
    def __init__(self) -> None:
        # crate the board
        self.board: list[list[int]] = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = COLOR_WHITE
        self.board[4][4] = COLOR_WHITE
        self.board[4][3] = COLOR_BLACK
        self.board[3][4] = COLOR_BLACK

        # set the first player
        self.who_plays: int = COLOR_BLACK

        self.game_history = GameHistory()

        self.game_history.append(self.board, (), (2, 2), -1)

    # All information about the board
    def get_possible_moves(self, player=None) -> list[tuple[int, int]]:
        """
        This function return the coordinate of each possible moves (x, y)
        :return: list of tuple [(x, y), (x', y'), ... , (x'', y'')]
        """
        if player is None:
            p = self.who_plays
        else:
            p = player

        moves: [tuple] = []

        for y in range(8):
            for x in range(8):
                if self.board[y][x] == 0 and self.all_possible_direction(x, y, p):
                    moves.append((x, y))

        return moves

    def all_possible_direction(self, x: int, y: int, player: int) -> bool:
        """
        This function check the 8 possibles rays required to place a piece on the board
        :param x: the position to check in x
        :param y: the position to check in y
        :param player: the value for player pieces
        :return: if player can put a piece at the given x, y position
        """
        possible_move: bool = False

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:

                if dx != 0 or dy != 0:
                    possible_move = possible_move or self.possible_direction(x, y, dx, dy, player)

                if possible_move:
                    return possible_move

        return possible_move

    def possible_direction(self, x: int, y: int, dx: int, dy: int, player: int) -> bool:
        """
        This function check if a move is possible in a specific direction
        :param x: the x starting point of the search
        :param y: the y starting point of the search
        :param dx: the x direction
        :param dy: the y direction
        :param player: the value for player pieces
        :return: Bool: True is it is possible to play, else False
        """
        px: int = x + dx
        py: int = y + dy

        opponent: int = 1 if player == 2 else 2
        opponent_meet: bool = False  # if there were opponent pieces in the ray

        while 0 <= px < 8 and 0 <= py < 8:
            board_value = self.board[py][px]

            # if there is an empty case
            if board_value == 0:
                return False

            # if there is an opponent piece
            elif board_value == opponent:
                opponent_meet = True

            # if there is a player piece
            elif board_value == player:
                if opponent_meet:
                    return True
                else:
                    return False

            px += dx
            py += dy

        return False

    @property
    def get_board(self) -> list[list[int]]:
        return deepcopy(self.board)

    @property
    def get_player(self) -> int:
        return self.who_plays

    # all actions on the board
    def place_piece(self, x: int, y: int) -> None:
        """
        This function places a piece on the board
        :param x: the x pos of the move
        :param y: the y pos of the move
        :return: None
        """
        # check if the move is possible
        if (x, y) in self.get_possible_moves():
            # place the piece
            self.board[y][x] = self.who_plays

            self.game_history.append(self.get_board, (x, y), self.get_score, self.who_plays)

            # update the board
            self.update_board(x, y)

            # switch player
            self.switch_player()

            statu = self.game_statu
            if statu == SCORE_CANT_WHITE:
                self.who_plays = COLOR_BLACK
            elif statu == SCORE_CANT_BLACK:
                self.who_plays = COLOR_WHITE

        else:
            self.switch_player()

    @property
    def game_statu(self) -> int:
        """
        This function check if the game is finished, return PIECE_NONE if the game is not finished,
        or return the value of the piece of the winner
        :return: the type of score
        """
        board_as_list: [int] = [self.board[y][x] for y in range(8) for x in range(8)]

        # if both can't
        if len(self.get_possible_moves(COLOR_BLACK)) == 0 and len(self.get_possible_moves(COLOR_WHITE)) == 0:
            return self.get_winner

        # if black can't play
        elif len(self.get_possible_moves(COLOR_BLACK)) == 0:
            return SCORE_CANT_BLACK

        # if white can't play
        elif len(self.get_possible_moves(COLOR_WHITE)) == 0:
            return SCORE_CANT_WHITE

        if 0 in board_as_list:
            return SCORE_NOT_FINISH

        return self.get_winner

    @property
    def get_winner(self) -> int:
        """
        This function return the winner of the game
        :return: SCORE_WIN_W: white wins, SCORE_WIN_B: black wins, SCORE_TIE: tie
        """
        score_black, score_white = self.get_score

        if score_white > score_black or score_black <= 1:
            return SCORE_WIN_W

        elif score_white < score_black or score_white <= 1:
            return SCORE_WIN_B

        else:
            return SCORE_TIE

    @property
    def get_score(self) -> tuple:
        board_as_list: [int] = [self.board[y][x] for y in range(8) for x in range(8)]
        return board_as_list.count(COLOR_BLACK), board_as_list.count(COLOR_WHITE)

    # all internal functions of the board
    def switch_player(self) -> None:
        self.who_plays = 1 if self.who_plays == 2 else 2

    def update_board(self, x: int, y: int) -> None:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:

                if dx != 0 or dy != 0:
                    self.update_board_direction(x, y, dx, dy, self.who_plays)

    def update_board_direction(self, x: int, y: int, dx: int, dy: int, player: int) -> None:
        px: int = x + dx
        py: int = y + dy

        opponent: int = 1 if player == 2 else 2

        updates: [tuple] = []

        while 0 <= px < 8 and 0 <= py < 8:
            if self.board[py][px] == opponent:
                updates.append((px, py))

            elif self.board[py][px] == player:

                for pos in updates:
                    self.board[pos[1]][pos[0]] = player

                return

            else:
                return

            px += dx
            py += dy


class GameHistory:
    """
    This class creates a game history for othello
    """

    def __init__(self) -> None:

        self.board_history: [[[int]]] = []
        self.move_history: [str] = []
        self.score_history: [tuple] = []
        self.color_history: [int] = []

        # iterator function
        self.inter_n: int = 0
        self.inter_max: int = 0

        self.move_count: int = 0  # number of move in the history

    def __iter__(self):
        self.iter_n = 0
        self.iter_max = len(self.board_history)
        return self

    def __next__(self) -> tuple:
        if self.iter_n < self.iter_max:

            return_value: tuple = (
                self.board_history[self.iter_n],
                self.move_history[self.iter_n],
                self.score_history[self.iter_n],
                self.color_history[self.iter_n]
            )
            self.iter_n += 1

            return return_value
        else:
            raise StopIteration

    def append(self, board: [[int]], move: tuple, score: tuple, color: int):
        # add element in the history
        self.board_history.append(deepcopy(board))
        self.move_history.append(deepcopy(move))
        self.score_history.append(deepcopy(score))
        self.color_history.append(color)

        self.move_count += 1

    @property
    def get_move_count(self) -> int:
        return self.move_count
