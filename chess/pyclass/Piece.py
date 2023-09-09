import pygame
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self, x: int, y: int, color: str, board, name: str, MV: str = "", type: str = "", Disc: str = ""):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.name = name
        self.MV = MV
        self.type = type
        self.Disc = Disc
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + color + '_'+ name + '.png')
        self.img = pygame.image.load(img_path)

    #change the location of the Piece on the Board
    def move(self, board, x: int, y: int) -> None:
        self.board.squares[self.x][self.y].occupying_piece = None
        self.x = x
        self.y = y
        self.board = board
        self.board.squares[x][y].occupying_piece = self
        self.board.game.selected_piece = None

    #flag the square the piece is on for highlighting
    def set_highlight(self, default: bool = True) -> None:
        (self.board.squares[self.x][self.y]).set_highlight(default)

    #moves the piece and handle all the acounting
    def move_piece(self, square: Square):
        self.move(square.board, square.x, square.y)

    def draw(self, display, center):
        Drawimg = pygame.transform.scale(self.img, (3 * self.board.tile_width // 4, 3 * self.board.tile_height // 4))
        centering_rect = Drawimg.get_rect()
        centering_rect.center = center
        display.blit(Drawimg, centering_rect.topleft)
        
    def detailed_draw(self, display, center):
        pass
        #Name = self.Board.game.font.render(self.name, True, (0,0,0), None)
        #MV = text = self.Board.game.font.render(self.mv, True, (0,0,0), None)