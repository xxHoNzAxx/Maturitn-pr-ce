import pygame
from attacks import attacks_guide
from backpack import open_att_guide, load_bg, load_counter

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)

def rules():
    rules = True
    turnoff_rules = pygame.image.load('pictures/maps/back_arrow.png')
    turnoff_rules_rect = pygame.Rect(0,0,100,100)
    while rules == True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if turnoff_rules_rect.collidepoint(mouse_pos):
                    rules = False
                    break
                if open_att_guide.rect.collidepoint(mouse_pos):
                    attacks_guide()
        
        SCREEN.fill((0,0,0))
        SCREEN.blit(turnoff_rules, (0,0))
        open_att_guide.draw()
        pygame.display.update()
    load_bg()
    load_counter()


