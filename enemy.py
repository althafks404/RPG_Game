import pygame
from settings  import *
from entity import Entity
from util import *
class Enemy(Entity):
    def __init__(self, enemy_name,pos,group,obstacle_sprite,damage_player,trigger_death_particle):
        super().__init__(group)
        self.sprite_type        = 'enemy'
        #graphics setup
        self.enemy_assets(enemy_name)
        self.status             = 'idle'
        self.image              = self.animations[self.status][self.frame_index]
        
        #enemy movement
        self.rect               = self.image.get_rect(topleft = pos)
        self.hitbox            = self.rect.inflate(0,-10)
        self.obstacle_sprite    = obstacle_sprite

        #enemy stats
        self.enemy_name         = enemy_name
        enemy_info              = enemy_data[self.enemy_name]
        self.health             = enemy_info['health']
        self.exp                = enemy_info['exp']
        self.attack_damage      = enemy_info['damage']
        self.speed              = enemy_info['speed']
        self.resistance         = enemy_info['resistance']
        self.attack_radius      = enemy_info['attack_radius']
        self.notice_radius      = enemy_info['notice_radius']
        self.attack_type        = enemy_info['attack_type']

        # player interaction
        self.can_attack         = True
        self.attack_time        = None
        self.attack_cooldown    = 400
        self.damage_player      = damage_player
        self.trigger_death_particle   = trigger_death_particle

        # invincibility_ timer
        self.vunlarable         = True
        self.hit_time           = None
        self.invincibility      = 300


    def enemy_assets(self,name):
        self.animations = {
            'idle'   :  [],
            'move'   :  [],
            'attack' :  []

        }
        main_path            = f'graphics/monsters/{name}/'
        for animation in self.animations:
            self.animations[animation] = import_folder(main_path  + animation)

    def player_distance_direction(self,player):
        enemy_vec                   = pygame.math.Vector2(self.rect.center)
        player_vec                  = pygame.math.Vector2(player.rect.center)
        distance                    = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction               = (player_vec - enemy_vec).normalize()
        else:
            direction               = pygame.math.Vector2()
        return distance,direction
    
    def enemy_animation(self):
        animation                    = self.animations[self.status]
        self.frame_index            += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image                  = animation[int(self.frame_index)]
        self.rect                   = self.image.get_rect(center = self.hitbox.center)
        if not self.vunlarable:
            #the enemy need to be flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255) 
    
    def get_status(self,player):
        distance            = self.player_distance_direction(player)[0]
        
        if distance <= self.attack_radius and self.can_attack :
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def action(self,player):
        if self.status == 'attack':
            self.attack_time    = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)

        elif self.status == 'move':
            self.direction = self.player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def attack_cooldown_time(self):
        current_time            = pygame.time.get_ticks()
        if not self.can_attack:  
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vunlarable:
            if current_time - self.hit_time >= self.invincibility:
                self.vunlarable = True

    def get_damage(self,player,attack_type):
        if self.vunlarable:
            self.direction = self.player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health  -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            #magic damage
            self.hit_time   = pygame.time.get_ticks()
            self.vunlarable = False

    def check_death(self):
        if self.health <= 0 :
                self.kill()
                self.trigger_death_particle(self.rect.center,self.enemy_name)

    def hit_reaction(self):
        if not self.vunlarable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction() 
        self.player_movement(self.speed)
        self.enemy_animation()
        self.attack_cooldown_time()
        self.check_death()
    def enemy_update(self,player):
        self.get_status(player)
        self.action(player)
        
