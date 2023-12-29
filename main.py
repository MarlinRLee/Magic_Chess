import pygame

from Game import Game

pygame.init()
pygame.display.set_caption("Magic Chess")
pygame_icon = pygame.image.load('chess\\imgs\\artifact.png')
pygame.display.set_icon(pygame_icon)

WINDOW_DIM = (900, 600)
SQUARE_NUMBER = 8
HAND_SIZE = 7

if __name__ == '__main__':
	screen = pygame.display.set_mode(WINDOW_DIM)
	game = Game(WINDOW_DIM, SQUARE_NUMBER, HAND_SIZE)
	game.run(screen)

  
  
  
#server: recive two possitions
#send them to the other to handle