'''
GUI for Reversi
'''
import os
import sys
from typing import Dict, Tuple
import click
import pygame
from reversi import Reversi
from bot import random_move, best_move, seer_move



os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class ReversiUI:
    """
    Gui editor initializer class for Reversi
    """

    board_size: int
    num_players: int
    othello: bool
    bot_type: str
    num_bots: int
    window: int
    border: int
    color_code: Dict[int, Tuple[int, int, int]]
    surface: pygame.surface.Surface
    clock: pygame.time.Clock
    square: int


    def __init__(self, board_size, num_players, othello, bot_type, num_bots,
                 window: int = 600, border: int =  10):
        """
        Constructor

            board_size: size of the board
            num_players: number of players
            othello: othello or non-othello variant of Reversi
            window: size of the window
            border: width of the border
        """
        self.board_size = board_size
        self.board = Reversi(board_size, num_players, othello)
        self.bot_type = bot_type
        self.num_bots = num_bots
        if num_bots > num_players:
            raise ValueError ("Number of bots > number of total players")
        self.bot_players = []
        for i in range (self.num_bots):
            self.bot_players.append(self.board.num_players - i)
        self.window = window
        self.border = border
        self.color_code = {}
        self.color_code[1] = (0, 0, 0)
        self.color_code[2] = (255, 255, 255)
        self.color_code[3] = (0, 0, 255)
        self.color_code[4] = (255, 64, 64)
        self.color_code[5] = (255, 127, 0)
        self.color_code[6] = (178, 58, 238)
        self.color_code[7] = (0, 206, 209)
        self.color_code[8] = (255, 20, 147)
        self.color_code[9] = (0, 201, 87)
        self.square = (self.window - 2 * self.border) // self.board_size
        pygame.init()
        pygame.display.set_caption("Reversi")

        self.surface = pygame.display.set_mode((window,
                                               window))
        self.clock = pygame.time.Clock()
        self.event_loop()


    def draw_window(self) -> None:
        """
        Draws window for Reversi game
        """
        if not self.board.done:
            for rownum in range(self.board_size):
                for colnum in range(self.board_size):
                    fill = (122, 122, 122)
                    rect = (self.border + rownum * self.square,
                            self.border + colnum * self.square,
                            self.square, self.square)
                    if (rownum, colnum) in self.board.available_moves:
                        fill = (255, 215, 0)

                    pygame.draw.rect(self.surface, color=fill,
                                    rect=rect)
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                        rect=rect, width=1)


            for i, row in enumerate(self.board.grid):
                for j, cell in enumerate(row):
                    center = (self.border + i*self.square + self.square // 2, self.border + j*self.square + self.square // 2)
                    if cell is not None:
                        color = self.color_code[cell]
                        pygame.draw.circle(self.surface, color=color,
                                            center=center, radius=self.square // 2)
                        if self.board.turn == cell and color == self.color_code[cell]:
                            pygame.draw.circle(self.surface, color=(255, 215, 0),
                                            center=center, radius=self.square // 2, width=5)


    def event_loop(self) -> None:
        '''
        Events for game occur here
        '''
        while True:

            if self.bot_type != "none" and self.board.turn in self.bot_players:
                if self.bot_type == "random":
                    pygame.time.wait(750)
                    random_move(self.board)
                if self.bot_type == "smart":
                    pygame.time.wait(750)
                    best_move(self.board, self.board.turn)
                if self.bot_type == "very-smart":
                    pygame.time.wait(750)
                    seer_move(self.board, self.board.turn)

            if self.board.done:
                if len(self.board.outcome) == 1:
                    winner = str(self.board.outcome[0])
                    message = f'The winner is Player {winner}!'
                else:
                    players = []
                    for player in self.board.outcome:
                        players.append(str(player))
                    winners = ', '.join(players)
                    message = f'Tie between players {winners}!'
                font = pygame.font.Font('freesansbold.ttf', 32)
                self.surface.fill((255, 255, 255))
                text = font.render(message, True, (0, 0, 0))
                t_Rect = text.get_rect()
                t_Rect.center = ((self.window + self.border) // 2, (self.window + self.border) // 2)
                self.surface.blit(text, t_Rect)

            events = pygame.event.get()
            pygame.display.set_caption('Reversi')
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONDOWN
                    and self.board.turn not in self.bot_players):
                    y, x = pygame.mouse.get_pos()
                    row = (y - self.border) // self.square
                    col= (x - self.border) // self.square
                    if (0 <= row < len(self.board.grid)
                        and 0 <= row < len(self.board.grid[0])):
                        if self.board.legal_move((row,col)):
                            self.board.apply_move((row,col))


            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)

@click.command("gui")
@click.option('-n', '--num-players', default=2, type=click.INT, help='Number of players')
@click.option('-s', '--board-size', default=8, type=click.INT, help='Board size')
@click.option('--othello/--non-othello', default=True)
@click.option("-b", "--bot",
              type=click.Choice(["none","random", "smart", "very-smart"]),
              default="none")
@click.option("-nb","--num-bots", type=click.INT, default=0)
def cmd(num_players, board_size, othello, bot, num_bots):
    ReversiUI(board_size, num_players, othello, bot, num_bots)


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
