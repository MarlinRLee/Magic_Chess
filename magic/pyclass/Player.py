# /* Player.py
import random
import pygame

from chess.pyclass.Board import Board
from chess.pyclass.Piece import Piece
#Player
class Player:
    def __init__(self, color, card_size, off_set, game, Hand_size, LibraryName):
        
        self.Library_bounds = [[off_set[0], off_set[0] + card_size[0] * 1.25], 
                                [off_set[1], off_set[1] + card_size[1]]]
        Hand_offset = [off_set[0] + 1.5 * card_size[0], off_set[1]]
        Hand_dim = [Hand_size * card_size[0], card_size[1]] 
         
        self.bounds = [[off_set[0], off_set[0] + 1.5 * card_size[0] + Hand_dim[0]],
                       [off_set[1], off_set[1] + card_size[1]]]

        self.Hand = Board(Hand_dim, Hand_offset, game, size_x = Hand_size, size_y = 1,
                            colors = [(220, 208, 194), (220, 208, 194), (100, 249, 83), (100, 249, 83)])
        self.color = color
        self.game = game
        self.Library = self.init_Lib(LibraryName, self.Hand)
        self.LibRect = pygame.Rect(
            self.Library_bounds[0][0],
            self.Library_bounds[1][0],
            card_size[0] * 1.25,
            card_size[1])
        pygame.font.init()
        text_font = pygame.font.SysFont('times new roman', 15)
        self.LibText = text_font.render('Draw', False, (0, 0, 0))

        
    def handle_click(self, click_pos):
        if self.game.inbound(click_pos, self.Hand.bounds):
            self.Hand.handle_click(click_pos)
            return None
        if self.game.inbound(click_pos, self.Library_bounds):
            self.draw_lib()
            return None
        self.game.selected_piece = None
        return None
        
    def init_Lib(self, LibraryName, board):
        deck = []
        with open(LibraryName) as file:
            for line in file:
                lineArray = line.split()
                Name, MV, Type, Text_Box = lineArray
                deck.append(Piece(0, 0, self.color, board, Name, MV, Type, Text_Box))
        return deck
        
    def suffle(self):
        random.shuffle(self.Library)
        
    def draw_lib(self):
        if len(self.Library) != 0:
            self.Hand.add(self.Library.pop())
        
    def draw(self, display):
        self.Hand.draw(display)
        
        #draw library
        pygame.draw.rect(display, (128, 64, 0), self.LibRect)
        display.blit(self.LibText, self.LibRect.topleft)