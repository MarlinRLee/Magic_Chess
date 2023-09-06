import pygame
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self,x: int, y: int, color: str, Board, name: str):
        self.x = x
        self.y = y
        self.color = color
        self.Board = Board
        self.name = name
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + color + '_'+ name + '.png')
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (3 * Board.tile_width // 4, 3 * Board.tile_height // 4))

    #change the location of the Piece on the Board
    def move(self, Board, x: int, y: int) -> None:
        self.Board.squares[self.x][self.y].occupying_piece = None
        self.x = x
        self.y = y
        self.Board = Board
        self.Board.squares[x][y].occupying_piece = self
        self.Board.game.selected_piece = None

    #flag the square the piece is on for highlighting
    def set_highlight(self, default: bool = True) -> None:
        (self.Board.squares[self.x][self.y]).set_highlight(default)

    #moves the piece and handle all the acounting
    def move_piece(self, square: Square):
        self.move(square.Board, square.x, square.y)
