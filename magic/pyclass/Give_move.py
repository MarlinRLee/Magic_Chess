import random
from magic.pyclass.Card import Card
from chess.pyclass.Moves import Promotion_Attack

class Give_move(Card):
    def __init__(self, Hand, Name, MV, Func, is_attack):
        #summon_name = to_summon.__class__.__name__
        text_box = "Give " + Func.__name__ 
        super().__init__(Hand, Name, MV, "upgrade.png", text_box)
        #self.Move = Move
        self.added_attacks.append(Promotion_Attack)
        self.Func = Func 
        self.add_attack = is_attack

    def move_piece(self, square, piece):
        #augment piece
        if self.add_attack:
            piece.added_attacks.append(self.Func)
        else:
            piece.added_moves.append(self.Func)
        super().move_piece(square)