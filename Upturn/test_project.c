#include <criterion/criterion.h>
#include "pos.h"
#include "board.h"
#include "logic.h"
#include <stdlib.h>



Test(make_pos, simple) {
    pos test = make_pos(1, 2);
    cr_assert(test.r == 1);
    cr_assert(test.c == 2);
}

Test(make_pos, complex) {
    pos test = make_pos(38, 0);
    cr_assert(test.r == 38);
    cr_assert(test.c == 0);
}

Test(posqueue_new, empty) {
    posqueue* new = posqueue_new();
    cr_assert(new->len == 0);
    posqueue_free(new);
}

Test(pos_enqueue, multiple) {
    posqueue* new = posqueue_new();
    pos p = make_pos(1, 1);
    pos p2 = make_pos(2, 2);
    pos_enqueue(new, p);
    pos_enqueue(new, p2);
    cr_assert(new->len == 2);
    cr_assert(new->tail->p.r == 2);
    cr_assert(new->tail->p.c == 2);
    cr_assert(new->head->p.r == 1);
    cr_assert(new->head->p.c == 1);
    posqueue_free(new);
}

Test(pos_enqueue, single) {
    posqueue* new = posqueue_new();
    pos p2 = make_pos(2, 2);
    pos_enqueue(new, p2);
    cr_assert(new->len == 1);
    cr_assert(new->tail->p.r == 2);
    cr_assert(new->tail->p.c == 2);
    posqueue_free(new);
}

Test(pos_dequeue, norm) {
    posqueue* new = posqueue_new();
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(5, 7);
    pos_enqueue(new, p1);
    pos_enqueue(new, p2);
    pos test = pos_dequeue(new);
    cr_assert(test.r == 1);
    cr_assert(test.c == 1);
    cr_assert(new->len == 1);
    cr_assert(new->head->p.r == 5);
    cr_assert(new->head->p.c == 7);
    posqueue_free(new);
}

Test(pos_dequeue, one) {
    posqueue* new = posqueue_new();
    pos p1 = make_pos(1, 1);
    pos_enqueue(new, p1);
    pos test = pos_dequeue(new);
    cr_assert(test.r == 1);
    cr_assert(test.c == 1);
    cr_assert(new->len == 0);
    cr_assert(new->head == NULL);
    posqueue_free(new);
}

Test(posqueue_free, list) {
    posqueue* new = posqueue_new();
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(5, 7);
    pos_enqueue(new, p1);
    pos_enqueue(new, p2);
    posqueue_free(new);
}


Test(board_new, small) {
    board* new = board_new(5, 5, MATRIX);
    for (unsigned int i=0; i < 5; i++) {
        for (unsigned int j=0; j < 5; j++) {
            cr_assert(new->u.matrix[i][j] == EMPTY);
        }
    }
    board_free(new);
}

Test(board_new, crooked) {
    board* new = board_new(5, 10, MATRIX);
    for (unsigned int i=0; i < 10; i++) {
        for (unsigned int j=0; j < 5; j++) {
            cr_assert(new->u.matrix[i][j] == EMPTY);
        }
    }
    board_free(new);
}

Test(board_new, big) {
    board* new = board_new(50, 50, MATRIX);
    for (unsigned int i=0; i < 50; i++) {
        for (unsigned int j=0; j < 50; j++) {
            cr_assert(new->u.matrix[i][j] == EMPTY);
        }
    }
    board_free(new);
}

Test(board_new, bit_small) {
    board* new = board_new(5, 5, BITS);
    for (unsigned int i=0; i < 5; i++) {
        for (unsigned int j=0; j < 5; j++) {
            cr_assert(board_get(new, make_pos(i, j)) == EMPTY);
        }
    }
    board_free(new);
}

Test(board_new, bit_crooked) {
    board* new = board_new(5, 10, BITS);
    for (unsigned int i=0; i < 10; i++) {
        for (unsigned int j=0; j < 5; j++) {
            cr_assert(board_get(new, make_pos(i, j)) == EMPTY);
        }
    }
    board_free(new);
}
//board_free works as intended; implemented in other tests

Test(board_show, every_case) {
    board* new = board_new(65, 65, BITS);
    pos p = make_pos(1, 1);
    pos p2 = make_pos(4, 4);
    board_set(new, p, WHITE);
    board_set(new, p2, BLACK);
}

Test(board_get, simple) {
    board* b = board_new(3, 3, BITS);
    
    board_set(b, make_pos(0, 0), EMPTY);
    board_set(b, make_pos(1, 1), BLACK);
    board_set(b, make_pos(2, 2), WHITE);

    cr_assert_eq(board_get(b, make_pos(0, 0)), EMPTY);
    cr_assert_eq(board_get(b, make_pos(1, 1)), BLACK);
    cr_assert_eq(board_get(b, make_pos(2, 2)), WHITE);

    board_free(b);
}

Test(board_set, easy) {
    board* b = board_new(3, 3, BITS);

    board_set(b, make_pos(0, 0), BLACK);
    board_set(b, make_pos(1, 2), WHITE);

    cr_assert_eq(board_get(b, make_pos(0, 0)), BLACK);
    cr_assert_eq(board_get(b, make_pos(1, 2)), WHITE);

    board_free(b);
}



Test(new_game, basic) {
    game* new = new_game(4, 4, 4, BITS);
    cr_assert(new->b->width == 4);
    cr_assert(new->b->height == 4);
    cr_assert(new->player == BLACKS_TURN);
    cr_assert(new->last_rotation == NO_ROTATION);

    game_free(new);
}

Test(place_piece, 0) {
    game* new = new_game(4, 4, 4, BITS);
    cr_assert(place_piece(new, make_pos(0, 0)));
    cr_assert(board_get(new->b, make_pos(0, 0)) == BLACK);
    game_free(new);
}

Test(place_piece, 8) {
    game* new = new_game(5, 10, 10, BITS);
    new->player = WHITES_TURN;
    cr_assert(place_piece(new, make_pos(8, 2)));
    cr_assert(board_get(new->b, make_pos(8, 2)) == WHITE);
    game_free(new);
}

Test(rotate, cw) {
    game* new = new_game(5, 10, 6, BITS);
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(3, 5);
    posqueue* black = posqueue_new();
    posqueue* white = posqueue_new();
    pos_enqueue(black, p1);
    pos_enqueue(white, p2);
    new->black_queue = black;
    new->white_queue = white;
    board_set(new->b, p1, BLACK);
    board_set(new->b, p2, WHITE);
    cr_assert(rotate(new, true));
    pos new_p1 = make_pos(1, 4);
    pos new_p2 = make_pos(5, 2);
    cr_assert(board_get(new->b, new_p1) == BLACK);
    cr_assert(board_get(new->b, new_p2) == WHITE);
    game_free(new);
}


Test(rotate, ccw) {
    game* new = new_game(5, 10, 6, BITS);
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(3, 5);
    posqueue* black = posqueue_new();
    posqueue* white = posqueue_new();
    pos_enqueue(black, p1);
    pos_enqueue(white, p2);
    new->black_queue = black;
    new->white_queue = white;
    board_set(new->b, p1, BLACK);
    board_set(new->b, p2, WHITE);
    cr_assert(rotate(new, false));
    pos new_p1 = make_pos(8, 1);
    pos new_p2 = make_pos(4, 3);
    cr_assert(board_get(new->b, new_p1) == BLACK);
    cr_assert(board_get(new->b, new_p2) == WHITE);
    game_free(new);
    
}

Test(uplift, small) {
    game* new = new_game(5, 10, 6, BITS);
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(3, 5);
    posqueue* black = posqueue_new();
    posqueue* white = posqueue_new();
    pos_enqueue(black, p1);
    pos_enqueue(white, p2);
    new->black_queue = black;
    new->white_queue = white;
    board_set(new->b, p1, BLACK);
    board_set(new->b, p2, WHITE);
    cr_assert(uplift(new, BLACK));
    pos new_p1 = make_pos(0, 1);
    cr_assert(board_get(new->b, new_p1) == BLACK);
    game_free(new);
}

Test(uplift, medium) {
    game* new = new_game(5, 10, 6, BITS);
    pos p2 = make_pos(3, 5);
    posqueue* white = posqueue_new();
    pos_enqueue(white, p2);
    new->white_queue = white;
    board_set(new->b, p2, WHITE);
    cr_assert(uplift(new, WHITE));
    pos new_p2 = make_pos(0, 5);
    cr_assert(board_get(new->b, new_p2) == WHITE);
    game_free(new);
}

Test(uplift, piece) {
    game* new = new_game(5, 10, 6, BITS);
    pos p1 = make_pos(1, 1);
    pos p2 = make_pos(5, 1);
    posqueue* black = posqueue_new();
    posqueue* white = posqueue_new();
    pos_enqueue(black, p1);
    pos_enqueue(white, p2);
    new->black_queue = black;
    new->white_queue = white;
    board_set(new->b, p1, BLACK);
    board_set(new->b, p2, WHITE);
    cr_assert(uplift(new, WHITE));
    pos new_p2 = make_pos(2, 1);
    cr_assert(board_get(new->b, new_p2) == WHITE);
    game_free(new);
}

Test(game_outcome, w_win) {
    game* new = new_game(5, 10, 10, BITS);
    for (unsigned int i=2; i < 7; i++) {
        board_set(new->b, make_pos(i, 2), WHITE);
    }
    cr_assert(game_outcome(new) == WHITE_WIN);
    game_free(new);
}

Test(game_outcome, b_win) {
    game* new = new_game(3, 7, 3, BITS);
    for (unsigned int j = 2; j < 5; j++) {
        board_set(new->b, make_pos(2, j), BLACK);
    }
    outcome result = game_outcome(new);

    cr_assert(result == BLACK_WIN);
    game_free(new);
}


Test(game_outcome, diagonal_win) {
    game* new = new_game(3, 7, 3, BITS);

    for (unsigned int i = 0; i < 3; i++) {
        board_set(new->b, make_pos(i, i), BLACK);
    }

    outcome result = game_outcome(new);
    cr_assert(result == BLACK_WIN);
    game_free(new);
}

Test(game_outcome, draw) {
    game* new = new_game(3, 3, 3, BITS);

    board_set(new->b, make_pos(0, 0), BLACK);
    board_set(new->b, make_pos(0, 1), WHITE);
    board_set(new->b, make_pos(0, 2), BLACK);
    board_set(new->b, make_pos(1, 0), WHITE);
    board_set(new->b, make_pos(1, 1), BLACK);
    board_set(new->b, make_pos(1, 2), WHITE);
    board_set(new->b, make_pos(2, 0), WHITE);
    board_set(new->b, make_pos(2, 1), BLACK);
    board_set(new->b, make_pos(2, 2), WHITE);

    outcome result = game_outcome(new);
    cr_assert(result == DRAW);
    game_free(new);
}


Test(game_outcome, in_progress) {
    game* new = new_game(3, 4, 3, BITS);
    board_set(new->b, make_pos(0, 0), BLACK);
    board_set(new->b, make_pos(0, 1), WHITE);
    board_set(new->b, make_pos(0, 2), BLACK);

    outcome result = game_outcome(new);
    cr_assert(result == IN_PROGRESS);
    game_free(new);
}


