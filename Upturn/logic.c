#include <stdbool.h>
#include "board.h"
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

enum turn {
    BLACKS_TURN,
    WHITES_TURN
};

typedef enum turn turn;


enum outcome {
    IN_PROGRESS,
    BLACK_WIN,
    WHITE_WIN,
    DRAW
};

typedef enum outcome outcome;


enum rotation {
    NO_ROTATION,
    CLOCKWISE,
    COUNTERCLOCKWISE
};

typedef enum rotation rotation;


struct game {
    unsigned int run;
    board* b;
    posqueue *black_queue, *white_queue;
    turn player;
    rotation last_rotation;
};

typedef struct game game;



game* new_game(unsigned int run, unsigned int width,
               unsigned int height, enum type type) {
    posqueue* black = posqueue_new();
    posqueue* white = posqueue_new();
    board* b = board_new(width, height, type);
    game* new = (game*)malloc(sizeof(game));
    new->b = b;
    new->run = run;
    new->black_queue = black;
    new->white_queue = white;
    new->player = BLACKS_TURN;
    new->last_rotation = NO_ROTATION;
    return new;
}


void game_free(game* g) {
    board_free(g->b);
    posqueue_free(g->black_queue);
    posqueue_free(g->white_queue);
    free(g);
}

bool place_piece(game* g, pos p) {
    cell piece = EMPTY;
    
    if (board_get(g->b, p) == EMPTY) {
        if (g->player == BLACKS_TURN) {
            piece = BLACK;
            pos_enqueue(g->black_queue, p);
        } else if (g->player == WHITES_TURN) {
            piece = WHITE;
            pos_enqueue(g->white_queue, p);
        } 
        board_set(g->b, p, piece);
    } else {
        return false;
    }

    if (g->player == WHITES_TURN) {
        g->player = BLACKS_TURN;
    } else {
        g->player = WHITES_TURN;
    }
    g->last_rotation = NO_ROTATION;
    return true;
}

/* Given an original posqueue pointer, a bool representing clockwise, and the new height and width,
returns a new posqueue with the entries inside rotated according to the rotated board
*/
posqueue* rotate_positions(posqueue* original, bool clockwise, unsigned int neww, unsigned int newh) {
    posqueue* rotated = posqueue_new();

    pq_entry* node = original->head;
    while (node) {
        unsigned int row = node->p.r;
        unsigned int col = node->p.c;
        pos rotated_pos;

        if (!clockwise) {
            rotated_pos.r = newh - 1 - col;
            rotated_pos.c = row;
        } else {
            rotated_pos.r = col;
            rotated_pos.c = neww - 1 - row;
        }

        pos_enqueue(rotated, rotated_pos);
        node = node->next;
    }

    return rotated;
}

/* struct ThreadArgs holds the original and rotated instances
of the board when using the rotate function, and includes the 'row' value
indicating which row will be rotated and the direction
*/
typedef struct {
    board* original;
    bool clockwise;
    unsigned int row;
    board* rotated;
} ThreadArgs;


/* rotate_row takes in a pointer to a ThreadArgs instance
and uses its information to recauculate the row coordinates after rotation; returns
void
*/
void* rotate_row(void* args) {
    ThreadArgs* threadArgs = (ThreadArgs*)args;
    board* org = threadArgs->original;
    bool clockwise = threadArgs->clockwise;
    unsigned int row = threadArgs->row;
    board* rotated_board = threadArgs->rotated;

    unsigned int newh = org->width;
    unsigned int neww = org->height;

    for (unsigned int j = 0; j < neww; ++j) {
        pos loc;
        if (!clockwise) {
            loc = make_pos(j, newh - 1 - row);
        } else {
            loc = make_pos(neww - 1 - j, row);
        }
        board_set(rotated_board, make_pos(row, j), board_get(org, loc));
    }


    pthread_exit(NULL);
}

/* threads_rotate takes in the board and a direction and returns a new, rotated board 
using threads with new board placements. Utilizes rotate_row function
to efficiently rotate rows of the board using threads
*/
board* threads_rotate(board* old, bool clockwise) {
    unsigned int newh = old->width;
    unsigned int neww = old->height;

    board* new = board_new(neww, newh, old->type);
    if (new == NULL) {
        perror("Board creation failed");
        return NULL;
    }

    pthread_t threads[newh];
    ThreadArgs* threadArgsArray = malloc(newh * sizeof(ThreadArgs));
    if (threadArgsArray == NULL) {
        perror("Memory allocation failed");
        board_free(new);
        return NULL;
    }

    for (unsigned int i = 0; i < newh; ++i) {
        threadArgsArray[i].original = old;
        threadArgsArray[i].clockwise = clockwise;
        threadArgsArray[i].row = i;
        threadArgsArray[i].rotated = new;

        if (pthread_create(&threads[i], NULL, rotate_row, (void*)&threadArgsArray[i]) != 0) {
            perror("Thread creation failed");
            free(threadArgsArray);
            board_free(new);
            return NULL;
        }
    }
    for (unsigned int i = 0; i < newh; ++i) {
        pthread_join(threads[i], NULL);
    }

    return new;
}



bool rotate(game* g, bool clockwise) {
    if ((clockwise && g->last_rotation == COUNTERCLOCKWISE) ||
    ((!clockwise) && g->last_rotation == CLOCKWISE)) {
        return false;
    }

    unsigned int newh = g->b->width;
    unsigned int neww = g->b->height;
    
    board* transf = threads_rotate(g->b, clockwise);
    if (transf == NULL) {
        return false;
    }

    posqueue* rotated_black = rotate_positions(g->black_queue, clockwise, neww, newh);
    posqueue* rotated_white = rotate_positions(g->white_queue, clockwise, neww, newh);

    posqueue_free(g->black_queue);
    posqueue_free(g->white_queue);

    g->b = transf;
    g->black_queue = rotated_black;
    g->white_queue = rotated_white;
   
    if (clockwise) {
        g->last_rotation = CLOCKWISE;
    } else {
        g->last_rotation = COUNTERCLOCKWISE;
    }

    if (g->player == BLACKS_TURN) {
        g->player = WHITES_TURN;
    } else {
        g->player = BLACKS_TURN;
    }

    return true;
}

bool uplift(game* g, cell c) {
    pos piece;
    pos check;
    if (c == BLACK) {
        if (g->black_queue->head == NULL || g->black_queue->len == 0) {
            return false;
        }
        check.r = g->black_queue->head->p.r - 1;
        check.c = g->black_queue->head->p.c;
        if (g->black_queue->head->p.r <= 0 || 
        board_get(g->b, check) != EMPTY) {
            printf("At board limit!\n");
            return false;
        }
        piece = pos_dequeue(g->black_queue);
    } else if (c == WHITE) {
        if (g->white_queue->head == NULL || g->white_queue->len == 0) {
            return false;
        }
        check.r = g->white_queue->head->p.r - 1;
        check.c = g->white_queue->head->p.c;
        if (g->white_queue->head->p.r <= 0 ||
        board_get(g->b, check) != EMPTY) {
            printf("At board limit!\n");
            return false;
        }
        piece = pos_dequeue(g->white_queue);
    }
    
    pos p = {piece.r - 1, piece.c};
    cell move = board_get(g->b, p);
    
    
    while (p.r >= 0 && move == EMPTY) {
        if (p.r == 0) {
            break;
        }
        p.r--;
        move = board_get(g->b, p);
    }
    
    if (p.r >= 0 && move != EMPTY) {
        p.r++;
    } 

    board_set(g->b, p, c);
    board_set(g->b, piece, EMPTY);
    if (g->player == BLACKS_TURN) {
        g->player = WHITES_TURN;
    } else {
        g->player = BLACKS_TURN;
    }
    g->last_rotation = NO_ROTATION;
    
    if (c == BLACK) {
        pos_enqueue(g->black_queue, p);
    } else {
        pos_enqueue(g->white_queue, p);
    }
    return true;
}

outcome game_outcome(game* g) {
    
    for (int i = 0; i < g->b->height; i++) {
        int w_count = 0;
        int b_count = 0;
        for (int j = 0; j < g->b->width; j++) {
            if (board_get(g->b, make_pos(i, j)) == BLACK) {
                b_count++;
                
            } else if (board_get(g->b, make_pos(i, j)) == WHITE) {
                w_count++;
            }
            if (w_count == g->run) {
                return WHITE_WIN;
            } else if (b_count == g->run) {
                return BLACK_WIN;
            } 
        }   
    }
    
    for (int j = 0; j < g->b->width; j++) {
        int w_count = 0;
        int b_count = 0;
        for (int i = 0; i < g->b->height; i++) {
            if (board_get(g->b, make_pos(i, j)) == BLACK) {
                b_count++;
                
            } else if (board_get(g->b, make_pos(i, j)) == WHITE) {
                w_count++;
            }
            if (w_count == g->run) {
                return WHITE_WIN;
            } else if (b_count == g->run) {
                return BLACK_WIN;
            }
        }   
    }    
    
    for (int i = 0; i < g->b->height; i++) {
    for (int j = 0; j < g->b->width; j++) {
        int b_count = 0;
        int w_count = 0;
        for (int k = 0; k < g->run; k++) {
            if (i + k < g->b->height && j + k < g->b->width) {
                cell current_cell = board_get(g->b, make_pos(i + k, j + k));
                if (current_cell == WHITE) {
                    w_count++;
                    if (w_count == g->run) {
                        return WHITE_WIN;
                    }
                    b_count = 0;
                } else if (current_cell == BLACK) {
                    b_count++;
                    if (b_count == g->run) {
                        return BLACK_WIN;
                    }
                    w_count = 0;
                }
            }
        }
    }
}

    for (int i = 0; i < g->b->height; i++) {
        for (int j = 0; j < g->b->width; j++) {
            if (board_get(g->b, make_pos(i, j)) == EMPTY) {
                return IN_PROGRESS;
            }
        }
    }
    return DRAW;
}



