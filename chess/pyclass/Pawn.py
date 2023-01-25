from chess.pyclass.Piece import Piece
from chess.pyclass.Square import Square
from chess.pyclass.Basic_units import Knight, Rook, Bishop, Queen
from chess.pyclass.Moves import Pawn_Move, Pawn_Attack

class Pawn(Piece):
    def __init__(self, x, y, color, board, has_moved = False, dead = False):
        super().__init__(x, y, color, board, "P", has_moved, dead)
        self.added_moves.append(Pawn_Move)
        self.added_attacks.append(Pawn_Attack)

    def move(self, x, y):
        super().move(x, y)
        if y == 0 or y == self.board.size - 1:
            print("promote enter name of upgraded piece")
            upgrade = "Q" #input()
            self.promote(upgrade)

    def promote(self, name):
        Queen_img_info = Queen(0, 0, self.color, self.board)
        self.__class__ = Queen
        self.name = name
        self.img = Queen_img_info.img