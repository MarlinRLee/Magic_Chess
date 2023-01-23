import random
from magic.pyclass.Card import Card
from chess.pyclass.Moves import Destroy_Attack

class Destroy_piece(Card):
    def __init__(self, Hand, Name, MV):
        #summon_name = to_summon.__class__.__name__
        text_box = "destroy non king"
        super().__init__(Hand, Name, MV, "destroy.png", text_box)
        #self.Move = Move
        self.added_attacks.append(Destroy_Attack)

    def move_piece(self, square, piece):
        #augment piece
        piece.remove()
        super().move_piece(square)