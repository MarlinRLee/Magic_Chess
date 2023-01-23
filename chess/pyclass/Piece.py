import pygame
#from chess.pyclass.Board import Board
from chess.pyclass.Square import Square
import os

#creates a general Piece with no moves
class Piece:
    def __init__(self,x: int, y: int, color: str, board,
                         name: str, has_moved: bool = False, dead: bool = False):
        self.x = x
        self.y = y
        self.has_moved = has_moved
        self.dead = dead
        self.color = color
        self.board = board
        self.name = name

        self.added_moves = []
        self.added_attacks = []
        self.added_rules = []
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + color + '_'+ name + '.png')
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (3 * board.tile_width // 4, 3 * board.tile_height // 4))

    #change the location of the Piece on the board
    def move(self, x: int, y: int) -> None:
        self.board.squares[self.x][self.y].occupying_piece = None
        self.x = x
        self.y = y
        self.has_moved = True
        self.board.squares[x][y].occupying_piece = self

    #flag the square the piece is on for highlighting
    def set_highlight(self, default: bool = True) -> None:
        (self.board.squares[self.x][self.y]).set_highlight(default)

    def remove(self) -> None:
        """handle special behavior of removed units. currently only kings have special behvior"""
        self.dead = True
        self.board.squares[self.x][self.y].occupying_piece = None

    #get list of moves the piece can make
    def move_options(self):
        options = []
        for move_funcs in self.added_moves:
            options += move_funcs(self)
        return options

    #get list of attacks the piece can make
    def attack_options(self):
        options = []
        for attack_func in self.added_attacks:
            options += attack_func(self)
        return options

    #moves the piece and handle all the acounting
    def move_piece(self, square: Square, cap_piece = None):
        #add to the history log
        start_square = self.board.squares[self.x][self.y]
        move = (self.name, [start_square.x, start_square.y], [square.x, square.y])
        self.board.History.append(move)

        #remove dead piece
        if cap_piece is not None:
            cap_piece.remove()
        
        #move the piece and end the turn
        self.move(square.x, square.y)
        self.board.game.end_turn()
