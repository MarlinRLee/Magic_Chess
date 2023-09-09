# /* Card.py
import pygame
import os

# Tile creator
class Card:#.__class__.__name__
    def __init__(self, hand, Name, mv, pix, Text_Box):
        self.Name = Name
        self.mv = mv
        self.Board = hand.game.Board
        self.hand = hand
        self.team_color = hand.color

        self.highlight = False
        self.highlight_color = (100, 249, 83)

        self.added_moves = []
        self.added_attacks = []
        self.added_rules = []
        self.front_img = self.init_front_img(self.hand.card_width, self.hand.height,
                                                            Name, mv, pix, Text_Box)
        self.back_img = self.init_back_img(self.hand.card_width, self.hand.height)

    def init_back_img(self, card_width, height):
        draw_obj = []
        bliz_obj = []
        Boarder_color = (150, 75, 0)
        Boarder = pygame.Rect(
            (card_width//42),
            (height//48),
            card_width - (card_width//21),
            height - (height//24))
        draw_obj.append([Boarder_color, Boarder])
        return (draw_obj, bliz_obj)



    def init_front_img(self, card_width, height, Name, mv, pix, Text_Box):
        draw_obj = []
        bliz_obj = []
        #Boarder plot
        Boarder_color = (150, 75, 0)
        Boarder = pygame.Rect(
            (card_width//42),
            (height//48),
            card_width - (card_width//21),
            height - (height//24))
        draw_obj.append([Boarder_color, Boarder])

        #main rect
        inside_color = (255, 0, 0)
        temp = pygame.Rect(
            (card_width//21),
            (height//24),
            card_width - (card_width // 10.5),
            height - (height//12))
        draw_obj.append([inside_color, temp])

        #Name box
        title_box_color = (200, 200, 200)
        title_box = pygame.Rect(
            (card_width // 14),
            (height // 20),
            card_width - (card_width // 7),
            height // 10)
        draw_obj.append([title_box_color, title_box])


        #text rect
        inside_color = (150, 150, 150)
        text_rect = pygame.Rect(
            (card_width//21),
            15*(height//24),
            card_width - (card_width // 10.5),
            height - 2*(height//3))
        draw_obj.append([inside_color, text_rect])

        #plot image
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, '..\\imgs\\' + pix)
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (5*card_width//6, height//3))
        centering_rect = img.get_rect()
        centering_rect.center = (draw_obj[0][1]).center
        X, Y = centering_rect.topleft
        Y = Y - (height * .1)
        bliz_obj.append([img, (X, Y)])

        #Text Name
        text = self.hand.game.font.render(Name, True, (0,0,0), None)
        X, Y = title_box.topleft
        Y = Y
        bliz_obj.append([text, (X, Y)])
        #Text MV
        text = self.hand.game.font.render(str(mv), True, (0,0,0), None)
        X, Y = title_box.topright
        X = X - text.get_width()
        bliz_obj.append([text, (X, Y)])
        
        #Text box 
        text = self.hand.game.box_font.render(Text_Box, True, (0,0,0), None)
        X, Y = text_rect.center
        X = X  - text.get_width()//2
        bliz_obj.append([text, (X, Y)])
        return (draw_obj, bliz_obj)



    def act(self, game):
        game.selected_piece = self
        game.Hands[2].cards[0] = self
        pass

    def set_highlight(self,):
        self.highlight = True

    def move_piece(self, square):
        self.Board.game.selected_piece = None
        self.hand.cards.remove(self)

    def draw(self, display, Card_num = None):
        self.draw_gen(display, self.front_img, Card_num)
        #self.draw_gen(display, self.back_img, Card_num)

    def draw_gen(self, display, schemea, Card_num = None):
        draw_obj, bliz_obj = schemea
        x_offset = self.hand.offset[0] + Card_num * self.hand.card_width
        y_offset = self.hand.offset[1]
        #draw base shape and handle highlight
        color, Top_shape = draw_obj[0]
        if self.highlight:
            color = self.highlight
            self.highlight = False
        pygame.draw.rect(display, color, Top_shape.move(x_offset, y_offset))

        #draw all the other shapes
        for color, shape in draw_obj[1:]:
                pygame.draw.rect(display, color, shape.move(x_offset, y_offset))
        
        #draw non shapes
        for img, offset in bliz_obj:
            X, Y = offset
            X += x_offset
            Y += y_offset
            display.blit(img, (X, Y))