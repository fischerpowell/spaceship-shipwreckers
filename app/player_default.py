import pygame
import numpy as np
from status_effect import StatusEffect
from guns import DefaultGun


class Player:

    def __init__(self, img, size, pos):
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.saved_img = None

        self.rect = self.original_img.get_rect()
        self.rect.center = pos
        self.momentum_x = 0
        self.momentum_y = 0
        self.angle = 0
        self.alive = True
        self.hp = 3
        self.hp_img = pygame.image.load('textures/health{}.png'.format(self.hp)).convert_alpha()
        self.hp_img = pygame.transform.scale(self.hp_img, (250, 100))
        self.hp_rect = self.hp_img.get_rect()
        self.revive_img = pygame.image.load('textures/revive.png').convert_alpha()
        self.revive_img = pygame.transform.scale(self.revive_img, (90, 90))
        self.revive_rect = self.revive_img.get_rect()
        self.revive_count = 0
        self.revive_font = pygame.font.Font('textures/upheavtt.ttf', 40)
        self.revive_text = self.revive_font.render("x0", True, (255, 255, 255))
        
        self.hurt_img = pygame.image.load('textures/playerhurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.rotated_rect = self.rect
        self.done = False
        self.used_interactable = False
        self.status_effects = set()
        self.effect_types = []
        self.score = 0
        self.falling = False
        self.levels = 0
        self.timer = 0
        self.final_score = 0
        self.dying = False
        self.die_timer = 0
        self.wormhole_timer = 0
        self.forcefield = False
        self.frozen = False
        self.jetpack = False
        self.gun = DefaultGun
        self.added_score = 0
        self.background_img = 'background1.png'
        self.dash_countdown = 0
        self.pickup_sound = pygame.mixer.Sound('sounds/pickup.mp3')
        self.pickup_sound.set_volume(.3)
        self.hurt_sound = pygame.mixer.Sound('sounds/playerhurt.mp3')
        self.hurt_sound.set_volume(.5)
        self.dead_sound = pygame.mixer.Sound('sounds/playerdead.mp3')
        self.dead_sound.set_volume(.28)
        self.revive_sound = pygame.mixer.Sound('sounds/revive.mp3')
        self.revive_sound.set_volume(.38)
        self.no_vend_sound = pygame.mixer.Sound('sounds/no_vend.mp3')
        self.no_vend_sound.set_volume(.75)
        self.vend_sound = pygame.mixer.Sound('sounds/vend.mp3')
        self.vend_sound.set_volume(.75)
        self.wormhole_sound = pygame.mixer.Sound('sounds/wormhole.mp3')
        self.wormhole_sound.set_volume(.5)
        self.win_sound = pygame.mixer.Sound('sounds/warp.mp3')
        self.win_sound.set_volume(.4)
        self.score_delta = 0

    def move(self, camera_pos):
        pos_x, pos_y = camera_pos

        max_speed = 12

        x_input = False
        y_input = False

        key = pygame.key.get_pressed()
        
        if key[pygame.K_w]:
            if self.momentum_y >= -max_speed:
                self.momentum_y -= .5
            y_input = True
        if key[pygame.K_a]:
            if self.momentum_x >= -max_speed:
                self.momentum_x -= .5
            x_input = True
        if key[pygame.K_s]:
            if self.momentum_y <= max_speed:
                self.momentum_y += .5
            y_input = True
        if key[pygame.K_d]:
            if self.momentum_x <= max_speed:
                self.momentum_x += .5
            x_input = True

        
        if not x_input:
            if self.momentum_x > 0:
                self.momentum_x -= .5
            elif self.momentum_x < 0:
                self.momentum_x += .5
        if not y_input:
            if self.momentum_y > 0:
                self.momentum_y -= .5
            elif self.momentum_y < 0:
                self.momentum_y += .5
        
        dash_mod = 1

        if not self.block_dict['left'] and not self.block_dict['right']:
            if self.dash_countdown > 0 and self.momentum_x != 0:
                if self.momentum_x > 0:
                    self.momentum_x += dash_mod
                else:
                    self.momentum_x -= dash_mod
            elif abs(self.momentum_x) > max_speed:
                if self.momentum_x > 0:
                    self.momentum_x = max_speed
                else:
                    self.momentum_x = -max_speed
                
            self.rect.x += self.momentum_x
            pos_x -= self.momentum_x
        else:
            if self.block_dict['left']:
                if self.momentum_x > 0:
                    self.rect.x += self.momentum_x
                    pos_x -= self.momentum_x
                elif self.momentum_x < 0:
                    self.momentum_x = 0
            if self.block_dict['right']:
                if self.momentum_x < 0:
                    self.rect.x += self.momentum_x
                    pos_x -= self.momentum_x
                elif self.momentum_x > 0:
                    self.momentum_x = 0
            


        if not self.block_dict['up'] and not self.block_dict['down']:
            if self.dash_countdown > 0 and self.momentum_y != 0:
                if self.momentum_y > 0:
                    self.momentum_y += dash_mod
                else:
                    self.momentum_y -= dash_mod
            elif abs(self.momentum_y) > max_speed:
                if self.momentum_y > 0:
                    self.momentum_y = max_speed
                else:
                    self.momentum_y = -max_speed
            self.rect.y += self.momentum_y
            pos_y -= self.momentum_y
                
        else:
            if self.block_dict['up']:
                if self.momentum_y > 0:
                    self.rect.y += self.momentum_y
                    pos_y -= self.momentum_y
                elif self.momentum_y < 0:
                    self.momentum_y = 0
            if self.block_dict['down']:
                if self.momentum_y < 0:
                    self.rect.y += self.momentum_y
                    pos_y -= self.momentum_y
                elif self.momentum_y > 0:
                    self.momentum_y = 0



        return (pos_x, pos_y)

    def change_angle(self, camera_pos, mouse_pos):
        mouse_pos = (camera_pos[0] - mouse_pos[0], camera_pos[1] - mouse_pos[1])
        delta_x, delta_y = (self.rect.centerx + mouse_pos[0], self.rect.centery + mouse_pos[1])
        if abs(delta_x) > 0:
            if delta_x < 0:
                self.angle =  - np.rad2deg(np.arctan(delta_y / delta_x))
            else:
                self.angle =  - np.rad2deg(np.arctan(delta_y / delta_x)) + 180
            
    def fall(self):
        self.original_img = pygame.transform.scale(self.original_img, tuple([size * .9 for size in self.original_img.get_size()]))

    
    def die(self, sound_on):
        if sound_on:
            self.dead_sound.play()
        pos = self.rect.center
        self.original_img = pygame.image.load('textures/playerdead.png').convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, (150, 150))
        self.rect = self.original_img.get_rect()
        self.rect.center = pos
    

    def hurt(self):
        if self.hurt_timer % 1 == 0:
            self.hurt_anim = True
        elif self.hurt_timer % .5 == 0:
            self.hurt_anim = False
        self.hurt_timer -= 0.125

    def collision_check(self, check_rect):
        if check_rect.collidepoint(self.rotated_rect.midbottom):
            self.block_dict['down'] = True
        if check_rect.collidepoint(self.rotated_rect.midtop):
            self.block_dict['up'] = True
        if check_rect.collidepoint(self.rotated_rect.midleft):
            self.block_dict['left'] = True
        if check_rect.collidepoint(self.rotated_rect.midright):
            self.block_dict['right'] = True

    def interact_check(self, interactables, wormholes, end, sound_on):
        inter_num = self.rect.collidelist(interactables)
        removed_interactable = None
        if inter_num != -1:
            interactable = interactables[inter_num]
            self.interact(interactable, sound_on)
            if not 'wormhole' in str(interactable.type):
                if interactable.type != 'end':
                    interactables.remove(interactable)
                    removed_interactable = interactable
                    if not "vending" in str(interactable.type):
                        self.added_score += 15

            else:
                if self.wormhole_timer == 0:
                    if '1' in str(interactable.type):
                        self.rect.center = wormholes[0].rect.center
                    else:
                        self.rect.center = wormholes[1].rect.center
                    self.momentum_x = 0
                    self.momentum_y = 0
                    self.wormhole_timer = 40
                    if sound_on:
                        self.wormhole_sound.play()

        return interactables, removed_interactable

    
    def interact(self, interactable, sound_on):
        if interactable.type == 'end':
            self.levels += 1
            self.done = True
            if sound_on:
                self.win_sound.play()
        elif 'vending-' in str(interactable.type):
            vending_price = int(interactable.type.removeprefix('vending-'))
            if self.score >= vending_price:

                
                self.score_delta += vending_price

                self.set_revive(self.revive_count + 1)
                self.score -= vending_price
                interactable.type = 'used-vending'
                if sound_on:
                    self.vend_sound.play()
            else:
                if sound_on:
                    self.no_vend_sound.play()

        elif interactable.type == 0:
            if self.hp < 3:
                self.hp += 1
                self.hp_img = pygame.image.load('textures/health{}.png'.format(self.hp)).convert_alpha()
                self.hp_img = pygame.transform.scale(self.hp_img, (250, 100))
            self.status_effects.add(StatusEffect(0, 70, (125, 125)))
            if sound_on:
                self.pickup_sound.play()
        elif interactable.type == 1:
            self.status_effects.add(StatusEffect(1, 100, (125, 125)))
            if sound_on:
                self.pickup_sound.play()
        elif interactable.type == 2:
            self.status_effects.add(StatusEffect(2, 110, (125, 125)))
            if sound_on:
                self.pickup_sound.play()
        elif interactable.type == 3:
            self.status_effects.add(StatusEffect(3, 150, (125, 125)))
            if sound_on:
                self.pickup_sound.play()
        elif interactable.type == 4:
            self.status_effects.add(StatusEffect(4, 320, (125, 125)))
            if sound_on:
                self.pickup_sound.play()
        return interactable

    def status_check(self):
        current_effects = set()
        current_types = set()
        for effect in self.status_effects:
            effect.countdown()
            if effect.timer > 0:
                current_effects.add(effect)
                current_types.add(effect.type)
        self.status_effects = current_effects
        current_types = list(current_types)
        current_types.sort(reverse = True)
        self.effect_types = current_types

    def render(self, display):
        if self.hurt_anim == True:
            self.img = pygame.transform.rotate(self.hurt_img, self.angle)
        else:
            self.img = pygame.transform.rotate(self.original_img, self.angle)

        self.rotated_rect = self.img.get_rect(center = (round(self.rect.centerx), round(self.rect.centery)))
        display.blit(self.img, self.rotated_rect)


    def render_hp(self, display):
        display.blit(self.hp_img, (25, 25))

    def set_revive(self, new_value):
        self.revive_count = new_value
        self.revive_text = self.revive_font.render(f"x {new_value}", True, (255, 255, 255))



    def render_revive(self, display):
        if self.revive_count > 0:
            display.blit(self.revive_img, (300, 25))
            display.blit(self.revive_text, (385, 25))
        
    