import pygame
import level_gen
import random
from bullet import Rocket
from guns import Sniper
from player_default import Player
import bosses

class Block:
    def __init__(self, img, pos, size):
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos

class SpecialTile:
    def __init__(self, img, rel_coords, size, type):
        self.rel_coords = rel_coords
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect()
        self.rect.center = (rel_coords[0] * 150 + 275, rel_coords[1] * 150 + 275)
        self.type = type
        self.timer = 0


    def render(self, display):
        display.blit(self.img, self.rect)
        
class Box:
    def __init__(self, img, rel_coords, size):
        self.rel_coords = rel_coords
        self.original_img = pygame.image.load(img).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, size)
        self.rect = self.original_img.get_rect()
        self.rect.center = (rel_coords[0] * 150 + 275, rel_coords[1] * 150 + 275)
        self.hurt_img = pygame.image.load('textures/box_hurt.png').convert_alpha()
        self.hurt_img = pygame.transform.scale(self.hurt_img, size)
        self.hurt_timer = 0
        self.hurt_anim = False
        self.hp = 3
        self.alive = True
        self.break_sound = pygame.mixer.Sound('sounds/boxbreak.mp3')
        self.break_sound.set_volume(.5)
        self.hurt_sound = pygame.mixer.Sound('sounds/boxhurt.mp3')
        self.hurt_sound.set_volume(.75)
        self.item_sound = pygame.mixer.Sound('sounds/boxitem.mp3')
        self.item_sound.set_volume(.5)

    
    def hurt(self):
        if self.alive:
            if self.hurt_timer % 1 == 0:
                self.hurt_anim = True
            elif self.hurt_timer % .5 == 0:
                self.hurt_anim = False
            self.hurt_timer -= 0.125
        else:
            self.hurt_anim = False

    def render(self, display):
        if self.hurt_anim:
            display.blit(self.hurt_img, self.rect)
        else:
            display.blit(self.original_img, self.rect)

class Item:
    def __init__(self, rel_coords, size, type):
        self.type = type
        if self.type == 0:
            self.img = pygame.image.load('textures/hpup.png').convert_alpha()
        elif self.type == 1:
            self.img = pygame.image.load('textures/atomicclock.png').convert_alpha()
        elif self.type == 2:
            self.img = pygame.image.load('textures/jetpack.png').convert_alpha()
        elif self.type == 3:
            self.img = pygame.image.load('textures/uvcoil.png').convert_alpha()
        elif self.type == 4:
            self.img = pygame.image.load('textures/duplicator.png').convert_alpha()
        else:
            self.img = pygame.image.load('textures/item.png').convert_alpha()
        self.img = pygame.transform.rotate(self.img, random.randint(-45, 45))
        self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect()
        self.rect.center = (rel_coords[0] * 150 + 275, rel_coords[1] * 150 + 275)

    def render(self, display):
        display.blit(self.img, self.rect)



        

def map_constructor(level):
    blocks = []
    for row in range(level.size[1]):
        for column in range(level.size[0]):
            if level.map[row][column] in ['B', '@', '%', '!', '8', '$', '&']:
                block_gen = random.randint(0, 10)
                if block_gen == 0:
                    blocks.append(Block('textures/block_rust.png', (column * 150 + 200, row * 150 + 200), (150, 150)))
                elif block_gen in range(1, 4):
                    blocks.append(Block('textures/block_rust_mild.png', (column * 150 + 200, row * 150 + 200), (150, 150)))
                else:
                    blocks.append(Block('textures/block.png', (column * 150 + 200, row * 150 + 200), (150, 150)))
                

    return blocks



def Main(screen, res, clock, player, boss, sound_on):
    pygame.event.set_grab(True)
    display = pygame.Surface((1920, 1080))
    world = pygame.Surface((4150, 4150), pygame.SRCALPHA)
    background = pygame.image.load('textures/' + player.background_img).convert()
    background = pygame.transform.scale(background, (1920, 1080))

    scale_ratio = (display.get_size()[0] / res[0], display.get_size()[1] / res[1])
    if player.levels == 11:
        level = level_gen.Level((len(boss.ship_map[0]), len(boss.ship_map)), 0, 80, 3, preset = boss.ship_map)
    else:
        level = level_gen.Level((len(boss.ship_map[0]), len(boss.ship_map)), 0, 5, 3, preset = boss.ship_map)

    blocks = map_constructor(level)

    start = SpecialTile('textures/start.png', level.start_coords, (75, 75), 'start')
    end = SpecialTile('textures/end.png', level.end_coords, (100, 100), 'end')
    
    camera_pos = (display.get_size()[0] / 2 - player.rect.centerx, display.get_size()[1] / 2 - player.rect.centery)

    hero_bullets = []

    # enemies = [random.choices([RocketEnemy('textures/enemyrocket.png', coords, (126, 82)), DefaultEnemy('textures/enemy.png', coords, (126, 82))], [1, 4], k = 1)[0] for coords in level.enemy_coords]

    enemies = [boss]

    boxes = [Box('textures/box.png', coords, (121, 99)) for coords in level.box_coords]

    enemy_bullets = []

    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])

    interactables = [Item(rel_coords, (75, 75), random.choices([0, 1, 2, 3, 4], weights=[4, 1, 2, 1, 3], k=1)[0]) for rel_coords in level.item_coords]

    wormholes = []

    player.rect.center = start.rect.center
    player.done = False
    player.momentum_x = 0
    player.momentum_y = 0

    if level.wormholes:
        for i in range(2):
            wormholes.append(SpecialTile('textures/wormhole.png', level.wormhole_coords[i], (120, 120), 'wormhole' + str(i)))

    for wormhole in wormholes:
        interactables.append(wormhole)

    score_font = pygame.font.Font('textures/upheavtt.ttf', 50)

    paused_img = pygame.image.load('textures/paused.png').convert_alpha()
    paused_img = pygame.transform.scale(paused_img, (400, 400))
    paused_img_rect = paused_img.get_rect()
    paused_img_rect.center = (res[0] / 2, res[1] / 2)

    paused = False

    frozen_img = pygame.image.load('textures/frozen.png').convert_alpha()
    frozen_img = pygame.transform.scale(frozen_img, (1920, 1080))

    forcefield_img = pygame.image.load('textures/forcefield.png').convert_alpha()
    forcefield_img = pygame.transform.scale(forcefield_img, (128, 128))
    forcefield_rect = forcefield_img.get_rect()

    magnet_img = pygame.image.load('textures/magnet.png').convert_alpha()
    magnet_img = pygame.transform.scale(magnet_img, (150, 150))
    magnet_rect = magnet_img.get_rect()

    blittable_interactables = []   

    grace_timer = 30


    while boss.rect.collidelist(boxes) != -1 or level.map[boss.rel_coords[1]][boss.rel_coords[0]] == '#':
        boss.refresh_coords((random.randint(0, len(boss.ship_map[0]) - 1), random.randint(0, len(boss.ship_map) - 1)))


    while True:
        if not paused:
            player.timer += clock.tick(50) / 1000

            player.added_score = 0

            if type(player.gun) is Sniper:
                if player.gun.countdown != 0:
                    player.gun.countdown -= .5
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if player.alive and not player.dying and not player.falling:
                            hero_bullets = player.gun.shoot(player.rect, player.angle, hero_bullets, sound_on)
                    elif event.button == 3:
                        if not player.dying:
                            blittable_interactables, removed_interactable = player.interact_check(blittable_interactables, wormholes, end, sound_on)
                            if removed_interactable != None:
                                interactables.remove(removed_interactable)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                    if event.key == pygame.K_e:
                        if not player.dying:
                            blittable_interactables, removed_interactable = player.interact_check(blittable_interactables, wormholes, end, sound_on)
                            if removed_interactable != None:
                                interactables.remove(removed_interactable)
                    if event.key == pygame.K_LSHIFT and player.dash_countdown == 0:
                        player.dash_countdown = 10
            camera_pos = (display.get_size()[0] / 2 - player.rect.centerx, display.get_size()[1] / 2 - player.rect.centery)

            if player.dash_countdown > 0:
                player.dash_countdown -= 1


            rel_mouse_pos = (pygame.mouse.get_pos()[0] * scale_ratio[0], pygame.mouse.get_pos()[1] * scale_ratio[1])
            if not player.dying:
                player.change_angle(camera_pos, rel_mouse_pos)
            world.fill((0, 0, 0, 0))
            display.blit(background, (0, 0))

            viewport_range = [
                [round(player.rect.centerx - display.get_size()[0] / 2 - 150), round(player.rect.centerx + display.get_size()[0] / 2 + 150)],
                [round(player.rect.centery - display.get_size()[1] / 2 - 150), round(player.rect.centery + display.get_size()[1] / 2 + 150)]
            ]

            blittable_blocks = blocks

            blittable_enemies = [enemy for enemy in enemies if enemy.alive]

            blittable_boxes = boxes
            for block in blittable_blocks:
                world.blit(block.img, block.rect)


            if not player.jetpack:

                if player.rect.collidelist(blittable_blocks) == -1 and not player.falling:
                    player.falling = True
                    player.saved_img = player.original_img.copy()
                    if sound_on:
                        player.dead_sound.play()
            if 1 in player.effect_types:
                player.frozen = True
            else:
                player.frozen = False

            
            if 2 in player.effect_types:
                player.jetpack = True
            else:
                player.jetpack = False

            if 3 in player.effect_types:
                player.forcefield = True
            else:
                player.forcefield = False

            if grace_timer > 0:
                grace_timer -= 1


            player.block_dict = {}

            for box in blittable_boxes:
                box.render(world)
                if box.alive:
                    player.collision_check(box.rect)
                    bullet_hit = box.rect.collidelist(hero_bullets)
                    if bullet_hit != -1:
                        box.hp -= hero_bullets[bullet_hit].damage
                        box.hurt_timer = 3
                        hero_bullets[bullet_hit].active = False
                        if sound_on:
                            box.hurt_sound.play()
                    bullet_hit = box.rect.collidelist(enemy_bullets)
                    if bullet_hit != -1:
                        box.hp -= enemy_bullets[bullet_hit].damage
                        box.hurt_timer = 3
                        enemy_bullets[bullet_hit].active = False
                        if sound_on:
                            box.hurt_sound.play()

                if box.hp <= 0:
                    if box.alive:
                        box.alive = False

                        box.original_img = pygame.image.load('textures/box_broken.png').convert_alpha()
                        box.original_img = pygame.transform.scale(box.original_img, (150, 150))
                        box.rect = box.original_img.get_rect()
                        box.rect.center = (box.rel_coords[0] * 150 + 275, box.rel_coords[1] * 150 + 275)
                        if bullet_hit == -1:
                            player.added_score += 20
                        if random.randint(0, 2) == 1:
                            if player.hp <= 1:

                                interactables.append(Item(box.rel_coords, (75, 75), random.choices([0, 1, 2, 3, 4], weights=[6, 1, 2, 1, 3], k=1)[0]))
                            else:
                                interactables.append(Item(box.rel_coords, (75, 75), random.choices([0, 1, 2, 3, 4], weights=[4, 1, 2, 1, 3], k=1)[0]))
                            if sound_on:
                                box.item_sound.play()
                        elif sound_on:
                            box.break_sound.play()


                if box.hurt_timer != 0:
                    box.hurt()


            open_dict = {open_key : False for open_key in ['left', 'right', 'up', 'down'] if open_key not in player.block_dict.keys()}

            player.block_dict.update(open_dict)

            start.render(world)

            blittable_interactables = [inter for inter in interactables if inter.rect.topleft[0] in range(viewport_range[0][0], viewport_range[0][1]) and inter.rect.topleft[1] in range(viewport_range[1][0], viewport_range[1][1])]

            for inter in blittable_interactables:
                inter.render(world)
                        
            for enemy in blittable_enemies:
                
                enemy.render(world)
                if not player.frozen:
                    enemy.change_angle(player.rect.center)
                    if player.alive and not player.dying and not player.falling and enemy.clockwise == None and grace_timer == 0:
                        if type(enemy.gun) is Sniper:
                            if enemy.gun.countdown != 0:
                                enemy.gun.countdown -= .5
                        if enemy.strafe_countdown == 0:
                            if random.randint(0, boss.strafe_freq) == 0:
                                enemy.strafe_mod = random.randint(enemy.strafe_range[0], enemy.strafe_range[1])
                                enemy.strafe_countdown = 20
                        else:
                            enemy.strafe_countdown -= 1
                        if enemy.move_countdown != 0:
                            enemy.move(player, blittable_blocks, [tb for tb in blittable_boxes if tb.alive])
                            enemy.move_countdown -= 1
                        else:
                            if random.randint(0, boss.move_freq) == 0:
                                enemy.move_countdown = random.randint(boss.move_range[0], boss.move_range[1])

                        if enemy.contemplate_shooting():
                            enemy_bullets = enemy.gun.shoot(enemy.rect, enemy.angle, enemy_bullets, sound_on)
                bullet_hit = enemy.rect.collidelist(hero_bullets)
                if bullet_hit != -1:
                    enemy.hp -= hero_bullets[bullet_hit].damage
                    enemy.hurt_timer = 3
                    hero_bullets[bullet_hit].active = False
                    if random.choices([True, False], [1, boss.break_mod], k=1)[0]:
                        broken_block = blocks[random.randint(0, len(blocks) - 1)]
                        if broken_block.rect.collidelist(boxes) == -1 and broken_block.rect.collidelist(interactables) == -1 and broken_block.rect.collidelist([player.rect, enemy.rect, end.rect, start.rect]) == -1:
                            blocks.remove(broken_block)
                    if enemy.hp <= 0:
                        player.added_score += 100
                        enemy.alive = False
                        interactables.append(end)
                        if sound_on:
                            enemy.dead_sound.play()
                    elif sound_on:
                        enemy.hurt_sound.play()
                friendly_hit = enemy.rect.collidelist(enemy_bullets)
                if friendly_hit != -1:
                    if enemy_bullets[friendly_hit].age >= enemy_bullets[friendly_hit].max_age:
                        enemy.hp -= enemy_bullets[friendly_hit].damage
                        enemy.hurt_timer = 3
                        enemy_bullets[bullet_hit].active = False
                        if enemy.hp <= 0:
                            player.added_score += 100
                            interactables.append(end)
                            if sound_on:
                                enemy.dead_sound.play()
                        elif sound_on:
                            enemy.hurt_sound.play()
                if enemy.hurt_timer != 0:
                    enemy.hurt()


            if player.wormhole_timer > 0:
                player.wormhole_timer -= 1      

            if player.hurt_timer != 0:
                player.hurt()

            if player.falling and player.original_img.get_size()[0] >= 1:
                player.fall()
                player.forcefield = False
            elif player.falling and player.original_img.get_size()[0] < 1:
                if player.revive_count > 0:
                    player.original_img = player.saved_img.copy()
                    player.set_revive(player.revive_count - 1)
                    player.rect.center = start.rect.center
                    player.falling = False
                    player.rect.center = start.rect.center
                    player.momentum_x = 0
                    player.momentum_y = 0
                    player.hp_img = pygame.image.load('textures/health3.png').convert_alpha()
                    player.hp_img = pygame.transform.scale(player.hp_img, (250, 100))
                    player.hp = 3
                    if sound_on:
                        player.revive_sound.play()
                else:

                    player.alive = False

            if player.dying:
                if player.die_timer <= 0:
                    if player.revive_count > 0:
                        player.set_revive(player.revive_count - 1)
                        player.original_img = player.saved_img.copy()
                        player.rect.center = start.rect.center
                        player.hp_img = pygame.image.load('textures/health3.png').convert_alpha()
                        player.hp_img = pygame.transform.scale(player.hp_img, (250, 100))
                        player.hp = 3
                        player.dying = False
                        player.original_img = player.saved_img.copy()
                        player.rect.center = start.rect.center
                        player.momentum_x = 0
                        player.momentum_y = 0
                        if sound_on:
                            player.revive_sound.play()
                    else:
                        player.alive = False

                else:
                    player.die_timer -= 1


            if len(player.status_effects) > 0:
                player.status_check()

            if player.alive:
                if player.jetpack:
                    magnet_rect.center = player.rect.center
                    world.blit(magnet_img, magnet_rect)
                if player.forcefield:
                    forcefield_rect.center = player.rect.center
                    world.blit(forcefield_img, forcefield_rect)
                player.render(world)
                if not player.falling and not player.dying:
                    camera_pos = player.move(camera_pos)

            for bullet in hero_bullets:
                if bullet.active:
                    bullet.age += 1
                    bullet.move_bullet(player)
                    if bullet.rect.x in range(viewport_range[0][0], viewport_range[0][1]) and bullet.rect.y in range(viewport_range[1][0], viewport_range[1][1]):
                        world.blit(bullet.rotated_img, bullet.rect)
                    if bullet.age >= bullet.max_age:
                        bullet.active = False
                else:
                    hero_bullets.remove(bullet)

            for bullet in enemy_bullets:
                if bullet.active:
                    if type(bullet) is Rocket:
                        bullet_col = bullet.rect.collidelist(hero_bullets)
                        if bullet_col != -1:
                            bullet.active = False
                            hero_bullets[bullet_col].active = False
                    if not player.frozen:
                        bullet.age += 1
                        bullet.move_bullet(player)
                    if bullet.rect.x in range(viewport_range[0][0], viewport_range[0][1]) and bullet.rect.y in range(viewport_range[1][0], viewport_range[1][1]):
                        world.blit(bullet.rotated_img, bullet.rect)
                    if bullet.age >= bullet.max_age:
                        bullet.active = False
                    if not player.forcefield:
                        if player.rect.collidepoint(bullet.rect.center):
                                if not player.dying and not player.falling:
                                    if sound_on:
                                        player.hurt_sound.play()
                                    player.hp -= bullet.damage
                                    player.hurt_timer = 3
                                    if player.hp >= 0:
                                        player.hp_img = pygame.image.load('textures/health{}.png'.format(player.hp)).convert_alpha()
                                    else:
                                        player.hp_img = pygame.image.load('textures/health0.png').convert_alpha()
                                    player.hp_img = pygame.transform.scale(player.hp_img, (250, 100))
                                    bullet.active = False
                                    if player.hp <= 0:
                                        player.saved_img = player.original_img.copy()
                                        player.die_timer = 75
                                        player.dying = True
                                        player.die(sound_on)
                    else:
                        if forcefield_rect.collidepoint(bullet.rect.center):
                                if not bullet.bounced:
                                    bullet.bullet_bounce(forcefield_rect.center)
                                    bullet.bounced = True
        
                        else:
                            bullet.bounced = False
                            
                else:
                    enemy_bullets.remove(bullet)
            display.blit(world, camera_pos)

            effect_counter = 0

            if player.frozen:
                display.blit(frozen_img, (0, 0))

            for effect_type in player.effect_types:
                for effect in player.status_effects:
                    if effect.type == effect_type:
                        effect.render(display, (display.get_size()[0] - 25, effect_counter * 125 + 25))
                        effect_counter += 1
                        break

            if player.done:
                player.added_score += 200

            if 4 in player.effect_types:
                player.added_score *= 2


            player.score += player.added_score

            if player.done or not player.alive:
                break

            player.render_hp(display)
            player.render_revive(display)

            score_text = score_font.render('SCORE: {}'.format(player.score), True, (255, 255, 255))
            display.blit(score_text, (25, 135))

            level_text = score_font.render('LEVEL: {}'.format(player.levels), True, (255, 255,255))
            display.blit(level_text, (25, 185))

            timer_text = score_font.render('TIME: {}'.format(round(player.timer, 2)), True, (255, 255,255))
            display.blit(timer_text, (25, 235))

            display_scale = pygame.transform.scale(display, res)

            
            screen.blit(display_scale, (0, 0))
            

            pygame.display.update()
        else:
            pygame.event.set_grab(False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.set_grab(True)
                        paused = False
            screen.blit(paused_img, paused_img_rect)
            pygame.display.update()

if __name__ == '__main__':
    Main(pygame.display.set_mode((1920, 1080)), (1920, 1080), 0, Player('textures/playershoulder1.png', (126, 82), (0, 0)), bosses.ShotGunBoss('textures/enemy.png', (1, 1), (126, 82)))