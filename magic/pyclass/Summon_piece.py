from magic.pyclass.Card import Card
from chess.pyclass.Moves import Summon_move

class Summon_piece(Card):
    def __init__(self, Hand, Name, MV, to_summon):
        summon_name = to_summon(0, 0, "White", Hand.game.game_objects[0], dead = True).name
        text_box = "Summon " + summon_name
        super().__init__(Hand, Name, MV, "Summon.png", text_box)
        self.to_summon = to_summon
        self.added_moves.append(Summon_move)

    def move_piece(self, square):
        new_piece = (self.to_summon)(square.x, square.y, self.team_color, self.board)
        square.occupying_piece = new_piece
        super().move_piece(square)
