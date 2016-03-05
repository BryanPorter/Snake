# Bryan Porter A01519722

import sys
import time
import pygame
from pygame.locals import *
import random  #used for next apple location

import score
import state
import title
import snake
import random

class Game(state.State):
	def __init__(self, set):
		self.score = 0
		self.snake_Segs = [] # An array to store snake segments used as iterable
		self.speed = set[0]
		self.grow_count = set[1]
		self.grid_size = set[2] # The size of the grid in comparison to the snake (default is a 12x12 grid)
		self.count_down = -1 # counter for after snake loses
		self.color = random.randrange(0, 5)  # randomly selects the game's snake color
		self.last_moving = 0 # Prevents tail from missing a turn while the snake grows
		
# General and Display Constructors
		self.timer = pygame.time.Clock()
		self.display = pygame.display.get_surface()
		self.background = pygame.image.load("data/images/SnakeBg.png")
		self.score_font = pygame.font.Font("data/fonts/Timoteo.TTF", 50)
		self.score_count_font = pygame.font.Font("data/fonts/Timoteo.TTF", 30)
		self.display.blit(self.background, (0, 0))


# Board Constructor and determines the snake size
		self.board_image = pygame.image.load("data/images/Board.png")
		self.snake_size = self.board_image.get_width() / self.grid_size
		self.board_image = pygame.transform.scale(self.board_image, (self.grid_size * self.snake_size, self.grid_size * self.snake_size))  #scales board to match snake size  and eliminates overlap
		self.board_image_rect = pygame.Rect((self.display.get_width()/2 - self.board_image.get_width()/2, self.display.get_height()/2 - self.board_image.get_height()/2),
			(self.board_image.get_width(), self.board_image.get_height()))

# Constructor for Scoreboard
		self.game_score = self.score_font.render("SCORE", True, (255, 255, 255))
		self.game_score_rect = pygame.Rect((self.display.get_width()/5 - self.game_score.get_width(), self.display.get_height()/2 + self.game_score.get_height()),
			(self.game_score.get_width(), self.game_score.get_height()))
		self.display.blit(self.game_score, self.game_score_rect)

		self.score_count = self.score_count_font.render(str(self.score), True, (255, 255, 255))
		self.score_count_rect = pygame.Rect((self.display.get_width()/5 - self.score_count.get_width(), self.display.get_height()/2 + self.game_score.get_height()*2),
			(self.score_count.get_width(), self.score_count.get_height()))
	
# Constructor for Snake Head and Tail
		self.snake = snake.Head( # places snake in center position of the board with an inital direction of up
			self.grid_size /2 * self.snake_size + 500 - self.board_image.get_width()/2,
			self.grid_size /2 * self.snake_size + 300 - self.board_image.get_height()/2,
			self.snake_size, self.color)
		self.tail = snake.Tail(self.snake.pos_x, self.snake.pos_y, self.snake_size, self.color)

# Constructors for Apple	
		self.apple_image = pygame.image.load("data/images/Apple2.png")
		self.apple_image = pygame.transform.scale(self.apple_image, (self.snake_size, self.snake_size))
		self.new_Apple()
		
# Sound files
		self.go_sound =  pygame.mixer.Sound("data/sound/Game.wav")
		self.end_sound =  pygame.mixer.Sound("data/sound/GameOver.wav")
		self.go_sound.play(-1) # go_sound loops until stopped
	
# Function to cleanup after Game
	def exit(self):
		self.end_sound.stop()
		self.score = 0

	def reason(self):
		if self.count_down == 0:  # countdown that occurs when snake has left legal limits or hit tail
			return score.HighScores(self.score)
			
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return title.Title()
				if event.key == K_RIGHT or event.key ==K_KP6:
					self.snake.turn(1)
				if event.key == K_LEFT or event.key ==K_KP4:
					self.snake.turn(3);
				if event.key == K_UP or event.key ==K_KP8:
					self.snake.turn(0);
				if event.key == K_DOWN or event.key ==K_KP2:
					self.snake.turn(2);

	def act(self):
		self.timer.tick(3 * self.speed) # The lower the number the slower the snake

		if self.snake.pos_x == self.app_pos_x and self.snake.pos_y == self.app_pos_y:
			self.new_Apple()
			self.grow()
		self.display.blit(self.board_image, self.board_image_rect)

		self.snake.update()

	# horizontal and vertical distances the snake is from top left corner of the board
		dif_x = (self.snake.pos_x - (self.display.get_width()/2 - self.board_image.get_width()/2)) /self.snake_size 
		dif_y = (self.snake.pos_y - (self.display.get_height()/2 - self.board_image.get_height()/2)) / self.snake_size
		
# Check to see if snake is dead
		if ( dif_x == -1 or dif_x == self.grid_size or  
				dif_y == -1 or	dif_y == self.grid_size):
			self.start_count()

		dir = self.snake.current_Direction # dir is passed to the following segment to give it direction
		if self.snake.length > 1:
			for seg in self.snake_Segs:
				if self.snake.pos_x == seg.pos_x and self.snake.pos_y == seg.pos_y:
					self.start_count()
				dir = seg.update(dir)
				if -1 < dir < 4: #it does not show a stopped snake segment
					self.display.blit(seg.image, seg.rect)
		self.tail.update(dir, self.last_moving)  #last_moving prevents tail from disconnecting while snake is growing
		self.count_down -= 1
		
		self.display.blit(self.apple_image, self.apple_image_rect)
		self.display.blit(self.snake.image, self.snake.rect)
		self.display.blit(self.tail.image, self.tail.rect)
		pygame.display.update()
		
# Method that finds a new position that there for a new apple Where snake is not
	def new_Apple(self):
		self.app_pos_x = random.randrange(0, self.grid_size) * self.snake_size + 500 - self.board_image.get_width()/2
		self.app_pos_y = random.randrange(0, self.grid_size) * self.snake_size + 300 - self.board_image.get_height()/2
		if self.snake.pos_x == self.app_pos_x and self.snake.pos_y == self.app_pos_y:
			self.new_Apple()
		for seg in self.snake_Segs:
			if seg.pos_x == self.app_pos_x and seg.pos_y == self.app_pos_y:
				self.new_Apple()
		
		self.apple_image_rect = ((self.app_pos_x, self.app_pos_y), (self.snake_size, self.snake_size))
		
# Method called when snake reaches an apple increments score and changes apple position
	def grow(self):
		posX = self.snake.pos_x
		posY = self.snake.pos_y
		dir = self.snake.current_Direction
		
		if len(self.snake_Segs) > 0:
			for seg in self.snake_Segs:
				posX = seg.pos_x
				posY = seg.pos_y
				dir = seg.current_Direction
		
		for i in range(self.grow_count):
			self.snake_Segs.append(snake.Snake_Segment(posX, posY, self.snake_size, self.color))

		self.last_moving = dir
		
		self.snake.length += self.grow_count
		self.score += self.snake.length * self.speed / ((self.grid_size-3) / 2) +1
		self.new_Apple()
		
		self.score_count = self.score_count_font.render(str(self.score), True, (255, 255, 255))
		self.score_count_rect = pygame.Rect((self.display.get_width()/5 - self.score_count.get_width(), self.display.get_height()/2 + self.game_score.get_height()*2),
			(self.score_count.get_width(), self.score_count.get_height()))

		self.display.blit(self.background, (0, 0))
		self.display.blit(self.game_score, self.game_score_rect)
		self.display.blit(self.score_count, self.score_count_rect)
	
# Method that is called when snake has died to begin count-down
	def start_count(self):
		if self.snake.current_Direction < 4:
			self.go_sound.stop()
			self.end_sound.play()
			self.snake.current_Direction += 4
			self.count_down = len(self.snake_Segs) + 1
			self.speed += len(self.snake_Segs)/8
			
			
			
			
			

			