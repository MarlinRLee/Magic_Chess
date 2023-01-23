# /* Hand.py
import pygame
import random

from magic.pyclass.Summon_piece import Summon_piece
from magic.pyclass.Give_move import Give_move
from chess.pyclass.Pawn import Pawn
from chess.pyclass.Basic_units import Knight, Rook, Bishop, Queen

from chess.pyclass.Moves import (Bishop_Move, Bishop_Attack, King_Move, King_Attack,
                                Knight_Move, Knight_Attack, Pawn_Move, Pawn_Attack,
                                Rook_Attack, Rook_Move) 

# Tile creator
class Hand:
    def __init__(self, hand_dim, offset, game, color, hand_size = 7):
        self.game = game

        self.color = color
        self.hand_size = hand_size
        self.max_mv = 0
        self.mv = self.max_mv



        self.draw_color = (255, 255, 255)
        self.width, self.height = hand_dim#height
        self.bounds = [[offset[0], offset[0] + self.width],
                       [offset[1], offset[1] + self.height]]
        self.card_width = (hand_dim[0]) // hand_size
        self.offset = offset
        self.cards = []
        self.rect = pygame.Rect(
                                offset[0],
                                offset[1],
                                hand_dim[0],
                                hand_dim[1])
        self.add_rand_card()
        self.add_rand_card()

    def pix_to_cord(self, pix_pos):
        pix_x, pix_y = pix_pos
        x = (pix_x - self.offset[0]) // self.card_width
        return x

    def handle_click(self, click_pos):
        x = self.pix_to_cord(click_pos)
        if self.game.turn == self.color and x < len(self.cards):
            card = self.cards[x]
            self.act(card)

    def act(self, card):
        if self.mv >= card.mv:
            card.act(self.game)

    def add_rand_card(self):
        #Give_move
        #Summon_piece
        summon_card = bool(random.getrandbits(1))
        if summon_card:
            MV, gen_class = random.choice(((3, Knight), (5, Rook), (3, Bishop), (9, Queen)))
            new_card = Summon_piece(self, "Create Unit", MV, gen_class)
        else:
            add_Attack = bool(random.getrandbits(1))
            if add_Attack:
                MV, attack_add = random.choice(((4, Bishop_Attack), (2, King_Attack), 
                                                (3, Knight_Attack), (3, Pawn_Attack),
                                                (4, Rook_Attack)))
                new_card = Give_move(self, "Upgrade Unit", MV, attack_add, True)
            else:
                MV, move_add = random.choice(((7, Bishop_Move), (3, King_Move), 
                                                (5, Knight_Move), (1, Pawn_Move),
                                                (8, Rook_Move)))
                new_card = Give_move(self, "Upgrade Unit", MV, move_add, False)
        self.cards.append(new_card)

    def start_turn(self):
        self.max_mv += 1
        self.mv = self.max_mv
        print(self.mv)
        if len(self.cards) < self.hand_size:
            self.add_rand_card()

    def draw(self, display):
        pygame.draw.rect(display, self.draw_color, self.rect)
        MV_text = "Mana: " + str(self.mv) + "/" + str(self.max_mv)
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(MV_text,True,  (255, 255, 255))
        display.blit(text, (50, self.offset[1]))
        for i, card in enumerate(self.cards):
            card.draw(display, i)