import pygame
import random
from guns import DefaultGunEnemy, RocketLauncher
import numpy as np

class DefaultEnemy:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 3
        self.hurt_img = pygame.image.load('textures/enemyhurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.gun = DefaultGunEnemy()
        self.hurt_sound = pygame.mixer.Sound('sounds/enemyhurt.mp3')
        self.hurt_sound.set_volume(1.1)
        self.dead_sound = pygame.mixer.Sound('sounds/enemydead.mp3')
        self.dead_sound.set_volume(1.5)

    def change_angle(self, player_pos):
        delta_x, delta_y = (self.rect.centerx - player_pos[0], self.rect.centery - player_pos[1])
        if abs(delta_x) > 0:
            if delta_x < 0:
                desired_angle =  - np.rad2deg(np.arctan(delta_y / delta_x))
            else:
                desired_angle =  - np.rad2deg(np.arctan(delta_y / delta_x)) + 180
            
            
            
            if abs((desired_angle - self.angle)) % 360 > 15:
                if self.clockwise == None:
                    if (self.angle - desired_angle) % 360 > 180:
                        self.clockwise = False
                    else:
                        self.clockwise = True
                else:
                    if self.clockwise:
                        self.angle -= 7
                    else:
                        self.angle += 7

            else:
                self.angle = desired_angle
                self.clockwise = None

    def hurt(self):
        if self.hurt_timer % 1 == 0:
            self.hurt_anim = True
        elif self.hurt_timer % .5 == 0:
            self.hurt_anim = False
        self.hurt_timer -= 0.125


    def render(self, display):
        if self.hurt_anim == True:
            self.img = pygame.transform.rotate(self.hurt_img, self.angle)
        else:
            self.img = pygame.transform.rotate(self.original_img, self.angle)
        self.rotated_rect = self.img.get_rect(center = (round(self.rect.centerx), round(self.rect.centery)))
        display.blit(self.img, self.rotated_rect)

    def contemplate_shooting(self):
        if random.randint(0, 100) == 0:
            return True
        
class RocketEnemy:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 3
        self.hurt_img = pygame.image.load('textures/enemyrockethurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.gun = RocketLauncher()
        self.hurt_sound = pygame.mixer.Sound('sounds/enemyhurt.mp3')
        self.hurt_sound.set_volume(1.1)
        self.dead_sound = pygame.mixer.Sound('sounds/enemydead.mp3')
        self.dead_sound.set_volume(1.5)

    def change_angle(self, player_pos):
        delta_x, delta_y = (self.rect.centerx - player_pos[0], self.rect.centery - player_pos[1])
        if abs(delta_x) > 0:
            if delta_x < 0:
                desired_angle =  - np.rad2deg(np.arctan(delta_y / delta_x))
            else:
                desired_angle =  - np.rad2deg(np.arctan(delta_y / delta_x)) + 180
            
            
            
            if abs((desired_angle - self.angle)) % 360 > 15:
                if self.clockwise == None:
                    if (self.angle - desired_angle) % 360 > 180:
                        self.clockwise = False
                    else:
                        self.clockwise = True
                else:
                    if self.clockwise:
                        self.angle -= 7
                    else:
                        self.angle += 7

            else:
                self.angle = desired_angle
                self.clockwise = None

    def hurt(self):
        if self.hurt_timer % 1 == 0:
            self.hurt_anim = True
        elif self.hurt_timer % .5 == 0:
            self.hurt_anim = False
        self.hurt_timer -= 0.125

    def render(self, display):
        if self.hurt_anim == True:
            self.img = pygame.transform.rotate(self.hurt_img, self.angle)
        else:
            self.img = pygame.transform.rotate(self.original_img, self.angle)
        self.rotated_rect = self.img.get_rect(center = (round(self.rect.centerx), round(self.rect.centery)))
        display.blit(self.img, self.rotated_rect)

    def contemplate_shooting(self):
        if random.randint(0, 100) == 0:
            return True