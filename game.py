import time
import pygame
from chess.pyclass.Board import Board
from magic.pyclass.Hand import Hand

class game():
    def __init__(self, window_size: int, num_squares: int = 8, num_cards: int = 7):
        self.font = pygame.font.Font('freesansbold.ttf', 8)
        self.box_font = self.font
        self.turn = 'White'
        self.selected_piece = None
        self.game_objects = []
        self.life = [0, 0]
        self.gen_game(window_size, num_squares, num_cards)

    def gen_game(self, window_size: int, num_squares: int, num_cards: int):
        """creates the board object and the two hand objects needed for a normal game"""
        X, Y = window_size
        board_dim = (X // 2, Y // 2)
        board_offset = (X // 3,  Y // 4)
        self.game_objects.append(Board(board_dim, board_offset, self,  num_squares))

        hand_dim = ((X*7)//10, Y // 5)
        hand_offset = (150, 10)
        self.game_objects.append(Hand(hand_dim, hand_offset, self, color = "White", hand_size = num_cards))
        hand_offset = (hand_offset[0], Y - hand_offset[1] - hand_dim[1])
        self.game_objects.append(Hand(hand_dim, hand_offset, self, color = "Black", hand_size = num_cards))

    def end_turn(self):
        self.selected_piece = None
        self.turn = 'White' if self.turn == 'Black' else 'Black'
        for Hand in self.game_objects[1:]:
            if Hand.color == self.turn:
                Hand.start_turn()
        #time.sleep(2)


    def handle_click(self, click_pos):
        for game in self.game_objects:
            if self.inbound(click_pos, game.bounds):
                game.handle_click(click_pos)
                return None
        print("plz click inbound")
        return None
    
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])

    def draw(self, display):
        if self.selected_piece is not None:
            self.selected_piece.set_highlight()

            for square in self.selected_piece.move_options():
                square.set_highlight()

            for square, piece in self.selected_piece.attack_options():
                square.set_highlight()
        
        for game in self.game_objects:
            game.draw(display)
