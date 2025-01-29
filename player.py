import pygame
from settings import *
from debug import debug
from util import import_folder
from weapon import Weapon
from entity import Entity
class Player(Entity):
    def __init__(self,pos,group,obstacle_sprite,create_attack,despawn_weapon,create_magic):
        super().__init__(group)
        self.image                 = pygame.image.load('graphics/test/player.png')
        self.rect                  = self.image.get_rect(topleft = pos)
        self.hitbox                = self.rect.inflate(0,-26)

        #self.direction             = pygame.math.Vector2()
        #self.speed                 = 5
        self.pos                   = pygame.math.Vector2()
        self.obstacle_sprite      = obstacle_sprite

        self.attacking             = False
        self.cooldown_time         = 400
        self.attack_time           = None
        #asset setup
        self.import_player_animation()
        self.status                = 'down'  # here the status will be held resopnsible for the which state to pick up an animation state eg : attack_right
        #self.frame_index           = 0
        #self.animation_speed       = 0.15

        self.create_attack         = create_attack
        self.despawn_weapon        = despawn_weapon
        self.weapon_index          = 0
        self.weapon                = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon     = True
        self.weapon_switch_time    = None
        self.weapon_switch_cooldown = 200

        #magic
        self.create_magic           = create_magic
        self.magic_index            = 0
        self.weapon                 = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic       = True
        self.magic_switch_time      = None
        self.magic_switch_cooldown  = 200

        self.stats                  = {'health':100,'energy':60,'attack':10,'magic':4,'speed':5}
        self.health                 = self.stats['health'] 
        self.energy                 = self.stats['energy'] 
        self.exp                    = 123
        self.speed                  = self.stats['speed']

        self.vunlarable             = True
        self.hit_time               = None
        self.invicibility_duration  = 500

    def import_player_animation(self):
        image_path         = 'graphics/player/'
        self.animations     = {

                    'up'                    : [],
                    'down'                  : [],
                    'left'                  : [],
                    'right'                 : [],

                    'right_idle'            : [],
                    'left_idle'             : [],
                    'up_idle'               : [],
                    'down_idle'             : [],

                    'right_attack'          : [],
                    'left_attack'           : [],
                    'up_attack'             : [],
                    'down_attack'           : []


        }

        for frame in self.animations.keys():
            full_path                      = image_path + frame
            self.animations[frame]         = import_folder(full_path)

    def player_input(self):
        keys                       = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y       =-1
            self.status            = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y       = 1
            self.status            = 'down'
        else:
            self.direction.y       = 0
        if keys[pygame.K_LEFT]:
            self.direction.x       =-1
            self.status            = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x       = 1
            self.status            = 'right'
        else:
            self.direction.x       = 0

    def player_attack(self):
        keys                       = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking         = True
            self.attack_time       = pygame.time.get_ticks()
            self.create_attack()
              
    def player_magic(self):
        keys                       = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking         = True
            self.attack_time       = pygame.time.get_ticks()
            style                  = list(magic_data.keys())[self.magic_index]
            strength               = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            cost                   = list(magic_data.values())[self.magic_index]['cost']
            self.create_magic(style,strength,cost)
   
    def weapon_chamge(self):
        keys    = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon  = False
            if  self.weapon_index < len(list(weapon_data.keys())) - 1 :
                self.weapon_index  += 1
            else:
                self.weapon_index  = 0
            self.weapon             = list(weapon_data.keys())[self.weapon_index]
            self.weapon_switch_time = pygame.time.get_ticks()

        if keys[pygame.K_e] and self.can_switch_magic:
            self.can_switch_magic  = False
            if  self.magic_index < len(list(magic_data.keys())) - 1 :
                self.magic_index  += 1
            else:
                self.magic_index  = 0
            self.magic              = list(magic_data.keys())[self.magic_index]
            self.magic_switch_time = pygame.time.get_ticks()

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def attack_cooldown(self):
        current_time                    = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.cooldown_time + weapon_data[self.weapon]['cooldown']:
                self.attacking          = False
                self.despawn_weapon()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_cooldown >= self.weapon_switch_time:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_cooldown >= self.magic_switch_time:
                self.can_switch_magic = True

        if not self.vunlarable:
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vunlarable = True
   
    def get_status(self):

        # idle state 
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def animate(self):
        frame          = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frame):
            self.frame_index = 0
        # setting the image
        self.image     = frame[int(self.frame_index)]
        self.rect      = self.image.get_rect(center = self.hitbox.center)

        #flicker

        if not self.vunlarable:
            alpha    = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def energy_recovery(self):
        if self.energy <= self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.player_movement(self.speed)
        self.player_input()
        self.player_attack()
        self.player_magic()
        self.attack_cooldown()
        self.get_status()
        self.animate()
        self.weapon_chamge()
        self.energy_recovery()