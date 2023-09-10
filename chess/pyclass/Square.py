# /* Square.py
import pygame

# Tile creator
class Square:
    def __init__(self, x, y, width, height, offset, board, colors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board  = board
        self.color = 'White' if (x + y) % 2 == 0 else 'Black'
        self.occupying_piece = None
        self.occupying_Land = None
        
        if colors is None:
            colors = [(220, 208, 194), (53, 53, 53), (100, 249, 83), (0, 228, 10)]
        
        white_color, black_color, high_white, high_black = colors
        self.draw_color = white_color if self.color == 'White' else black_color
        self.highlight_color = high_white if self.color == 'White' else high_black
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(
            x * width + offset[0],
            y * height + offset[1],
            self.width,
            self.height)

    # get the formal notation of the tile
    def get_coord(self):
        columns = 'abcdefghijklmnopqrstuvwxyz'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display, detailed = False):
        color = self.highlight_color if self.highlight else self.draw_color
        pygame.draw.rect(display, color, self.rect)
        if self.occupying_Land != None:
            if detailed:
                self.occupying_Land.detailed_draw(display, self.rect.center)
            else:
                self.occupying_Land.draw(display, self.rect.center)
        # adds the chess piece icons
        if self.occupying_piece != None:
            if detailed:
                self.occupying_piece.detailed_draw(display, self.rect.center)
            else:
                self.occupying_piece.draw(display, self.rect.center)
        self.highlight = False
        
    def set_highlight(self, default = True):
        self.highlight = default