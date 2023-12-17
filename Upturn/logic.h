#ifndef LOGIC_H
#define LOGIC_H

#include <stdbool.h>
#include "board.h"


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

/* Begins a new game by returning an instance of the game struct;
consists of run, the number of pieces in a row needed to win, width 
and height of the board, and type, MATRIX or BITS*/
game* new_game(unsigned int run, unsigned int width,
               unsigned int height, enum type type);

/* Given an instance of a game, g, frees the associated board
and the black and white posqueues within the struct, if any; returns
nothing */
void game_free(game* g);

/* Places a piece on the board of g at position p if the 
position is empty. Returns true if the placement was successful,
false if not (there was already a piece there)*/
bool place_piece(game* g, pos p);

/* Rotates the board 90 degrees clockwise or counterclockwise;
corresponding piece positions are also rotated, including adjustment
in the black and white queues and piece positions. If a player has just
rotated in one direction, the other player cannot rotate in the 
opposite direction consecutively*/
bool rotate(game* g, bool clockwise);

/* Takes the last placed piece, stored in black and white
queues, of the specified color, c, 
and raises its height position to the top of the board, or directly
below the first piece it comes into contact with*/
bool uplift(game* g, cell c);

/* Determines the current outcome of the game; the game is won 
if a player has placed run  amount of pieces on the board
consecutively either horizontally, vertically, or diagonally.
Returns IN_PROGRESS, BLACK_WIN, WHITE_WIN, or DRAW */
outcome game_outcome(game* g);

#endif /* LOGIC_H */
