# /* Player.py
import xml.etree.ElementTree as ET
import random
import pygame

from chess.pyclass.Board import Board
from chess.pyclass.Piece import Piece
#Player
class Player:
    def __init__(self, color, card_size, off_set, game, Hand_size, LibraryName):
        
        self.Library_bounds = [[off_set[0], off_set[0] + card_size[0] * 1.25], 
                                [off_set[1], off_set[1] + card_size[1] * .5]]
        Hand_offset = [off_set[0] + 1.5 * card_size[0], off_set[1]]
        Hand_dim = [Hand_size * card_size[0], card_size[1]] 
         
        self.bounds = [[off_set[0], off_set[0] + 1.5 * card_size[0] + Hand_dim[0]],
                       [off_set[1], off_set[1] + card_size[1]]]

        self.Hand = Board(Hand_dim, Hand_offset, game, size_x = Hand_size, size_y = 1,
                            colors = [[(220, 208, 194), (220, 208, 194)], 
                                      [(100, 249, 83), (100, 249, 83)], 
                                      [(249, 100, 83), (249, 100, 83)]],
                            isHand = True)
        self.color = color
        self.game = game
        self.Library = self.init_Lib(LibraryName)
        self.LibRect = pygame.Rect(
            self.Library_bounds[0][0],
            self.Library_bounds[1][0],
            self.Library_bounds[0][1] - self.Library_bounds[0][0],
            self.Library_bounds[1][1] - self.Library_bounds[1][0])
        pygame.font.init()
        text_font = pygame.font.SysFont('times new roman', 15)
        self.LibText = text_font.render('Click to Draw', False, (0, 0, 0))

        
    def handle_click(self, click_pos, internal = True):
        if self.game.click_board(click_pos, "Hand", self.Hand, internal):
            return None
        
        if self.game.inbound(click_pos, self.Library_bounds):
            self.game.send(["Draw", self.game.net.id])
            return None
        if internal:
            self.game.selected_piece = None
        else:
            self.game.OpSelected_piece = None
      
    def suffle(self):#TODO make it work from the server
        self.game.send(["Shuffle"])
        
        
    def draw(self, display, Hidden = False):
        if Hidden:
            card_show = "Blank"
        else:
            #draw library
            card_show = "Simi"
            pygame.draw.rect(display, (128, 64, 0), self.LibRect)
            display.blit(self.LibText, self.LibRect.midleft)
        self.Hand.draw(display, detailed = card_show)
        

        
    def init_Lib(self, LibraryName):    
        if LibraryName == None:
            return
        with open(LibraryName) as file:
            for line in file:
                num, Name = line.strip().split(",")
                #ask server for info based on on Name            
                self.game.send(["AddCard", int(num), Name.strip()])
        self.suffle()