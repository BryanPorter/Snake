# Bryan Porter A01519722

import pygame
import state
import title

pygame.init()
display = pygame.display.set_mode((1000,600)) #Sets the game size on the image
pygame.display.set_caption("Snake Game--Arrow Keys to turn, ESC to Quit")

class PlayGame():
    def __init__(self):
        self.sm = state.StateMachine(self, title.Title())

    def start(self):
        while True:
            self.sm.update()

if __name__ == "__main__":
    game = PlayGame()
    game.start()