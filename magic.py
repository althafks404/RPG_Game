import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animaion_player    = animation_player

    def heal(self,player,strenght,cost,group):
        if player.energy >= cost:
            player.health += strenght
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animaion_player.create_heal_particle('aura',player.rect.center,group)
            self.animaion_player.create_heal_particle('heal',player.rect.center + pygame.math.Vector2(0,-60),group)
        
    
    def flame(self,player,cost,groups):
        if player.energy >= cost:
            #player.energy -= cost

            if player.status.split('_')[0]  == 'right':
                direction = pygame.math.Vector2(1,0)

            elif player.status.split('_')[0]  == 'left':
                direction = pygame.math.Vector2(-1,0)

            elif  player.status.split('_')[0]  == 'up':
                direction = pygame.math.Vector2(0,-1)

            else :
                direction = pygame.math.Vector2(0,1)

            for index in range(1,6):
                if direction.x :# horizontal
                    offset_x = (direction.x * index ) * TILESIZE
                    x        = player.rect.centerx + offset_x + randint(-TILESIZE // 3 , TILESIZE // 3)
                    y        = player.rect.centery + randint(-TILESIZE // 3 , TILESIZE // 3)
                    self.animaion_player.create_flame_particle('flame',(x,y),groups)
                else:#vertical
                    offset_y = (direction.y * index ) * TILESIZE
                    x        = player.rect.centerx  + randint(-TILESIZE // 3 , TILESIZE // 3)
                    y        = player.rect.centery + offset_y +  randint(-TILESIZE // 3 , TILESIZE // 3)
                    self.animaion_player.create_flame_particle('flame',(x,y),groups)
