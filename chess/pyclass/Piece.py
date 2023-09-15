import pygame
from TEXTWRAP import drawTextAdjust
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self, x: int, y: int, color: str, board, name: str, MV: str = "0", 
                 type: str = "", Text_Box: str = "Default",
                 imgName: str = ""):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.isLand = type == "Land"
        self.name = name
        self.MV = MV
        self.type = type
        self.Text_Box = Text_Box
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + imgName)
        self.img = pygame.image.load(img_path)
    
    def copy(toCopyPiece):
        newPiece = Piece(toCopyPiece.x,toCopyPiece.y,toCopyPiece.color,toCopyPiece.board,
                         toCopyPiece.name, toCopyPiece.MV, toCopyPiece.type, toCopyPiece.Text_Box,
                         "../MTG_Art/doom_blade.jpg")
        return newPiece

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

    def draw(self, display, rect, width = None, height = None):
        if width is None:
            width = 3 * self.board.tile_width // 4
        if height is None:
            height = 3 * self.board.tile_height // 4
        Drawimg = pygame.transform.scale(self.img, (width, height))
        if(self.color == "White"):
            Drawimg = pygame.transform.flip(Drawimg, True, True)
        centering_rect = Drawimg.get_rect()
        centering_rect.center = rect.center
        display.blit(Drawimg, centering_rect.topleft)
        
    def simi_detailed_draw(self, display, rect):
        #blitz topbar
        Top_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 5)
        Top_Rect.topleft = rect.topleft
        top_bar = self.name + " " + self.MV
        drawTextAdjust(display, top_bar, (0,0,0), Top_Rect)
        img_rect = pygame.Rect(rect)
        img_rect.center = (rect.center[0], rect.center[1] + self.board.tile_height / 4)
        self.draw(display, img_rect,
                  self.board.tile_width // 2, self.board.tile_height // 4)
        
    def detailed_draw(self, display, rect):        
        #Bliz img
        img_rect = pygame.Rect(rect)
        img_rect.center = (rect.center[0], rect.center[1] - self.board.tile_height / 5)
        self.draw(display, img_rect,
                  self.board.tile_width // 2, self.board.tile_height // 4)
    
        #blitz topbar
        Top_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 10)
        Top_Rect.topleft = (rect.topleft[0], rect.topleft[1])
        top_bar = self.name + " " + self.MV
        drawTextAdjust(display, top_bar, (0,0,0), Top_Rect)
        
        #blitz textbox
        Bot_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 2)
        Bot_Rect.center = (rect.center[0], rect.center[1] + 30)
        drawTextAdjust(display, self.Text_Box, (0,0,0), Bot_Rect)