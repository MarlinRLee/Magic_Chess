# /* Player.py
import random
import pygame

from chess.pyclass.Board import Board
from chess.pyclass.Piece import Piece
#Player
class Player:
    def __init__(self, color, size, off_set, game, Hand_size, LibraryName):
        x_offset, y_offset = off_set
        width, height = size
        self.bounds = [[x_offset, x_offset + width], 
                                [y_offset, y_offset + height]]
        self.Hand = Board(size, off_set, game, size_x = Hand_size, size_y = 1,
                            colors = [(220, 208, 194), (220, 208, 194), (100, 249, 83), (100, 249, 83)])
        self.Library_bounds = [[x_offset, x_offset + width], 
                                [y_offset, y_offset + height]]
        self.color = color
        self.game = game
        self.Library = self.init_Lib(LibraryName, self.Hand)
        
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
        
    def draw(self):
        if len(self.Library) != 0:
            self.Hand.add(self.Library.pop())
        
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])
        
    def handle_click(self, click_pos):
        if self.inbound(click_pos, self.Hand.bounds):
            self.Hand.handle_click(click_pos)
            #return None
        if self.inbound(click_pos, self.Library_bounds):
            self.draw()
            return None
        self.game.selected_piece = None
        return None