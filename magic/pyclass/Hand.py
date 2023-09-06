# /* Hand.py
import pygame
import random

# Tile creator
class Hand:
    def __init__(self, hand_dim, offset, game, color, hand_size = 7):
        self.game = game

        self.color = color
        self.hand_size = hand_size
        self.max_mv = 1
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

    def pix_to_cord(self, pix_pos):
        pix_x, pix_y = pix_pos
        x = (pix_x - self.offset[0]) // self.card_width
        return x

    def handle_click(self, click_pos):
        x = self.pix_to_cord(click_pos)
        if self.game.turn == self.color and x < len(self.cards):
            card = self.cards[x]
            self.act(card)

    def add_rand_card(self):
        return None

    def draw(self, display):
        #pygame.draw.rect(display, self.draw_color, self.rect)
        #MV_text = "Mana: " + str(self.mv) + "/" + str(self.max_mv)
        #font = pygame.font.Font('freesansbold.ttf', 20)
        #text = font.render(MV_text,True,  (255, 255, 255))
        #display.blit(text, (50, self.offset[1]))
        for i, card in enumerate(self.cards):
            card.draw(display, i)