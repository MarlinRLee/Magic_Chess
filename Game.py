from functools import reduce
import tkinter
import tkinter.filedialog
import pygame
from chess.pyclass.Board import Board
from chess.pyclass.Piece import Piece
from chess.pyclass.Player import Player

from Network import Network

class Game:
    def __init__(self, window_size: int, num_squares: int = 8, num_cards: int = 7):
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.selected_piece = None
        self.op_selected_piece = None
        self.Players = []
        self.net = Network()
        self.gen_game(window_size, num_squares, num_cards)

    def gen_game(self, window_size: int, num_squares: int, num_cards: int):
        """creates the Board object and the two Hand objects needed for a normal game"""
        X, Y = window_size
        #Create Board
        Board_dim = (3 * X // 5, 3 * Y // 5)
        Board_offset = (X // 3,  7 * Y // 40) #Do math to put Board between Hands
        self.Board = Board(Board_dim, Board_offset, self,  num_squares)
        self.Board.setup_board()
        
        Card_dim = (X // 10, Y // 5)
        #Create your Hand
        Player_offset = (X / 8, Y - Card_dim[1] - .01 * Y)#better calcs
        deckFile = self.prompt_file()
        deckFile = "Test_Deck.txt"
        self.Players.append(Player("Black", Card_dim, Player_offset, self, Hand_size = num_cards, 
                                   LibraryName = deckFile))
        
        #Create opponents Hand
        Small_Card_dim = (Card_dim[0] * 3 / 4, Card_dim[1] * 3 / 4)
        Player_offset = (1 * X / 3, .01 * Y)
        #deckFile = self.prompt_file()
        deckFile = "Test_Deck.txt"
        self.Players.append(Player("White",  Small_Card_dim, Player_offset, self, Hand_size = num_cards, 
                                   LibraryName = None))
        
     
        #Create CardViewer
        Viewer_dim = (Card_dim[0] * 1.75, Card_dim[1] * 2.5)
        Viewer_offset = (X / 50, Y / 5)
        self.Viewer = Board(Viewer_dim, Viewer_offset, self, size_x = 1, size_y = 1)
        
        #Create stack
        stack_offset = (X / 4.5, Y / 5)
        Stack_dim = (Card_dim[0] *  .75, Card_dim[1] * 2)
        self.Stack = Board(Stack_dim, stack_offset, self, size_x = 1, size_y = 5)


    def handle_click(self, click_pos, internal = True):
        if (self.click_board(click_pos, "Main", self.Board, internal) or
            self.click_board(click_pos, "Stack", self.Stack, internal)):
            return None
            
        if self.inbound(click_pos, self.Players[0].bounds):
            self.Players[0].handle_click(click_pos, internal)
            return None

        if internal:
            self.selected_piece = None
            self.send(["Click", "None", -1, -1])
        else:
            self.op_selected_piece = None
        print("plz click inbound")
    
    def click_board(self, click_pos, Name, Board, internal):
        if self.inbound(click_pos, Board.bounds):
                x, y = Board.pix_to_cord(click_pos)
                Board.handle_click((x,y), internal)
                if internal:
                    if Name == "Main":
                        y = self.Board.size_x - y - 1
                        x = self.Board.size_y - x - 1
                    self.send(["Click", Name, str(x), str(y)])
                return True
        else:
            return False
    
    def handle_click_server(self, Name, X, Y):
        if Name == "Main":
            self.Board.handle_click((X, Y), internal = False)
        elif Name == "Stack":
            self.Stack.handle_click((X, Y), internal = False)
        elif Name == "Hand":
            self.Players[1].Hand.handle_click((X, Y), internal = False)
        else:
            self.op_selected_piece = None
    
    
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])

    def draw(self, display):
        display.fill((100, 100, 100))
        self.highlight_selected_pieces()
        for player in self.Players:
            player.draw(display, Hidden=player.color == "White")
        self.Stack.draw(display, detailed="Min")
        self.Viewer.Draw_Select(display)
        self.Board.draw(display)
        pygame.display.update()
        
    def highlight_selected_pieces(self):
        if self.selected_piece:
            self.selected_piece.set_highlight("Team")
        if self.op_selected_piece:
            self.op_selected_piece.set_highlight("Opp")
            
    def prompt_file(self):
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top)
        top.destroy()
        return file_name
 
    def run(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.process_events()
            self.update_server_messages()
            self.draw(screen)
            clock.tick(60)
            
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(pygame.mouse.get_pos())
                
    def update_server_messages(self):
        server_msg = ""
        while server_msg != "Noted":
            reply = self.send(["todo"])
            id, server_msg = reply.split("::")
            self.process_server_message(id, server_msg)
            
    
    def process_server_message(self, id, message):
        msg = message.split(",,,")
        match msg[0]:
            case "Click":
                name, x, y = msg[1:]
                self.handle_click_server(name, int(x), int(y))
            case "Draw":
                name, cost, type, subtype, text_box = msg[1:]
                to_draw_Player = self.Players[int(id) != int(self.net.id)]
                to_draw_Player.Hand.add(Piece(-1, -1, to_draw_Player.color, to_draw_Player.Hand,
                                              name, cost, type, subtype, text_box))
                
                
                
    def send(self, data_array):
        flat_data = reduce(lambda x, y: str(x) + ",,," + str(y), data_array)
        data = str(self.net.id) + "::" + flat_data
        return self.net.send(data)

    def parse_data(self, data):
        try:
            data_array = data.split("::")[1].split(",,")
            return (int(data_array[0]), int(data_array[1]))
        except:
            return (0, 0)