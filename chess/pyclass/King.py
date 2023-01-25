from chess.pyclass.Piece import Piece
from chess.pyclass.Moves import King_Move, King_Attack

class King(Piece):
    def __init__(self, x, y, color, board, has_moved = False, dead = False):
        super().__init__(x, y, color, board, "K", has_moved, dead)
        if not dead:
            life_loc = 0 if self.color == 'White' else 1
            board.game.life[life_loc] += 1
        self.added_moves.append(King_Move)
        self.added_attacks.append(King_Attack)

    def remove(self):
        life_loc = 0 if self.color == 'White' else 1
        self.board.game.life[life_loc] -= 1
        super().remove()
