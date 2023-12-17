#ifndef BOARD_H
#define BOARD_H

#include "pos.h"


enum cell {
    EMPTY,
    BLACK,
    WHITE
};

typedef enum cell cell;


union board_rep {
    enum cell** matrix;
    unsigned int* bits;
};

typedef union board_rep board_rep;

enum type {
    MATRIX, BITS
};


struct board {
    unsigned int width, height;
    enum type type;
    board_rep u;
};

typedef struct board board;

/* Takes in a width, height, and type (either a MATRIX or BITS type)
and returns an instance of the board struct, containing the width and height
values, the type of board, and a pointer board representation matrix with
elements made of cells*/
board* board_new(unsigned int width, unsigned int height, enum type type);

/* Iterates through each row in the board and 
frees each allocated row, then the overall matrix*/
void board_free(board* b);

/* Prints out the board representation,
blacnk spaces indicated with ., white pieces with o, and
black pieces with *. Grid coords greater than 9 are replaced with
capital letters, then lowercase letters, then ?. */
void board_show(board* b);

/* Returns the value located at the coordinates in p on board b;
values possible are EMPTY, WHITE, and BLACK, and are type cell. */
cell board_get(board* b, pos p);

/* Changes the value located at position p on board b; changes 
value to c, cell, wihtout returning anything*/
void board_set(board* b, pos p, cell c);

#endif /* BOARD_H */
