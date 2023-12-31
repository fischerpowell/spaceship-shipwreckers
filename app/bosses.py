import pygame
from guns import ShotGun, Akimbo, Sniper, TripleGun
import numpy as np
import random


class ShotGunBoss:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 45
        self.hurt_img = pygame.image.load('textures/sgbosshurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.speed = 7
        self.gun = ShotGun('bullet.png', 'enemy')
        self.ship_map = [['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]
        self.strafe_mod = 0
        self.strafe_countdown = 0
        self.move_countdown = 0
        self.moving = False
        self.angle_mod = 0
        self.move_freq = 20
        self.strafe_freq = 15
        self.move_range = (80, 130)
        self.break_mod = 1
        self.strafe_range = (-45, 45)
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
                        self.angle -= 9
                    else:
                        self.angle += 9

            else:
                self.angle = desired_angle
                self.clockwise = None

    def move(self, player, blocks_list, box_list):
        delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod))
        new_point = pygame.Rect((0, 0), (40, 40))
        new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
        if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
            good_point = True
            self.angle_mod = 0
        else:
            good_point = False

        while not good_point:
            delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            new_point = pygame.Rect((0, 0), (40, 40))
            new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
            if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
                good_point = True
            else:
                self.angle_mod += 3

        self.rect.center = new_point.center

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
        if random.randint(0, 80) == 0:
            return True
        
    def refresh_coords(self, rel_coords):
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)

class AkimboBoss:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 35
        self.hurt_img = pygame.image.load('textures/akbosshurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.speed = 12
        self.gun = Akimbo('bullet.png', 'enemy')
        self.ship_map = [['#', 'B', 'B', 'B', 'B', 'B', 'B', '#'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', '#', 'B', 'B', 'B', 'B', '#', 'B'],
                        ['B', '#', 'B', 'B', 'B', 'B', '#', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['B', '#', 'B', 'B', 'B', 'B', '#', 'B'],
                        ['B', '#', 'B', 'B', 'B', 'B', '#', 'B'],
                        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                        ['#', 'B', 'B', 'B', 'B', 'B', 'B', '#']]
        self.strafe_mod = 0
        self.strafe_countdown = 0
        self.move_countdown = 0
        self.moving = False
        self.angle_mod = 0
        self.move_freq = 20
        self.strafe_freq = 25
        self.move_range = (80, 130)
        self.break_mod = 3
        self.strafe_range = (-80, 80)
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

    def move(self, player, blocks_list, box_list):
        delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod))
        new_point = pygame.Rect((0, 0), (40, 40))
        new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
        if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
            good_point = True
            self.angle_mod = 0
        else:
            good_point = False

        while not good_point:
            delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            new_point = pygame.Rect((0, 0), (40, 40))
            new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
            if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
                good_point = True
            else:
                self.angle_mod += 3

        self.rect.center = new_point.center

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
        if random.randint(0, 75) == 0:
            return True
        
    def refresh_coords(self, rel_coords):
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)

class SniperBoss:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 30
        self.hurt_img = pygame.image.load('textures/sniperbosshurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.speed = 8
        self.gun = Sniper('bullet.png', 'enemy')
        self.ship_map = [['#', '#', '#', '#', 'B', 'B', 'B', 'B', 'B', 'B', '#', '#', '#', '#'],
                         ['#', '#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#', '#'],
                         ['#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#'],
                         ['#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', '#', '#', '#', '#', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', '#', '#', '#', '#', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#'],
                         ['#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#'],
                         ['#', '#', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '#', '#'],
                         ['#', '#', '#', '#', 'B', 'B', 'B', 'B', 'B', 'B', '#', '#', '#', '#']
                        ]
        self.strafe_mod = 0
        self.strafe_countdown = 0
        self.move_countdown = 0
        self.moving = False
        self.angle_mod = 0
        self.move_freq = 40
        self.strafe_freq = 5
        self.move_range = (50, 100)
        self.break_mod = 2
        self.strafe_range = (160, 380)
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
                        self.angle -= 5
                    else:
                        self.angle += 5

            else:
                self.angle = desired_angle
                self.clockwise = None

    def move(self, player, blocks_list, box_list):
        delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod))
        new_point = pygame.Rect((0, 0), (40, 40))
        new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
        if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
            good_point = True
            self.angle_mod = 0
        else:
            good_point = False

        while not good_point:
            delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            new_point = pygame.Rect((0, 0), (40, 40))
            new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
            if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
                good_point = True
            else:
                self.angle_mod += 3

        self.rect.center = new_point.center

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
        if random.randint(0, 75) == 0:
            return True
        
    def refresh_coords(self, rel_coords):
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)


class TripleBoss:
    def __init__(self, img, rel_coords, size):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)
        self.alive = True
        self.angle = random.randint(0, 359)
        self.hp = 40
        self.hurt_img = pygame.image.load('textures/triplebosshurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.clockwise = None
        self.speed = 10
        self.gun = TripleGun('bullet.png', 'enemy')
        self.ship_map = [['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B'],
                         ['B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B'],
                         ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B'],
                         ['B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B'],
                         ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', '#', '#', 'B', 'B', '#', '#', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
                         
        ]
        self.strafe_mod = 0
        self.strafe_countdown = 0
        self.move_countdown = 0
        self.moving = False
        self.angle_mod = 0
        self.move_freq = 20
        self.strafe_freq = 20
        self.move_range = (80, 130)
        self.break_mod = 1.5
        self.strafe_range = (-60, 60)
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

    def move(self, player, blocks_list, box_list):
        delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod))
        new_point = pygame.Rect((0, 0), (40, 40))
        new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
        if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
            good_point = True
            self.angle_mod = 0
        else:
            good_point = False

        while not good_point:
            delta_x = self.speed * np.cos(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            delta_y = -self.speed * np.sin(np.deg2rad(self.angle + self.strafe_mod + self.angle_mod))
            new_point = pygame.Rect((0, 0), (40, 40))
            new_point.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)
            if new_point.collidelist(blocks_list) != -1 and new_point.collidelist(box_list) == -1:
                good_point = True
            else:
                self.angle_mod += 3

        self.rect.center = new_point.center

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
        if random.randint(0, 75) == 0:
            return True
        
    def refresh_coords(self, rel_coords):
        self.rel_coords = rel_coords
        self.rect.center = (rel_coords[0] * 150 + 280, rel_coords[1] * 150 + 280)