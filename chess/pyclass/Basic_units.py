import pygame
import os
from chess.pyclass.Piece import Piece
#from chess.pyclass.Board import Board
from chess.pyclass.Moves import (Knight_Move, Knight_Attack,
                                Bishop_Move, Bishop_Attack,
                                Rook_Move, Rook_Attack)

#Creates the clasic Knight Piece from chess
class Knight(Piece):
    def __init__(self, x: int, y: int, color: str, board, has_moved: bool = False, dead: bool = False) -> Piece:
        super().__init__(x, y, color, board, "N", has_moved, dead)
        self.added_moves.append(Knight_Move)
        self.added_attacks.append(Knight_Attack)

#Creates the clasic Bishop Piece from chess
class Bishop(Piece):
    def __init__(self, x: int, y: int, color: str, board, has_moved: bool = False, dead: bool = False) -> Piece:
        super().__init__(x, y, color, board, "B", has_moved, dead)
        self.added_attacks.append(Bishop_Attack)
        self.added_moves.append(Bishop_Move)

#Creates the clasic Queen Piece from chess
class Queen(Piece):
    def __init__(self, x: int, y: int, color: str, board, has_moved: bool = False, dead: bool = False) -> Piece:
        super().__init__(x, y, color, board, "Q", has_moved, dead)
        self.added_moves.append(Rook_Move)
        self.added_moves.append(Bishop_Move)
        self.added_attacks.append(Rook_Attack)
        self.added_attacks.append(Bishop_Attack)

#Creates the clasic Rook Piece from chess
class Rook(Piece):
    def __init__(self, x: int, y: int, color: str, board, has_moved: bool = False, dead: bool = False) -> Piece:
        super().__init__(x, y, color, board, "R", has_moved, dead)
        self.added_moves.append(Rook_Move)
        self.added_attacks.append(Rook_Attack)
