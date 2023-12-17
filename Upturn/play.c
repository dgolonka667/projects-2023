#include <stdlib.h>
#include <stdio.h>
#include "logic.h"
#include "board.h"
#include <string.h>


bool do_turn(game* game, char r, char c) {
    bool work;
    bool turn;
    bool place;

    switch(r) {
        case '!':
            switch(c) {
                case '>':
                    work = rotate(game, true);
                    if (!work) {
                        printf("Rotation failed\n");
                    }
                    break;
                case '<':
                    work = rotate(game, false);
                    if (!work) {
                        printf("Rotation failed\n");
                    }
                    break;
                case 'B':
                    turn = uplift(game, BLACK);
                    if (!turn) {
                        printf("Upturn failed\n");
                    }
                    break;
                case 'W':
                    turn = uplift(game, WHITE);
                    if (!turn) {
                        printf("Upturn failed\n");
                    }
                    break;
                default:
                    printf("Invalid character: %c\n", c);
                    return false;
            }
            return true;
        default:
            if (!(('0' <= r && r <= '9') || ('A' <= r && r <= 'Z') || 
            ('a' <= r && r <= 'z')) || !(('0' <= c && c <= '9') || 
            ('A' <= c && c <= 'Z') || ('a' <= c && c <= 'z'))) {
                printf("Invalid character: %c %c\n", r, c);
                return false;
            }
            char r_str[2] = {r, '\0'};
            char c_str[2] = {c, '\0'};

            unsigned int row = atoi(r_str);
            unsigned int col = atoi(c_str);

            pos loc = make_pos(row, col);
            place = place_piece(game, loc);

            if (!place) {
                printf("Piece placement failed\n");
                return false;
            }
            break;
    }
    return true;
}


int main(int argc, char *argv[]) {
    unsigned int run, width, height;
    enum type constr;

    for (unsigned int i=1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0) {
            height = atoi(argv[i+1]);
        }
        if (strcmp(argv[i], "-w") == 0) {
            width = atoi(argv[i+1]);
        }
        if (strcmp(argv[i], "-r") == 0) {
            run = atoi(argv[i+1]);
        }
        if (strcmp(argv[i], "-m") == 0) {
            constr = MATRIX;
        } else if (strcmp(argv[i], "-b") == 0) {
            constr = BITS;
    }
    }

    game* new = new_game(run, width, height, constr); 
    
    char r, c;
    while (game_outcome(new) == IN_PROGRESS) {

        board_show(new->b);
        if (new->player == BLACKS_TURN) {
            printf("Black:  \n");
            scanf("%c %c%*c", &r, &c);

        } else {
            printf("White:  \n");
            scanf("%c %c%*c", &r, &c);

        }
        do_turn(new, r, c);
        

    }
    outcome match = game_outcome(new);
    switch(match){
        case 1:
            board_show(new->b);
            printf("Black wins!\n");
            break;
        case 2:
            board_show(new->b);
            printf("White wins!\n");
            break;
        case 3:
            board_show(new->b);
            printf("Draw! Get better, skill issue.\n");
            break;
        default:
            break;
    }
    game_free(new);
    return 0;
}
