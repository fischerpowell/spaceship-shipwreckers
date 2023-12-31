import pygame
import numpy as np

class Bullet:
    def __init__(self, img, pos, size, angle, max_age, shooter, damage, speed):
        self.original_img = img
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rotated_img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.rotated_img.get_rect()
        self.rect.center = pos
        self.speed = speed
        self.angle = angle
        self.active = True
        self.age = 0
        self.max_age = max_age
        self.shooter = shooter
        self.bounced = False
        self.damage = damage

    def move_bullet(self, player):
        delta_x = self.speed * np.cos(np.deg2rad(self.angle))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle))
        self.rect.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)

    def bullet_bounce(self, center_pos):
        delta_x = self.rect.centerx - center_pos[0]
        delta_y = self.rect.centery - center_pos[1]
        try:
            rel_tan = np.rad2deg(np.arctan((delta_y * .444444) / (delta_x * .444444)))
        except ZeroDivisionError:
            rel_tan = np.rad2deg(np.arctan((delta_y * .444444) / ((delta_x + 0.0001) * .444444)))
        rel_surface = rel_tan + 90
        rel_angle = self.angle + rel_surface
        rel_bounce = -rel_angle
        new_angle = rel_bounce - rel_surface
        self.rotated_img = pygame.transform.rotate(self.original_img, new_angle)
        self.angle = new_angle

class Rocket:
    def __init__(self, img, pos, size, angle, max_age, shooter, damage):
        self.original_img = img
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rotated_img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.rotated_img.get_rect()
        self.rect.center = pos
        self.speed = 9
        self.angle = angle
        self.active = True
        self.age = 0
        self.max_age = max_age
        self.shooter = shooter
        self.bounced = False
        self.clockwise = None
        self.damage = damage
        self.break_sound = pygame.mixer.Sound('sounds/rocketbreak.mp3')
        self.break_sound.set_volume(.2)

    def move_bullet(self, player):
        if player.alive and not player.dying and not player.falling:
            dx, dy = (self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if abs(dx) > 0:
                if dx < 0:
                    desired_angle =  - np.rad2deg(np.arctan(dy / dx))
                else:
                    desired_angle =  - np.rad2deg(np.arctan(dy / dx)) + 180
                
            
                if abs((desired_angle - self.angle)) % 360 > 15:
                    if self.clockwise == None:
                        if (self.angle - desired_angle) % 360 > 180:
                            self.clockwise = False
                        else:
                            self.clockwise = True
                    else:
                        if self.clockwise:
                            self.angle -= 3
                        else:
                            self.angle += 3

                else:
                    self.angle = desired_angle
                    self.clockwise = None
            self.rotated_img = pygame.transform.rotate(self.original_img, self.angle)
        delta_x = self.speed * np.cos(np.deg2rad(self.angle))
        delta_y = -self.speed * np.sin(np.deg2rad(self.angle))
        self.rect.center = (self.rect.centerx + delta_x, self.rect.centery + delta_y)

    def bullet_bounce(self, center_pos):
        self.active = False