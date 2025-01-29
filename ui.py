import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface        = pygame.display.get_surface()
        self.font                   = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        #ui Bar setup
        self.health_bar_rect        = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT) 
        self.energy_bar_rect        = pygame.Rect(10,40,ENERGY_BAR_WIDTH,BAR_HEIGHT)
        # convert weapon_index dic
        self.weapon_image           = []
        for weapon in weapon_data.values():
            path = weapon['graphics']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_image.append(weapon)
        #converting magic_index to dictionary
        self.magic_image            = []
        for magic in magic_data.values():   # the valuse() looks for a specific data such as graphics and return the path
            path = magic['graphics']
            magic  = pygame.image.load(path).convert_alpha() 
            self.magic_image.append(magic)
   
    def show_bar(self,current,max_amount,bg_rect,color):
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        #converting stats to pixel
        ratio                      = current / max_amount
        current_width              = bg_rect.width  * ratio
        current_rect               = bg_rect.copy()
        current_rect.width         = current_width
        #drawing the stats
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3) 

    def show_exp(self,exp):
        text_surf                  = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x                          = self.display_surface.get_size()[0] - 20
        y                          = self.display_surface.get_size()[1] - 20
        text_rect                  = text_surf.get_rect(bottomright = (x,y))
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def selection_box(self,left,top,has_switched):
        bg_rect                    = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_ACTIVE_COLOR,bg_rect,8)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,8)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        self.bg_rect = self.selection_box(10,630,has_switched)
        self.weapon_surf = self.weapon_image[weapon_index]
        self.weapon_rect = self.weapon_surf.get_rect(center = self.bg_rect.center)
        self.display_surface.blit(self.weapon_surf,self.weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect       = self.selection_box(100,630,has_switched)
        self.magic_surf = self.magic_image[magic_index]
        self.magic_rect = self.magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(self.magic_surf,self.magic_rect)

   
    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)    
        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)   # this is for the weapon item
        self.magic_overlay(player.magic_index,not player.can_switch_magic)
        #self.selection_box(100,630)      # this is for the magic item
    
