import pygame

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


def Main(screen, res, gun):

    display = pygame.Surface((1920, 1080), pygame.SRCALPHA)

    font = pygame.font.Font('textures/upheavtt.ttf', 40)

    score_font = pygame.font.Font('textures/upheavtt.ttf', 70)

    yes_button = Button((300, 100), 'YES', font)

    no_button = Button((300, 100), 'NO', font)
    

    background = pygame.image.load('textures/background1.png').convert()
    background_scale = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))

    gun_text = score_font.render('TAKE GUN: {}?'.format(gun), True, (255, 255, 255))
    gun_text_rect = gun_text.get_rect()
    gun_text_rect.center = (1920 / 2, 1080 / 2 - 100)

    selected = False

    while True:
        scale_ratio = (display.get_size()[0] / pygame.display.Info().current_w, display.get_size()[1] / pygame.display.Info().current_h)
        rel_mouse_pos = (pygame.mouse.get_pos()[0] * scale_ratio[0], pygame.mouse.get_pos()[1] * scale_ratio[1])



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if yes_button.rect.collidepoint(rel_mouse_pos):
                        new_gun = True
                        selected = True
                    elif no_button.rect.collidepoint(rel_mouse_pos):
                        new_gun = False
                        selected = True
                    
                        


        if selected:
            break

        screen.blit(background_scale, (0, 0))

        yes_button.render(display, (1920 / 2, 1080 / 2 + 120))
        no_button.render(display, (1920 / 2, 1080 / 2 + 240))
        
        display.blit(gun_text, gun_text_rect)
        
        display_scale = pygame.transform.scale(display, res)
        screen.blit(display_scale, (0, 0))

        pygame.display.update()
    return new_gun
