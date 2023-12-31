# try:
import game
import pygame
import start
import game_over
from player_default import Player
from guns import DefaultGun, ShotGun, Akimbo, TripleGun, Sniper
import boss_level
import bosses
import random
import new_gun
import end_game
from random import shuffle

def next_song(song_queue, song_num, mixer):
    song_num += 1
    mixer.stop()
    try:
        mixer.load(song_queue[song_num])
        mixer.play(loops=-1)
        return song_num
    except IndexError:
        mixer.load(song_queue[0])
        mixer.play(loops=-1)
        return 0
    


pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init()

pygame.mixer.init()

pygame.display.set_caption('Spaceship Shipwreckers')

mode = 0

res = (2560, 1440)




pygame.display.set_icon(pygame.image.load("textures/end.png"))


music_list = ['music/akimbo_1.ogg', 'music/beginning.ogg', 'music/end_1.ogg', 'music/mars.ogg', 'music/snipe.ogg']
song = -1


while True:
    if mode == 0:
        pygame.event.set_grab(False)
        display = pygame.display.set_mode(res, pygame.FULLSCREEN)
        sound_on, music_on = start.Main(display, res)
        if music_on:
            pygame.mixer.music.set_volume(.15)
        else:
            pygame.mixer.music.set_volume(0)

        
        mode = 1

    elif mode == 1:
        pygame.event.set_grab(True)
        display = pygame.display.set_mode(res, pygame.FULLSCREEN)
        clock = pygame.time.Clock()

        player = Player('textures/playershoulder1.png', (126, 82), (0, 0))
        player.gun = DefaultGun()
        shuffle(music_list)


        

        song = next_song(music_list, song, pygame.mixer.music)


        game.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, sound_on)
        


        while player.alive:
            game.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, sound_on)



            if player.levels == 3:
                player.background_img = 'background2.png'
                boss_level.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, bosses.ShotGunBoss('textures/sgboss.png', (random.randint(0, 9), random.randint(0, 9)), (145, 94)), sound_on)
                song = next_song(music_list, song, pygame.mixer.music)

            
            if player.levels == 7:
                player.background_img = 'background3.png'
                boss_level.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, bosses.AkimboBoss('textures/akboss.png', (random.randint(0, 7), random.randint(0, 11)), (116, 74)), sound_on)
                song = next_song(music_list, song, pygame.mixer.music)
                

            if player.levels == 11:
                player.background_img = 'background4.png'
                boss_level.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, bosses.SniperBoss('textures/sniperboss.png', (random.randint(0, 13), random.randint(0, 13)), (126, 82)), sound_on)
                song = next_song(music_list, song, pygame.mixer.music)

            if player.levels == 15:
                player.background_img = 'background5.png'
                boss_level.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), clock, player, bosses.TripleBoss('textures/tripleboss.png', (random.randint(0, 13), random.randint(0, 13)), (126, 82)), sound_on)
                song = next_song(music_list, song, pygame.mixer.music)

            if player.levels == 4 and player.alive:
                player.score += 1000
                if new_gun.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), 'SHOTGUN'):
                    player.original_img = pygame.image.load('textures/playershouldersg.png').convert_alpha()
                    player.original_img = pygame.transform.scale(player.original_img, (126, 82))
                    player.hurt_img = pygame.image.load('textures/playerhurtsg.png').convert_alpha()
                    player.hurt_img = pygame.transform.scale(player.hurt_img, (126, 82))
                    player.gun = ShotGun('bullet_hero.png', 'hero')

            if player.levels == 8 and player.alive:
                player.score += 1000
                if new_gun.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), 'GUNS AKIMBO'):
                    player.original_img = pygame.image.load('textures/playershoulderak.png').convert_alpha()
                    player.original_img = pygame.transform.scale(player.original_img, (129, 82))
                    player.hurt_img = pygame.image.load('textures/playerhurtak.png').convert_alpha()
                    player.hurt_img = pygame.transform.scale(player.hurt_img, (129, 82))
                    player.gun = Akimbo('bullet_hero.png', 'hero')

            if player.levels == 12 and player.alive:
                player.score += 1000
                if new_gun.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), 'SNIPER RIFLE'):
                    player.original_img = pygame.image.load('textures/playersniper.png').convert_alpha()
                    player.original_img = pygame.transform.scale(player.original_img, (129, 82))
                    player.hurt_img = pygame.image.load('textures/playersniperhurt.png').convert_alpha()
                    player.hurt_img = pygame.transform.scale(player.hurt_img, (129, 82))
                    player.gun = Sniper('bullet_hero.png', 'hero')


            if player.levels == 16 and player.alive:
                if end_game.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h)):
                    player.score += 2000
                    player.alive = False
                    break
                if new_gun.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), 'SPLIT END RIFLE'):
                    player.score += 2000
                    player.original_img = pygame.image.load('textures/playertriplegun.png').convert_alpha()
                    player.original_img = pygame.transform.scale(player.original_img, (129, 82))
                    player.hurt_img = pygame.image.load('textures/playertriplegunhurt.png').convert_alpha()
                    player.hurt_img = pygame.transform.scale(player.hurt_img, (129, 82))
                    player.gun = TripleGun('bullet_hero.png', 'hero')


        mode = 2

    elif mode == 2:
        pygame.event.set_grab(False)
        pygame.mixer.music.stop()
        time_bonus = round(player.levels / player.timer * 2000)
        player.final_score = round(player.score + time_bonus)
        mode = game_over.Main(display, (pygame.display.Info().current_w, pygame.display.Info().current_h), player, time_bonus)
        

# except:
#     pass