import pygame
from util import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.particle_frames = {

                        # magic 
                        'flame'         : import_folder('graphics/particles/flame/frames'),
                        'aura'          : import_folder('graphics/particles/aura'),
                        'heal'          : import_folder('graphics/particles/heal/frames'),

                        #attack
                        'claw'          : import_folder('graphics/particles/claw'),
                        'slash'         : import_folder('graphics/particles/slash'),
                        'sparkle'       :import_folder('graphics/particles/sparkle'),
                        'leaf_attack'   :import_folder('graphics/particles/leaf_attack'),
                        'thunder'       :import_folder('graphics/particles/thunder'),

                        #monster death

                        'squid'         : import_folder('graphics/particles/smoke_orange'),
                        'raccoon'        : import_folder('graphics/particles/raccoon'),
                        'spirit'        : import_folder('graphics/particles/nova'),
                        'bamboo'        : import_folder('graphics/particles/bamboo'),

                        #leafs

                        'leaf'          :(
                                            import_folder('graphics/particles/leaf1'),
                                            import_folder('graphics/particles/leaf2'),
                                            import_folder('graphics/particles/leaf3'),
                                            import_folder('graphics/particles/leaf4'),
                                            import_folder('graphics/particles/leaf5'),
                                            import_folder('graphics/particles/leaf6'),
                                            self.reflect_images(import_folder('graphics/particles/leaf1')),
                                            self.reflect_images(import_folder('graphics/particles/leaf2')),
                                            self.reflect_images(import_folder('graphics/particles/leaf3')),
                                            self.reflect_images(import_folder('graphics/particles/leaf4')),
                                            self.reflect_images(import_folder('graphics/particles/leaf5')),
                                            self.reflect_images(import_folder('graphics/particles/leaf6')),

                        ),



        }

    def reflect_images(self,leaf_frames):
        new_frames          = []
        for frame in leaf_frames:
            flipped_frame  = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_grass_particle(self,pos,groups):
        animation_frames    = choice(self.particle_frames['leaf'])
        ParticleEffect(pos,animation_frames,groups)

    def create_player_particle(self,animation_type,pos,groups):
        animation_frame     = self.particle_frames[animation_type]
        ParticleEffect(pos,animation_frame,groups)

    def create_heal_particle(self,animation_type,pos,groups):
        animation_frame     = self.particle_frames[animation_type]
        ParticleEffect(pos,animation_frame,groups)

    def create_flame_particle(self,animation_type,pos,groups):
        animation_frame     = self.particle_frames[animation_type]
        ParticleEffect(pos,animation_frame,groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frame,groups):
        super().__init__(groups)
        self.frame_index            = 0
        self.animation_speed        = 0.15
        self.sprite_type            = 'magic'
        self.frames                 = animation_frame
        self.image                  = self.frames[self.frame_index]
        self.rect                   = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index  >= len(self.frames):
            self.kill()
        else:
            self.image            = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()