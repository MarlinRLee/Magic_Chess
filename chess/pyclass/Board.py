import pygame
import random

# Game state checker
from chess.pyclass.Square import Square
from chess.pyclass.Pawn import Pawn
from chess.pyclass.Basic_units import Knight, Rook, Bishop, Queen
from chess.pyclass.King import King
from magic.pyclass.Card import Card

class Board:
    def __init__(self, board_size, off_Set, game, size = 8):

        self.game = game

        x_offset, y_offset = off_Set
        width, height = board_size
        self.bounds = [[x_offset, x_offset + width], 
                        [y_offset, y_offset + height]]

        self.size = size
        self.offset = (x_offset, y_offset)
        self.height = height
        self.tile_width = width // size
        self.tile_height = height // size

        self.squares = self.generate_squares()
        self.History = [[None]]
        
        self.setup_board()

    def generate_squares(self):
        output = []
        for x in range(self.size):
            output.append([])
            for y in range(self.size):
                output[x].append(
                    Square(x, y, self.tile_width, self.tile_height, self.offset)
                )
        return output

    def setup_board(self):
        for color, row in [("White", 0), ("Black", self.size - 1)]:
            for x in range(self.size):
                if x == self.size//2:
                    self.squares[x][row].occupying_piece = King(x, row, color, self)
                else:
                    classes = (Knight, Rook, Bishop, Queen)
                    #self.squares[x][row].occupying_piece = random.choice(classes)(x, row, color, self)
        for color, row in [("White", 1), ("Black", self.size - 2)]:
            for x in range(self.size):
                self.squares[x][row].occupying_piece = Pawn(x, row, color, self)#Pawn

    def inbound(self,x,y):
        return 0 <= x < self.size and 0 <= y < self.size

    def pix_to_cord(self, pix_pos):
        pix_x, pix_y = pix_pos
        x = (pix_x - self.offset[0]) // self.tile_width
        y = (pix_y - self.offset[1]) // self.tile_height
        return x, y

    def handle_click(self, click_pos):
        x, y = self.pix_to_cord(click_pos)
        if not self.inbound(x, y): return None
        square_bound = self.squares[x][y]
        self.act(square_bound)

    def act(self, clicked_square):
        #may be None
        clicked_piece = clicked_square.occupying_piece
        card_to_cast = (isinstance(self.game.selected_piece, Card))
        if (clicked_piece is not None and 
            clicked_piece.color == self.game.turn and
            not card_to_cast):
            self.game.selected_piece = clicked_piece

        if self.game.selected_piece is None:
            return None

        to_move_piece = self.game.selected_piece
        for square in to_move_piece.move_options():
            if square is clicked_square:
                to_move_piece.move_piece(clicked_square)
                return None
            
        for square, piece in to_move_piece.attack_options():
            if square is clicked_square:
                to_move_piece.move_piece(clicked_square, piece)
                return None
        return None

    def draw(self, display):
        for square_row in self.squares:
            for square in square_row:
                square.draw(display)