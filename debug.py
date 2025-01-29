import pygame
pygame.init()
font = pygame.font.Font(None,30)

def debug(info,posx = 10,posy = 10):
    display_surface = pygame.display.get_surface()
    debug_surf      = font.render(str(info),True,'white')
    debug_rect      = debug_surf.get_rect(topleft =(posx,posy))
    pygame.draw.rect(display_surface,'black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)
