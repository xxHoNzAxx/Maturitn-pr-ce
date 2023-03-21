import pygame
from chance import *


class Picture:
    def __init__(self, image, pos, size):
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(pos[0],pos[1], size[0],size[1])
        self.pos = pos
        self.visible = False

    def draw(self):
        SCREEN.blit(self.image, (self.pos))
        

endturn = Picture('pictures/dice/endturn.png', (1300,750), (280,103))
backpack = Picture('pictures/maps/Backpack.png', (1400,600), (100,119))
pc = Picture('pictures/maps/PC.png', (1400,450), (100,119))
badges = Picture('pictures/maps/badge_case.png', (1400,300), (100,119))
back_arrow = Picture('pictures/maps/back_arrow.png', (300,100), (100,100))
swap = Picture('pictures/maps/swap.png', (400,100), (214,90))
cancel = Picture('pictures/maps/cancel.png', (650,100), (214,90))
rules_pic = Picture('pictures/maps/rules.png', (0,800), (100,100))
open_att_guide = Picture('pictures/maps/attack_guide.png', (1000,350), (428,180))

background = pygame.image.load('pictures/maps/map.png')

def load_bg():
    SCREEN.fill((0,100,150))
    SCREEN.blit(background, ((SCREEN.get_width() - 1094) / 2,0))

def load_counter():
    pygame.draw.rect(SCREEN, (255,0,0), pygame.Rect(650,800,150,60))
    pygame.draw.rect(SCREEN, (0,0,255), pygame.Rect(800,800,150,60))
    pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(650,800,300,60), 5)
    text_score1 = FONT.render(str(Player1.lvl), True, (0, 0, 0))
    text_score2 = FONT.render(str(Player2.lvl), True, (0, 0, 0))
    SCREEN.blit(text_score1, (680,805))
    SCREEN.blit(text_score2, (830,805))


def open_backpack(player):
    br = True
    player.backpack_inside = []
    player.backpack_inside.extend(player.backpack)
    player.backpack_inside.extend(player.z_moves)

    player.backpack_inside.sort(key=lambda x: x.type)
    while br == True:
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_arrow.rect.collidepoint(mouse_pos):
                    br = False
                    break
                for i in player.backpack_inside:
                    if i.rect.collidepoint(mouse_pos):
                        i.info_visible = True
                        for j in player.backpack_inside:
                            if j != i:
                                j.info_visible = False

    

        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300,100,1000,650))
        a = 310
        b = 180
        
        for i in player.backpack_inside:
            i.rect = pygame.Rect(a,b,100,100)
            i.rect_visible = True
            pygame.draw.rect(SCREEN, (255,255,255), i.rect)
            SCREEN.blit(i.small_image, (a,b))
            
            a += 110
            if a > 760:
                a = 310
                b += 110
            
            if i.info_visible == True:
                i.draw_info_card((900,100))

        back_arrow.draw()

        pygame.display.update()
    for i in player.backpack_inside:
        i.rect_visible = False
    load_bg()
    load_counter()

def open_pc(player):
    br = True
    while br == True:
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_arrow.rect.collidepoint(mouse_pos):
                    br = False
                    break
                for i in player.mons:
                    if i.rect.collidepoint(mouse_pos):
                        i.pc_visible = True
                        marked_mon = i
                        for j in player.mons:
                            if j != i:
                                j.pc_visible = False

                    if i.pc_visible == True and swap.rect.collidepoint(mouse_pos) and swap.visible == True:
                        swap_on = True
                        marked_mon = i

                        while swap_on == True:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    if cancel.rect.collidepoint(mouse_pos):
                                        swap_on = False

                                        break
                                    for i in player.mons:
                                        if i.rect.collidepoint(mouse_pos):
                                            if player.mons.index(i) > player.mons.index(marked_mon):
                                                player.mons[player.mons.index(i)], player.mons[player.mons.index(marked_mon)] = player.mons[player.mons.index(marked_mon)], player.mons[player.mons.index(i)]
                                            elif player.mons.index(i) < player.mons.index(marked_mon):
                                                player.mons[player.mons.index(marked_mon)], player.mons[player.mons.index(i)] = player.mons[player.mons.index(i)], player.mons[player.mons.index(marked_mon)]
                                            swap_on = False
                                            break
                            cancel.draw()
                            pygame.display.update()


        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300,100,1000,650))
        a = 310
        b = 200
        
        for i in player.mons:
            i.rect = pygame.Rect(a,b,100,100)
            i.rect_visible = True
            pygame.draw.rect(SCREEN, (255,255,255), i.rect)
            i.pc_image = pygame.transform.scale(i.image, (100,100))
            SCREEN.blit(i.pc_image, (a,b))

            if i.pc_visible == True:
                i.draw_info_card((900,100))
                pygame.draw.rect(SCREEN, (0,255,0), pygame.Rect(a,b,100,100), 5)

            a += 110 
            if a > 760:
                a = 310
                b += 110

        back_arrow.draw()
        swap.visible = False
        if isinstance(player.pos[0], GymField):
            swap.visible = True
            swap.draw()

        pygame.display.update()
    for i in player.mons:
        i.rect_visible = False
    load_bg()
    load_counter()

def mega_pick(player, pos):
    mega_offer = []
    if player.mega_count < 2:
        for mon in player.mons:
            if mon.mega == True and mon.lvl == 10:
                mega_offer.append(mon)
        br = True
        if len(mega_offer) == 0:
            br = False
        else:
            offer = random.choice(mega_offer)
        
        while br == True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pass_rect.collidepoint(mouse_pos):
                        br = False
                        break
                    if claim_rect.collidepoint(mouse_pos):
                        offer.mega_evolve()
                        player.mega_count += 1
                        br = False
                        break

            pass_rect = pygame.Rect(pos[0]+225, pos[1]+530, 150, 60)
            text_pass = FONT.render('Pass', True, (0, 0, 0))
            claim_rect = pygame.Rect(pos[0]+25, pos[1]+530, 150, 60)
            text_claim = FONT.render('Claim', True, (0, 0, 0))
            text1 = FONT.render('Do you want to', True, (0, 0, 0))
            text2 = FONT.render('megaevolve ' +offer.name+'?', True, (0, 0, 0))
            text_name = FONT.render(offer.name, True, (0,0,0))
            pygame.draw.rect(SCREEN, (255,255,255), (pos[0], pos[1], 400,600))
            pygame.draw.rect(SCREEN, (200,0,0), pass_rect)
            SCREEN.blit(text_pass, (pos[0]+250, pos[1]+540))
            pygame.draw.rect(SCREEN, (0,200,0), claim_rect)
            SCREEN.blit(text_claim, (pos[0]+50, pos[1]+540))
            SCREEN.blit(text1, (pos[0]+10, pos[1]+300))
            SCREEN.blit(text2, (pos[0]+10, pos[1]+350))
            SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
            SCREEN.blit(offer.image, (pos[0]+70, pos[1]+60))
            pygame.display.update()


def open_badge_case(player):
    br = True

    while br == True:
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_arrow.rect.collidepoint(mouse_pos):
                    br = False
                    break
        count = FONT.render(str(len(player.badge_case))+' / 8', True, (0,0,0))
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300,100,1000,650))
        a = 550
        b = 300
        
        for i in player.badge_case:
            SCREEN.blit(i.image, (a,b))
            
            a += 110
            if a > 950:
                a = 550
                b += 110

        back_arrow.draw()
        SCREEN.blit(count, (750,200))
        pygame.display.update()
    load_bg()
    load_counter()
