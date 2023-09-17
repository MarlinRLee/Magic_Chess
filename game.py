from functools import reduce
import tkinter
import tkinter.filedialog
import pygame
from chess.pyclass.Board import Board
from chess.pyclass.Player import Player

from Network import Network

class game():
    def __init__(self, window_size: int, num_squares: int = 8, num_cards: int = 7):
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.box_font = self.font
        self.selected_piece = None
        self.Players = []
        self.net = Network()
        
        self.gen_game(window_size, num_squares, num_cards)

    def gen_game(self, window_size: int, num_squares: int, num_cards: int):
        """creates the Board object and the two hand objects needed for a normal game"""
        X, Y = window_size
        #Create Board
        Board_dim = (3 * X // 5, 3 * Y // 5)
        Board_offset = (X // 3,  7 * Y // 40) #Do math to put Board between hands
        self.Board = Board(Board_dim, Board_offset, self,  num_squares)
        self.Board.setup_board()
        
        Card_dim = (X // 10, Y // 5)
        #Create your hand
        Player_offset = (X / 8, Y - Card_dim[1] - .01 * Y)#better calcs
        #deckFile = self.prompt_file()
        deckFile = "Test_Deck.txt"
        self.Players.append(Player("Black", Card_dim, Player_offset, self, Hand_size = num_cards, 
                                   LibraryName = deckFile))
        
        #Create opponents hand
        Small_Card_dim = (Card_dim[0] * 3 / 4, Card_dim[1] * 3 / 4)
        Player_offset = (1 * X / 3, .01 * Y)
        #deckFile = self.prompt_file()
        deckFile = "Test_Deck.txt"
        self.Players.append(Player("White",  Small_Card_dim, Player_offset, self, Hand_size = num_cards, 
                                   LibraryName = deckFile))
        
     
        #Create CardViewer
        Viewer_dim = (Card_dim[0] * 1.75, Card_dim[1] * 2.5)
        Viewer_offset = (X / 50, Y / 5)
        self.Viewer = Board(Viewer_dim, Viewer_offset, self, size_x = 1, size_y = 1)
        
        #Create stack
        stack_offset = (X / 4.5, Y / 5)
        Stack_dim = (Card_dim[0] *  .75, Card_dim[1] * 2)
        self.Stack = Board(Stack_dim, stack_offset, self, size_x = 1, size_y = 5)


    def handle_click(self, click_pos):
        if self.inbound(click_pos, self.Board.bounds):
                self.Board.handle_click(click_pos)
                return None
        for player in self.Players:
            if self.inbound(click_pos, player.bounds):
                player.handle_click(click_pos)
                return None
        if self.inbound(click_pos, self.Stack.bounds):
            self.Stack.handle_click(click_pos)
            return None
        game.selected_piece = None
        print("plz click inbound")
        return None
    
    def inbound(self, click, bounds):
        return (bounds[0][0] <= click[0] <= bounds[0][1] and
                bounds[1][0] <= click[1] <= bounds[1][1])

    def draw(self, display):
        display.fill((100, 100, 100))
        if self.selected_piece is not None:
            self.selected_piece.set_highlight()
        
        for player in self.Players:
            player.draw(display)
        
        self.Stack.draw(display, detailed = "Min")
        
        self.Viewer.Draw_Select(display)
        
        self.Board.draw(display)
        pygame.display.update()
        
    def prompt_file(self):
        """Create a Tk file dialog and cleanup when finished"""
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfilename(parent=top)
        top.destroy()
        return file_name

    
    
    def run(self, screen):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            click_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Quit the game if the user presses the close button
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    # If the mouse is clicked
                    if event.button == 1:
                        self.send(["Click", str(click_pos[0]), str(click_pos[1])])
                        self.handle_click(click_pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.selected_piece = None   
                        
            serverMsg = ""
            while serverMsg != "Noted":
                reply = self.send(["todo"])
                print("===========")
                print(reply)
                print("===========")
                arr = reply.split(":")
                mesg = arr[1].split(",")
                match mesg[0]:
                    case "Click":
                        self.handle_click(self.parse_data(reply))
                    case "Draw":
                        pass#TODO
                
            #handle other client click
            
            # Draw the Board
            self.draw(screen)
            
    def send(self, data_array):
        flat_data = reduce(lambda x, y: str(x) + "," + str(y), data_array)
        data = str(self.net.id) + ":" + flat_data
        reply = self.net.send(data)
        return reply
    
    def parse_data(self, data):
        try:
            data_array = data.split(":")[1].split(",")
            return (int(data_array[0]), int(data_array[1]))
        except:
            return (0, 0)