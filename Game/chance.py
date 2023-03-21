import pygame
import random
from cards import *

class Chance:
    def __init__(self, name, type, zname=''):
        self.name = name
        self.image = pygame.image.load('pictures/chance/'+self.name+'.png')
        self.type = type
        self.zname = zname
        if self.type == 'zcrystal':
            self.zname = zname
        chance_list.append(self)
        self.small_image = pygame.transform.scale(self.image, (100,100))
        self.info_visible = False
        self.br = False

    def draw_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        SCREEN.blit(self.image, (pos[0]+40, pos[1]+30))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        SCREEN.blit(text_name, (pos[0]+60, pos[1]+20))
        self.claim_rect = pygame.Rect(pos[0]+130, pos[1]+500, 150, 60)
        text_claim = FONT.render('Claim', True, (0, 0, 0))
        self.claim_visible = True
        
        pygame.draw.rect(SCREEN, (0, 200, 0), self.claim_rect)
        SCREEN.blit(text_claim, (pos[0]+150, pos[1]+505))
        pygame.display.update()
    
    def draw_info_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1], 1, 600))
        SCREEN.blit(self.image, (pos[0]+40, pos[1]+30))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        SCREEN.blit(text_name, (pos[0]+60, pos[1]+20))

        if self.type == 'beast_ball':
            text1 = FONT.render('Can catch Ultra Beast', True, (0, 0, 0))
            SCREEN.blit(text1, (pos[0]+10, pos[1]+400))
        elif self.type == 'zcrystal':
            text1 = FONT.render('Your pokemon with', True, (0, 0, 0))
            text2 = FONT.render('same first attack type', True, (0, 0, 0))
            text3 = FONT.render('as this crystal, can', True, (0, 0, 0))
            text4 = FONT.render('use Z move', True, (0, 0, 0))
            SCREEN.blit(text1, (pos[0]+10, pos[1]+350))
            SCREEN.blit(text2, (pos[0]+10, pos[1]+400))
            SCREEN.blit(text3, (pos[0]+10, pos[1]+450))
            SCREEN.blit(text4, (pos[0]+10, pos[1]+500))

    def hit(self):
        return 1


    def do_something(self, player, trainer):
        self.br = False
        if self.type == 'zcrystal':
            player.z_moves.append(self)
            chance_list.remove(self)
            self.br = True
        
        elif self.type == 'mon_spawn':
            if player.pos[0].location == 'orange':
                self.spawn = random.choice(orange_spawn)
            elif player.pos[0].location == 'gray':
                self.spawn = random.choice(gray_spawn)
            elif player.pos[0].location == 'blue':
                self.spawn = random.choice(blue_spawn)
            elif player.pos[0].location == 'green':
                self.spawn = random.choice(green_spawn)
            elif player.pos[0].location == 'yellow':
                self.spawn = random.choice(yellow_spawn)
            elif player.pos[0].location == 'purple':
                self.spawn = random.choice(purple_spawn)
            elif player.pos[0].location == 'white':
                self.spawn = random.choice(white_spawn)
            elif player.pos[0].location == 'brown':
                self.spawn = random.choice(brown_spawn)

            while True:
                br = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.spawn.catch_visible == True:
                            if self.spawn.catch_rect.collidepoint(mouse_pos):
                                self.spawn.catch_visible = False
                                self.spawn.fight_visible = False
                                Karp.draw_cards(player, (200,100))
                                if Karp.catch > 0:
                                    player.mons.append(self.spawn)
                                    if player.pos[0].location == 'orange':
                                        orange_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'gray':
                                        gray_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'blue':
                                        blue_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'green':
                                        green_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'yellow':
                                        yellow_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'purple':
                                        purple_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'white':
                                        white_spawn.remove(self.spawn)
                                    elif player.pos[0].location == 'brown':
                                        brown_spawn.remove(self.spawn)
                                    
                                    br = True
                                    break
                                else:
                                    br = True
                                    break
                        if self.spawn.fight_visible == True:
                                if self.spawn.fight_rect.collidepoint(mouse_pos):
                                    self.spawn.catch_visible = False
                                    self.spawn.fight_visible = False
                                    turn_count = 0
                                    while True:
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                mouse_pos = pygame.mouse.get_pos()
                                                if player.active_mon.attack1_visible == True:
                                                    if player.active_mon.attack1_rect.collidepoint(mouse_pos):
                                                        turn_count +=1
                                                        player.active_mon.attack1_visible = False
                                                        player.active_mon.z_rect_visible = False
                                                        player.active_mon.attack2_visible = False
                                                        self.spawn.fight(player, player.active_mon.attack1, turn_count)
                                                        pygame.display.update()
                                                if player.active_mon.attack2_visible == True:
                                                    if player.active_mon.attack2_rect.collidepoint(mouse_pos):
                                                        turn_count +=1
                                                        player.active_mon.attack1_visible = False
                                                        player.active_mon.z_rect_visible = False
                                                        player.active_mon.attack2_visible = False
                                                        self.spawn.fight(player, player.active_mon.attack2, turn_count)
                                                        pygame.display.update()
                                                if player.active_mon.z_rect_visible == True and player.zmove_used == False:
                                                    if player.active_mon.z_rect.collidepoint(mouse_pos):
                                                        turn_count +=1
                                                        player.zmove_used = True
                                                        player.active_mon.z_rect_visible = False
                                                        player.active_mon.attack1_visible = False
                                                        player.active_mon.attack2_visible = False
                                                        self.spawn.fight(player, player.active_mon.z_move, turn_count)
                                                        pygame.display.update()
                                            
                                        if player.draw_fight_mon((300,100)) == 0:
                                            br = True
                                            break 
                                        elif self.spawn.hp <= 0:
                                            player.active_mon.lvlup()
                                            player.lvl += 1
                                            br = True 
                                            break
                                        else:
                                            self.spawn.draw_spawn_card((800,100))
                                            player.draw_fight_mon((300,100))
                                            pygame.display.update()
                self.spawn.draw_spawn_card((800, 100))
                pygame.display.update()
                if br == True:
                    break

            self.br = True

        elif self.type == 'trainer_fight' or self.type == 'rocket_fight':
            turn_count = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if player.active_mon.attack1_visible == True:
                            if player.active_mon.attack1_rect.collidepoint(mouse_pos):
                                turn_count += 1
                                player.active_mon.attack1_visible = False
                                player.active_mon.z_rect_visible = False
                                player.active_mon.attack2_visible = False
                                trainer.fight(player, player.active_mon.attack1, turn_count)
                                pygame.display.update()
                        if player.active_mon.attack2_visible == True:
                            if player.active_mon.attack2_rect.collidepoint(mouse_pos):
                                turn_count += 1
                                player.active_mon.attack1_visible = False
                                player.active_mon.z_rect_visible = False
                                player.active_mon.attack2_visible = False
                                trainer.fight(player, player.active_mon.attack2, turn_count)
                                pygame.display.update()
                        if player.active_mon.z_rect_visible == True and player.zmove_used == False:
                            if player.active_mon.z_rect.collidepoint(mouse_pos):
                                turn_count += 1
                                player.zmove_used = True
                                player.active_mon.z_rect_visible = False
                                player.active_mon.attack1_visible = False
                                player.active_mon.attack2_visible = False
                                trainer.fight(player, player.active_mon.z_move, turn_count)
                                pygame.display.update()
                
                if player.draw_fight_mon((300,100)) == 0:
                    self.br = True
                    trainer.mon.respawn_mon()
                    break
                 
                elif trainer.mon.hp <= 0:
                    player.active_mon.lvlup()
                    player.lvl += 1
                    self.br = True
                    trainer.mon.respawn_mon()
                    break
                else:
                    trainer.draw_card((800,100))
                    player.draw_fight_mon((300,100))
                    pygame.display.update()

        elif self.type == 'beast_ball':
            player.backpack.append(self)
            chance_list.remove(self)
            self.br = True
        
        elif self.type == 'pokecenter':
            for i in player.mons:
                i.hp = i.max_hp
            self.br = True
        
        elif self.type == 'ball':
            if self in player.inventory:
                pass
            else:
                player.inventory.append(self)
            self.br = True
    
    

normaliumz = Chance('Normalium Z', 'zcrystal', breakneck_blitz)
fightiniumz = Chance('Fightinium Z', 'zcrystal', allout_pummeling)
flyiniumz = Chance('Flyinium Z', 'zcrystal', supersonic_skystrike)
poisoniumz = Chance('Poisonium Z', 'zcrystal', acid_downpour)
groundiumz = Chance('Groundium Z', 'zcrystal', tectonic_rage)
rockiumz = Chance('Rockium Z', 'zcrystal', continental_crush)
buginiumz = Chance('Buginium Z', 'zcrystal', savage_spinout)
ghostiumz = Chance('Ghostium Z', 'zcrystal', neverending_nightmare)
steeliumz = Chance('Steelium Z', 'zcrystal', corkscrew_crash)
firiumz = Chance('Firium Z', 'zcrystal', inferno_overdrive)
wateriumz = Chance('Waterium Z', 'zcrystal', hydro_vortex)
grassiumz = Chance('Grassium Z', 'zcrystal', bloom_doom)
electriumz = Chance('Electrium Z', 'zcrystal', gigavolt_havoc)
psychiumz = Chance('Psychium Z', 'zcrystal', shattered_psyche)
iciumz = Chance('Icium Z', 'zcrystal', subzero_slammer)
dragoniumz = Chance('Dragonium Z', 'zcrystal', devastating_drake)
darkiniumz = Chance('Darkinium Z', 'zcrystal', black_hole_eclipse)
fairiumz = Chance('Fairium Z', 'zcrystal', twinkle_tackle)

mon_spawn = Chance('Wild pokemon', 'mon_spawn')
mon_spawn1 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn2 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn3 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn4 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn5 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn6 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn7 = Chance('Wild pokemon', 'mon_spawn')
mon_spawn8 = Chance('Wild pokemon', 'mon_spawn')

trainer_fight = Chance('Trainer fight', 'trainer_fight')
trainer_fight1 = Chance('Trainer fight', 'trainer_fight')
trainer_fight2 = Chance('Trainer fight', 'trainer_fight')

rocket_fight = Chance('Rocket fight', 'rocket_fight')
rocket_fight1 = Chance('Rocket fight', 'rocket_fight')
rocket_fight2 = Chance('Rocket fight', 'rocket_fight')

beast_ball = Chance('Beast Ball', 'beast_ball')
beast_ball1 = Chance('Beast Ball', 'beast_ball')
beast_ball2 = Chance('Beast Ball', 'beast_ball')
beast_ball3 = Chance('Beast Ball', 'beast_ball')
beast_ball4 = Chance('Beast Ball', 'beast_ball')
beast_ball5 = Chance('Beast Ball', 'beast_ball')
beast_ball6 = Chance('Beast Ball', 'beast_ball')

pokecenter = Chance('Pokecenter', 'pokecenter')
pokecenter1 = Chance('Pokecenter', 'pokecenter')
pokecenter2 = Chance('Pokecenter', 'pokecenter')
pokecenter3 = Chance('Pokecenter', 'pokecenter')
pokecenter4 = Chance('Pokecenter', 'pokecenter')
pokecenter5 = Chance('Pokecenter', 'pokecenter')

nihilego = UltraBeast('Nihilego', [109, 53, 47, 127, 131, 103], ['rock', 'poison', 0, 0, 0, 0])
nihilego.set_attacks([acid, pound, headbutt, venoshock, head_smash], [tickle])
xurkitree = UltraBeast('Xurkitree', [83, 89, 71, 173, 71, 83], ['electric', '', 0, 0, 0, 0])
xurkitree.set_attacks([spark, thunder_shock, thunderbolt, signal_beam, discharge, zap_cannon, thunder_punch, power_whip], [thunder_wave])
buzzwole = UltraBeast('Buzzwole', [107, 139, 139, 53, 53, 79], ['bug', 'fighting', 0, 0, 0, 0])
buzzwole.set_attacks([leech_life, hammer_arm, superpower, dynamic_punch, ice_punch, thunder_punch, mega_punch], [harden, bulk_up])
guzzlord = UltraBeast('Guzzlord', [223, 101, 53, 97, 53, 43], ['dark', 'dragon', 0, 0, 0, 0])
guzzlord.set_attacks([bite, iron_tail, crunch, hammer_arm, stomp, dragon_rush, steamroller], [])
naganadel = UltraBeast('Naganadel', [73, 73, 73, 127, 73, 121], ['poison', 'dragon', 0, 0, 0, 0])
naganadel.set_attacks([acid, dragon_pulse, peck, venoshock, poison_jab, air_slash], [growl, nasty_plot, charm])
pheromosa = UltraBeast('Pheromosa', [71, 139, 37, 137, 37, 151], ['bug', 'fighting', 0, 0, 0, 0])
pheromosa.set_attacks([rapid_spin, swift, silver_wind, bug_buzz, stomp], [leer, quilver_dance, agility])
celesteela = UltraBeast('Celesteela', [97, 101, 103, 107, 101, 61], ['steel', 'flying', 0, 0, 0, 0])
celesteela.set_attacks([air_slash, tackle, iron_head, giga_drain, flash_cannon, seed_bomb], [harden, metal_sound, iron_defense])
kartana = UltraBeast('Kartana', [59, 181, 131, 59, 31, 109], ['grass', 'steel', 0, 0, 0, 0])
kartana.set_attacks([furry_cutter, razor_leaf, aerial_ace, night_slash, leaf_blade, xscissor, air_slash, psycho_cut], [swords_dance, defog])
stakataka = UltraBeast('Stakataka', [61, 131, 211, 53, 101, 13], ['rock', 'steel', 0, 0, 0, 0])
stakataka.set_attacks([tackle, rock_throw, iron_head, rock_slide], [iron_defense])
blacephalon = UltraBeast('Blacephalon', [53, 127, 53, 151, 79, 107], ['fire', 'ghost', 0, 0, 0, 0])
blacephalon.set_attacks([astonish, ember, flame_burst, fire_blast, shadow_ball], [calm_mind])



                