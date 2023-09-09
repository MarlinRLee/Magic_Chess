# Game state checker
from chess.pyclass.Square import Square
from chess.pyclass.Piece import Piece

class Board:
    def __init__(self, board_size, off_Set, game, size_x = 8, size_y = 8, colors = None):

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

        self.squares = self.generate_squares(colors)

    def generate_squares(self, colors):
        output = []
        for x in range(self.size_x):
            output.append([])
            for y in range(self.size_y):
                output[x].append(
                    Square(x, y, self.tile_width, self.tile_height, self.offset, self, colors)
                )
        return output

    def setup_board(self):
        for color, row in [("White", 0), ("Black", self.size_y - 1)]:
            self.squares[self.size_y//2][row].occupying_piece = Piece(self.size_x//2, row, color, 
                                                                    self, "K")

    def inbound(self,x,y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def pix_to_cord(self, pix_pos):
        pix_x, pix_y = pix_pos
        x = (pix_x - self.offset[0]) // self.tile_width
        y = (pix_y - self.offset[1]) // self.tile_height
        return int(x), int(y)

    def handle_click(self, click_pos):
        x, y = self.pix_to_cord(click_pos)
        if not self.inbound(x, y): return None
        clicked_square = self.squares[x][y]
        #may be None
        clicked_piece = clicked_square.occupying_piece
        if (clicked_piece is not None and 
            self.game.selected_piece is None):
            self.game.selected_piece = clicked_piece
            return None
        if self.game.selected_piece is None:
            return None
        self.game.selected_piece.move_piece(clicked_square)
        return None

    def draw(self, display):
        for square_row in self.squares:
            for square in square_row:
                square.draw(display)
                
    def Hand_draw(self, display):
        for square_row in self.squares:
            for square in square_row:
                square.draw_Card(display)
                
    def Draw_Select(self, display):
        s_piece = self.game.selected_piece
        self.squares[0][0].occupying_piece = s_piece
        self.squares[0][0].draw_Card(display)
        
    def add(self, Piece):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if(self.squares[x][y].occupying_piece == None):
                    self.squares[x][y].occupying_piece = Piece
                    Piece.x = x
                    Piece.y = y
                    return
        raise Exception("Board is full")