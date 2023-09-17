# Game state checker
from chess.pyclass.Square import Square
from chess.pyclass.Piece import Piece

class Board:
    def __init__(self, board_size, off_Set, game, size_x = 8, size_y = 8, 
                 colors = None, isHand = False):
        
        self.isHand = isHand

        self.game = game

        x_offset, y_offset = off_Set
        width, height = board_size
        self.bounds = [[x_offset, x_offset + width], 
                        [y_offset, y_offset + height]]

        self.size_x = size_x
        self.size_y = size_y
        self.offset = (x_offset, y_offset)
        self.height = height
        self.tile_width = width // size_x
        self.tile_height = height // size_y
        
        if colors is None:#white_color, black_color, high_white, high_black = colors
            colors = [[(155, 155, 194), (53, 53, 53)], 
                    [(155, 255, 194), (53, 153, 53)], 
                    [(255, 155, 194), (153, 53, 53)]]   
        
        self.Base_Color, self.Team_Highlight, self.Opp_Highlight = colors

        self.squares = self.generate_squares()

    def generate_squares(self):
        output = []
        for x in range(self.size_x):
            output.append([])
            for y in range(self.size_y):
                color = 'White' if (x + y) % 2 == 0 else 'Black'
                output[x].append(
                    Square(x, y, self.tile_width, self.tile_height, self.offset, self, color)
                )
        return output

    def inbound(self,x,y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def pix_to_cord(self, pix_pos):
        pix_x, pix_y = pix_pos
        x = (pix_x - self.offset[0]) // self.tile_width
        y = (pix_y - self.offset[1]) // self.tile_height
        return int(x), int(y)

    def handle_click(self, clicked, internal = True):
        x, y = clicked
        relPiece = self.game.selected_piece if internal else self.game.OpSelected_piece
        if not self.inbound(x, y): return None
        clicked_square = self.squares[x][y]
        #may be None
        clicked_piece = clicked_square.occupying_piece
        if clicked_piece is None:
            clicked_piece = clicked_square.occupying_Land
            
        if (clicked_piece is not None and relPiece is None):
            if internal:
                self.game.selected_piece = clicked_piece
                relPiece = clicked_piece
            else:
                self.game.OpSelected_piece = clicked_piece
                relPiece = clicked_piece
            return None
        
        if relPiece is None:
            return None
        
        relPiece.move_piece(clicked_square)
        if internal:
            self.game.selected_piece = None
        else:
            self.game.OpSelected_piece = None
        return None

    def draw(self, display, detailed = "Min"):
        for square_row in self.squares:
            for square in square_row:
                square.draw(display, detailed = detailed)
                
                
    def Draw_Select(self, display):
        s_piece = self.game.selected_piece
        if s_piece is not None:
            real_loc = s_piece.board
            s_piece.board = self
            self.squares[0][0].occupying_piece = s_piece
        self.squares[0][0].draw(display, detailed = "Full")
        if s_piece is not None:
            s_piece.board = real_loc
            self.squares[0][0].occupying_piece = None
        
    def add(self, Piece):
        for x in range(self.size_x):
            for y in range(self.size_y):
                cur_square = self.squares[x][y]
                if(cur_square.occupying_piece == None and cur_square.occupying_Land == None):
                    if Piece.isLand:
                        self.squares[x][y].occupying_Land = Piece
                    else:
                        self.squares[x][y].occupying_piece = Piece
                    Piece.x = x
                    Piece.y = y
                    return None
                
    def setup_board(self):
        self.squares[self.size_x//2][0].occupying_piece = Piece(self.size_x//2, 0, "White", 
                                                            self,"K", type = "Piece", subtype = "king")
        self.squares[self.size_x//2 - 1][self.size_y - 1].occupying_piece = Piece(self.size_x//2 - 1, self.size_y - 1, "Black", 
                                                            self,"K", type = "Piece", subtype = "king")