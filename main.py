import pygame

from game import game

pygame.init()

WINDOW_DIM = (900, 600)
SQUARE_NUMBER = 8
HAND_SIZE = 7

if __name__ == '__main__':
	screen = pygame.display.set_mode(WINDOW_DIM)
	game = game(WINDOW_DIM, SQUARE_NUMBER, HAND_SIZE)
	game.run(screen)

  
  
  
#server: recive two possitions
#send them to the other to handle