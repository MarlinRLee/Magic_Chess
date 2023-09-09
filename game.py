import pygame
from chess.pyclass.Board import Board
from magic.pyclass.Player import Player

class game():
    def __init__(self, window_size: int, num_squares: int = 8, num_cards: int = 7):
        self.font = pygame.font.Font('freesansbold.ttf', 8)
        self.box_font = self.font
        self.selected_piece = None
        self.Board = None
        self.Players = []
        self.life = [0, 0]
        self.gen_game(window_size, num_squares, num_cards)

    def gen_game(self, window_size: int, num_squares: int, num_cards: int):
        """creates the Board object and the two hand objects needed for a normal game"""
        X, Y = window_size
        
        #Create Board
        Board_dim = (3 * X // 5, 3 * Y // 5)
        Board_offset = (X // 3,  7 * Y // 40) #Do math to put Board between hands
        self.Board = Board(Board_dim, Board_offset, self,  num_squares)
        self.Board.setup_board()
        

        #Create opponents hand
        Player_dim = ((X*7) // 15, 2 * Y // 15)
        Player_offset = (240, 10)
        self.Players.append(Player("White", Player_dim, Player_offset, self, Hand_size = 7, LibraryName = "Test_Deck.txt"))
        
        #Create your hand
        Player_dim = (Player_dim[0] * 3 // 2, Player_dim[1] * 3 // 2)
        Player_offset = (150, Y - Player_offset[1] - Player_dim[1])#better calcs
        self.Players.append(Player("Black", Player_dim, Player_offset, self, Hand_size = 7, LibraryName = "Test_Deck.txt"))
        
        #Create CardViewer
        Player_dim = (Player_dim[0] // num_cards, Player_dim[1])
        Viewer_offset = (X / 10, 3 * Y / 5)
        self.Viewer = Board(Player_dim, Viewer_offset, self, size_x = 1, size_y = 1)
        
        stack_offset = (X / 10, 1 / 5 * Y)
        self.Stack = Board(Player_dim, stack_offset, self, size_x = 1, size_y = 1)
        #self.Hands[2].add_rand_card()
        #time.sleep(2)


    def handle_click(self, click_pos):
        if self.inbound(click_pos, self.Board.bounds):
                self.Board.handle_click(click_pos)
                return None
        for player in self.Players:
            if self.inbound(click_pos, player.bounds):
                player.handle_click(click_pos)
                return None
        #for Library in self.Librarys:
        #    if self.inbound(click_pos, Library.bounds):
        #        Library.handle_click(click_pos)
        #        return None
        if self.inbound(click_pos, self.Stack.bounds):
            self.Stack.handle_click(click_pos)
            return None
        game.selected_piece = None
        print("plz click inbound")
        return None
    
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])

    def draw(self, display):
        if self.selected_piece is not None:
            self.selected_piece.set_highlight()
        
        for player in self.Players:
            player.Hand.draw(display)
        
        self.Stack.draw(display)
        
        self.Viewer.Draw_Select(display)
        
        self.Board.draw(display)
