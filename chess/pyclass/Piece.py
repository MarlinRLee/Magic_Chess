import pygame
from text_wrap import drawTextAdjust
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self, x: int, y: int, color: str, board, name: str, MV: str = "0", 
                 type: str = "", subtype: str = "", Text_Box: str = "Default"):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.isLand = type == "Land"
        self.name = name
        self.MV = MV
        self.type = type
        self.subtype = subtype
        self.Text_Box = Text_Box

        imgName = ""
        if type in ("Piece", "Land"):
            imgName = subtype.split()[0] + ".png"
        else:
            imgName = type.split()[0] + ".png"
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + imgName)
        try:
            self.img = pygame.image.load(img_path)
        except:
            self.img = pygame.Surface((10, 10))
            self.img.fill((255, 255, 255))
    
    #moves the piece and handle all the acounting
    def move_piece(self, square: Square):
        self.move(square.board, square.x, square.y)
    
    #change the location of the Piece on the Board
    def move(self, board, x: int, y: int) -> None:
        if self.isLand:
            self.board.squares[self.x][self.y].occupying_Land = None
        else:
            self.board.squares[self.x][self.y].occupying_piece = None
        old_x = self.x
        old_y = self.y
        old_board = self.board
        self.x = x
        self.y = y
        
        target_square = board.squares[x][y]
        if old_board.isHand and board.isHand:
            if target_square.occupying_Land != None:
                target_square.occupying_Land.move(old_board, old_x, old_y)
            elif target_square.occupying_piece != None:
                target_square.occupying_piece.move(old_board, old_x, old_y)
        if self.isLand:
            target_square.occupying_Land = self
        else:
            target_square.occupying_piece = self
        self.board = board


    #flag the square the piece is on for highlighting
    def set_highlight(self, default: str = "None") -> None:
        (self.board.squares[self.x][self.y]).set_highlight(default)

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
                
    def Blank_draw(self, display, rect):
        Small_rect = rect.scale_by(.9)
        Small_rect.center = rect.center
        pygame.draw.rect(display, (200, 200, 200), 
                         Small_rect)
        return Small_rect
    
    def simi_detailed_draw(self, display, rect):
        #draw inner shape
        Small_rect = self.Blank_draw(display, rect)
        
        
        #blitz topbar
        Top_Rect = pygame.Rect(0,0, self.board.tile_width, self.board.tile_height // 5)
        Top_Rect.topleft = Small_rect.topleft
        top_bar = self.name + " " + self.MV
        drawTextAdjust(display, top_bar, (0,0,0), Top_Rect)
        img_rect = pygame.Rect(Small_rect)
        img_rect.center = (Small_rect.center[0], Small_rect.center[1] + self.board.tile_height / 8)
        self.draw(display, img_rect,
                  self.board.tile_width // 1.5, self.board.tile_height // 2)
        
    def detailed_draw(self, display, rect):
        #draw inner shape
        Small_rect = rect.scale_by(.9)
        Small_rect.center = rect.center
        pygame.draw.rect(display, (200, 200, 200), 
                         Small_rect) 
               
        #Bliz img
        img_rect = pygame.Rect(Small_rect)
        img_rect.center = (Small_rect.center[0], Small_rect.center[1] - self.board.tile_height / 5)
        self.draw(display, img_rect,
                  self.board.tile_width // 2, self.board.tile_height // 4)
    
        #blitz topbar
        Top_Rect = pygame.Rect(0,0, Small_rect.width, Small_rect.height // 10)
        Top_Rect.topleft = (Small_rect.topleft[0], Small_rect.topleft[1])
        top_bar = self.name + " " + self.MV
        drawTextAdjust(display, top_bar, (0,0,0), Top_Rect)
        pygame.draw.line(display, (0, 0, 0), Top_Rect.bottomleft, Top_Rect.bottomright)
        
        #blitz textbox
        Bot_Rect = pygame.Rect(0,0, Small_rect.width, Small_rect.height // 2.2)
        Bot_Rect.bottomright = (Small_rect.bottomright[0], Small_rect.bottomright[1])
        drawTextAdjust(display, self.Text_Box, (0,0,0), Bot_Rect)
        pygame.draw.line(display, (0, 0, 0), Bot_Rect.topleft, Bot_Rect.topright)
        
        
        #blitz Type_Rect
        Type_Rect = pygame.Rect(0,0, Small_rect.width, Small_rect.height // 10)
        Type_Rect.bottomleft = (Bot_Rect.topleft[0], Bot_Rect.topleft[1])
        Type_bar = self.type + "  ---  " + self.subtype
        drawTextAdjust(display, Type_bar, (0,0,0), Type_Rect)
        
        pygame.draw.line(display, (0, 0, 0), Type_Rect.bottomleft, Type_Rect.bottomright)