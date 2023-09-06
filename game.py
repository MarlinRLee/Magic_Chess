import pygame
from chess.pyclass.Board import Board
from magic.pyclass.Hand import Hand

class game():
    def __init__(self, window_size: int, num_squares: int = 8, num_cards: int = 7):
        self.font = pygame.font.Font('freesansbold.ttf', 8)
        self.box_font = self.font
        self.turn = 'White'
        self.selected_piece = None
        self.Board = None
        self.Hands = []
        self.life = [0, 0]
        self.gen_game(window_size, num_squares, num_cards)

    def gen_game(self, window_size: int, num_squares: int, num_cards: int):
        """creates the board object and the two hand objects needed for a normal game"""
        X, Y = window_size
        
        #Create board
        board_dim = (3 * X // 5, 3 * Y // 5)
        board_offset = (X // 3,  7 * Y // 40) #Do math to put board between hands
        self.Board = Board(board_dim, board_offset, self,  num_squares)

        #Create opponents hand
        hand_dim = ((X*7) // 15, 2 * Y // 15)
        hand_offset = (240, 10)
        self.Hands.append(Hand(hand_dim, hand_offset, self, color = "White", hand_size = num_cards))
        
        #Create your hand
        hand_dim = (hand_dim[0] * 3 // 2, hand_dim[1] * 3 // 2)
        hand_offset = (150, Y - hand_offset[1] - hand_dim[1])
        self.Hands.append(Hand(hand_dim, hand_offset, self, color = "Black", hand_size = num_cards))
        
        #Draw both players starting cards
        for i in range(num_cards):
            for hand in self.Hands:
                hand.add_rand_card()
        
        
        #Create CardViewer
        hand_dim = (hand_dim[0] // 7, hand_dim[1])
        hand_offset = (X / 10, Y / 3)
        self.Hands.append(Hand(hand_dim, hand_offset, self, color = "Grey", hand_size = 1))
        self.Hands[2].add_rand_card()
        #time.sleep(2)


    def handle_click(self, click_pos):
        if self.inbound(click_pos, self.Board.bounds):
                self.Board.handle_click(click_pos)
                return None
        for hand in self.Hands:
            if self.inbound(click_pos, hand.bounds):
                hand.handle_click(click_pos)
                return None
        print("plz click inbound")
        return None
    
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])

    def draw(self, display):
        if self.selected_piece is not None:
            self.selected_piece.set_highlight()
        
        for hand in self.Hands:
            hand.draw(display)
        
        self.Board.draw(display)
