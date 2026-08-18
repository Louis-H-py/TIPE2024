#include <iostream>

#define HASHTABLE_CAPACITY 10000000

using bitboard = unsigned long long int;

/* In the tree search, engine is always represented by the black board ,and the opponent by the white board */

const int not_found_table = -100;

const bitboard POWER_2[64] = {
        9223372036854775808,4611686018427387904,2305843009213693952,1152921504606846976,576460752303423488,288230376151711744,144115188075855872,72057594037927936,36028797018963968,18014398509481984,9007199254740992,4503599627370496,2251799813685248,1125899906842624,562949953421312,281474976710656,140737488355328,70368744177664,35184372088832,17592186044416,8796093022208,4398046511104,2199023255552,1099511627776,549755813888,274877906944,137438953472,68719476736,34359738368,17179869184,8589934592,4294967296,2147483648,1073741824,536870912,268435456,134217728,67108864,33554432,16777216,8388608,4194304,2097152,1048576,524288,262144,131072,65536,32768,16384,8192,4096,2048,1024,512,256,128,64,32,16,8,4,2,1,
};

/* Utils functions */

int min(int a, int b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

/* Game functions */

void place_piece(bitboard *player_board, bitboard *opponent_board, int pos) {

    bitboard o_board = *opponent_board;
    bitboard p_board = *player_board;
    bitboard opponent_edit;
    bitboard player_edit;

    p_board |= POWER_2[pos]; // place piece

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

            p = POWER_2[pos + (i * d)];

            if (opponent_meet) {
                if ((p_board & p) == 0) {
                    if ((o_board & p) == 0) {
                        break;
                    } else {
                        opponent_edit &= ~p;
                        player_edit |= p;
                    }
                } else {
                    opponent_edit &= ~POWER_2[pos + d];
                    player_edit |= POWER_2[pos + d];

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

bool is_legal_move(bitboard player_board, bitboard opponent_board, int pos) {

    // check if the case is empty
    if (((player_board | opponent_board) & POWER_2[pos])) {
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

            p = POWER_2[pos + (i * d)];

            if (opponent_meet) {
                // If there is an empty case
                if ((player_board & p) == 0) {
                    // If there is no opponent piece
                    if ((opponent_board & p) == 0) {
                        break;
                    }
                } else {
                    // if there is a player piece
                    return true;
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

    return false;
}


bitboard get_all_legal_moves(bitboard player_board, bitboard opponent_board) {
    bitboard legal_move = 0;

    for (int i = 0; i < 64; i++) {
        if (is_legal_move(player_board, opponent_board, i)) {
            legal_move += POWER_2[i];
        }
    }

    return legal_move;
}


/* Engine functions */

class HashTable {
private:
    struct Entry {
        bitboard white_board;
        bitboard black_board;
        int reward;
    };

    unsigned int len = 0;

    Entry *table = new Entry[HASHTABLE_CAPACITY];

    unsigned int index(bitboard wb, bitboard bb) const {
        for (int i = 0; i < len; i++) {
            if (table[i].white_board == wb && table[i].black_board == bb) {
                return i + 1; // index + 1
            }
        }
        return 0; // 0 if not founded
    };

public:
    void add(bitboard wb, bitboard bb, int r) {
        if (len < HASHTABLE_CAPACITY) {
            table[len].white_board = wb;
            table[len].black_board = bb;
            table[len].reward = r;
            len += 1;
        }
    };

    int get(bitboard wb, bitboard bb) {
        unsigned int ind = index(wb, bb);
        if (ind == 0) {
            return not_found_table;
        } else {
            return table[ind - 1].reward;
        }
    }
};

int board_evaluate(bitboard board) {
    int count = 0;

    while (board) {
        count += board & 1;
        board >>= 1;
    }
    return count;
}


int explore_node(bitboard white_board, bitboard black_board, int depth, int max_depth, int *stats, HashTable H) {

    if (depth == max_depth) {
        return board_evaluate(black_board);
    }

    bitboard legal_moves;
    bitboard temp_w_board;
    bitboard temp_b_board;
    int reward;
    int temp_reward;
    int i;
    int hash_reward;

    hash_reward = H.get(white_board, black_board);

    if (hash_reward != not_found_table) {
        return hash_reward;
    }

    // Player turn
    if (depth % 2 == 1) {

        reward = 64; // impossible reward to do the min

        // get every possible moves
        legal_moves = get_all_legal_moves(white_board, black_board);

        for (i = 0; i < 64; i++) {

            if ((legal_moves & POWER_2[i]) != 0) {
                temp_w_board = white_board;
                temp_b_board = black_board;

                place_piece(&temp_w_board, &temp_b_board, i);

                *stats += 1;

                temp_reward = explore_node(temp_w_board, temp_b_board, depth + 1, max_depth, stats, H);

                reward = min(reward, temp_reward);
            }
        }

        H.add(white_board, black_board, temp_reward);

        return reward;
    } else {

        reward = 0; // impossible reward to do the max

        // get every possible moves
        legal_moves = get_all_legal_moves(black_board, white_board);

        for (i = 0; i < 64; i++) {

            if ((legal_moves & POWER_2[i]) != 0) {
                temp_w_board = white_board;
                temp_b_board = black_board;

                *stats += 1;

                place_piece(&temp_b_board, &temp_w_board, i);

                temp_reward = explore_node(temp_w_board, temp_b_board, depth + 1, max_depth, stats, H);

                reward = max(reward, temp_reward);
            }
        }

        H.add(white_board, black_board, temp_reward);

        return reward;
    }
}


int get_best_move(bitboard white_board, bitboard black_board, bool white_engine, int max_depth, int *stats) {
    bitboard wb;
    bitboard bb;

    if (white_engine) {
        wb = black_board;
        bb = white_board;
    } else {
        wb = white_board;
        bb = black_board;
    }

    int best_move = -11;
    int best_reward = -1;
    int temp_reward;
    int i;

    bitboard legal_moves;
    bitboard temp_w_board;
    bitboard temp_b_board;

    // create the hashtable
    HashTable H;

    legal_moves = get_all_legal_moves(bb, wb);

    for (i = 0; i < 64; i++) {

        if ((legal_moves & POWER_2[i]) != 0) {
            temp_w_board = wb;
            temp_b_board = bb;

            place_piece(&temp_b_board, &temp_w_board, i);

            temp_reward = explore_node(temp_w_board, temp_b_board, 1, max_depth, stats, H);
            if (temp_reward > best_reward) {
                best_reward = temp_reward;

                best_move = i;
            }
        }
    }

    return best_move;
}

int get_move_reward(bitboard white_board, bitboard black_board, bool white_engine, int max_depth, int *stats) {
    bitboard wb;
    bitboard bb;

    if (white_engine) {
        wb = black_board;
        bb = white_board;
    } else {
        wb = white_board;
        bb = black_board;
    }

    HashTable H;

    return explore_node(wb, bb, 0, max_depth, stats, H);
}

/* Export function */
extern "C" {
int cpp_get_move_reward(bitboard white_board, bitboard black_board, bool white_engine, int max_depth, int *stats) {
    return get_move_reward(white_board, black_board, white_engine, max_depth, stats);
}
}

extern "C" {
int cpp_get_best_move(bitboard white_board, bitboard black_board, bool white_engine, int max_depth, int *stats) {
    return get_best_move(white_board, black_board, white_engine, max_depth, stats);
}
}