#include <iostream>

using bitboard = unsigned long long int;


const int COLOR_WHITE = 1;
const int COLOR_BLACK = 2;

// utils
void array_as_bitboard(int board[8][8], bitboard *white_board, bitboard *black_board) {

    int y;
    int x;

    bitboard wb = *white_board;
    bitboard bb = *black_board;

    bitboard mask = 1;

    for (y = 0; y < 8; y++) {
        for (x = 0; x < 8; x++) {

            if (board[y][x] == COLOR_WHITE) {
                wb += mask << (8 * (7 - y) + (7 - x));
            } else if (board[y][x] == COLOR_BLACK) {
                bb += mask << (8 * (7 - y) + (7 - x));
            }
        }
    }

    *white_board = wb;
    *black_board = bb;
}

// FUNCTION ALREADY WRITTEN
int min(int a, int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

// FUNCTION ALREADY WRITTEN
int is_legal_move(bitboard player_board, bitboard opponent_board, int pos) {

    bitboard mask = 1;

    // check if the case is empty
    if (((player_board | opponent_board) & (mask << (63 - pos)))) {
        return false;
    }

    int n;
    int i;
    int j;
    bool opponent_meet;
    int d;
    bitboard p;

    // check every 8 possible directions
    int list_n[8] = {pos / 8, // ^
                     pos % 8, // <-
                     min(pos / 8, 7 - (pos % 8)), // ^>
                     min(pos / 8, pos % 8), // <^
                     7 - (pos / 8), // V
                     min(7 - (pos / 8), 7 - (pos % 8)), // V>
                     min(7 - (pos / 8), pos % 8),  // <V
                     7 - (pos % 8) // ->
    };

    int list_d[8] = {-8, -1, -7, -9, 8, 9, 7, 1};

    for (j = 0; j < 8; j++) {

        n = list_n[j];
        d = list_d[j];

        opponent_meet = false;

        for (i = 1; i < (n + 1); i++) {

            p = mask << (63 - (pos + (i * d)));

            if (opponent_meet) {
                // If there is an empty case
                if ((player_board & p) == 0) {
                    // If there is no opponent piece
                    if ((opponent_board & p) == 0) {
                        break;
                    }
                } else {
                    // if there is a player piece
                    return j + 1;
                }
            } else {
                // If the first piece upward if an opponent piece
                if ((opponent_board & p) != 0) {
                    opponent_meet = true;
                } else {
                    break;
                }
            }
        }
    }

    return 0;
}

// FUNCTION ALREADY WRITTEN
void place_piece(bitboard *player_board, bitboard *opponent_board, int pos) {

    bitboard o_board = *opponent_board;
    bitboard p_board = *player_board;
    bitboard opponent_edit;
    bitboard player_edit;

    bitboard mask = 1;

    p_board |= mask << (63 - pos); // place piece


    // edit every 8 possible directions

    int n;
    int i;
    int j;
    bool opponent_meet;
    int d;
    bitboard p;

    int list_n[8] = {pos / 8, // ^
                     pos % 8, // <-
                     min(pos / 8, 7 - (pos % 8)), // ^>
                     min(pos / 8, pos % 8), // <^
                     7 - (pos / 8), // V
                     min(7 - (pos / 8), 7 - (pos % 8)), // V>
                     min(7 - (pos / 8), pos % 8),  // <V
                     7 - (pos % 8) // ->
    };

    int list_d[8] = {-8, -1, -7, -9, 8, 9, 7, 1};

    for (j = 0; j < 8; j++) {

        opponent_edit = o_board;
        player_edit = p_board;

        n = list_n[j];
        d = list_d[j];

        opponent_meet = false;

        for (i = 1; i < (n + 1); i++) {

            p = mask << (63 - (pos + (i * d)));

            if (opponent_meet) {
                if ((p_board & p) == 0) {
                    if ((o_board & p) == 0) {
                        break;
                    } else {
                        opponent_edit &= ~p;
                        player_edit |= p;
                    }
                } else {
                    opponent_edit &= ~(mask << (63 - (pos + d)));
                    player_edit |= (mask << (63 - (pos + d)));

                    o_board = opponent_edit;
                    p_board = player_edit;
                    break;
                }
            } else {
                if ((o_board & p) != 0) {
                    opponent_meet = true;
                } else {
                    break;
                }
            }
        }
    }

    *player_board = p_board;
    *opponent_board = o_board;
}


// Function to export
void legal_moves_array(int board[8][8], bool reversed) {
    // load as bitboard
    bitboard wb = 0;
    bitboard bb = 0;

    array_as_bitboard(board, &wb, &bb);

    if (reversed) {
        for (int i = 0; i < 64; i++) {
            if (is_legal_move(bb, wb, i)) {
                board[i / 8][i % 8] = 1;
            } else {
                board[i / 8][i % 8] = 0;
            }
        }
    } else {
        for (int i = 0; i < 64; i++) {
            if (is_legal_move(wb, bb, i)) {
                board[i / 8][i % 8] = 1;
            } else {
                board[i / 8][i % 8] = 0;
            }
        }
    }
}

void place_piece(int board[8][8], int pos, int value) {
    bitboard wb = 0;
    bitboard bb = 0;

    array_as_bitboard(board, &wb, &bb);

    if (value == COLOR_BLACK) {
        place_piece(&bb, &wb, pos);
    } else {
        place_piece(&wb, &bb, pos);
    }

    bitboard mask = 1;

    for (int i = 0; i < 64; i++) {

        if ((wb & (mask << i)) != 0) {
            board[7 - (i / 8)][7 - (i % 8)] = COLOR_WHITE;

        } else if ((bb & (mask << i)) != 0) {
            board[7 - (i / 8)][7 - (i % 8)] = COLOR_BLACK;

        } else {
            board[7 - (i / 8)][7 - (i % 8)] = 0;
        }
    }
}

extern "C" {
void cpp_legal_moves_array(int board[8][8], bool reversed) {
    return legal_moves_array(board, reversed);
}
}

extern "C" {
void cpp_place_piece(int board[8][8], int pos, int value) {
    return place_piece(board, pos, value);
}
}