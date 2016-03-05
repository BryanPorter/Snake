# Bryan Porter A01519722

import sys
import pygame
from pygame.locals import *

import game
import score
import state

class Title(state.State):
	settings = [3, 1, 12]
	def __init__(self):
# Sets the font, sizes, and sets the background image
		self.display = pygame.display.get_surface()
		self.background = pygame.image.load("data/images/SnakeBackground5.png")
		self.item_font = pygame.font.Font("data/fonts/Timoteo.TTF", 40)
		self.title_font = pygame.font.Font("data/fonts/Timoteo.TTF", 150)

		self.min_sett = [1, 1, 5]  # Limits for gameplay settings [speed, grow_rate, and grid size]
		self.max_sett = [5, 30, 40]
        
		self.show_instr = False
		self.sett_pg = False
		
		self.menu1_list = ["Start", "Rules", "Scores", "Settings", "Exit"]
		self.menu2_list = ["Speed", "Grow Rate", "Grid Size", "Return"]
		
		self.menu_setup(self.menu1_list)
		
# Inititalizes the title to show Snake		
		self.title = self.title_font.render("Snake!", True, (0, 0, 0))
		self.title_rect = pygame.Rect((self.display.get_width()/2 - self.title.get_width()/2, self.display.get_height()/2 - 1.5*self.title.get_height()),
			(self.title.get_width(), self.title.get_height()))
        
		self.instr_image = pygame.image.load("data/images/SnakeInstructions2.png").convert()

		self.music = pygame.mixer.Sound("data/sound/Title.wav")
		self.music.play()

	def exit(self):
		self.music.stop()

	def reason(self):
		for event in pygame.event.get():
			if event.type == QUIT: #Closes the game
				pygame.quit()
				sys.exit()
			if event.type == MOUSEMOTION:  # Mouse Movement Events used for selecting menu items
				for i in xrange(len(self.menu_rects)):
					if self.menu_rects[i].collidepoint(pygame.mouse.get_pos()):
						self.next(i)
				if self.sett_pg:
					for i in xrange(len(self.sett_rects)):
						if self.sett_rects[i].collidepoint(pygame.mouse.get_pos()):
							self.next(i)
							
			if event.type == MOUSEBUTTONDOWN: # Mouse click events used to select items and change settings
				if self.sett_pg:
					for i in xrange(len(self.sett_rects)):
						if self.sett_rects[i].collidepoint(pygame.mouse.get_pos()):
							if pygame.mouse.get_pos()[0] < 420 and Title.settings[i] > self.min_sett[i]:
								Title.settings[i] -= 1
							if pygame.mouse.get_pos()[0] > 430 and Title.settings[i] < self.max_sett[i]:
								Title.settings[i] += 1
							self.sett_items[i] = self.item_font.render(self.get_set_str(), True, (255, 255, 255))

				if self.show_instr: self.show_instr = False
				else:
					for i in xrange(len(self.menu_rects)):
						if self.menu_rects[i].collidepoint(pygame.mouse.get_pos()):
							rslt = self.select()  #rslt is for events that change state, (viewing scores or playing game)
							if rslt != None: return rslt
							break  #prevents index out of range error when switching to setting page
				
			if event.type == KEYDOWN:
				if self.show_instr:
					if event.key == K_RETURN or event.key == K_KP_ENTER:
						self.show_instr = False
					elif event.key == K_SPACE:
						return game.Game(self.settings)
						
				elif self.sett_pg:
					if event.key == K_UP or event.key == K_KP8:
						self.next(self.current_choice - 1)
					if event.key == K_DOWN or event.key == K_KP2:
						self.next(self.current_choice + 1)
					if event.key == K_RETURN or event.key == K_KP_ENTER:
						self.select()
					if event.key == K_RIGHT or event.key == K_KP6:
						if self.current_choice < 3 and self.settings[self.current_choice] != self.max_sett[self.current_choice]:
							Title.settings[self.current_choice] += 1 
							self.sett_items[self.current_choice] = self.item_font.render(self.get_set_str(), True, (255, 255, 255))
					if event.key == K_LEFT or event.key == K_KP4:
						if self.current_choice < 3 and self.settings[self.current_choice] != self.min_sett[self.current_choice]:
								Title.settings[self.current_choice] -= 1 
								self.sett_items[self.current_choice] = self.item_font.render(self.get_set_str(), True, (255, 255, 255))

				else: # Currently displaying the main menu
					if event.key == K_RETURN or event.key == K_KP_ENTER:
						rslt = self.select()
						if rslt != None: return rslt
					if event.key == K_UP or event.key ==K_KP8:
						self.next(self.current_choice - 1)
					if event.key == K_DOWN or event.key ==K_KP2:
						self.next(self.current_choice + 1)
						
# Method used to determine which menu item is the current choice
	def next(self, val):
		self.menu_items[self.current_choice] = self.item_font.render(self.menu_list[self.current_choice], True, (0, 0, 0)) # changes old choice to black
		if self.current_choice < 3:
			self.sett_items[self.current_choice] = self.item_font.render("    " + str(self.settings[self.current_choice]), True, (0, 0, 0))
		self.current_choice = val % len(self.menu_list)
		self.menu_items[self.current_choice] = self.item_font.render(self.menu_list[self.current_choice], True, (255, 255, 255)) # changes new choice to white
		if self.current_choice < 3:
			self.sett_items[self.current_choice] = self.item_font.render(self.get_set_str(), True, (255, 255, 255))
	
	def select(self):
		if self.sett_pg:
			if self.current_choice == 3: # Return to main menu
				self.menu_setup(self.menu1_list)
				self.sett_pg = False
		else: 
			if self.current_choice == 0:
				return game.Game(self.settings) #change state to game
			elif self.current_choice == 1:
				self.show_instr = True
			elif self.current_choice == 2:
				return score.HighScores()  #change state to score
			elif self.current_choice == 3:
				self.menu_setup(self.menu2_list)
				self.sett_pg = True
				self.current_choice = 0
			elif self.current_choice == 4: # User has elected to quit
				pygame.quit()
				sys.exit()

	def act(self): # Method is used to update the display
		if self.show_instr: self.display.blit(self.instr_image, (0, 0))
		else:
			self.display.blit(self.background, (0, 0))
			self.display.blit(self.title, self.title_rect)
			for i in xrange(len(self.menu_list)):
				self.display.blit(self.menu_items[i], self.menu_rects[i])
			
			if self.sett_pg:
				for i in xrange (len(self.settings)):
					self.display.blit(self.sett_items[i], self.sett_rects[i] )

		pygame.display.update()

# Method used to render a menu item for each of a list of strings and select the first
	def menu_setup(self, lst):
		self.menu_list = lst
		self.menu_items = []
		self.menu_rects = []
		
		for i in xrange(len(self.menu_list)):
			self.menu_items.append( self.item_font.render(self.menu_list[i], True, (0, 0, 0)))
			self.menu_rects.append( pygame.Rect((self.display.get_width()/4 - self.menu_items[0].get_width(), self.display.get_height()/2 + i *.75 * self.menu_items[i].get_height()),
				(self.menu_items[i].get_width(), self.menu_items[i].get_height())))

		self.sett_items = []
		self.sett_rects = []
				
		for i in xrange(len(Title.settings)):
			self.sett_items.append( self.item_font.render("    " + str(self.settings[i]) + "     ", True, (0, 0, 0)))
			self.sett_rects.append( pygame.Rect((self.display.get_width()/4 + self.menu_items[0].get_width(), self.display.get_height()/2 + i *.75 * self.menu_items[i].get_height()),
				(self.sett_items[i].get_width(), self.sett_items[i].get_height())))

		self.current_choice = 0
		self.next(0)

# Method to determine strings of settings based on the limit values
	def get_set_str(self):
		if Title.settings[self.current_choice] == self.min_sett[self.current_choice]:
			strng = "    " + str(Title.settings[self.current_choice])
		else: strng = "  < " + str(Title.settings[self.current_choice])
			
		if Title.settings[self.current_choice] != self.max_sett[self.current_choice]:
			strng = strng + " >  "
		return strng
			
			
			
			
			
			
			
			
			
			