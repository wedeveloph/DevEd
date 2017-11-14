# Import necessary modules
import pygame
from pygame.locals import * # Import all of pygame's local variables

# Always call this function before doing anything with pygame
pygame.init()

# The program's "main" function
def main():
	# Declare local variables
	width = 640 # Dimensions of the display
	height = 480
	background_color = (255, 255, 255) # RGB color tuple (0 - 255)

	# Setup display
	# display.set_mode(dimentions_tuple, flags=0, color_depth)
	display_surface = pygame.display.set_mode((width, height), 0, 32)
	pygame.display.set_caption("My first game!")

	# Internal "game clock"
	game_clock = pygame.time.Clock()

	# Main loop
	while True:
		# Color the display with the chosen background color
		display_surface.fill(background_color)

		# Handle "events"
		# Events are anything that relates to user input including
		# keyboard, mouse, and even quitting.

		# Pygame automatically keeps track of user input in real time.
		# We can access the list of inputs by the player through pygame.event.get()
		for e in pygame.event.get(): # For every event in the queue,
			if e.type == QUIT: # Checks if the "type" of event that occurred was a "QUIT" event
				quit() # Quit the game when the user "quits" the app

			if e.type == KEYDOWN:
				if e.key == K_UP:
					background_color = (255, 0, 0) # Pressing the "up" key makes the background red

			if e.type == KEYUP:
				background_color = (255, 255, 0) # Releasing any key will make the background yellow

			if e.type == MOUSEBUTTONDOWN:
				background_color = (0, 255, 0) # Holding the mouse button down makes it green

			if e.type == MOUSEBUTTONUP:
				background_color = (0, 0, 255) # Releasing the mouse button makes it blue

		# Update the display everytime it changes
		pygame.display.update()

		# Cap the FPS to 60
		game_clock.tick(60)

# Call the main() function and run the game
main()
