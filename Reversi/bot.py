'''
Bots for Reversi

And command for running bot simulations
'''

import random
import math
from typing import Dict
import click
from reversi import ReversiBase, Reversi

results: Dict[str,int] = {}

def random_move(revgame: ReversiBase) -> None:
    '''
    Make a random move on a game of Reversi

    Input:
        revgame [ReversiBase]: the game of Reversi
    '''
    possible = revgame.available_moves
    if possible != []:
        pick = random.randint(0,len(possible) - 1)
        revgame.apply_move(possible[pick])

def best_move(revgame: ReversiBase, turn: int) -> None:
    '''
    Make a move that results in the most number of pieces for a player
    immediately following in a game of Reversi

    Input:
        revgame [ReversiBase]: the game of Reversi
        turn [int]: the current player's turn
    '''
    most = 0
    best: list[tuple[int,int]] = []
    possible = revgame.available_moves
    if possible != []:
        for move in possible:
            potential = 0
            temp = revgame.simulate_moves([move])
            for row in temp.grid:
                for cell in row:
                    if cell is not None and cell == turn:
                        potential += 1
            if potential > most:
                most = potential
                best = []
                best.append(move)
            elif potential == most:
                best.append(move)
        if best:
            pick = random.randint(0,len(best) - 1)
            revgame.apply_move(best[pick])

def seer_move(revgame: ReversiBase, turn: int) -> None:
    '''
    Make the move that results in the highest average number of pieces for a
    player in a game of Reversi after on the next player's turn
    (assuming the next player's choice is random/unpredictable)

    Input:
        revgame [ReversiBase]: the game of Reversi
        turn [int]: the current player's turn
    '''
    possible = revgame.available_moves
    highest = -math.inf
    best = []
    for move in possible:
        total = 0
        step_one = revgame.simulate_moves([move])
        if step_one.done:
            best = [move]
            break
        next_possible = step_one.available_moves
        if next_possible:
            for move_two in next_possible:
                final = step_one.simulate_moves([move_two])
                for row in final.grid:
                    for cell in row:
                        if cell == turn:
                            total += 1
            if total / len(next_possible) > highest:
                highest = total / len(next_possible)
                best = []
                best.append(move)
            elif total / len(next_possible) == highest:
                best.append(move)
    if best:
        pick = random.randint(0,len(best) - 1)
        revgame.apply_move(best[pick])

@click.command("bot")
@click.option("-n", "--num-games", type=click.INT, default="100")
@click.option("-1", "--player1",
              type=click.Choice(["random", "smart", "very-smart"]),
              default="random")
@click.option("-2", "--player2",
              type=click.Choice(["random", "smart", "very-smart"]),
              default="random")

def cmd(num_games,player1,player2):
    '''
    Runs simulation/test of bots given command line parameters
    '''
    for _ in range(int(num_games)):
        game = Reversi(8,2,True)
        while not game.done:
            if (game.turn == 1 and player1 == "random"
                or game.turn == 2 and player2 == "random"):
                random_move(game)
            if (game.turn == 1 and player1 == "smart"
                or game.turn == 2 and player2 == "smart"):
                best_move(game,game.turn)
            if (game.turn == 1 and player1 == "very-smart"
                or game.turn == 2 and player2 == "very-smart"):
                seer_move(game, game.turn)
        if len(game.outcome) > 1:
            results["Tie"] = results.get("Tie",0) + 1
        elif game.outcome == [1]:
            results["1"] = results.get("1",0) + 1
        elif game.outcome == [2]:
            results["2"] = results.get("2",0) + 1

    win1 = results.get("1",0) / num_games * 100
    win2 = results.get("2",0) / num_games * 100
    wintie = results.get("Tie",0) / num_games * 100

    print(f"Player 1 wins: {win1:.2f}%")
    print(f"Player 2 wins: {win2:.2f}%")
    print(f"Ties: {wintie:.2f}%")

if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
