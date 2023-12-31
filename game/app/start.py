import pygame
import random

class Button:
    def __init__(self, size, text, font):
        self.img = pygame.image.load('textures/button.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, size)
        self.font = font
        self.text = text
        text = self.font.render(text, True, (255, 255 ,255))
        text_rect = text.get_rect()
        text_rect.center = (size[0] / 2, size[1] / 2)
        self.img.blit(text, text_rect)
        self.rect = self.img.get_rect()
        
    def render(self, display, pos):
        self.rect.center = pos
        display.blit(self.img, self.rect)


def Main(screen, res):
    display = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    font = pygame.font.Font('textures/upheavtt.ttf', 40)

    start_button = Button((300, 100), 'Start Game', font)

    start_game = False

    quit_button = Button((300, 100), 'Quit', font)

    background = pygame.image.load('textures/background1.png').convert()
    background_scale = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))

    logo = pygame.image.load('textures/logo.png').convert_alpha()
    logo = pygame.transform.scale(logo, (1000, 500))
    logo_rect = logo.get_rect()

    planet1 = pygame.image.load('textures/' + random.choice(['mars.png', 'tech.png'])).convert_alpha()
    planet1 = pygame.transform.scale(planet1, (150, 150))

    planet2 = pygame.image.load('textures/' + random.choice(['blueplanet.png', 'green.png'])).convert_alpha()
    planet2 = pygame.transform.scale(planet2, (125, 125))

    sound_on = True

    sound_button = pygame.image.load('textures/soundon.png').convert_alpha()
    sound_rect = sound_button.get_rect()
    sound_rect.center = (1820, 980)

    music_on = True

    music_button = pygame.image.load('textures/musicon.png').convert_alpha()
    music_rect = music_button.get_rect()
    music_rect.center = (1650, 980)


    while True:
        scale_ratio = (display.get_size()[0] / pygame.display.Info().current_w, display.get_size()[1] / pygame.display.Info().current_h)
        rel_mouse_pos = (pygame.mouse.get_pos()[0] * scale_ratio[0], pygame.mouse.get_pos()[1] * scale_ratio[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.rect.collidepoint(rel_mouse_pos):
                        start_game = True
                    elif quit_button.rect.collidepoint(rel_mouse_pos):
                        pygame.quit()
                    elif sound_rect.collidepoint(rel_mouse_pos):
                        if sound_on:
                            sound_on = False
                            sound_button = pygame.image.load('textures/soundoff.png').convert_alpha()
                        else:
                            sound_on = True
                            sound_button = pygame.image.load('textures/soundon.png').convert_alpha()

                    elif music_rect.collidepoint(rel_mouse_pos):
                        if music_on:
                            music_on = False
                            music_button = pygame.image.load('textures/musicoff.png').convert_alpha()
                        else:
                            music_on = True
                            music_button = pygame.image.load('textures/musicon.png').convert_alpha()

        if start_game:
            return (sound_on, music_on)

        background_scale = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        screen.blit(background_scale, (0, 0))

        start_button.render(display, (1920 / 2, 1080 / 2 + 140))
        quit_button.render(display, (1920 / 2, 1080 / 2 + 260))
        logo_rect.center = (1920 / 2, 1080 / 2 - 250)
        display.blit(logo, logo_rect)
        
        display.blit(planet1, (1550, 450))
        display.blit(planet2, (400, 850))

        display.blit(sound_button, sound_rect)
        display.blit(music_button, music_rect)

        display_scale = pygame.transform.scale(display, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        screen.blit(display_scale, (0, 0))

        pygame.display.update()