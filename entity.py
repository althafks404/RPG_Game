import pygame
from math import sin
class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index                = 0
        self.animation_speed            = 0.15
        self.direction                  = pygame.math.Vector2()

    def player_movement(self,speed):
        if self.direction.magnitude() != 0:  
            self.direction          = self.direction.normalize()
            #########################################################################
            # here the if statement states that if the player move diagonally       #
            # the player moves significantly fastes.Because of the trig fuction     #
            # so the direction has a lenght more than 0                             #
            # so if it has more length then the direcion will need to be normalized #
            #########################################################################
        #self.rect.center            += self.direction * self.speed
        self.hitbox.x                  += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y                  += self.direction.y * speed
        self.collision('vertical')
        self.rect.center                = self.hitbox.center
     
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    

        if direction == 'vertical':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0