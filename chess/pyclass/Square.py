# /* Square.py
import pygame

# Tile creator
class Square:
    def __init__(self, x, y, width, height, offset, Board):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Board  = Board
        self.color = 'White' if (x + y) % 2 == 0 else 'Black'
        self.draw_color = (220, 208, 194) if self.color == 'White' else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == 'White' else (0, 228, 10)
        self.occupying_piece = None
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

    def draw(self, display):
        # configures if tile should be light or dark or highlighted tile
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)
            
        # adds the chess piece icons
        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
        self.highlight = False

    def set_highlight(self, default = True):
        self.highlight = default