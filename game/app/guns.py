from bullet import Bullet, Rocket
import numpy as np
import pygame
import random

class DefaultGun:
    def __init__(self):
        self.img = pygame.image.load('textures/bullet_hero.png').convert_alpha()
        self.laser1 = pygame.mixer.Sound('sounds/laser1.mp3')
        self.laser2 = pygame.mixer.Sound('sounds/laser2.mp3')
        self.laser1.set_volume(.2)
        self.laser2.set_volume(.2)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):
        bullet_list.append(Bullet(self.img, (
            player_rect.centerx + 58 * np.cos(np.deg2rad(player_angle - 20)),
            player_rect.centery - 58 * np.sin(np.deg2rad(player_angle - 20))
            ), (30, 30), player_angle, 100, 'hero', 1, 20))
        sound = random.choice([self.laser1, self.laser2])
        if sound_on:
            sound.play()
        return bullet_list
    
class DefaultGunEnemy:
    def __init__(self):
        self.img = pygame.image.load('textures/bullet.png').convert_alpha()
        self.laser1 = pygame.mixer.Sound('sounds/enemylaser1.mp3')
        self.laser2 = pygame.mixer.Sound('sounds/enemylaser2.mp3')
        self.laser1.set_volume(.2)
        self.laser2.set_volume(.2)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):
        bullet_list.append(Bullet(self.img, (
            player_rect.centerx + 58 * np.cos(np.deg2rad(player_angle - 20)),
            player_rect.centery - 58 * np.sin(np.deg2rad(player_angle - 20))
            ), (30, 30), player_angle, 100, 'enemy', 1, 20))
        sound = random.choice([self.laser1, self.laser2])
        if sound_on:
            sound.play()
        return bullet_list
    
class RocketLauncher:
    def __init__(self):
        self.img = pygame.image.load('textures/rocket.png').convert_alpha()
        self.sound = pygame.mixer.Sound('sounds/rocket.mp3')
        self.sound.set_volume(.2)

    def shoot(self, enemy_rect, player_angle, bullet_list, sound_on):
        bullet_list.append(Rocket(self.img, (
            enemy_rect.centerx + 58 * np.cos(np.deg2rad(player_angle - 20)),
            enemy_rect.centery - 58 * np.sin(np.deg2rad(player_angle - 20))
            ), (65, 65), player_angle, 250, 'enemy', 1))
        if sound_on:
            self.sound.play()
        return bullet_list
    
class ShotGun:
    def __init__(self, bullet_img, shooter):
        self.img = pygame.image.load('textures/' + bullet_img).convert_alpha()
        self.shooter = shooter
        self.sound1 = pygame.mixer.Sound('sounds/shotgun1.mp3')
        self.sound1.set_volume(.35)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):



        for low in range(1, 5):
            bullet_list.append(Bullet(self.img, (
                player_rect.centerx + 56 * np.cos(np.deg2rad(player_angle - 20)),
                player_rect.centery - 56 * np.sin(np.deg2rad(player_angle - 20))
                ), (30, 30), player_angle + random.randint(-15 * low, 15 * low), 15, self.shooter, 1, 20))
        
        if sound_on:
            self.sound1.play()
        return bullet_list
    
class Akimbo:
    def __init__(self, bullet_img, shooter):
        self.img = pygame.image.load('textures/' + bullet_img).convert_alpha()
        self.shooter = shooter
        self.sound1 = pygame.mixer.Sound('sounds/akimbo1.mp3')
        self.sound1.set_volume(.35)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):


        bullet_list.append(Bullet(self.img, (
            player_rect.centerx + 60 * np.cos(np.deg2rad(player_angle + 25)),
            player_rect.centery - 60 * np.sin(np.deg2rad(player_angle + 25))
            ), (30, 30), player_angle + 15, 40, self.shooter, 1, 20))
        bullet_list.append(Bullet(self.img, (
            player_rect.centerx + 60 * np.cos(np.deg2rad(player_angle - 25)),
            player_rect.centery - 60 * np.sin(np.deg2rad(player_angle - 25))
            ), (30, 30), player_angle - 15, 40, self.shooter, 1, 20))
        
        if sound_on:
            self.sound1.play()
        return bullet_list
    
class TripleGun:
    def __init__(self, bullet_img, shooter):
        self.img = pygame.image.load('textures/'+ bullet_img).convert_alpha()
        self.shooter = shooter
        self.sound1 = pygame.mixer.Sound('sounds/triple1.mp3')
        self.sound1.set_volume(.35)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):
        for mod in [-15, 0, 15]:
            bullet_list.append(Bullet(self.img, (
                player_rect.centerx + 58 * np.cos(np.deg2rad(player_angle - 20)),
                player_rect.centery - 58 * np.sin(np.deg2rad(player_angle - 20))
                ), (30, 30), player_angle + mod, 100, self.shooter, 1, 20))
        if sound_on:
            self.sound1.play()
        return bullet_list
    
class Sniper:
    def __init__(self, bullet_img, shooter):
        self.img = pygame.image.load('textures/' + bullet_img).convert_alpha()
        self.countdown = 0
        self.shooter = shooter
        self.sound1 = pygame.mixer.Sound('sounds/sniper1.mp3')
        self.sound1.set_volume(.2)

    def shoot(self, player_rect, player_angle, bullet_list, sound_on):
        if self.countdown == 0:
            bullet_list.append(Bullet(self.img, (
                player_rect.centerx + 58 * np.cos(np.deg2rad(player_angle - 20)),
                player_rect.centery - 58 * np.sin(np.deg2rad(player_angle - 20))
                ), (30, 30), player_angle, 100, self.shooter, 3, 30))
            self.countdown = 10

            if sound_on:
                self.sound1.play()

        return bullet_list
    
