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
        self.rect = self.img.get_rect()
        self.img.blit(text, text_rect)
        
        
    def render(self, display, pos):
        self.rect.center = pos
        display.blit(self.img, self.rect)


def Main(screen, res, player, time_bonus):

    display = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    font = pygame.font.Font('textures/upheavtt.ttf', 40)

    score_font = pygame.font.Font('textures/upheavtt.ttf', 70)

    start_button = Button((300, 100), 'Start Over', font)

    menu_button = Button((300, 100), 'Main Menu', font)
    

    quit_button = Button((300, 100), 'Quit', font)

    background = pygame.image.load('textures/background1.png').convert()
    background_scale = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))

    start_over = False

    main_menu = False

    level_text = score_font.render('LEVELS COMPLETE: {}'.format(player.levels), True, (255, 255, 255))
    level_text_rect = level_text.get_rect()
    level_text_rect.center = (1920 / 2, 1080 / 2 - 400)

    timer_text = score_font.render('TIME ALIVE: {} SECONDS'.format(round(player.timer, 2)), True, (255, 255, 255))
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.center = (1920 / 2, 1080 / 2 - 300)

    game_score = player.score + player.score_delta
    final_score = game_score + time_bonus


    score_text = score_font.render('GAME SCORE: {}'.format(game_score), True, (255, 255, 255))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (1920 / 2, 1080 / 2 - 200)

    time_text = score_font.render('TIME BONUS: {}'.format(time_bonus), True, (255, 255, 255))
    time_text_rect = time_text.get_rect()
    time_text_rect.center = (1920 / 2, 1080 / 2 - 100)

    # print('-----------')
    # print(player.score)
    # print(player.score_delta)

    final_score_text = score_font.render('FINAL SCORE: {}'.format(final_score), True, (255, 255, 255))
    final_score_text_rect = final_score_text.get_rect()
    final_score_text_rect.center = (1920 / 2, 1080 / 2)

    planet1 = pygame.image.load('textures/' + random.choice(['mars.png', 'tech.png'])).convert_alpha()
    planet1 = pygame.transform.scale(planet1, (150, 150))

    planet2 = pygame.image.load('textures/' + random.choice(['blueplanet.png', 'green.png'])).convert_alpha()
    planet2 = pygame.transform.scale(planet2, (125, 125))

    while True:
        scale_ratio = (display.get_size()[0] / pygame.display.Info().current_w, display.get_size()[1] / pygame.display.Info().current_h)
        rel_mouse_pos = (pygame.mouse.get_pos()[0] * scale_ratio[0], pygame.mouse.get_pos()[1] * scale_ratio[1])



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.rect.collidepoint(rel_mouse_pos):
                        start_over = True
                    elif menu_button.rect.collidepoint(rel_mouse_pos):
                        main_menu = True
                    elif quit_button.rect.collidepoint(rel_mouse_pos):
                        pygame.quit()


        if start_over or main_menu:
            break

        screen.blit(background_scale, (0, 0))

        start_button.render(display, (1920 / 2, 1080 / 2 + 120))
        menu_button.render(display, (1920 / 2, 1080 / 2 + 240))
        quit_button.render(display, (1920 / 2, 1080 / 2 + 360))
        
        display.blit(level_text, level_text_rect)
        display.blit(timer_text, timer_text_rect)
        display.blit(score_text, score_text_rect)
        display.blit(time_text, time_text_rect)
        display.blit(final_score_text, final_score_text_rect)
        
        display.blit(planet1, (1450, 400))
        display.blit(planet2, (400, 850))

        display_scale = pygame.transform.scale(display, res)
        screen.blit(display_scale, (0, 0))

        pygame.display.update()
    if start_over:
        return 1
    elif main_menu:
        return 0