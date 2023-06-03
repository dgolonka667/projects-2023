"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from copy import deepcopy


BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""


class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError

class Reversi(ReversiBase):
    """
    Reversi class, inheriting from ReversiBase ABC
    """
    _side: int
    _players: int
    _othello: bool
    _board: "Board"
    _grid: List[List[Optional[int]]]

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect,
                        if players > 9 or < 2, or if players >= side
        """
        if players > 9 or players < 2:
            raise ValueError ("Players must be between 2 and 9")
        if side < 3:
            raise ValueError ("Side must be >= 3")
        if players > side:
            raise ValueError ("Side must be >= players")
        if (side % 2 == 0 and players % 2 == 0
            or side % 2 == 1 and players % 2 == 1):
            super().__init__(side, players, othello)
        else:
            raise ValueError ("Parity not met, both players and sides "
                              "must either be even or odd")
        self._board = Board(side)

        if othello:
            if players == 2:
                self._board.add_piece(1, (side//2 - 1,side//2))
                self._board.add_piece(1, (side//2,side//2 - 1))
                self._board.add_piece(2, (side//2 - 1,side//2 - 1))
                self._board.add_piece(2, (side//2,side//2))
            else:
                raise ValueError ("Othello varient only allowed with 2 players")

        self._turn = 1
        self._num_moves = 0
        self._grid = [[None] * self._side for _ in range(self._side)]
        for i, row in enumerate(self._board.grid):
            for j, piece in enumerate(row):
                if piece is not None:
                    self._grid[i][j] = piece.value


    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return self._grid

    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self.players_av_moves(self.turn)

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        for i in range(1, self.num_players + 1):
            if self.players_av_moves(i):
                return False
        return True

    @property
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        pp_dict = {}
        ret_lst: List[int] = []
        if self.done:
            for row in self._grid:
                for cell in row:
                    if cell is not None:
                        if cell not in pp_dict:
                            pp_dict[cell] = 0
                        pp_dict[cell] += 1
            max_pieces_on_board = max(pp_dict.values())
            for player, piececount in pp_dict.items():
                if piececount == max_pieces_on_board and player is not None:
                    ret_lst.append(player)
            ret_lst.sort()
        return ret_lst

    @property
    def change_turn(self) -> None:
        '''
        Changes turns to the next player that has an available move
        if the game is not done
        '''
        if not self.done:
            if self._turn == self._players:
                self._turn = 1
            else:
                self._turn += 1
            if not self.available_moves:
                self.change_turn

    #
    # METHODS
    #

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        i, j = pos
        if  not ((0 <= i <= self._side - 1) and  (0 <= j <= self._side - 1)):
            raise ValueError("Outside of board limits")
        return self._grid[i][j]


    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        row,col = pos
        if not (0 <= row < self._side and 0 <= col < self._side):
            raise ValueError("Position is outside board limits")
        return pos in self.available_moves

    def open_spaces(self) ->  List[Tuple[int, int]]:
        '''
        Determines all of the open spaces on a board

        Inputs:
            b [Board]: the board

        Output [List[Tuple[int,int]]]: list of all open locations on a board
        '''
        open_space = []
        for i, row in enumerate(self._board.grid):
            for j, _ in enumerate(row):
                if self._board.grid[i][j] is None:
                    open_space.append((i,j))
        return open_space

    def check_end(self, val:int,loc:Tuple[int,int],ydir:int,xdir:int) -> bool:
        '''
        Checks whether the is a piece of the same name at the end of the line
        of the other players' pieces

        Inputs:
            val [int]: the value of the current player's piece
            loc [Tuple[int,int]]: the location of an open space
            ydir [int]: direction along the y axis where other piece val present
            xdir [int]: direction along the x axis where other piece val present

        Output [bool]: True if there is a piece of the same name along the line
                    False otherwise
        '''
        row, col = loc
        if self._grid[row + ydir][col + xdir] == val:
            return True
        if self._grid[row + ydir][col + xdir] is None:
            return False
        if (0 <= (row + (2 * ydir)) < len(self._grid) and
            0 <= (col + (2 * xdir)) < len(self._grid[0])):
            return self.check_end(val,(row + ydir,col + xdir),ydir,xdir)
        return False

    def players_av_moves(self, turn: int) -> ListMovesType:
        '''
        Produces a list of availible moves for a given player in an ongoing
        game.

        Inputs:
            turn [int]: the player whose turn it is

        Returns [List[Tuple[int,int]]]: availible moves for the player.
        '''
        possible = set()
        if not self._othello and self._num_moves < self._players ** 2:
            top_left = (self._side//2) - self._players//2
            for i in range(top_left, top_left+self._players):
                for j in range(top_left, top_left + self._players):
                    if self._grid[i][j] is None:
                        possible.add((i,j))
        else:
            open_space = self.open_spaces()
            for cell in open_space:
                row, col = cell
                for i in range(row-1, row+2):
                    for j in range(col-1, col + 2):
                        if (0 <= i < len(self._grid)
                            and 0 <= j < len(self._grid[0])
                            and (i != row or j != col)):
                            if (self._grid[i][j] != turn and
                                self.check_end(turn,cell, i - row, j - col)):
                                possible.add((row,col))
        moves = list(possible)
        moves.sort()
        return moves

    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos [Tuple[int,int]]: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        row, col = pos
        if  not ((0 <= row <= self._side - 1) and  (0 <= col <= self._side - 1)):
            raise ValueError("Location is outside board.")
        if self._board.add_piece(self.turn, (row,col)):
            self._grid[row][col] = self.turn
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (0 <= i < self._side
                    and 0 <= j < self._side
                    and (i != row or j != col)):
                    if (self._board.grid[i][j] != self.turn
                        and self.check_end(self.turn, pos, i-row, j-col)):
                        if (self._othello or
                            self._num_moves >= self._players ** 2):
                            self.flip_pieces(self.turn, pos, i-row, j-col)
        self._num_moves += 1
        self.change_turn

    def flip_pieces(self,val:int,start:Tuple[int,int],ydir:int,xdir:int)-> None:
        '''
        Flips over pieces as a result of a move being played, in a specific
        direction

        Inputs:
            val [int]: the value of the current player's piece
            loc [Tuple[int,int]]: the location of an open space
            ydir [int]: direction along the y axis where other piece val present
            xdir [int]: direction along the x axis where other piece val present

        Output: None
        '''
        row, col = start
        if (self._grid[row + ydir][col + xdir] != val
            and self._grid[row + ydir][col + xdir] is not None):
            to_flip = self._board.grid[row+ydir][col+xdir]
            if to_flip is not None:
                to_flip.value = val
                self._grid[row+ydir][col+xdir] = val
        if (0 <= row + (2 * ydir) < len(self._grid)
            and 0 <= col + (2 * xdir) < len(self._grid[0])):
            if self.check_end(val,(row + ydir,col + xdir),ydir,xdir):
                self.flip_pieces(val,(row + ydir,col + xdir),ydir,xdir)

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        if self._side != len(grid):
            raise ValueError ("New gameboard size != old gameboard size")
        if not isinstance(turn, int) or turn > self._players:
            raise ValueError ("turn input must be an integer or the provided\
                              turn is greater than the number of players")
        newboard = Board(len(grid))
        nummoves = 0
        for i, row in enumerate(grid):
            for j, num in enumerate(row):
                if (not ((isinstance(num, int) and 0 < num <= self._players)
                         or num is None)):
                    raise ValueError ("one or more board pieces is not \
                                      an int or None")
                if num is not None:
                    newboard.add_piece(num,(i,j))
                    self._grid[i][j] = num
                    nummoves += 1

        self._board = newboard
        self._turn = turn
        if not self.available_moves:
            self.change_turn
        self._num_moves = nummoves

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        sim = deepcopy(self)
        for move in moves:
            row, col = move
            if not (0 <= row < self._side and 0 <= col < self._side):
                raise ValueError("Position is outside board limits")
            sim.apply_move(move)
        return sim

class Board():
    """
    Class to represent a game board.

    Attributes:
        side (int): number of cells on a side
        grid (list(list(Piece))): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    side: int
    grid: List[List[Optional["Piece"]]]

    def __init__(self, side: int):
        self.side = side
        self.grid = [[None] * side for _ in range(side)]

    def add_piece(self, val: int, location: Tuple[int, int]) -> bool:
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        row, col = location

        if self.grid[row][col] is None:
            self.grid[row][col] = Piece(val)
            return True
        return False

    @property
    def is_full(self) -> bool:
        '''
        Determines whether a board is full
        '''
        for row in self.grid:
            if None in row:
                return False

        return True

class Piece():
    '''
    Class to represent a game piece

    Attributes:
        value (int): the number corresponding to the player

    Methods:
        None
    '''
    value: int
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"
