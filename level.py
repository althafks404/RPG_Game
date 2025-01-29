import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from util import import_csv_layout, import_folder
from random import randint,choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particle import AnimationPlayer
from magic import MagicPlayer
class Level:
    def __init__(self):
        #sprite group setup
        self.visible_sprite                     = YsortCameraGroup()
        self.obstacle_sprite                    = pygame.sprite.Group()
        #setting a display surface
        self.display_surface                    = pygame.display.get_surface()
        self.current_attack                     = None
        self.attack_sprite                      = pygame.sprite.Group()
        self.attackable_sprite                  = pygame.sprite.Group()
        self.create_map()
        self.ui                                 = UI()
        #particle effect
        self.animation_player                   = AnimationPlayer()
        #magic spell
        self.magic_player                       = MagicPlayer(self.animation_player)

    def create_map(self):

        layouts = {
                
                'boundary' : import_csv_layout('map/map_FloorBlocks.csv'),
                'grass'    : import_csv_layout('map/map_Grass.csv'),
                'object'   : import_csv_layout('map/map_Objects.csv'),
                'entities' : import_csv_layout('map/map_Entities.csv'),

        }

        graphics = {
                'grass'    : import_folder('graphics/grass'),
                'grass3'    : 'graphics/grass/grass_3.png',
                'object'   : import_folder('graphics/objects')
        }


        for style,layout in layouts.items():    # the style are the items like 'boundary' and 'layout' are the files 
            for row_index , row in enumerate(layout):
                for col_index , col in enumerate(row):
                   if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprite],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprite,self.obstacle_sprite,self.attackable_sprite],'grass',random_grass_image)
                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            Tile((x,y),[self.visible_sprite,self.obstacle_sprite],'object',surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.despawn_weapon,self.create_magic)
                            else:
                                if  col  == '390':
                                    enemy_name = 'bamboo'
                                elif col == '391':
                                    enemy_name = 'spirit'
                                elif col == '392':
                                    enemy_name = 'raccoon'
                                else:
                                    enemy_name = 'squid'
                                Enemy(enemy_name,(x,y),[self.visible_sprite,self.attackable_sprite],self.obstacle_sprite,self.damage_player,self.trigger_death_particle)


        #for row_index,row in enumerate(WORLD_MAP):  # row is te y pos
            #for col_index , col in enumerate(row): # col is the y pos
               # x = col_index * TILESIZE
               # y = row_index * TILESIZE
               # if col == 'x':
                #    Tile((x , y),[self.visible_sprite,self.obstacle_sprite])
                #elif col == 'p':
                 #   self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite)
                      
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprite,self.attack_sprite])

    def player_attack_logic(self):
        if self.attackable_sprite:
            for attack_sprite  in self.attack_sprite:
                collision_sprite =pygame.sprite.spritecollide(attack_sprite,self.attackable_sprite,False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        if target_sprite.sprite_type == 'grass':
                            pos  = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particle(pos - offset,[self.visible_sprite])
                                pass
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def create_magic(self,style,strenght,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strenght,cost,[self.visible_sprite])
        
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprite,self.attack_sprite])

    def despawn_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def damage_player(self,amount,attack_type):

        if self.player.vunlarable:
            self.player.health -= amount
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particle
            self.animation_player.create_player_particle(attack_type,self.player.rect.center,[self.visible_sprite])

    def trigger_death_particle(self,pos,particle_type):
        self.animation_player.create_player_particle(particle_type,pos,self.visible_sprite)

    def run(self):
        self.visible_sprite.rendering(self.player)
        #update and draw the sprite and game
        self.visible_sprite.update()
        #debug(self.player.direction)
        self.ui.display(self.player)


        self.visible_sprite.enemy_update(self.player)
        self.player_attack_logic()


#creating a new camera sprite group

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset  = pygame.math.Vector2()

        #creating the floor map for the game

        self.floor_surf      = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_surf_rect = self.floor_surf.get_rect(topleft = (0,0))

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        #drawing the floor

    def rendering(self,player):
        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        #drawing the floor
        self.floor_offset_pos = self.floor_surf_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,self.floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite : sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites           = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)