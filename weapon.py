import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,group,):
        super().__init__(group)
        self.sprite_type        = 'weapon'
        self.direction          = player.status.split('_',)[0]
        self.weapon_image_path  = f'graphics/weapons/{player.weapon}/{self.direction}.png'
        self.image              = pygame.image.load(self.weapon_image_path).convert_alpha()
        #placement of the weapon
        if self.direction=='right':
             self.rect           = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif self.direction == 'left':
            self.rect           = self.image.get_rect(midright = player.rect.midleft  + pygame.math.Vector2(0,16))
        elif self.direction  == 'up':
            self.rect           = self.image.get_rect(midbottom   = player.rect.midtop + pygame.math.Vector2(-10,0))
        else:
            self.rect            = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
