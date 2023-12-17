#include <stdlib.h>
#include <stdio.h>
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


board* board_new(unsigned int width, unsigned int height, enum type type) {
    if (width == 0 || height == 0) {
        fprintf(stderr, "Must be 2 dimensional\n");
        exit(1);
    }
    
    board* new_board = malloc(sizeof(board));
    new_board->width = width;
    new_board->height = height;
    new_board->type = type;
    unsigned int bit_len = 0;
    if (type != MATRIX) {
        bit_len = (2 * width * height) / 32;
        if ((width / height) % 32 == 0 || (2 * width * height) < 32) {
            bit_len++;
        }
        new_board->u.bits = (unsigned int*)malloc(bit_len * sizeof(unsigned int));
        for (unsigned int i=0; i < bit_len; i++) {
            new_board->u.bits[i] = 0;
        }
        return new_board;
    }
    
    new_board->u.matrix = (cell**)malloc(height * sizeof(cell*));
    for (unsigned int i=0; i < height; i++) {
        new_board->u.matrix[i] = (cell*)malloc(width * sizeof(cell));
        for (unsigned int j=0; j < width; j++) {
            new_board->u.matrix[i][j] = EMPTY;
        }
    }
    return new_board;

}


void board_free(board* b) {
    if (b->type != MATRIX) {
        free(b->u.bits);
    } else {
        for (unsigned int i=0; i < b->height; i++) {
            free(b->u.matrix[i]);
        }
        free(b->u.matrix);
    }
    free(b);
}


/* Given an integer, num, converts num to
an uppercase or lowercase letter, or a ? depending on how high
num is. num should be higher than 9*/
char large_char(unsigned int num) {
    char new;
    
    if (62 <= num) {
        new = '?';
    } else {
         if (num < 36) {
            new = 'A' + (num - 10);
        } else {
            new = 'a' + (num - 36);
        }
    }
    
    return new;
}

cell board_get(board* b, pos p) {
    if (b->height < p.r || b->width < p.c) {
        printf("Out of bounds error\n");
        exit(1);
    }
    if (b->type == MATRIX) {
        return b->u.matrix[p.r][p.c];
    }
    unsigned int i = (2 * (p.r * b->width + p.c));
    unsigned int loc = i / 32;
    unsigned int position = i % 32;
    return ((b->u.bits[loc] >> position) & 0x3);
    
}

void board_show(board* b) {
    unsigned int w = b->width;
    unsigned int h = b->height;
    char piece = '.';
    
    for (unsigned int i=0; i < w; i++) {
        if (i == 0) {
            printf("  ");
        }
        if (i < 10) {
            printf("%d ", i);
        } else {
            printf("%c ", large_char(i));
        }
    }
    printf(" ");
    printf("\n");
    for (unsigned int j=0; j < h; j++) {
        if (j < 10) {
            printf("%d ", j);
        } else {
            printf("%c ", large_char(j));
        }
        for (unsigned int z=0; z < w; z++) {
            if (board_get(b, make_pos(j, z)) == BLACK) {
                piece = '*';
            } else if (board_get(b, make_pos(j, z)) == WHITE) {
                piece = 'o';
            } else {
                piece = '.';
            }
            printf("%c ", piece);
        }
        printf("\n");
    }
}


void board_set(board* b, pos p, cell c) {
    if (b->height < p.r || b->width < p.c) {
        printf("Out of bounds error\n");
        exit(1);
    }
    if (b->type == MATRIX) {
        b->u.matrix[p.r][p.c] = c;
    }
    unsigned int i = (2 * (p.r * b->width + p.c));
    unsigned int loc = i / 32;
    unsigned int position = i % 32;
    b->u.bits[loc] &= ~(0x3 << position);
    b->u.bits[loc] |= (c << position);
}


