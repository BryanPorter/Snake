# Bryan Porter A01519722

import sys
import pygame
import re
from pygame import *

import state
import title

class HighScores(state.State):
	high_scores = []
	def __init__(self, newScore = -1):
		self.score_loc = "data/scores.txt"
		self.score_loc2 = "data/scores_copy.txt"  # Backup copy for if all high scores are erased from scores.txt
		self.last_score = newScore
		self.initials = ""
		self.rank =20
		
		self.fail_sound = pygame.mixer.Sound("data/sound/Score.wav")
		self.success_sound = pygame.mixer.Sound("data/sound/Fanfare.wav")
		
		if len(HighScores.high_scores) < 1:
			self.getHighScores(self.score_loc, self.score_loc2)

		if(newScore > 0):
			HighScores.high_scores.append(( self.initials, newScore))
		
		HighScores.high_scores.sort(key = lambda x: x[1], reverse = True)
		
		for x, score in enumerate(HighScores.high_scores):  # Tells where the user placed compared to others, used for highlighting, and entering initials
			if score[0] == self.initials and score[1] == self.last_score:
				self.rank = x

		if self.rank == 0:  # New High Score
			self.success_sound.play()
		elif self.rank < len(HighScores.high_scores) - 1: # Not the Lowest Score
			self.fail_sound.play()
		
		self.display = pygame.display.get_surface()
		self.background = pygame.image.load("data/images/SnakeBackground2.png")
		self.item_font = pygame.font.Font("data/fonts/Timoteo.TTF", 40)
		self.title_font = pygame.font.Font("data/fonts/Timoteo.TTF", 75)
		
		self.score = self.title_font.render("High Scores!", True, (0, 0, 0))
		self.score_rect = pygame.Rect((self.display.get_width()/2 - self.score.get_width()/2, self.display.get_height()/8 - self.score.get_height()/2),
			(self.score.get_width(), self.score.get_height()))
			
	def act(self):
		self.display.blit(self.background, (0,0))
		self.display.blit(self.score, self.score_rect)

		for y, score in enumerate(HighScores.high_scores):
			if y != self.rank:
				self.display.blit(self.item_font.render(score[0], True, (0, 0, 0)), (self.display.get_width()/2 - 128, (self.score_rect.top + self.score.get_height()) + (35*(y+1))))
				self.display.blit(self.item_font.render(str(score[1]), True, (0, 0, 0)), (self.display.get_width()/2 + 48, (self.score_rect.top + self.score.get_height()) + (35*(y+1))))
			else:
				self.display.blit(self.item_font.render(score[0], True, (255, 255, 255)), (self.display.get_width()/2 - 128, (self.score_rect.top + self.score.get_height()) + (35*(y+1))))
				self.display.blit(self.item_font.render(str(score[1]), True, (255, 255, 255)), (self.display.get_width()/2 + 48, (self.score_rect.top + self.score.get_height()) + (35*(y+1))))

		pygame.display.update()

	def reason(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				return title.Title()
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_KP_ENTER:
					return title.Title()
				elif event.key == K_BACKSPACE:
					self.initials = self.initials[:-1]
				elif len(self.initials) < 3 and len(pygame.key.name(event.key)) == 1 and 96 < ord(pygame.key.name(event.key)) < 123: # Allowes user to enter initials
					self.initials = self.initials + pygame.key.name(event.key)
				if self.rank != 20:
					HighScores.high_scores[self.rank] = (self.initials, self.last_score)

# Cleanup function
	def exit(self):
		if len(HighScores.high_scores) > 10:
			del HighScores.high_scores[10:]
		self.saveHighScores(self.score_loc)
		self.success_sound.stop()

#Function to save scores to loc file
	def saveHighScores(self, loc):
		with open(loc, 'w') as outfile:
			for score in HighScores.high_scores:
				if(score[0] != ""):
					outfile.write(score[0] + "\t" + str(score[1]) + "\n")

# function to retrieve high scores from loc, or loc2 for backup
	def getHighScores(self, loc, loc2 = ""):
		if loc != "":
			with open(loc, 'r') as infile:
				for line in infile:
					score = re.split(r"\t", line)
					HighScores.high_scores.append((score[0], int(score[1])))
				
			if len(HighScores.high_scores) == 0:
				self.getHighScores(loc2)

			
			