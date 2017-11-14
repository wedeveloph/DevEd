## NOTES TO THE NEWBIE
## Hashtags (#) represent comments
## Everything else is actual code
## Please read them to have a better understanding of the code

# Load the necessary modules
# These always go at the top of the program code
import random # Random module for playing with random numbers
import pygame
from pygame.locals import * # Load all of pygame's local variables

# Always call this function before doing anything with pygame
pygame.init()

# Classes are blueprints for objects
# You can define the objects' properties and methods (what it is and what it does)

# Create the "player" object class that the user controls
# All subsequent classes hold the same concepts as the ones learned here
class Player(object):
	# __init__ is what we call a "constructor" method that "loads" all the information about this particular object
	# When creating a new player, it needs two parameters: x and y, meaning its spawn point
	def __init__(self, x, y):
		# Load the image that represents the player
		# Make sure the filename is exactly as is shown in the folder
		self.image = pygame.image.load("player.png")

		# These are the properties of an axis-aligned bounding box
		# It has a position, width, height, and velocities for both x and y components
		self.position = [x, y] # Spawn point of the player object based on given parameters
		self.dimensions = [50, 50] # [width, height] Used in collision detection
		self.velocity = [0, 0] # [x velocity, y velocity] Used in movement

	def draw(self, surface):
		# Draws the image on given surface at a certain position
		# Pygame draws images based on the top-left coordinate, thus it needs to be repositioned
		# Re-positions the drawing such that it is CENTERED at that position
		surface.blit(self.image, [self.position[0]-self.dimensions[0]/2, self.position[1]-self.dimensions[1]/2])

	def update(self):
		# This "update" method adds the velocity to its position so it can move
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

# Create the enemy
class Enemy(object):
	def __init__(self, x, y):
		self.image = pygame.image.load("item.png")
		self.position = [x, y]
		self.dimensions = [50, 50]

		# A constant velocity of x: -2 makes him move left
		# You may increase the net value to make him move faster
		# Adjust this value as you please
		self.velocity = [-2, 0]

	def update(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

	def draw(self, surface):
		surface.blit(self.image, [self.position[0]-self.dimensions[0]/2, self.position[1]-self.dimensions[1]/2])

	def collide(self, other):
		# The enemy has a collision method that checks if it has collided with another object
		horizontal_overlap = False
		vertical_overlap = False

		# Collision detection algorithm
		# Can be explained visually by Keith Leonardo hehe
		if abs(self.position[0]-other.position[0]) < self.dimensions[0]/2+other.dimensions[0]/2:
			horizontal_overlap = True
		if abs(self.position[1]-other.position[1]) < self.dimensions[1]/2+other.dimensions[1]/2:
			vertical_overlap = True

		# It is colliding only if they overlap both horizontally and vertically
		return horizontal_overlap and vertical_overlap

# Create the bullet
class Bullet(object):
	def __init__(self, player_position):
		# The spawn point of a bullet is the position of the player
		# Make a copy of the player position so whatever we do to the bullet doesn't affect the player
		self.position = player_position[:]

		self.dimensions = [10, 50]
		self.velocity = [15, 0]
		self.image = pygame.image.load("bullet.png")

	def update(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]

	def draw(self, surface):
		surface.blit(self.image, [self.position[0]-self.dimensions[0]/2, self.position[1]-self.dimensions[1]/2])


# Main function is what we call because this is the "meat" of our program
def main():
	# These are the initial variables we need for the game
	# Dimensions of the screen
	width = 1000
	height = 300

	# Colors are represented as R G B values ranging from (0 - 255)
	# You may play with these values as you wish
	bg_color = (0, 100, 0) # Color of the background
	font_color = (255, 255, 255) # Color of your text

	# Set up the display surface (the screen)
	# We don't need to customize our screen so we make the flags-value 0
	# Finally, a 32-bit color depth is good enough for us
	display_surface = pygame.display.set_mode((width, height), 0, 32)
	pygame.display.set_caption("Strawberry Fields Forever")

	# Internal game "clock"
	# Keeps track of the time in the game in "ticks"
	# If you're familiar with Minecraft, yeah this is how it works
	game_clock = pygame.time.Clock()

	player = Player(width/2, height/2) # Create a player object located at the center of our display

	score = 0 # Game score (how many strawberries you've hit)
	
	# Load the font, kinda like loading an image
	# "None" tells pygame to load a default font for you
	font = pygame.font.Font(None, 28)

	# Use the font to render some text
	# We converted the "score" number value into text so it can be rendered by the font
	# The "True" value tells pygame to smoothen the edges of the render
	score_surface = font.render("My score: "+str(score), True, font_color) # Render the score

	# We can have multiple enemies and bullets at one time on the screen, so keep them in a list
	# These lists allow us to keep track of each individual game object
	enemies = []
	bullets = []

	# Main game loop
	# For each iteration of the loop, do these things
	# Everything inside this loop runs forever until the game ends 
	while True:
		display_surface.fill(bg_color)

		# Update and draw the player to the display
		player.update()
		player.draw(display_surface)

		# Spawn a new enemy randomly as long as there are less than 10 enemies currently on the screen
		if random.randint(1, 50) == 1 and len(enemies) < 15:
			# Randomize the spawn point at the right side of the screen
			y = random.randint(0, height)
			enemies.append(Enemy(width, y))

		# Update the positions and velocities and draw each and every enemy to the display
		for e in enemies:
			e.update()
			e.draw(display_surface)

			# Kill the enemy if he is past the left side of the screen
			if e.position[0] < 0: # His x-position is less than 0
				enemies.remove(e)
				print "YOU LOSE BOI"

			# Call the enemy's collision function on the player
			# If they collide, you lose
			if e.collide(player):
				print "YOU LOSE BOI"

			for b in bullets:
				if e.collide(b):
					# Despawn the bullet and the enemy when they collide
					enemies.remove(e)
					bullets.remove(b)

					# Update the score and its surface with the new score
					score = score + 1
					score_surface = font.render("My score: "+str(score), True, font_color)

		# Draw the score text to the display at position (100, 100)
		display_surface.blit(score_surface, (100, 100)) 

		# Update and draw each and every bullet to the display
		for b in bullets:
			b.update()
			b.draw(display_surface)

		# Get all the events in the event queue
		for e in pygame.event.get():
			if e.type == QUIT:
				quit()
			if e.type == KEYDOWN:
				if e.key == K_UP:
					player.velocity[1] = -5 # Make the player's y velocity -5 to make him move up
				if e.key == K_DOWN:
					player.velocity[1] = 5
				if e.key == K_LEFT:
					player.velocity[0] = -5
				if e.key == K_RIGHT:
					player.velocity[0] = 5

				if e.key == K_SPACE:
					bullets.append(Bullet(player.position)) # Spawn a bullet at the player's position

			if e.type == KEYUP:
				if e.key == K_LEFT or e.key == K_RIGHT:
					player.velocity[0] = 0 # Stop him from moving horizontally by making his x velocity 0
				if e.key == K_UP or e.key == K_DOWN:
					player.velocity[1] = 0


		# Update the display everytime it changes
		pygame.display.update()

		# Tell the game clock to cap FPS to 60 to prevent timing issues
		# "The human eye can't perceive anything past 30 FPS" my ass
		game_clock.tick(60)

# Call our main function
main()