import pygame
import random
from attacks import *
from mons import *
from player import *

pygame.init()

trainer_list = []
rocket_list = []

class Badge:
    def __init__(self, name):
        self.name = name
        self.img = pygame.image.load('pictures/maps/'+self.name+'.png')
        self.image = pygame.transform.scale(self.img, (100,100))

class Trainermon:
    def __init__(self, name, base_stats, type1, type2= ''):
        self.type1 = type1
        self.type2 = type2
        self.base_stats = base_stats
        self.base_stats_pernament = base_stats
        self.name = name
        self.lvl = random.randrange(1,10)
        self.b_hp = base_stats[0]
        self.b_att = base_stats[1]
        self.b_defense = base_stats[2]
        self.b_sp_att = base_stats[3]
        self.b_sp_def = base_stats[4]
        self.b_spd = base_stats[5]
        self.first = True
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]

    def set_attacks(self, attacks=[], status=[]):
        self.dmg_attacks = attacks
        self.status_attacks = status
        self.attacks_respawn = self.dmg_attacks + self.status_attacks
        self.attack_list = self.dmg_attacks + self.status_attacks
        self.set_mon()

    def set_mon(self):
        self.burn = False
        self.confuse = False
        self.poison = False
        self.flinch = False
        self.hit_yourself = False
        self.freeze = False
        self.paralyze = False
        self.acc_stage = 0
        self.evasion_stage = 0
        self.hp_stage = 0
        self.att_stage = 0
        self.defense_stage = 0
        self.sp_att_stage = 0
        self.sp_def_stage = 0
        self.spd_stage = 0
        self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats_pernament[0], self.base_stats_pernament[1], self.base_stats_pernament[2], self.base_stats_pernament[3], self.base_stats_pernament[4], self.base_stats_pernament[5]
        self.max_hp = (((2*self.b_hp+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
        self.hp = (((2*self.b_hp+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
        self.att = (((2*self.b_att+self.ivs[1]+21)*self.lvl)/100)+5
        self.defense = (((2*self.b_defense+self.ivs[2]+21)*self.lvl)/100)+5
        self.sp_att = (((2*self.b_sp_att+self.ivs[3]+21)*self.lvl)/100)+5
        self.sp_def = (((2*self.b_sp_def+self.ivs[4]+21)*self.lvl)/100)+5
        self.spd = (((2*self.b_spd+self.ivs[5]+21)*self.lvl)/100)+5
        if self.first == True:
            self.first = False
            self.attack1 = random.choice(self.attack_list)
            self.attack_list.remove(self.attack1)
            if self.attack1 in self.status_attacks:
                self.attack2 = random.choice(self.dmg_attacks)
                self.attack_list.remove(self.attack2)
            else:
                self.attack2 = random.choice(self.attack_list)
                self.attack_list.remove(self.attack2)

    def respawn_mon(self):
        self.set = True
        self.attack_list = []
        self.attack_list.extend(self.attacks_respawn)
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        self.set_mon()

    def attack(self, move, enemy, turn_count):
        self.effectiveness1 = 1
        self.effectiveness2 = 1
        self.dmg = 0
        for i in super_effective[move.type]:
            if i == enemy.type1:
                self.effectiveness1 = 2
            if enemy.type2 != '':
                if i == enemy.type2:
                    self.effectiveness2 = 2

        for i in notvery_effective[move.type]:
            if i == enemy.type1:
                self.effectiveness1 = 0.5
            if enemy.type2 != '':
                if i == enemy.type2:
                    self.effectiveness2 = 0.5
        
        for i in no_effect[move.type]:
            if i == enemy.type1:
                self.effectiveness1 = 0
            if enemy.type2 != '':
                if i == enemy.type2:
                    self.effectiveness2 = 0

        if self.hit_yourself == True:
            if move.sp_atk == 'physical':
                self.dmg = (((((2*self.lvl)/5)+2)*40*(self.att/self.defense)/50)+2)
            if move.sp_atk == 'special':
                self.dmg = (((((2*self.lvl)/5)+2)*40*(self.sp_att/self.sp_def)/50)+2)
            self.hp = self.hp - self.dmg
        else:
            attack_effect(move, self, enemy, turn_count)
            if move.sp_atk == 'physical':
                self.dmg = ((((((2*self.lvl)/5)+2)*move.dmg*(self.att/enemy.defense)/50)+2)*self.effectiveness1*self.effectiveness2)
            if move.sp_atk == 'special':
                self.dmg = ((((((2*self.lvl)/5)+2)*move.dmg*(self.sp_att/enemy.sp_def)/50)+2)*self.effectiveness1*self.effectiveness2)
            self.dmg = self.dmg*move.multiplier
            for i in range(0, move.hit_number):
                enemy.hp = enemy.hp - self.dmg
            self.hp = self.hp + (self.dmg*move.heal_multiplier)
            self.hp = self.hp - (self.dmg*move.selfhit_multiplier)
            if self.hp >= self.max_hp:
                    self.hp = self.max_hp


class GymMon(Basic):
    def __init__(self, lvl, name, base_stats, type1, type2=''):
        self.name = name
        self.base_stats = base_stats
        self.base_stats_pernament = base_stats
        self.type1 = type1
        self.type2 = type2
        self.lvl = lvl
        self.image = pygame.image.load('pictures/mon_img/'+ self.name + '.png')
        self.b_hp = base_stats[0]
        self.b_att = base_stats[1]
        self.b_defense = base_stats[2]
        self.b_sp_att = base_stats[3]
        self.b_sp_def = base_stats[4]
        self.b_spd = base_stats[5]
        self.first = True
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]

    def set_mon(self):
        self.burn = False
        self.confuse = False
        self.poison = False
        self.flinch = False
        self.sleep = False
        self.freeze = False
        self.paralyze = False
        self.hit_yourself = False
        self.acc_stage = 0
        self.evasion_stage = 0
        self.hp_stage = 0
        self.att_stage = 0
        self.defense_stage = 0
        self.sp_att_stage = 0
        self.sp_def_stage = 0
        self.spd_stage = 0
        self.max_hp = (((2*self.b_hp+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
        self.hp = (((2*self.b_hp+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
        self.att = (((2*self.b_att+self.ivs[1]+21)*self.lvl)/100)+5
        self.defense = (((2*self.b_defense+self.ivs[2]+21)*self.lvl)/100)+5
        self.sp_att = (((2*self.b_sp_att+self.ivs[3]+21)*self.lvl)/100)+5
        self.sp_def = (((2*self.b_sp_def+self.ivs[4]+21)*self.lvl)/100)+5
        self.spd = (((2*self.b_spd+self.ivs[5]+21)*self.lvl)/100)+5
        if self.first == True:
            self.first = False
            self.attack1 = random.choice(self.attack_list)
            self.attack_list.remove(self.attack1)
            self.attack2 = random.choice(self.attack_list)
            self.attack_list.remove(self.attack2)


class Trainer:
    def __init__(self, name, mon):
        self.name = name
        self.image = pygame.image.load('pictures/trainer_img/'+self.name+'.png')
        self.mon = mon
        trainer_list.append(self)

    def draw_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        SCREEN.blit(self.image, (pos[0]+30, pos[1]+100))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        hp = round((100*self.mon.hp)/self.mon.max_hp)
        text_lvl = FONT.render('lvl:'+str(self.mon.lvl), True, (0, 0, 0))
        text_hp = FONT.render('HP: '+str(hp)+'%', True, (0, 0, 0))

        if ((100*self.mon.hp)/self.mon.max_hp) < 20:
            color = (225, 0, 0)
        elif ((100*self.mon.hp)/self.mon.max_hp) < 50:
            color = (225, 165, 0)
        else:
            color = (0, 225, 0)

        if self.mon.burn == True:
            SCREEN.blit(pygame.image.load('pictures/maps/burn.png'), (pos[0]+5, pos[1]+70))
        if self.mon.poison == True:
            SCREEN.blit(pygame.image.load('pictures/maps/poison.png'), (pos[0]+5, pos[1]+75))
        if self.mon.paralyze == True:
            SCREEN.blit(pygame.image.load('pictures/maps/paralyze.png'), (pos[0]+5, pos[1]+80))
        if self.mon.freeze == True:
            SCREEN.blit(pygame.image.load('pictures/maps/freeze.png'), (pos[0]+5, pos[1]+85))
        
        pygame.draw.rect(SCREEN, color, pygame.Rect(pos[0]+50, pos[1]+450, (((100*self.mon.hp)/self.mon.max_hp)*3), 60))
        SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
        SCREEN.blit(text_lvl, (pos[0]+270, pos[1]+50))
        SCREEN.blit(text_hp, (pos[0]+50, pos[1]+450))
        pygame.display.update()

    def fight(self, player, move, turn_count):
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300, 720, 900, 150))
        text3, text4, text5, text6, text7, text8, text9, text10, text11 = 0,0,0,0,0,0,0,0,0
        wait = True
        message = True
        message1 = False
        message2 = False
        message3 = False
        message4 = False
        if self.mon.hp > 0:
            if player.active_mon.hp > 0:
                if self.mon.spd > player.active_mon.spd:
                    used_move = random.choice((self.mon.attack1, self.mon.attack2))
                    if self.mon.confuse == True and random.randrange(1,4) == 1:
                        self.mon.hit_yourself = True
                    else:
                        self.mon.hit_yourself = False

                    if self.mon.hit_yourself == True:
                        text1 = FONT.render(self.mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                        self.mon.attack(used_move, player.active_mon, turn_count)
                    elif self.mon.flinch == True:
                        text1 = FONT.render(self.mon.name+' flinched!', True, (0, 0, 0))
                    elif self.mon.freeze == True:
                        if used_move.hit(self.mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            self.mon.freeze = False
                            self.mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.mon.name+' is frozen!', True, (0, 0, 0))
                    elif self.mon.paralyze == True:
                        if used_move.hit(self.mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            self.mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.mon.name+' is paralyzed!', True, (0, 0, 0))
                    elif used_move.hit(self.mon, player.active_mon) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                    else:
                        self.mon.attack(used_move, player.active_mon, turn_count)
                        if used_move.sp_atk == 'status':
                            text_self_efectivity = ''
                        elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                            text_self_efectivity = '(supereffective)'
                        elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                            text_self_efectivity = '(not very effective)'
                        elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                            text_self_efectivity = '(no effect)'
                        else:
                            text_self_efectivity = ''
                    
                    
                        text1 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                    

                    if player.active_mon.hp > 0:
                        if player.active_mon.confuse == True and random.randrange(1,4) == 1:
                            player.active_mon.hit_yourself = True
                        else:
                            player.active_mon.hit_yourself = False

                        if player.active_mon.hit_yourself == True:
                            text2 = FONT.render(player.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            player.active_mon.attack(move, self.mon, turn_count)
                        elif player.active_mon.flinch == True:
                            text2 = FONT.render(player.active_mon.name+' flinched!', True, (0, 0, 0))
                        elif player.active_mon.freeze == True:
                            if move.hit(player.active_mon, self.mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                player.active_mon.freeze = False
                                player.active_mon.attack(move, self.mon, turn_count)
                                if move.sp_atk == 'status':
                                    text_player_efectivity = ''
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                    text_player_efectivity = '(supereffective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                    text_player_efectivity = '(not very effective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                    text_player_efectivity = '(no effect)'
                                else:
                                    text_player_efectivity = ''
                                if move.type == 'zcrystal':
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' is frozen!', True, (0, 0, 0))

                        elif player.active_mon.paralyze == True:
                            if move.hit(player.active_mon, self.mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                player.active_mon.attack(move, self.mon, turn_count)
                                if move.sp_atk == 'status':
                                    text_player_efectivity = ''
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                    text_player_efectivity = '(supereffective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                    text_player_efectivity = '(not very effective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                    text_player_efectivity = '(no effect)'
                                else:
                                    text_player_efectivity = ''
                                if move.type == 'zcrystal':
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' is paralyzed!', True, (0, 0, 0))
                        elif move.hit(player.active_mon, self.mon) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))
                        
                        else:


                            player.active_mon.attack(move, self.mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = ''

                            if move.type == 'zcrystal':
                                text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))
                
                    else:
                        text2 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                        

                    if self.mon.hp < 0:
                        text3 = FONT.render(self.mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text3 = 0


                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.mon.burn == True:
                        self.mon.hp = (self.mon.hp - (self.mon.max_hp*(1/16)))
                        text5 = FONT.render(self.mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.mon.poison == True:
                        self.mon.hp = (self.mon.hp - (self.mon.max_hp*(1/16)))
                        text7 = FONT.render(self.mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if self.mon.confuse == True:
                        text8 = FONT.render(self.mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0

                    if player.active_mon.confuse == True:
                        text9 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.mon.hp < 0:
                        text10 = FONT.render(self.mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text10 = 0

                    if player.active_mon.hp < 0:
                        text11 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text11 = 0


                else:
                    if player.active_mon.confuse == True and random.randrange(1,4) == 1:
                        player.active_mon.hit_yourself = True
                    else:
                        player.active_mon.hit_yourself = False

                    if player.active_mon.hit_yourself == True:
                        text1 = FONT.render(player.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                        player.active_mon.attack(move, self.mon, turn_count)
                    elif player.active_mon.flinch == True:
                        text1 = FONT.render(player.active_mon.name+' flinched!', True, (0, 0, 0))
                    elif player.active_mon.freeze == True:
                        if move.hit(player.active_mon, self.mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            player.active_mon.freeze = False
                            player.active_mon.attack(move, self.mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            if player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = ''
                            if move.type == 'zcrystal':
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' is frozen!', True, (0, 0, 0))

                    elif player.active_mon.paralyze == True:
                        if move.hit(player.active_mon, self.mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            player.active_mon.attack(move, self.mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            if player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = ''
                            if move.type == 'zcrystal':
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' is paralyzed!', True, (0, 0, 0))
                    elif move.hit(player.active_mon, self.mon) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.mon.name+' avoided the attack!', True, (0, 0, 0))

                    else:
                        player.active_mon.attack(move, self.mon, turn_count)
                        if move.sp_atk == 'status':
                            text_player_efectivity = ''
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                            text_player_efectivity = '(supereffective)'
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                            text_player_efectivity = '(not very effective)'
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                            text_player_efectivity = '(no effect)'
                        else:
                            text_player_efectivity = ''

                        if move.type == 'zcrystal':
                            text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0, 0, 0))

                    if self.mon.hp > 0:
                        used_move = random.choice((self.mon.attack1, self.mon.attack2))
                        if self.mon.confuse == True and random.randrange(1,4) == 1:
                            self.mon.hit_yourself = True
                        else:
                            self.mon.hit_yourself = False
                        if self.mon.hit_yourself == True:
                            text2 = FONT.render(self.mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            self.mon.attack(used_move, player.active_mon, turn_count)
                        elif self.mon.flinch == True:
                            text2 = FONT.render(self.mon.name+' flinched!', True, (0, 0, 0))
                        elif self.mon.freeze == True:
                            if used_move.hit(self.mon, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                self.mon.freeze = False
                                self.mon.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''
                                text2 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.mon.name+' is frozen!', True, (0, 0, 0))
                        elif self.mon.paralyze == True:
                            if used_move.hit(self.mon, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                self.mon.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''
                                text2 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.mon.name+' is paralyzed!', True, (0, 0, 0))
                        elif used_move.hit(self.mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(self.mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        else:


                            self.mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 2 or self.mon.effectiveness1 * self.mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0.5 or self.mon.effectiveness1 * self.mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.mon.effectiveness1 * self.mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                        
                        
                            text2 = FONT.render(self.mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))

                    else:
                        text2 = FONT.render(self.mon.name+' fainted', True, (0, 0, 0))
                        

                    if player.active_mon.hp < 0:
                        text3 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text3 = 0


                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.mon.burn == True:
                        self.mon.hp = (self.mon.hp - (self.mon.max_hp*(1/16)))
                        text5 = FONT.render(self.mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.mon.poison == True:
                        self.mon.hp = (self.mon.hp - (self.mon.max_hp*(1/16)))
                        text7 = FONT.render(self.mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if self.mon.confuse == True:
                        text8 = FONT.render(self.mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0

                    if player.active_mon.confuse == True:
                        text9 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.mon.hp < 0:
                        text10 = FONT.render(self.mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text10 = 0

                    if player.active_mon.hp < 0:
                        text11 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text11 = 0

            pygame.display.update()

            while wait:
                while message == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message1 = True
                                message = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
                    SCREEN.blit(text_space, (750, 820))
                    SCREEN.blit(text1, (350, 725))
                    SCREEN.blit(text2, (350, 770))
                    if text3 != 0:
                        SCREEN.blit(text3, (350, 815))
                    pygame.display.update()  
                
                while message1 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message2 = True
                                message1 = False
                                break
                    if text4 == 0 and text5 == 0:
                        message2 = True
                        message1 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
                    SCREEN.blit(text_space, (750, 820))
                    if text4 != 0:
                        SCREEN.blit(text4, (350, 725))
                    if text5 != 0:
                        SCREEN.blit(text5, (350, 770))
                    pygame.display.update() 

                while message2 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message3 = True
                                message2 = False
                                break
                    if text6 == 0 and text7 == 0:
                        message3 = True
                        message2 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
                    SCREEN.blit(text_space, (750, 820))
                    if text6 != 0:
                        SCREEN.blit(text6, (350, 725))
                    if text7 != 0:
                        SCREEN.blit(text7, (350, 770))
                    pygame.display.update() 

                while message3 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message4 = True
                                message3 = False
                                break
                    if text8 == 0 and text9 == 0:
                        message4 = True
                        message3 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
                    SCREEN.blit(text_space, (750, 820))
                    if text8 != 0:
                        SCREEN.blit(text8, (350, 725))
                    if text9 != 0:
                        SCREEN.blit(text9, (350, 770))
                    pygame.display.update() 

                while message4 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                wait = False
                                message4 = False
                                break
                    self.mon.flinch = False
                    player.active_mon.flinch = False
                    if text10 == 0 and text11 == 0:
                        wait = False
                        message4 = False
                        break
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
                    SCREEN.blit(text_space, (750, 820))
                    if text10 != 0:
                        SCREEN.blit(text10, (350, 725))
                    if text11 != 0:
                        SCREEN.blit(text11, (350, 770))
                    pygame.display.update() 
                pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))

        if self.mon.hp <= 0:
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))
            text_win = FONT.render('you won', True, (0,0,0)) 
            SCREEN.blit(text_win, (350, 725))
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            wait = False
                text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                SCREEN.blit(text_space, (750, 820))
                pygame.display.update()
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
        pygame.display.update()


class Rocket(Trainer):
    def __init__(self, name, mon):
        self.name = name
        self.image = pygame.image.load('pictures/trainer_img/'+self.name+'.png')
        self.mon = mon
        rocket_list.append(self)



class GymLeader:
    def __init__(self, lvl, name, badge, mons=[]):
        self.lvl = lvl
        self.badge = badge
        self.name = name
        self.img = pygame.image.load('pictures/trainer_img/'+self.name+'.png')
        self.mons = mons
        self.defeated = False
        self.active_mon = self.mons[0]
  
    def draw_gym(self, pos):
        text_lvl = FONT.render('lvl:'+str(self.lvl), True, (0, 0, 0))
        SCREEN.blit(self.img, pos)
        SCREEN.blit(text_lvl, (pos[0]+300, pos[1]+350))
        self.fight_visible = True
        self.pass_visible = True
        self.pass_rect = pygame.Rect(pos[0]+200, pos[1], 150, 60)
        text_pass = FONT.render('Pass', True, (0, 0, 0))
        self.fight_rect = pygame.Rect(pos[0], pos[1], 150, 60)
        text_fight = FONT.render('Fight', True, (0, 0, 0))


        pygame.draw.rect(SCREEN, (200,0,0), self.fight_rect)
        SCREEN.blit(text_fight, (pos[0]+20, pos[1]+5))
        pygame.draw.rect(SCREEN, (0,200,0), self.pass_rect)
        SCREEN.blit(text_pass, (pos[0]+220, pos[1]+5))
        pygame.display.update()
    
    def draw_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        if self.active_mon.hp <= 0:
            if self.mons.index(self.active_mon) < 5:
                self.active_mon = self.mons[self.mons.index(self.active_mon) +1]
        SCREEN.blit(self.active_mon.image, (pos[0]+30, pos[1]+100))
        text_name = FONT.render(self.active_mon.name, True, (0, 0, 0))
        hp = round((100*self.active_mon.hp)/self.active_mon.max_hp)
        text_lvl = FONT.render('lvl:'+str(self.active_mon.lvl), True, (0, 0, 0))
        text_hp = FONT.render('HP: '+str(hp)+'%', True, (0, 0, 0))

        if ((100*self.active_mon.hp)/self.active_mon.max_hp) < 20:
            color = (225, 0, 0)
        elif ((100*self.active_mon.hp)/self.active_mon.max_hp) < 50:
            color = (225, 165, 0)
        else:
            color = (0, 225, 0)

        if self.active_mon.burn == True:
            SCREEN.blit(pygame.image.load('pictures/maps/burn.png'), (pos[0]+5, pos[1]+70))
        if self.active_mon.poison == True:
            SCREEN.blit(pygame.image.load('pictures/maps/poison.png'), (pos[0]+5, pos[1]+75))
        if self.active_mon.paralyze == True:
            SCREEN.blit(pygame.image.load('pictures/maps/paralyze.png'), (pos[0]+5, pos[1]+80))
        if self.active_mon.freeze == True:
            SCREEN.blit(pygame.image.load('pictures/maps/freeze.png'), (pos[0]+5, pos[1]+85))
        if self.active_mon.sleep == True:
            SCREEN.blit(pygame.image.load('pictures/maps/sleep.png'), (pos[0]+5, pos[1]+90))
        
        pygame.draw.rect(SCREEN, color, pygame.Rect(pos[0]+50, pos[1]+450, (((100*self.active_mon.hp)/self.active_mon.max_hp)*3), 60))
        SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
        SCREEN.blit(text_lvl, (pos[0]+270, pos[1]+50))
        SCREEN.blit(text_hp, (pos[0]+50, pos[1]+450))
        pygame.display.update()

    def fight(self, player, move, turn_count):
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300, 720, 900, 150))
        text3, text4, text5, text6, text7, text8, text9, text10, text11 = 0,0,0,0,0,0,0,0,0
        wait = True
        won = False
        for i in self.mons:
            if i.hp > 0:
                self.active_mon = i
                break
        message = True
        message1 = False
        message2 = False
        message3 = False
        message4 = False
        if self.active_mon.hp > 0:
            if player.active_mon.hp > 0:
                if self.active_mon.spd > player.active_mon.spd:
                    used_move = random.choice((self.active_mon.attack1, self.active_mon.attack2))
                    if self.active_mon.confuse == True and random.randrange(1,4) == 1:
                        self.active_mon.hit_yourself = True
                    else:
                        self.active_mon.hit_yourself = False

                    if self.active_mon.hit_yourself == True:
                        text1 = FONT.render(self.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                        self.active_mon.attack(used_move, player.active_mon, turn_count)
                    elif self.active_mon.flinch == True:
                        text1 = FONT.render(self.active_mon.name+' flinched!', True, (0,0,0))
                    elif self.active_mon.freeze == True:
                        if used_move.hit(self.active_mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            self.active_mon.freeze = False
                            self.active_mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.active_mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0,0,0))
                        else:
                            text1 = FONT.render(self.active_mon+' is frozen!', True, (0,0,0))
                    elif self.active_mon.paralyze == True:
                        if used_move.hit(self.active_mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            self.active_mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.active_mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0,0,0))
                        else:
                            text1 = FONT.render(self.active_mon+' is paralyzed!', True, (0,0,0))
                    elif used_move.hit(self.active_mon, player.active_mon) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                    else:
                        self.active_mon.attack(used_move, player.active_mon, turn_count)
                        if used_move.sp_atk == 'status':
                            text_self_efectivity = ''
                        elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                            text_self_efectivity = '(supereffective)'
                        elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                            text_self_efectivity = '(not very effective)'
                        elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                            text_self_efectivity = '(no effect)'
                        else:
                            text_self_efectivity = ''

                        text1 = FONT.render(self.active_mon.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0,0,0))
                    
                    if player.active_mon.hp > 0:
                        if player.active_mon.confuse == True and random.randrange(1,4) == 1:
                            player.active_mon.hit_yourself = True
                        else:
                            player.active_mon.hit_yourself = False

                        if player.active_mon.hit_yourself == True:
                            text2 = FONT.render(player.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            player.active_mon.attack(move, self.active_mon, turn_count)
                        elif player.active_mon.flinch == True:
                            text2 = FONT.render(player.active_mon.name+' flinched!', True, (0,0,0))
                        elif player.active_mon.freeze == True:
                            if move.hit(player.active_mon, self.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                player.active_mon.freeze = False
                                player.active_mon.attack(move, self.active_mon, turn_count)
                                if move.sp_atk == 'status':
                                    text_player_efectivity = ''
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                    text_player_efectivity = '(supereffective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                    text_player_efectivity = '(not very effective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                    text_player_efectivity = '(no effect)'
                                else:
                                    text_player_efectivity = ''
                                if move.type == 'zcrystal':
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' is frozen!', True, (0,0,0))
                        elif player.active_mon.paralyze == True:
                            if move.hit(player.active_mon, self.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                player.active_mon.attack(move, self.active_mon, turn_count)
                                if move.sp_atk == 'status':
                                    text_player_efectivity = ''
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                    text_player_efectivity = '(supereffective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                    text_player_efectivity = '(not very effective)'
                                elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                    text_player_efectivity = '(no effect)'
                                else:
                                    text_player_efectivity = ''
                                if move.type == 'zcrystal':
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' is paralyzed!', True, (0,0,0))
                        elif move.hit(player.active_mon, self.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        else:
                            player.active_mon.attack(move, self.active_mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = ''

                            if move.type == 'zcrystal':
                                text2 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0))
                    else:
                        text2 = FONT.render(player.active_mon.name+' fainted', True, (0,0,0))
                    

                    if self.active_mon.hp < 0:
                        text3 = FONT.render(self.active_mon.name+' fainted', True, (0,0,0))
                    else:
                        text3 = 0

                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.active_mon.burn == True:
                        self.active_mon.hp = (self.active_mon.hp - (self.active_mon.max_hp*(1/16)))
                        text5 = FONT.render(self.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.active_mon.poison == True:
                        self.active_mon.hp = (self.active_mon.hp - (self.active_mon.max_hp*(1/16)))
                        text7 = FONT.render(self.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if player.active_mon.confuse == True:
                        text8 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0

                    if self.active_mon.confuse == True:
                        text9 = FONT.render(self.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.active_mon.hp < 0:
                        text10 = FONT.render(self.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text10 = 0

                    if player.active_mon.hp < 0:
                        text11 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text11 = 0

                else:
                    if player.active_mon.confuse == True and random.randrange(1,4) == 1:
                        player.active_mon.hit_yourself = True
                    else:
                        player.active_mon.hit_yourself = False

                    if player.active_mon.hit_yourself == True:
                        text1 = FONT.render(player.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                        player.active_mon.attack(move, self.active_mon, turn_count)
                    elif player.active_mon.flinch == True:
                        text1 = FONT.render(player.active_mon.name+' flinched!', True, (0,0,0))
                    elif player.active_mon.freeze == True:
                        if move.hit(player.active_mon, self.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            player.active_mon.freeze = False
                            player.active_mon.attack(move, self.active_mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = '' 
                            if move.type == 'zcrystal':
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' is frozen!', True, (0,0,0))
                    elif player.active_mon.paralyze == True:
                        if move.hit(player.active_mon, self.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            player.active_mon.attack(move, self.active_mon, turn_count)
                            if move.sp_atk == 'status':
                                text_player_efectivity = ''
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                                text_player_efectivity = '(supereffective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                                text_player_efectivity = '(not very effective)'
                            elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                                text_player_efectivity = '(no effect)'
                            else:
                                text_player_efectivity = ''
                            if move.type == 'zcrystal':
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0)) 
                        else:
                            text1 = FONT.render(player.active_mon.name+' is paralyzed!', True, (0,0,0))
                    elif move.hit(player.active_mon, self.active_mon) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.active_mon.name+' avoided the attack!', True, (0, 0, 0))

                    else:
                        player.active_mon.attack(move, self.active_mon, turn_count)
                        if move.sp_atk == 'status':
                            text_player_efectivity = ''
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 2 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 4:
                            text_player_efectivity = '(supereffective)'
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.5 or player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0.25:
                            text_player_efectivity = '(not very effective)'
                        elif player.active_mon.effectiveness1 * player.active_mon.effectiveness2 == 0:
                            text_player_efectivity = '(no effect)'
                        else:
                            text_player_efectivity = '' 

                        if move.type == 'zcrystal':
                            text1 = FONT.render(player.active_mon.name+' used '+str(move.zname.name)+' '+text_player_efectivity, True, (0,0,0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' used '+str(move.name)+' '+text_player_efectivity, True, (0,0,0))

                    if self.active_mon.hp > 0:
                        used_move = random.choice((self.active_mon.attack1, self.active_mon.attack2))
                        if self.active_mon.confuse == True and random.randrange(1,4) == 1:
                            self.active_mon.hit_yourself = True
                        else:
                            self.active_mon.hit_yourself = False
                        if self.active_mon.hit_yourself == True:
                            text2 = FONT.render(self.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            self.active_mon.attack(used_move, player.active_mon, turn_count)
                        elif self.active_mon.flinch == True:
                            text2 = FONT.render(self.active_mon.name+' flinched!', True, (0,0,0))
                        elif self.active_mon.freeze == True:
                            if used_move.hit(self.active_mon, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                self.active_mon.freeze = False
                                self.active_mon.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''
                                text2 = FONT.render(self.active_mon.name+' used '+str(used_move.name+' '+text_self_efectivity), True, (0,0,0))
                            else:
                                text2 = FONT.render(self.active_mon.name+' is frozen!', True, (0,0,0))

                        elif self.active_mon.paralyze == True:
                            if used_move.hit(self.active_mon, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                self.active_mon.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                if self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''
                                text2 = FONT.render(self.active_mon.name+' used '+str(used_move.name+' '+text_self_efectivity), True, (0,0,0))
                            else:
                                text2 = FONT.render(self.active_mon.name+' is paralyzed!', True, (0,0,0))
                        elif used_move.hit(self.active_mon, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(self.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))

                        else:
                            self.active_mon.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            if self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 2 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.5 or self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.active_mon.effectiveness1 * self.active_mon.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                        
                            text2 = FONT.render(self.active_mon.name+' used '+str(used_move.name+' '+text_self_efectivity), True, (0,0,0))
                    else:
                        text2 = FONT.render(self.active_mon.name+' fainted', True, (0,0,0))

                    if player.active_mon.hp < 0:
                        text3 = FONT.render(player.active_mon.name+' fainted', True, (0,0,0))
                    else:
                        text3 = 0

                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.active_mon.burn == True:
                        self.active_mon.hp = (self.active_mon.hp - (self.active_mon.max_hp*(1/16)))
                        text5 = FONT.render(self.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.active_mon.poison == True:
                        self.active_mon.hp = (self.active_mon.hp - (self.active_mon.max_hp*(1/16)))
                        text7 = FONT.render(self.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if player.active_mon.confuse == True:
                        text8 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0

                    if self.active_mon.confuse == True:
                        text9 = FONT.render(self.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.active_mon.hp < 0:
                        text10 = FONT.render(self.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text10 = 0

                    if player.active_mon.hp < 0:
                        text11 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text11 = 0

            pygame.display.update()

            while wait:
                while message == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message1 = True
                                message = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
                    SCREEN.blit(text_space, (750, 820))
                    SCREEN.blit(text1, (350, 725))
                    SCREEN.blit(text2, (350, 770))
                    if text3 != 0:
                        SCREEN.blit(text3, (350, 815))
                    pygame.display.update()

                while message1 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message2 = True
                                message1 = False
                                break
                    if text4 == 0 and text5 == 0:
                        message2 = True
                        message1 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
                    SCREEN.blit(text_space, (750, 820))
                    if text4 != 0:
                        SCREEN.blit(text4, (350, 725))
                    if text5 != 0:
                        SCREEN.blit(text5, (350, 770))
                    pygame.display.update()

                while message2 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message3 = True
                                message2 = False
                                break
                    if text6 == 0 and text7 == 0:
                        message3 = True
                        message2 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
                    SCREEN.blit(text_space, (750, 820))
                    if text6 != 0:
                        SCREEN.blit(text6, (350, 725))
                    if text7 != 0:
                        SCREEN.blit(text7, (350, 770))
                    pygame.display.update()

                while message3 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                message4 = True
                                message3 = False
                                break
                    if text8 == 0 and text9 == 0:
                        message4 = True
                        message3 = False
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
                    SCREEN.blit(text_space, (750, 820))
                    if text8 != 0:
                        SCREEN.blit(text8, (350, 725))
                    if text9 != 0:
                        SCREEN.blit(text9, (350, 770))
                    pygame.display.update()

                while message4 == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                wait = False
                                message4 = False
                                break
                    self.active_mon.flinch = False
                    player.active_mon.flinch = False
                    if text10 == 0 and text11 == 0:
                        wait = False
                        message4 = False
                        break
                    text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
                    SCREEN.blit(text_space, (750, 820))
                    if text10 != 0:
                        SCREEN.blit(text10, (350, 725))
                    if text11 != 0:
                        SCREEN.blit(text11, (350, 770))
                    pygame.display.update()
                pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  


        if self.mons.index(self.active_mon) == 5 and self.active_mon.hp <= 0:
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150))  
            text_win = FONT.render('you won', True, (0,0,0))
            player.badge_case.append(self.badge) 
            won = True
            SCREEN.blit(text_win, (350, 725))
        if won == True:
            won = False
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.defeated = True
                            wait = False
                pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(350, 720, 900, 150)) 
                SCREEN.blit(text_win, (350, 725)) 
                text_space = FONT.render('press SPACE to continue', True, (0,0,0))
                SCREEN.blit(text_space, (750, 820))
                pygame.display.update()
        for mon in range(0,5):
            self.mons[mon].set_mon
        self.active_mon = self.mons[0]
        pygame.display.update()


cascade_badge = Badge('cascade badge')
volcano_badge = Badge('volcano badge')
rainbow_badge = Badge('rainbow badge')
marsh_badge = Badge('marsh badge')
boulder_badge = Badge('boulder badge')
soul_badge = Badge('soul badge')
earth_badge = Badge('earth badge')
thunder_badge = Badge('thunder badge')

gym_lvls = [2, 3, 4, 5, 6, 7, 8, 9]

brock_lvl = random.choice(gym_lvls)
gym_lvls.remove(brock_lvl)
g_graveler = GymMon(brock_lvl, 'Graveler', [55, 95, 115, 45, 45, 35], 'rock', 'ground')
g_graveler.set_attacks([tackle, rock_throw, bulldoze, earthquake, stone_edge, rock_blast, double_edge], [defense_curl])
g_rhyhorn = GymMon(brock_lvl, 'Rhyhorn', [80, 85, 95, 30, 30, 25], 'ground', 'rock')
g_rhyhorn.set_attacks([horn_attack, bulldoze, drill_run, stone_edge, earthquake, megahorn, rock_blast, fury_attack], [tail_whip, scary_face])
g_pineco = GymMon(brock_lvl, 'Pineco', [50, 65, 90, 35, 35, 15], 'bug')
g_pineco.set_attacks([tackle, bug_bite, rapid_spin, payback, double_edge, take_down], [iron_defense])
g_onix = GymMon(brock_lvl, 'Onix', [35, 45, 160, 30, 45, 70], 'rock', 'ground')
g_onix.set_attacks([tackle, rock_throw, dragon_breath, slam, iron_tail, stone_edge, double_edge, rock_slide, rock_tomb], [harden, screech])
g_forretress = GymMon(brock_lvl, 'Forretress', [75, 90, 140, 60, 60, 40], 'bug', 'steel')
g_forretress.set_attacks([zap_cannon, tackle, bug_bite, rapid_spin, payback, take_down, mirror_shot], [iron_defense])
g_golem = GymMon(brock_lvl, 'Golem', [80, 120, 130, 55, 65, 45], 'rock', 'ground')
g_golem.set_attacks([tackle, rock_throw, bulldoze, earthquake, stone_edge, rock_blast, double_edge, steamroller], [defense_curl])
brock = GymLeader(brock_lvl, 'Brock', boulder_badge, [g_graveler, g_rhyhorn, g_pineco, g_forretress, g_onix, g_golem])

misty_lvl = random.choice(gym_lvls)
gym_lvls.remove(misty_lvl)
g_staryu = GymMon(misty_lvl, 'Staryu', [30, 45, 55, 70, 55, 85], 'water')
g_staryu.set_attacks([tackle, water_gun, rapid_spin, swift, Bubble_beam, brine, psychic, hydro_pump, power_gem], [harden, confuse_ray])
g_seaking = GymMon(misty_lvl, 'Seaking', [80, 92, 65, 65, 80, 68], 'water')
g_seaking.set_attacks([megahorn, peck, horn_attack, water_pulse, poison_jab, fury_attack, waterfall], [tail_whip, supersonic, agility])
g_gyarados = GymMon(misty_lvl, 'Gyarados', [95, 125, 79, 60, 100, 81], 'water', 'flying')
g_gyarados.set_attacks([bite, twister, ice_fang, aqua_tail, crunch, hydro_pump, hurricane], [leer, scary_face])
g_golduck = GymMon(misty_lvl, 'Golduck', [80, 82, 78, 95, 80, 85], 'water')
g_golduck.set_attacks([aqua_jet, scratch, water_gun, water_pulse, zen_headbutt, aqua_tail, hydro_pump, fury_swipes], [tail_whip, screech, amnesia])
g_kingdra = GymMon(misty_lvl, 'Kingdra', [75, 95, 95, 95, 95, 85], 'water', 'dragon')
g_kingdra.set_attacks([hydro_pump, bubble, water_gun, twister, Bubble_beam, brine, dragon_pulse], [leer, agility, dragon_dance, smokescreen])
g_starmie = GymMon(misty_lvl, 'Starmie', [60, 75, 85, 100, 85, 115], 'water', 'psychic')
g_starmie.set_attacks([hydro_pump, water_gun, swift, rapid_spin], [confuse_ray])
misty = GymLeader(misty_lvl, 'Misty', cascade_badge, [g_staryu, g_seaking, g_gyarados, g_golduck, g_kingdra, g_starmie])

erika_lvl = random.choice(gym_lvls)
gym_lvls.remove(erika_lvl)
g_jumpluff = GymMon(erika_lvl, 'Jumpluff', [75, 55, 70, 55, 95, 110], 'grass', 'flying')
g_jumpluff.set_attacks([tackle, fairy_wind, giga_drain, bullet_seed, mega_drain], [tail_whip, poison_powder, stun_spore])
g_tangela = GymMon(erika_lvl, 'Tangela', [65, 55, 115, 100, 40, 60], 'grass')
g_tangela.set_attacks([vine_whip, giga_drain, ancient_power, slam, absorb, mega_drain, knock_off, power_whip], [poison_powder, growth, stun_spore, tickle])
g_victreebel = GymMon(erika_lvl, 'Victreebel', [80, 105, 65, 100, 70, 70], 'grass', 'poison')
g_victreebel.set_attacks([razor_leaf, leaf_blade, vine_whip, leaf_storm, leaf_tornado], [sweet_scent])
g_vileplume = GymMon(erika_lvl, 'Vileplume', [75, 80, 85, 110, 90, 50], 'grass', 'poison')
g_vileplume.set_attacks([petal_blizzard, acid, mega_drain], [poison_powder, stun_spore])
g_bellossom = GymMon(erika_lvl, 'Bellossom', [75, 80, 95, 90, 100, 50], 'grass')
g_bellossom.set_attacks([magical_leaf, leaf_storm, leaf_blade, petal_blizzard, mega_drain], [stun_spore, quilver_dance])
g_roselia = GymMon(erika_lvl, 'Roselia', [50, 60, 45, 100, 80, 65], 'grass', 'poison')
g_roselia.set_attacks([poison_sting, magical_leaf, giga_drain, petal_blizzard, absorb, mega_drain], [growth, stun_spore])
erika = GymLeader(erika_lvl, 'Erika', rainbow_badge, [g_jumpluff, g_tangela, g_victreebel, g_vileplume, g_bellossom, g_roselia])

janine_lvl = random.choice(gym_lvls)
gym_lvls.remove(janine_lvl)
g_crobat = GymMon(janine_lvl, 'Crobat', [85, 90, 80, 70, 80, 130], 'poison', 'flying')
g_crobat.set_attacks([astonish, bite, wing_attack, swift, poison_fang, leech_life, venoshock, air_slash, absorb], [screech, supersonic, confuse_ray])
g_weezing = GymMon(janine_lvl, 'Weezing', [65, 90, 120, 85, 70, 60], 'poison')
g_weezing.set_attacks([tackle, sludge, smog, sludge_bomb], [poison_gas, smokescreen])
g_spinarak = GymMon(janine_lvl, 'Spinarak', [40, 60, 40, 40, 40, 30], 'bug', 'poison')
g_spinarak.set_attacks([poison_sting, psychic, shadow_sneak, poison_jab, absorb, pin_missile, cross_poison], [string_shot, scary_face, agility])
g_ariados = GymMon(janine_lvl, 'Ariados', [70, 90, 70, 60, 70, 40], 'bug', 'poison')
g_ariados.set_attacks([bug_bite, poison_sting, shadow_sneak, psychic, poison_jab, absorb, pin_missile, fury_swipes, cross_poison], [swords_dance, agility, scary_face, string_shot])
g_venomoth = GymMon(janine_lvl, 'Venomoth', [70, 65, 60, 90, 75, 90], 'bug', 'poison')
g_venomoth.set_attacks([gust, bug_buzz, silver_wind, tackle, confusion, psybeam, signal_beam, leech_life, zen_headbutt, poison_fang, psychic], [quilver_dance, supersonic, poison_powder, stun_spore])
g_grimer = GymMon(janine_lvl, 'Grimer', [80, 80, 50, 40, 50, 25], 'poison')
g_grimer.set_attacks([pound, mud_bomb, sludge, sludge_wave, gunk_shot, sludge_bomb, mud_slap], [poison_gas, minimize, harden, screech])
janine = GymLeader(janine_lvl, 'Janine', soul_badge, [g_crobat, g_weezing, g_spinarak, g_ariados, g_venomoth, g_grimer])

lt_surge_lvl = random.choice(gym_lvls)
gym_lvls.remove(lt_surge_lvl)
g_raichu = GymMon(lt_surge_lvl, 'Raichu', [60, 90, 55, 90, 80, 110], 'electric')
g_raichu.set_attacks([thunder_shock, quick_attack, thunderbolt], [tail_whip])
g_voltorb = GymMon(lt_surge_lvl, 'Voltorb', [40, 30, 50, 55, 55, 100], 'electric')
g_voltorb.set_attacks([tackle, spark, swift, discharge], [screech])
g_electrode = GymMon(lt_surge_lvl, 'Electrode', [60, 50, 70, 80, 80, 150], 'electric')
g_electrode.set_attacks([tackle, spark, swift, discharge], [screech])
g_magneton = GymMon(lt_surge_lvl, 'Magneton', [50, 60, 95, 120, 70, 70], 'electric', 'steel')
g_magneton.set_attacks([zap_cannon, tackle, thunder_shock, spark, discharge], [supersonic, thunder_wave, metal_sound, screech])
g_electabuzz = GymMon(lt_surge_lvl, 'Electabuzz', [65, 83, 57, 95, 85, 105], 'electric')
g_electabuzz.set_attacks([quick_attack, thunder_shock, swift, discharge, thunderbolt, thunder], [leer, thunder_wave, screech])
g_elekid = GymMon(lt_surge_lvl, 'Elekid', [45, 63, 37, 65, 55, 95], 'electric')
g_elekid.set_attacks([quick_attack, swift, thunder_shock, discharge, thunderbolt, thunder], [leer, thunder_wave, screech])
lt_surge = GymLeader(lt_surge_lvl, 'Lt. Surge', thunder_badge, [g_raichu, g_voltorb, g_electrode, g_magneton, g_electabuzz, g_elekid])

sabrina_lvl = random.choice(gym_lvls)
gym_lvls.remove(sabrina_lvl)
g_kadabra = GymMon(sabrina_lvl, 'Kadabra', [40, 35, 30, 120, 70, 105], 'psychic')
g_kadabra.set_attacks([confusion, psybeam, psycho_cut, psychic], [])
g_espeon = GymMon(sabrina_lvl, 'Espeon', [65, 65, 60, 130, 95, 110], 'psychic')
g_espeon.set_attacks([tackle, confusion, quick_attack, swift, psybeam, psychic], [tail_whip, babydoll_eyes, sand_attack])
g_mrmime = GymMon(sabrina_lvl, 'Mr. Mime', [40, 45, 65, 100, 120, 90], 'psychic', 'fairy')
g_mrmime.set_attacks([magical_leaf, confusion, psybeam, psychic, double_slap], [meditate])
g_girafarig = GymMon(sabrina_lvl, 'Girafarig', [70, 80, 65, 90, 65, 85], 'normal', 'psychic')
g_girafarig.set_attacks([astonish, tackle, confusion, psybeam, zen_headbutt, crunch, psychic, stomp], [growl, nasty_plot, agility])
g_hypno = GymMon(sabrina_lvl, 'Hypno', [85, 73, 70, 73, 115, 67], 'psychic')
g_hypno.set_attacks([pound, confusion, headbutt, psybeam, zen_headbutt, psychic], [nasty_plot, poison_gas, swagger, meditate])
g_alakazam = GymMon(sabrina_lvl, 'Alakazam', [55, 50, 45, 135, 95, 120], 'psychic')
g_alakazam.set_attacks([confusion, psybeam, psycho_cut, psychic], [calm_mind])
sabrina = GymLeader(sabrina_lvl, 'Sabrina', marsh_badge, [g_kadabra, g_espeon, g_mrmime, g_girafarig, g_hypno, g_alakazam])

blaine_lvl = random.choice(gym_lvls)
gym_lvls.remove(blaine_lvl)
g_torkoal = GymMon(blaine_lvl, 'Torkoal', [70, 85, 140, 85, 70, 20], 'fire')
g_torkoal.set_attacks([ember, rapid_spin, body_slam, flamethrower, smog, flame_wheel, heat_wave, inferno, lava_plume], [iron_defense, amnesia, smokescreen])
g_magmar = GymMon(blaine_lvl, 'Magmar', [65, 95, 57, 100, 85, 93], 'fire')
g_magmar.set_attacks([ember, feint_attack, flamethrower, fire_blast, fire_punch, smog, flame_burst, lava_plume], [leer, confuse_ray, smokescreen])
g_rapidash = GymMon(blaine_lvl, 'Rapidash', [65, 100, 70, 80, 80, 105], 'fire')
g_rapidash.set_attacks([megahorn, poison_jab, quick_attack, ember, fire_blast, fury_attack, flame_wheel, take_down, inferno, flare_blitz, stomp, flame_charge], [growl, tail_whip, agility])
g_arcanine = GymMon(blaine_lvl, 'Arcanine', [90, 110, 80, 100, 80, 95], 'fire')
g_arcanine.set_attacks([thunder_fang, bite, fire_fang], [])
g_magcargo = GymMon(blaine_lvl, 'Magcargo', [60, 50, 120, 90, 80, 30], 'fire', 'rock')
g_magcargo.set_attacks([earth_power, ember, rock_throw, ancient_power, body_slam, flamethrower, smog, lava_plume, rock_slide], [harden, amnesia])
g_flareon = GymMon(blaine_lvl, 'Flareon', [65, 130, 60, 95, 110, 65], 'fire')
g_flareon.set_attacks([ember, tackle, quick_attack, bite, fire_fang, smog, flare_blitz, lava_plume], [tail_whip, babydoll_eyes, sand_attack, scary_face])
blaine = GymLeader(blaine_lvl, 'Blaine', volcano_badge, [g_torkoal, g_magmar, g_rapidash, g_arcanine, g_magcargo, g_flareon])

giovanni_lvl = random.choice(gym_lvls)
gym_lvls.remove(giovanni_lvl)
g_persian = GymMon(giovanni_lvl, 'Persian', [65, 70, 60, 65, 65, 115], 'normal')
g_persian.set_attacks([swift, play_rough, scratch, bite, feint_attack, slash, night_slash, fury_swipes, power_gem], [growl, screech, nasty_plot])
g_rhydon = GymMon(giovanni_lvl, 'Rhydon', [105, 130, 120, 45, 45, 40], 'ground', 'rock')
g_rhydon.set_attacks([hammer_arm, horn_attack, bulldoze, drill_run, stone_edge, earthquake, megahorn, take_down, stomp], [tail_whip])
g_nidoqueen = GymMon(giovanni_lvl, 'Nidoqueen', [90, 92, 87, 75, 85, 76], 'poison', 'ground')
g_nidoqueen.set_attacks([superpower, poison_sting, scratch, body_slam, earth_power, superpower, double_kick], [tail_whip])
g_dugtrio = GymMon(giovanni_lvl, 'Dugtrio', [35, 100, 50, 50, 70, 120], 'ground')
g_dugtrio.set_attacks([night_slash, scratch, astonish, bulldoze, mud_bomb, earth_power, slash, earthquake], [growl])
g_marowak = GymMon(giovanni_lvl, 'Marowak', [60, 80, 110, 50, 80, 45], 'ground')
g_marowak.set_attacks([bone_club, headbutt, bone_club, double_edge], [growl, tail_whip, leer])
g_kangaskhan = GymMon(giovanni_lvl, 'Kangaskhan', [105, 95, 80, 40, 80, 90], 'normal')
g_kangaskhan.set_attacks([bite, crunch, dizzy_punch, mega_punch], [leer, tail_whip])
giovanni_gym = GymLeader(giovanni_lvl, 'Giovanni', earth_badge, [g_persian, g_rhydon, g_nidoqueen, g_dugtrio, g_marowak, g_kangaskhan])


t_decidueye = Trainermon('Decidueye', [78, 107, 75, 100, 100, 70], 'grass', 'ghost')
t_decidueye.set_attacks([razor_leaf, astonish, peck, leaf_blade, brave_bird, fury_attack], [growl, nasty_plot])
hau = Trainer('Hau & Decidueye', t_decidueye)

t_pansear = Trainermon('Pansear', [50, 53, 48, 53, 48, 64], 'fire')
t_pansear.set_attacks([scratch, lick, bite, flame_burst, fire_blast, crunch, fury_swipes], [leer, amnesia])
chilli = Trainer('Chilli & Pansear', t_pansear)

t_golisopod = Trainermon('Golisopod', [75, 125, 140, 60, 90, 40], 'bug', 'water')
t_golisopod.set_attacks([furry_cutter, bug_bite, slash, pin_missile, rock_smash, razor_shell], [swords_dance, iron_defense, sand_attack])
guzma = Trainer('Guzma & Golisopod', t_golisopod)

t_vulpix = Trainermon('Vulpix', [38, 41, 40, 50, 65, 65], 'ice')
t_vulpix.set_attacks([powder_snow, ice_shard, icy_wind, payback, feint_attack, hex, ice_beam, blizzard, aurora_beam, extrasensory], [tail_whip, babydoll_eyes, confuse_ray])
lillie = Trainer('Lillie & Vulpix', t_vulpix)

t_turtonator = Trainermon('Turtonator', [60, 78, 135, 91, 85, 36], 'fire', 'dragon')
t_turtonator.set_attacks([ember, tackle, flamethrower, body_slam, dragon_pulse, smog], [iron_defense])
kiawe = Trainer('Kiawe & Turtonator', t_turtonator)

t_persian = Trainermon('Persian', [65, 60, 60, 75, 65, 115], 'dark')
t_persian.set_attacks([swift, scratch, bite, feint_attack, slash, night_slash, dark_pulse, fury_swipes, power_gem], [growl, screech, nasty_plot])
nanu = Trainer('Nanu & Persian', t_persian)

t_silvally = Trainermon('Silvally', [95, 95, 95, 95, 95, 95], 'normal')
t_silvally.set_attacks([iron_head, poison_fang, fire_fang, ice_fang, thunder_fang, tackle, pursuit, bite, aerial_ace, xscissor, crunch, air_slash, crush_claw, take_down, double_edge], [metal_sound])
gladion = Trainer('Gladion & Silvally', t_silvally)

t_squirtle = Trainermon('Squirtle', [44, 48, 65, 50, 64, 43], 'water')
t_squirtle.set_attacks([tackle, water_gun, bite, bubble, rapid_spin, water_pulse, hydro_pump], [tail_whip, withdraw, iron_defense])
tierno = Trainer('Tierno & Squirtle', t_squirtle)

t_axew = Trainermon('Axew', [46, 87, 60, 30, 40, 57], 'dragon')
t_axew.set_attacks([scratch, slash, dragon_claw, dragon_pulse], [leer, swords_dance])
iris = Trainer('Iris & Axew', t_axew)

t_pansage = Trainermon('Pansage', [50, 53, 48, 53, 48, 64], 'grass')
t_pansage.set_attacks([scratch, lick, bite, seed_bomb, crunch, vine_whip, fury_swipes], [leer])
cilan = Trainer('Cilan & Pansage', t_pansage)

t_panpour = Trainermon('Panpour', [50, 53, 48, 53, 48, 64], 'water')
t_panpour.set_attacks([scratch, lick, bite, water_gun, brine, crunch, fury_swipes], [leer])
cress = Trainer('Cress & Panpour', t_panpour)

t_braviary = Trainermon('Braviary', [100, 123, 75, 57, 75, 80], 'normal', 'flying')
t_braviary.set_attacks([superpower, peck, wing_attack, aerial_ace, slash, air_slash, fury_attack, crush_claw, brave_bird], [leer])
kukui = Trainer('Kukui & Braviary', t_braviary)

t_popplio = Trainermon('Popplio', [50, 54, 54, 66, 56, 40], 'water')
t_popplio.set_attacks([pound, water_gun, aqua_jet, Bubble_beam, hyper_voice, hydro_pump, moonblast, double_slap], [growl, babydoll_eyes])
lana = Trainer('Lana & Popplio', t_popplio)

t_hariyama = Trainermon('Hariyama', [144, 120, 60, 40, 60, 50], 'fighting')
t_hariyama.set_attacks([brine, tackle, wakeup_slap, close_combat, knock_off, arm_thrust, force_palm], [sand_attack])
hala = Trainer('Hala & Hariyama', t_hariyama)

t_fennekin = Trainermon('Fennekin', [40, 45, 40, 62, 60, 60], 'fire')
t_fennekin.set_attacks([scratch, ember, psybeam, flamethrower, psychic, fire_blast, flame_charge], [tail_whip, willowisp, howl])
serena = Trainer('Serena & Fennekin', t_fennekin)

t_bounsweet = Trainermon('Bounsweet', [42, 30, 38, 30, 38, 32], 'grass')
t_bounsweet.set_attacks([rapid_spin, razor_leaf, magical_leaf], [play_nice, sweet_scent, teeter_dance])
mallow = Trainer('Mallow & Bounsweet', t_bounsweet)

t_mudsdale = Trainermon('Mudsdale', [100, 125, 100, 55, 85, 35], 'ground')
t_mudsdale.set_attacks([bulldoze, earthquake, superpower, double_kick, stomp, mega_kick, mud_slap], [iron_defense])
hapu = Trainer('Hapu & Mudsdale', t_mudsdale)

t_pikachu = Trainermon('Pikachu', [35, 55, 40, 50, 50, 90], 'electric')
t_pikachu.set_attacks([thunder_shock, quick_attack, spark, discharge, slam, thunderbolt, thunder], [tail_whip, growl, thunder_wave])
ash = Trainer('Ash & Pikachu', t_pikachu)

t_torchic = Trainermon('Torchic', [45, 60, 40, 70, 50, 45], 'fire')
t_torchic.set_attacks([fire_punch, scratch, ember, peck, quick_attack, slash, double_kick, flare_blitz], [growl, bulk_up, sand_attack])
may = Trainer('May & Torchic', t_torchic)

t_lycanroc = Trainermon('Lycanroc', [75, 115, 65, 55, 65, 112], 'rock')
t_lycanroc.set_attacks([quick_attack, tackle, bite, rock_throw, crunch, stone_edge, rock_climb, rock_slide, rock_tomb], [leer, sand_attack, howl, scary_face])
olivia = Trainer('Olivia & Lycanroc', t_lycanroc)

t_bulbasaur = Trainermon('Bulbasaur', [45, 49, 49, 65, 65, 45], 'grass')
t_bulbasaur.set_attacks([razor_leaf, tackle, petal_blizzard, vine_whip, seed_bomb, take_down, double_edge], [growl, growth, poison_powder])
shauna = Trainer('Shauna & Bulbasaur', t_bulbasaur)



r_arbok = Trainermon('Arbok', [60, 95, 69, 65, 79, 80], 'poison')
r_arbok.set_attacks([crunch, ice_fang, thunder_fang, fire_fang, poison_sting, bite, acid, mud_bomb, acid_spray, gunk_shot], [leer, screech, glare])
ariana = Rocket('Ariana & Arbok', r_arbok)

r_seviper = Trainermon('Seviper', [73, 100, 60, 100, 60, 65], 'poison')
r_seviper.set_attacks([bite, lick, venoshock, poison_fang, night_slash, crunch], [swagger, screech, swords_dance, glare])
jessie = Rocket('Jessie & Seviper', r_seviper)

r_koffing = Trainermon('Koffing', [40, 65, 95, 60, 45, 35], 'poison')
r_koffing.set_attacks([tackle, sludge, smog, sludge_bomb], [poison_gas, smokescreen])
petrel = Rocket('Petrel & Koffing', r_koffing)

r_persian = Trainermon('Persian', [65, 70, 60, 65, 65, 115], 'normal')
r_persian.set_attacks([swift, play_rough, scratch, bite, feint_attack, slash, night_slash, fury_swipes, power_gem], [growl, screech, nasty_plot])
giovanni = Rocket('Giovanni & Persian', r_persian)

r_carnivine = Trainermon('Carnivine', [74, 100, 72, 90, 72, 46], 'grass')
r_carnivine.set_attacks([bite, vine_whip, feint_attack, crunch, leaf_tornado, power_whip], [growth, sweet_scent])
james = Rocket('James & Carnivine', r_carnivine)

r_meowth = Trainermon('Meowth', [40, 45, 35, 40, 40, 90], 'normal')
r_meowth.set_attacks([scratch, bite, feint_attack, slash, night_slash, fury_swipes], [growl, screech, nasty_plot])
r_meowth = Rocket('Meowth', r_meowth)

r_golbat = Trainermon('Golbat', [75, 80, 70, 65, 75, 90], 'poison', 'flying')
r_golbat.set_attacks([astonish, bite, wing_attack, swift, poison_fang, leech_life, venoshock, air_slash, absorb], [supersonic, confuse_ray])
proton = Rocket('Proton & Golbat', r_golbat)

