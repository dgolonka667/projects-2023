"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()

class ReversiMock(ReversiBase):
    """
    Mock implementation of ReversiBase.

    This mock implementation behaves according to the following rules:

    - It only supports two players and boards of size 4x4 and above.
    - The board is can be initialized the othello variant
    - Moves are legal if the position in the board is empty, and
      there is at least one piece (of any player) in an adjacent square
      (in any direction, including diagonals). Additionally, placing a piece in
      position (0,0) or (side-1, side-1) is always legal
    - If a player places a piece in position (0,0), the game ends, and that
      player wins the game. If a player places a piece in position
      (side-1, side-1), the game ends, and both players win the game
      (i.e., the game ends in a tie)
    - It does validate board positions. If a method is called with a position
      outside the board, the method will raise an exception.
    - It does not implement the ``load_game``
    - The ``simulate_moves`` method works for a single move.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The mock implementation "
                             "only supports two players")
        if side < 4:
            raise ValueError ("Side must be >= 4")
        if (side % 2 == 0 and players % 2 == 0
            or side % 2 == 1 and players % 2 == 1):
            super().__init__(side, players, othello)
        else:
            raise ValueError ("Parity not met, both players and sides"
                              "must either be even or odd")
        self._grid = [[None]*side for _ in range(side)]
        #1 DARK 2 LIGHT
        if othello:
            self._grid[side//2 - 1][side//2] = 1
            self._grid[side//2][side//2 - 1] = 1
            self._grid[side//2 - 1][side//2 - 1] = 2
            self._grid[side//2][side//2] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                if self.legal_move((r,c)):
                    moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return (self._grid[0][0] is not None or
        self._grid[self._side - 1][self._side - 1] is not None)

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][0] is not None:
            return [self._grid[0][0]]
        if self._grid[self._side - 1][self._side - 1] is not None:
            return [1, 2]
        return []

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        if not (0 <= r < self._side and 0 <= c < self._side):
            raise ValueError("Position is outside board limits")
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        if not (0 <= r < self._side and 0 <= c < self._side):
            raise ValueError("Position is outside board limits")
        if pos in [(0,0),(self._side - 1, self._side - 1)]:
            return True
        if self._grid[r][c] is not None:
            return False
        if self._grid[r][c] is None:
            neighbor = False
            for i in range(r-1,r+2):
                if 0 <= i < self._side:
                    for j in range(c-1,c+2):
                        if (0 <= j < self._side
                            and self._grid[i][j] is not None):
                            neighbor = True
            return neighbor
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        if not (0 <= r < self._side and 0 <= c < self._side):
            raise ValueError("Position is outside board limits")
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        sim = deepcopy(self)
        for r, c in moves:
            if not (0 <= r < self._side and 0 <= c < self._side):
                raise ValueError("Position is outside board limits")
            sim.apply_move((r,c))
        return sim

class ReversiBotMock(ReversiMock):
    '''
    DOC STRING
    '''

    @property
    def done(self) -> bool:
        for row in self._grid:
            if None in row:
                return False
        return True

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        if not (0 <= r < self._side and 0 <= c < self._side):
            raise ValueError("Position is outside board limits")
        if self._grid[r][c] is not None:
            return False
        if self._grid[r][c] is None:
            neighbor = False
            for i in range(r-1,r+2):
                if 0 <= i < self._side:
                    for j in range(c-1,c+2):
                        if (0 <= j < self._side
                            and self._grid[i][j] is not None):
                            neighbor = True
            return neighbor
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        if not (0 <= r < self._side and 0 <= c < self._side):
            raise ValueError("Position is outside board limits")
        self._grid[r][c] = self._turn
        for i in range(r-1,r+2):
            if 0 <= i < self._side:
                for j in range(c-1,c+2):
                    if (0 <= j < self._side
                        and self._grid[i][j] is not None
                        and self._grid[i][j] != self._turn):
                        self._grid[i][j] == self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1
