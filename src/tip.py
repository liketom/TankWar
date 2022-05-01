import pygame

class Tip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.enemy_life = pygame.image.load(r"..\image\enemy_num.png").convert_alpha()
        self.tank1_life = pygame.image.load(r"..\image\tank_T1_num.png").convert_alpha()
