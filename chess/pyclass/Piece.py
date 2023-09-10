import pygame
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self, x: int, y: int, color: str, board, name: str, MV: str = "0", 
                 type: str = "", Text_Box: str = "Default", isLand: bool = False,
                 imgName: str = ""):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.isLand = isLand
        self.name = name
        self.MV = MV
        self.type = type
        self.Text_Box = Text_Box
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + imgName)
        self.img = pygame.image.load(img_path)

    #change the location of the Piece on the Board
    def move(self, board, x: int, y: int) -> None:
        if self.isLand:
            self.board.squares[self.x][self.y].occupying_Land = None
        else:
            self.board.squares[self.x][self.y].occupying_piece = None
        self.x = x
        self.y = y
        self.board = board
        if self.isLand:
            self.board.squares[x][y].occupying_Land = self
        else:
            self.board.squares[x][y].occupying_piece = self


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
        
        Top_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 10)
        Bot_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 10)
        Drawimg = pygame.transform.scale(self.img, (2 * self.board.tile_width // 4, 1 * self.board.tile_height // 4))
        centering_rect = Drawimg.get_rect()
        centering_rect.center = (center[0], center[1] - self.board.tile_height / 5)
        Top_Rect.center = (center[0], center[1] - self.board.tile_height / 2.5)
        Bot_Rect.center = (center[0], center[1])
        display.blit(Drawimg, centering_rect.topleft)
        Name = self.board.game.font.render(self.name, True, (0,0,0), None)
        mv = self.board.game.font.render(self.MV, True, (0,0,0), None)
        textBox = self.board.game.font.render(self.Text_Box, True, (0,0,0), None)
        display.blit(Name, Top_Rect.topleft)
        display.blit(mv, (Top_Rect.topright[0] - self.board.tile_width / 3, Top_Rect.topright[1]))
        display.blit(textBox, Bot_Rect.topleft)