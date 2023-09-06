import pygame

from game import game

pygame.init()

WINDOW_DIM = (600, 600)
SQUARE_NUMBER = 8
HAND_SIZE = 5
screen = pygame.display.set_mode(WINDOW_DIM)

game = game(WINDOW_DIM, SQUARE_NUMBER, HAND_SIZE)

def draw(display):
	display.fill((100, 100, 100))
	game.draw(display)
	pygame.display.update()


if __name__ == '__main__':
	running = True
	while running:
		click_pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
	   			# If the mouse is clicked
				if event.button == 1:
					game.handle_click(click_pos)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					game.selected_piece = None   
		# Draw the board
		draw(screen)