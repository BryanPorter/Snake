# Bryan Porter A01519722

import time
import sys
import pygame
from pygame import *

import game

class Head():
	def __init__(self, posx, posy, size, color):
		self.current_Direction = 0;  #0 is up, 1 is right, 2 is down, 3 is left, 4 is none
		self.length = 1;
		self.last_pos = 4  # Used to prevent the snake from turning 180 degrees onto itself
		
		self.timer = pygame.time.Clock()
		self.image = pygame.image.load("data/images/SnakeHead" + str(color) + ".png")
		self.image = pygame.transform.scale(self.image, (size, size))
		
		self.pos_x = posx
		self.pos_y = posy
		self.rect = pygame.Rect((0, 0), (self.image.get_width(), self.image.get_height()))

	def update(self):
		move(self)
		self.last_pos = (self.current_Direction + 2) % 4	

	def turn(self, val):
		if self.current_Direction != val and self.current_Direction < 4:
			if self.last_pos != val or self.length == 1:  # Prevents snake from turning directly on itself
				turn = self.current_Direction - val
				self.current_Direction = (self.current_Direction + val) % 4
				self.current_Direction = val
				self.image = pygame.transform.rotate(self.image, (90 * turn))
		
		
class Snake_Segment():

	def __init__(self, pos_x, pos_y, size, color, dir = -4):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.current_Direction = dir  #initializes its direction to stopped
		self.last_dir = 1 # needed to show turn segments

		self.straight_image = pygame.image.load("data/images/SnakeSeg" + str(color) + ".png")
		self.straight_image = pygame.transform.scale(self.straight_image, (size, size))
		self.turn_image = pygame.image.load("data/images/TurnSeg" + str(color) + ".png")
		self.turn_image = pygame.transform.scale(self.turn_image, (size, size))
		
		self.image = self.straight_image
		self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.image.get_width(), self.image.get_height()))
		
	def update(self, next_dir):
		prev_dir = self.current_Direction
		move(self)

		if next_dir % 4 == self.current_Direction:
			self.image = self.straight_image
		
		elif self.current_Direction != next_dir: # snake has turned
			self.turnImage(next_dir)
			self.image = self.turn_image
		self.current_Direction = next_dir

		return prev_dir  # passed to following segment
		
	def turnImage(self, dir):
		self.straight_image = pygame.transform.rotate(self.straight_image, 90* (self.current_Direction - dir))
		if self.current_Direction == -4:
			self.turn_image = pygame.transform.rotate(self.turn_image, 360 + -90 * dir)
			self.last_dir = (dir-1) % 4
			
		elif dir == self.last_dir:
				self.turn_image = pygame.transform.rotate(self.turn_image, 180)
				self.last_dir = self.current_Direction
		else: 
			self.turn_image = pygame.transform.rotate(self.turn_image, -90 * (dir - self.current_Direction))
			self.last_dir = self.current_Direction


class Tail():
	def __init__(self, pos_x, pos_y, size, color, dir = 0):
		self.pos_x = pos_x
		self.pos_y = pos_y + size
		self.current_Direction = dir

		self.image = pygame.image.load("data/images/Tail" + str(color) + ".png")
		self.image = pygame.transform.scale(self.image, (size, size))
		self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.image.get_width(), self.image.get_height()))
		
	def update(self, dir, last_dir = -4):
		move(self)
		if dir != self.current_Direction and dir != -4: # snake has turned
			self.image = pygame.transform.rotate(self.image, 90 * (self.current_Direction - dir))
			self.current_Direction = dir
		elif dir == -4:  # prevents the tail from turning when stopped
			if self.current_Direction %4 != last_dir + dir % 4 and last_dir >= 0:
				self.image = pygame.transform.rotate(self.image, 90* (self.current_Direction - last_dir))
				self.current_Direction = last_dir
			self.current_Direction -= dir
		else: self.current_Direction = dir
			
# Method used for changing snake position, used by all snake parts
def move(self):
	if self.current_Direction == 0:
		self.pos_y -= self.image.get_height()
	if self.current_Direction == 1:
		self.pos_x += self.image.get_width()
	if self.current_Direction == 2:
		self.pos_y += self.image.get_width()
	if self.current_Direction == 3:
		self.pos_x -= self.image.get_width()

	self.rect = pygame.Rect((self.pos_x, self.pos_y), (self.image.get_width(), self.image.get_height()))


