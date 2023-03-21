import pygame
import random
from fields import *
from backpack import *
from rules import *

pygame.init()

FONT3 = pygame.font.Font('fonts/Adventure.ttf', 60)

class Dice:
    
    visible = True
    image_one = pygame.image.load('pictures/dice/dice1.png')
    image_two = pygame.image.load('pictures/dice/dice2.png')
    image_three = pygame.image.load('pictures/dice/dice3.png')
    image_four = pygame.image.load('pictures/dice/dice4.png')
    image_five = pygame.image.load('pictures/dice/dice5.png')
    image_six = pygame.image.load('pictures/dice/dice6.png')
    dice_done = False
    rect = pygame.Rect(1400, 10, 174, 218)

    @classmethod
    def roll_dice(cls):
        for i in range(20,random.randrange(50,100)):
            for j in (cls.image_one, cls.image_two, cls.image_three, cls.image_four, cls.image_five, cls.image_six):
                SCREEN.blit(j, (1400, 10))
                pygame.display.update()

        cls.dice_number = random.randrange(1,6)
        
        if cls.dice_number == 1:
            SCREEN.blit(cls.image_one, (1400, 10))
            pygame.display.update()
        elif cls.dice_number == 2:
            SCREEN.blit(cls.image_two, (1400, 10))
            pygame.display.update()
        elif cls.dice_number == 3:
            SCREEN.blit(cls.image_three, (1400, 10))
            pygame.display.update()
        elif cls.dice_number == 4:
            SCREEN.blit(cls.image_four, (1400, 10))
            pygame.display.update()
        elif cls.dice_number == 5:
            SCREEN.blit(cls.image_five, (1400, 10))
            pygame.display.update()
        elif cls.dice_number == 6:
            SCREEN.blit(cls.image_six, (1400, 10))
            pygame.display.update()

        cls.visible = False
        cls.dice_done = True


run = True
turn = True
next_pos = []
last_pos = []
was_gym = []
now_playing = Player1
last_player = Player1
can_roll = True
player_moved = False

def next_player():
    global now_playing
    if player_list.index(last_player)+1 <= len(player_list)-1:
        index = player_list.index(last_player)+1
        now_playing = player_list[index]
    else:
        now_playing = player_list[0]

def check_if_attack(mouse_pos, now_playing, turn_count, enemy):
    if now_playing.active_mon.attack1_visible == True:
        if now_playing.active_mon.attack1_rect.collidepoint(mouse_pos):
            turn_count += 1
            now_playing.active_mon.attack1_visible = False
            now_playing.active_mon.z_rect_visible = False
            now_playing.active_mon.attack2_visible = False
            enemy.fight(now_playing, now_playing.active_mon.attack1, turn_count)
            pygame.display.update()
    if now_playing.active_mon.attack2_visible == True:
        if now_playing.active_mon.attack2_rect.collidepoint(mouse_pos):
            turn_count += 1
            now_playing.active_mon.attack1_visible = False
            now_playing.active_mon.z_rect_visible = False
            now_playing.active_mon.attack2_visible = False
            enemy.fight(now_playing, now_playing.active_mon.attack2, turn_count)
            pygame.display.update()
    if now_playing.active_mon.z_rect_visible == True and now_playing.zmove_used == False:
        if now_playing.active_mon.z_rect.collidepoint(mouse_pos):
            turn_count += 1
            now_playing.zmove_used = True
            now_playing.active_mon.z_rect_visible = False
            now_playing.active_mon.attack1_visible = False
            now_playing.active_mon.attack2_visible = False
            enemy.fight(now_playing, now_playing.active_mon.z_move, turn_count)
            pygame.display.update()

while run:
        for i in fields_list:
            pygame.draw.circle(SCREEN, (0,0,0), (i.center), i.size)

        load_bg()
        load_counter()
        pygame.display.update()

        can_roll = True
        while now_playing == Player1 or now_playing == Player2:
            
            if can_roll == True:
                Dice.visible = True
                can_roll = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    now_playing = False
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        now_playing = npc
                    if event.key == pygame.K_SPACE:
                        if Dice.visible == True:
                            Dice.roll_dice()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if Dice.visible == True and Dice.rect.collidepoint(mouse_pos):
                        Dice.roll_dice()

                    if backpack.visible == True and backpack.rect.collidepoint(mouse_pos):
                        open_backpack(now_playing)

                    if pc.visible == True and pc.rect.collidepoint(mouse_pos):
                        open_pc(now_playing)

                    if badges.visible == True and badges.rect.collidepoint(mouse_pos):
                        open_badge_case(now_playing)
                    
                    if rules_pic.rect.collidepoint(mouse_pos):
                        rules()

                    if endturn.visible == True and endturn.rect.collidepoint(mouse_pos):
                        last_player = now_playing
                        now_playing = npc
                        break

                    for i in fields_list:
                        if i.shining == True and i.rect.collidepoint(mouse_pos):
                            now_playing.pos = [i]
                            now_playing.now_on = i
                            for j in fields_list:
                                j.shining = False
                                player_moved = True
                                load_bg()
                                load_counter()
                                for player in player_list:
                                    player.draw_player()
                                pygame.display.update()
            posx = 10
            posy = 5
            
            for i in now_playing.mons:
                if now_playing.mons.index(i) < 6:
                    i.draw_team((posx, posy))
                    posy += 70
            pygame.display.update()
            for i in now_playing.pos:
                if len(now_playing.pos) > 1:
                    i.shine()
                for player in player_list:
                    player.draw_player()

            if Dice.visible == True:
                backpack.visible = False
                pc.visible = False
                badges.visible = False
                endturn.visible = False
                SCREEN.blit(Dice.image_one, (1400,10))

            if Dice.dice_done == True:
                last_pos = []
                next_pos = []
                if isinstance(now_playing.pos[0], GymField) and Dice.dice_number == 1:
                    next_pos = now_playing.pos[0].next_fields
                    now_playing.pos.extend(next_pos)
                    next_pos = []
                else:
                    for a in range(1, Dice.dice_number+1):
                        for b in now_playing.pos:
                            last_pos.append(b.center)
                            for c in b.next_fields:
                                if c.gym == True:
                                    was_gym = [c]
                                elif c.center in last_pos:
                                    pass
                                else:
                                    next_pos.append(c)
                        now_playing.pos = next_pos
                        next_pos = []
                    last_pos = []

                    for i in was_gym:
                        now_playing.pos.append(i)
                        was_gym = []

                Dice.dice_done = False
            


            if player_moved == True:
                turn_count = 0
                backpack.visible = True
                pc.visible = True
                badges.visible = True
                endturn.visible = True
                player_moved = False
                for i in now_playing.pos:
                    pos = i
                trainer = random.choice(trainer_list)
                rocket = random.choice(rocket_list)
                
                chance = random.choice(chance_list)
                if isinstance(i, PokeField):
                    if now_playing.pos[0].location == 'orange':
                        spawn = random.choice(orange_spawn)
                    elif now_playing.pos[0].location == 'gray':
                        spawn = random.choice(gray_spawn)
                    elif now_playing.pos[0].location == 'blue':
                        spawn = random.choice(blue_spawn)
                    elif now_playing.pos[0].location == 'green':
                        spawn = random.choice(green_spawn)
                    elif now_playing.pos[0].location == 'yellow':
                        spawn = random.choice(yellow_spawn)
                    elif now_playing.pos[0].location == 'purple':
                        spawn = random.choice(purple_spawn)
                    elif now_playing.pos[0].location == 'white':
                        spawn = random.choice(white_spawn)
                    elif now_playing.pos[0].location == 'brown':
                        spawn = random.choice(brown_spawn)
                
                while isinstance(i, BattleField):
                    if len(now_playing.mons) < 1:
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            check_if_attack(mouse_pos, now_playing, turn_count, trainer)
                    
                    if now_playing.draw_fight_mon((300,100)) == 0:
                        trainer.mon.respawn_mon()
                        break 
                    elif trainer.mon.hp <= 0:
                        now_playing.active_mon.lvlup()
                        now_playing.lvl += 1
                        trainer.mon.respawn_mon()
                        break
                    else:
                        trainer.draw_card((800,100))
                        now_playing.draw_fight_mon((300,100))
                        pygame.display.update()

                while isinstance(i, RocketField):
                    if len(now_playing.mons) < 1:
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            check_if_attack(mouse_pos, now_playing, turn_count, rocket)
                    
                    if now_playing.draw_fight_mon((300,100)) == 0:
                        rocket.mon.respawn_mon()
                        break
                    elif rocket.mon.hp <= 0:
                        now_playing.active_mon.lvlup()
                        now_playing.lvl += 1
                        rocket.mon.respawn_mon()
                        break
                    else:
                        rocket.draw_card((800,100))
                        now_playing.draw_fight_mon((300,100))
                        pygame.display.update()

                while isinstance(i, ChanceField):  
                    br = False       
                    if isinstance(chance, UltraBeast):
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN: 
                                mouse_pos = pygame.mouse.get_pos()
                                if chance.catch_visible == True and any(i.type == 'beast_ball' for i in now_playing.backpack):
                                    if chance.catch_rect.collidepoint(mouse_pos):
                                        chance.catch_visible = False
                                        chance.fight_visible = False
                                        for i in now_playing.backpack:
                                            if i.type == 'beast_ball':
                                                x = i
                                                break
                                        now_playing.backpack.remove(x)
                                        now_playing.mons.append(chance)
                                        chance_list.remove(chance)
                                        br = True
                                        break
                                        
                                if chance.fight_visible == True:
                                    if chance.fight_rect.collidepoint(mouse_pos) and len(now_playing.mons) == 0:
                                        chance.catch_visible = False
                                        chance.fight_visible = False
                                        br = True
                                        break
                                    if chance.fight_rect.collidepoint(mouse_pos) and len(now_playing.mons) > 0:
                                        chance.catch_visible = False
                                        chance.fight_visible = False
                                        turn_count = 0
                                        while True:
                                            for event in pygame.event.get():
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    mouse_pos = pygame.mouse.get_pos()
                                                    check_if_attack(mouse_pos, now_playing, turn_count, chance)
                                                
                                            if now_playing.draw_fight_mon((300,100)) == 0:
                                                br = True
                                                break 
                                            elif chance.hp <= 0:
                                                now_playing.active_mon.lvlup()
                                                now_playing.lvl += 1
                                                br = True
                                                break
                                            else:
                                                chance.draw_spawn_card((800,100))
                                                now_playing.draw_fight_mon((300,100))
                                                pygame.display.update()
                        chance.draw_spawn_card((800, 100))
                        pygame.display.update()
                        if br == True:
                            break

                    if isinstance(chance, Chance):
                        if chance.type == 'trainer_fight':
                            who = trainer
                        else:
                            who = rocket
                        while True:
                            br = False
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    if chance.claim_rect.collidepoint(mouse_pos):
                                        if chance.type == 'trainer_fight' or chance.type == 'rocket_fight':
                                            if len(now_playing.mons) < 1:
                                                br = True
                                                break
                                        chance.do_something(now_playing, who)
                                        if chance.br == True:
                                            br = True
                                            break
                            if br == True:
                                break
                            chance.draw_card((800,100))
                    if br == True:
                        break

                while isinstance(i, PokeField):
                    br = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if spawn.catch_visible == True and len(now_playing.mons) < 26:
                                if spawn.catch_rect.collidepoint(mouse_pos):
                                    spawn.catch_visible = False
                                    spawn.fight_visible = False
                                    Karp.draw_cards(now_playing, (200,100))
                                    if Karp.catch > 0:
                                        now_playing.mons.append(spawn)
                                        if now_playing.pos[0].location == 'orange':
                                            orange_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'gray':
                                            gray_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'blue':
                                            blue_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'green':
                                            green_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'yellow':
                                            yellow_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'purple':
                                            purple_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'white':
                                            white_spawn.remove(spawn)
                                        elif now_playing.pos[0].location == 'brown':
                                            brown_spawn.remove(spawn)
                                            
                                        br = True
                                        break
                                    else:
                                        spawn.respawn_mon()
                                        br = True
                                        break
                            if spawn.fight_visible == True:
                                    if spawn.fight_rect.collidepoint(mouse_pos) and len(now_playing.mons) == 0:
                                        spawn.catch_visible = False
                                        spawn.fight_visible = False
                                        br = True
                                        break
                                    if spawn.fight_rect.collidepoint(mouse_pos) and len(now_playing.mons) > 0:
                                        turn_count = 0
                                        spawn.catch_visible = False
                                        spawn.fight_visible = False
                                        now_playing.draw_fight_mon((300,100))
                                        while True:
                                            for event in pygame.event.get():
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    mouse_pos = pygame.mouse.get_pos()
                                                    check_if_attack(mouse_pos, now_playing, turn_count, spawn)
                                                    
                                            if now_playing.draw_fight_mon((300,100)) == 0:
                                                br = True
                                                spawn.respawn_mon()
                                                break 
                                            elif spawn.hp <= 0:
                                                now_playing.active_mon.lvlup()
                                                now_playing.lvl += 1
                                                br = True 
                                                spawn.respawn_mon()
                                                break
                                            else:
                                                spawn.draw_spawn_card((800,100))
                                                now_playing.draw_fight_mon((300,100))
                                                pygame.display.update()
                    spawn.draw_spawn_card((800, 100))
                    pygame.display.update()
                    if br == True:
                        break

                if isinstance(i, MegaField):
                    mega_pick(now_playing, (300,100))

                if isinstance(i, GymField):
                    if i.location == 'orange':
                        gym_leader = blaine
                    elif i.location == 'white':
                        gym_leader = sabrina
                    elif i.location == 'gray':
                        gym_leader = brock
                    elif i.location == 'purple':
                        gym_leader = janine
                    elif i.location == 'brown':
                        gym_leader = giovanni_gym
                    elif i.location == 'blue':
                        gym_leader = misty
                    elif i.location == 'green':
                        gym_leader = erika
                    elif i.location == 'yellow':
                        gym_leader = lt_surge
                    gym_leader.pass_visible = True
                    gym_leader.fight_visible = True
                
                    for mon in now_playing.mons:
                        mon.set_mon()

                    now_playing.zmove_used = False

                while isinstance(i, GymField):
                    br = False
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                br = True
                                break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if gym_leader.pass_visible == True and gym_leader.pass_rect.collidepoint(mouse_pos):
                                br = True
                                gym_leader.fight_visible = False
                                gym_leader.pass_visible = False
                                for mon in now_playing.mons:
                                    mon.set_mon()
                                break
                            
                            if gym_leader.fight_visible == True and gym_leader.fight_rect.collidepoint(mouse_pos) and len(now_playing.mons) > 0:
                                for mon in gym_leader.mons:
                                    mon.set_mon()
                                gym_leader.fight_visible = False
                                gym_leader.pass_visible = False
                                turn_count = 0
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_pos = pygame.mouse.get_pos()
                                            check_if_attack(mouse_pos, now_playing, turn_count, gym_leader) 
                                                    
                                    if now_playing.draw_fight_mon((300,100)) == 0:
                                        br = True
                                        for mon in now_playing.mons:
                                            mon.set_mon()
                                        for mon in gym_leader.mons:
                                            mon.set_mon()
                                        break 
                                    elif gym_leader.defeated == True:
                                        now_playing.active_mon.lvlup()
                                        now_playing.active_mon.lvlup()
                                        now_playing.active_mon.lvlup()
                                        now_playing.lvl += 3
                                        gym_leader.defeated = False
                                        br = True 
                                        for mon in now_playing.mons:
                                            mon.set_mon()
                                        for mon in gym_leader.mons:
                                            mon.set_mon()
                                        break
                                    else:
                                        gym_leader.draw_card((800,100))
                                        now_playing.draw_fight_mon((300,100))
                                        pygame.display.update()
                    
                    gym_leader.draw_gym((500,100))

                    if gym_leader.badge in now_playing.badge_case:
                        gym_leader.fight_visible = False

                    if br == True:
                        now_playing.zmove_used = False
                        break

                load_bg()
                load_counter()
                pygame.display.update() 

            posx = 10
            posy = 5
            for i in now_playing.mons:
                if now_playing.mons.index(i) < 6:
                    i.draw_team((posx, posy))
                    posy += 70
            if backpack.visible == True:        
                backpack.draw()
            if badges.visible == True:        
                badges.draw()
            if pc.visible == True:
                pc.draw()
            rules_pic.draw()

            if endturn.visible == True:
                endturn.draw()
            pygame.display.update()

        next_player()

        if len(Player1.badge_case) == 8 or len(Player2.badge_case) == 8:
            p1_basic = 0
            p2_basic = 0
            p1_stage1 = 0
            p2_stage1 = 0
            p1_stage2 = 0
            p2_stage2 = 0
            for i in Player1.mons:
                if isinstance(i, Stage2):
                    if i.lvl == 10:
                        Player1.lvl += 3
                        p1_stage2 += 3
                    elif i.lvl > 5:
                        Player1.lvl += 2
                        p1_stage1 += 2
                    else:
                        Player1.lvl += 1
                        p1_basic += 1
                elif isinstance(i, Stage1):
                    if i.lvl > 5:
                        Player1.lvl += 2
                        p1_stage1 += 2
                    else:
                        Player1.lvl += 1
                        p1_basic += 1
                else:
                    Player1.lvl += 1
                    p1_basic += 1

            for i in Player2.mons:
                if isinstance(i, Stage2):
                    if i.lvl == 10:
                        Player2.lvl += 3
                        p2_stage2 += 3
                    elif i.lvl > 5:
                        Player2.lvl += 2
                        p2_stage1 += 2
                    else:
                        Player2.lvl += 1
                        p2_basic += 1
                elif isinstance(i, Stage1):
                    if i.lvl > 5:
                        Player2.lvl += 2
                        p2_stage1 += 2
                    else:
                        Player2.lvl += 1
                        p2_basic += 1
                else:
                    Player2.lvl += 1
                    p2_basic += 1
            br = True
            while br == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            br = False
                            break
                if Player1.lvl > Player2.lvl:
                    winner = 'Red Player'
                    color = (255,0,0)
                elif Player1.lvl < Player2.lvl:
                    winner = 'Blue Player'
                    color = (0,0,255)
                else:
                    winner = 'draw'
                    color = (0,255,0)

                if winner == 'draw':
                    text_winner = FONT3.render('It´s a draw', True, color)
                else:
                    text_winner = FONT3.render(winner+' wins', True, color)

                text_end = FONT3.render('press ESC to quit', True, (255,255,255))
                text_p1_basic = FONT3.render('Basic pokemons + '+str(p1_basic), True, (255,0,0))
                text_p1_stage1 = FONT3.render('Stage 1 pokemons + '+str(p1_stage1), True, (255,0,0))
                text_p1_stage2 = FONT3.render('Stage 2 pokemons + '+str(p1_stage2), True, (255,0,0))
                text_p2_basic = FONT3.render('Basic pokemons + '+str(p2_basic), True, (0,0,255))
                text_p2_stage1 = FONT3.render('Stage 1 pokemons + '+str(p2_stage1), True, (0,0,255))
                text_p2_stage2 = FONT3.render('Stage 2 pokemons + '+str(p2_stage2), True, (0,0,255))

                SCREEN.fill((0,0,0))
                SCREEN.blit(text_winner, (500,400))
                SCREEN.blit(text_end, (500,600))
                SCREEN.blit(text_p1_basic, (200,100))
                SCREEN.blit(text_p1_stage1, (200,150))
                SCREEN.blit(text_p1_stage2, (200,200))
                SCREEN.blit(text_p2_basic, (800,100))
                SCREEN.blit(text_p2_stage1, (800,150))
                SCREEN.blit(text_p2_stage2, (800,200))

                
                load_counter()
                pygame.display.update()
        