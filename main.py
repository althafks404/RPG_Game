import pygame
import sys
from settings import *
from debug import debug
from level import Level
class Game:
    def __init__(self):

        #game initialization
        pygame.init()
        self.screen                      = pygame.display.set_mode((HEIGHT , WIDTH))
        self.clock                       = pygame.time.Clock()     
        pygame.display.set_caption('Zelda Adventure')
        self.level                       = Level()    # creating the instace of the level class  
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                    exit()

            keys                       = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.exit()
                exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()
