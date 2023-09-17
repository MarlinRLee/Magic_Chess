# /* Square.py
import pygame

# Tile creator
class Square:
    def __init__(self, x, y, width, height, offset, board, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board  = board
        self.color = color
        self.occupying_piece = None
        self.occupying_Land = None       
        
        self.highlight = "None"
        self.rect = pygame.Rect(
            x * width + offset[0],
            y * height + offset[1],
            self.width,
            self.height)

    def draw(self, display, detailed = "Min"):
        order = self.color != "White"

        match self.highlight:
            case "None":    
                color = self.board.Base_Color[order]
            case "Team":  
                color = self.board.Team_Highlight[order]
            case "Opp":
                color = self.board.Opp_Highlight[order]
        #Blank
        pygame.draw.rect(display, color, self.rect)
        for toDraw in [self.occupying_Land, self.occupying_piece]:
            if toDraw != None:
                match detailed:
                    case "Full":
                        toDraw.detailed_draw(display, self.rect)
                    case "Simi":
                        toDraw.simi_detailed_draw(display, self.rect)
                    case "Min":
                        toDraw.draw(display, self.rect)
                    case "Blank":
                        toDraw.Blank_draw(display, self.rect)
        self.highlight = "None"
        
    def set_highlight(self, default = "None"):
        self.highlight = default
        
    # get the formal notation of the tile
    #def get_coord(self):
    #    columns = 'abcdefghijklmnopqrstuvwxyz'
    #    return columns[self.x] + str(self.y + 1)