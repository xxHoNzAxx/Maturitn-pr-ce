import pygame
import random
from trainers import *

shown_cards = []

class Karp:
    def __init__(self, ball, append=True):
        self.ball = ball
        if self.ball == True:
            self.img = pygame.image.load('pictures/maps/Ball.png')
        else:
            self.img = pygame.image.load('pictures/maps/Karp.png')
        if append == True:
            Player1.inventory.append(self)
            Player2.inventory.append(self)

    def draw_back(self, pos):
        shown_cards.clear()
        self.rect = pygame.Rect(pos[0], pos[1], 100, 100)
        pygame.draw.rect(SCREEN, (255,255,255), self.rect)
        pygame.display.update()
    
    def draw_front(self, pos):
        shown_cards.append(self)
        SCREEN.blit(self.img, (pos[0], pos[1], 100, 100))
        pygame.display.update()
    br = False
    @classmethod
    def draw_cards(cls, player, pos):
        cls.br = False
        random.shuffle(player.inventory)
        a = pos[0]
        b = pos[1]
        for i in player.inventory:
            i.draw_back((a, b))
            if a + 130 < 600:
                a += 130
            else:
                a = pos[0]
                b += 130
        pygame.display.update()
        pick = True
        while pick:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    a = pos[0]
                    b = pos[1]
                    for i in player.inventory:
                        if i.rect.collidepoint(mouse_pos):
                            if player.inventory.index(i) < 4:
                                a = pos[0] + player.inventory.index(i)*130
                            elif player.inventory.index(i) < 8:
                                b = pos[1] + 130
                                a = pos[0] + (player.inventory.index(i) - 4)*130
                            else:
                                b = pos[1] + 260
                                a = pos[0] + (player.inventory.index(i) - 8)*130
                            if len(shown_cards) < 3:
                                i.draw_front((a,b))
                            if len(shown_cards) == 3:
                                pick = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pick = False
                    pygame.display.update()

        cls.catch = 0
        for i in shown_cards:
            if i.ball == True:
                cls.catch = 1
        cls.br = True
                
            
karp1 = Karp(False)
karp2 = Karp(False)
karp3 = Karp(False)
karp4 = Karp(False)
karp5 = Karp(False)
karp6 = Karp(False)
karp7 = Karp(False)
karp8 = Karp(False)
karp9 = Karp(False)
ball1 = Karp(True)
ball2 = Karp(True)
ball3 = Karp(True, False)
