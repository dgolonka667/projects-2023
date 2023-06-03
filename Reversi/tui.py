"""
TUI for Reversi
"""
import click
import pygame
import cowsay  # type: ignore
from termcolor import colored # type: ignore
from reversi import Reversi
from bot import random_move, best_move, seer_move


class TUIPlayer:
    """
    Simple class to store information about a TUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """
    board_size: int
    num_players: int
    othello: bool
    reversi: Reversi

    def __init__(self, board_size: int, num_players: int, othello: bool, \
                 reversi:Reversi, players):
        """ Constructor

        Args:
            board_size: The size of the squae board
            num_players: The amount of players
            othello: If the game follows the othello configuration
        """

        self.board_size = board_size
        self.num_players = num_players
        self.othello = othello
        self.players = players


#stub = Reversi(board_size, 2,  True)
grid = []

def print_board(board_size:int) -> None:
    """ Prints the board to the screen

    Args:
        grid: The board to print

    Returns: None
    """
    #prints entire grid as horizontal walls
    for x in range(0, ((board_size * 3) - (board_size - 1))):
        grid.append(["─"] * ((board_size* 3) - (board_size - 1)))

    #prints all potentially piece spaces as blank
    for i, xrow in enumerate(grid):
        for j, _ in enumerate(xrow):
            if i % 2 == 1 and j % 2 == 1:
                grid[i][j] = " "

    #applies all vertical walls
    for row in range(1, (board_size * 3) - (board_size), 2):
        for col in range(0, (board_size * 3) - (board_size - 1), 2):
            grid[row][col] = "│"

    #applies all upper border "┬"
    for row in range(0, (board_size * 3) - (board_size), 2):
        grid[0][row] = "┬"

    #applies all lower border "┴"
    for row in range(0, (board_size * 3) - (board_size -1 ), 2):
        grid[(board_size * 3) - (board_size)][row] = "┴"

    #applies all left border "├"
    for row in range(0, (board_size * 3) - (board_size), 2):
        grid[row][0] = "├"

    #applies all right border "┴"
    for row in range(0, (board_size * 3) - (board_size -1), 2):
        grid[row][(board_size * 3) - (board_size)] = "┤"

    #applies all intersection pieces ┼"
    for i, xrow2 in enumerate(grid):
        for j, _ in enumerate(xrow2):
            if i % 2 == 0 and j % 2 == 0 and \
                i != 0 and i != (board_size * 3) - (board_size) \
                    and j != 0 and j != (board_size * 3) - (board_size):
                grid[i][j] = "┼"

    #applies all corners
    grid[0][0] = "┌"
    grid[(board_size * 3) - (board_size)][(board_size * 3) - (board_size)] = "┘"
    grid[0][(board_size * 3) - (board_size)] = "┐"
    grid[(board_size * 3) - (board_size)][0] = "└"

def play_reversi(stub: Reversi, bot_type: str, num_bots: int):
    """ 
    Plays a game of Reversi on the terminal

    Args:
        board_size: the
        players: A dictionary mapping piece colors to
          TUIPlayer objects.

    Returns: None

    """
    players = {1 : colored("1", "light_red"), \
               2 : colored("2", "light_yellow"),\
                3 : colored("3", "light_green"), \
                4 : colored("4", "green", attrs=["dark"]),\
                5 : colored("5", "light_cyan"),
                6 : colored("6", "blue"), \
                7 : colored("7", "light_magenta"), \
                8 : colored("8", "black"),\
                9 : colored("9", "white")}
    bot_players = []
    for i in range (num_bots):
        bot_players.append(stub.num_players - i)

    while not stub.done:
        #Apply stub piece positions
        for r in range(len(stub.grid)):
            for c in range(len(stub.grid[0])):
                value = stub.grid[r][c]
                if value is not None:
                    player_color = players[int(value)]
                    grid[(r*2) + 1][(c*2) + 1] = player_color

        #Print the game board
        board_cols = []
        for char in grid:
            board_cols.append("".join(char))
        game_board = str("\n".join(board_cols))

        print()
        print(game_board)
        print()
        
        if bot_type != "none" and stub.turn in bot_players:
            print(f"It is Bot Player {stub._turn}'s turn.")
            print()
            if bot_type == "random":
                pygame.time.wait(750)
                random_move(stub)
            if bot_type == "smart":
                pygame.time.wait(750)
                best_move(stub, stub.turn)
            if bot_type == "very-smart":
                pygame.time.wait(750)
                seer_move(stub, stub.turn)
        else:
            print(f"It is Player {stub._turn}'s turn. Here are your available moves:")
            print()

            #Print the list of available moves
            for i, move in enumerate(stub.available_moves):
                (x, y) = move
                print(f"{(i + 1)}).", (x+1, y+1))

            #Prompt the player for a desired move
            print()
            selection = input("Please select a move:")

            #Check if move is in available_moves
            while (int(selection) - 1) not in range(0, len(stub.available_moves)):
                selection = input("Move outside of provided list, please select a new move:")

            #Apply move and move on
            selected = stub.available_moves[int(selection) - 1]
            stub.apply_move(selected)
            (r, c) = selected

        if stub.done:
            for r in range(len(stub.grid)):
                for c in range(len(stub.grid[0])):
                    value = stub.grid[r][c]
                    if value is not None:
                        player_color = players[int(value)]
                        grid[(r*2) + 1][(c*2) + 1] = player_color
            board_cols = []
            for char in grid:
                board_cols.append("".join(char))
            game_board = str("\n".join(board_cols))
            print(game_board)
            if len(stub.outcome) == 1:
                print(cowsay.get_output_string('trex', f"Congrats Player {stub.outcome[0]}!"))
            else:
                winners = ""
                for player in stub.outcome:
                    winners = winners + (str(player)) + " "
                print(cowsay.get_output_string('trex', f"It's a tie! Congrats {winners}!"))

#
#Command-line Interface
#

@click.command("bot")
@click.option("-n", "--num-players", default=2)
@click.option("-s", "--board-size", default=8)
@click.option("--othello/--non-othello", default=True)
@click.option("-b", "--bot",
              type=click.Choice(["none","random", "smart", "very-smart"]),
              default="none")
@click.option("-nb","--num-bots", type=click.INT, default=0)


def cmd(num_players, board_size, othello, bot, num_bots):
    print_board(board_size)
    stub = Reversi(board_size, num_players, othello)
    play_reversi(stub, bot, num_bots)


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter