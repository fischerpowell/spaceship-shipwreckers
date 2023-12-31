import pygame

class StatusEffect:
    def __init__(self, type, duration, size):
        self.type = type
        self.timer = duration
        if self.type == 0:
            self.img = pygame.image.load('textures/hpup_block.png').convert_alpha()
        elif self.type == 1:
            self.img = pygame.image.load('textures/atomicclock_block.png').convert_alpha()
        elif self.type == 2:
            self.img = pygame.image.load('textures/jetpack_block.png').convert_alpha()
        elif self.type == 3:
            self.img = pygame.image.load('textures/uvcoil_block.png').convert_alpha()
        elif self.type == 4:
            self.img = pygame.image.load('textures/duplicator_block.png').convert_alpha()
        else:
            self.img = pygame.image.load('textures/item_block.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect()
        
    def countdown(self):
        self.timer -= 1
    
    def render(self, display, pos):
        self.rect.topright = pos
        display.blit(self.img, self.rect)