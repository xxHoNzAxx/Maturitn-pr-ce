import pygame
import random
from attacks import *

pygame.init()

FONT = pygame.font.Font('fonts/Adventure.ttf', 40)
FONT2 = pygame.font.Font('fonts/Adventure.ttf', 30)

chance_list = []

cross = pygame.image.load('pictures/maps/cross.png')
check = pygame.image.load('pictures/maps/check.png')

white_spawn = []
blue_spawn = []
green_spawn = []
orange_spawn = []
gray_spawn = []
brown_spawn = []
yellow_spawn = []
purple_spawn = []

legends = []

super_effective = {
    'normal': [''],
    'fire': ['grass', 'ice', 'bug', 'steel'],
    'water': ['fire', 'ground', 'rock'],
    'grass': ['water', 'ground', 'rock'],
    'electric': ['water', 'flying'],
    'ice': ['grass', 'ground', 'flying', 'dragon'],
    'fighting': ['normal', 'ice', 'rock', 'dark', 'steel'],
    'poison': ['grass', 'fairy'],
    'ground': ['fire', 'electric', 'poison', 'rock', 'steel'],
    'flying': ['grass', 'fighting', 'bug'],
    'psychic': ['fighting', 'poison'],
    'bug': ['grass', 'psychic', 'dark'],
    'rock': ['fire', 'ice', 'flying', 'bug'],
    'ghost': ['psychic', 'ghost'],
    'dragon': ['dragon'],
    'dark': ['psychic', 'ghost'],
    'steel': ['ice', 'rock', 'fairy'],
    'fairy': ['fighting', 'dragon', 'dark']
}

notvery_effective = {
    'normal': ['rock', 'steel'],
    'fire': ['fire', 'water', 'rock', 'dragon'],
    'water': ['water', 'grass', 'dragon'],
    'grass': ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'],
    'electric': ['grass', 'electric', 'dragon'],
    'ice': ['fire', 'water', 'ice', 'steel'],
    'fighting': ['poison', 'flying', 'psychic', 'bug', 'fairy'],
    'poison': ['poison', 'ground', 'rock', 'ghost'],
    'ground': ['grass', 'bug'],
    'flying': ['electric', 'rock', 'steel'],
    'psychic': ['psychic', 'steel'],
    'bug': ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'],
    'rock': ['fighting', 'ground', 'steel'],
    'ghost': ['dark'],
    'dragon': ['steel'],
    'dark': ['fighting', 'dark', 'fairy'],
    'steel': ['fire', 'water', 'electric', 'steel'],
    'fairy': ['fire', 'poison', 'steel']
}

no_effect = {
    'normal': ['ghost'],
    'fire': [''],
    'water': [''],
    'grass': [''],
    'electric': ['ground'],
    'ice': [''],
    'fighting': ['ghost'],
    'poison': ['steel'],
    'ground': ['flying'],
    'flying': [''],
    'psychic': ['dark'],
    'bug': [''],
    'rock': [''],
    'ghost': ['normal'],
    'dragon': ['fairy'],
    'dark': [''],
    'steel': [''],
    'fairy': ['']
}

def draw_status(who, pos):
    if who.burn == True:
        SCREEN.blit(pygame.image.load('pictures/maps/burn.png'), (pos[0]+5, pos[1]+70))
    if who.poison == True:
        SCREEN.blit(pygame.image.load('pictures/maps/poison.png'), (pos[0]+5, pos[1]+75))
    if who.paralyze == True:
        SCREEN.blit(pygame.image.load('pictures/maps/paralyze.png'), (pos[0]+5, pos[1]+80))
    if who.freeze == True:
        SCREEN.blit(pygame.image.load('pictures/maps/freeze.png'), (pos[0]+5, pos[1]+85))


class Basic:
    def __init__(self, name, base_stats1, type=[]):
        self.name1 = name
        self.name = self.name1
        self.base_stats = base_stats1
        self.base_stats_pernament = base_stats1
        self.base_stats1_pernament = base_stats1
        self.type1 = type[0]
        self.type2 = type[1]
        self.stage1_type1 = type[2]
        self.stage1_type2 = type[3]
        self.stage2_type1 = type[4]
        self.stage2_type2 = type[5]
        self.image1 = pygame.image.load('pictures/mon_img/'+ self.name + '.png')
        for i in random.choices(range(1,11), weights=(33,20,15,10,7,5,4,3,2,1), k=1):
            self.lvl = i
        self.b_hp = base_stats1[0]
        self.b_att = base_stats1[1]
        self.b_defense = base_stats1[2]
        self.b_sp_att = base_stats1[3]
        self.b_sp_def = base_stats1[4]
        self.b_spd = base_stats1[5]
        self.catch_visible = False
        self.fight_visible = False
        self.z_rect_visible = False
        self.pc_visible = False
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        self.mega = False
        self.mega_evolved = False
        self.set = True

        if self.type1 in ['normal', 'flying', 'fairy']:
            white_spawn.append(self)
        elif self.type1 in ['fire', 'dark']:
            orange_spawn.append(self)
        elif self.type1 in ['poison', 'psychic', 'ghost']:
            purple_spawn.append(self)
        elif self.type1 in ['rock', 'steel']:
            gray_spawn.append(self)
        elif self.type1 in ['electric', 'ice']:
            yellow_spawn.append(self)
        elif self.type1 in ['water']:
            blue_spawn.append(self)
        elif self.type1 in ['grass', 'bug']:
            green_spawn.append(self)
        elif self.type1 in ['ground', 'dragon', 'fighting']:
            brown_spawn.append(self)


    def set_attacks(self, attacks=[], status=[]):
        self.dmg_attacks = attacks
        self.status_attacks = status
        self.attacks_respawn = self.dmg_attacks + self.status_attacks
        self.attack_list = self.dmg_attacks + self.status_attacks
        self.set_mon()

    def set_mon(self):
        self.burn = False
        self.confuse = False
        self.hit_yourself = False
        self.poison = False
        self.flinch = False
        self.freeze = False
        self.paralyze = False
        if self.mega_evolved == True:
            self.name = self.name4
            self.base_stats = []
            self.base_stats.extend(self.base_stats4_pernament)
        elif isinstance(self, Stage2):
            if self.lvl == 10:
                self.name = self.name3
                self.base_stats = []
                self.base_stats.extend(self.base_stats3_pernament)
            elif self.lvl > 5:
                self.name = self.name2
                self.base_stats = []
                self.base_stats.extend(self.base_stats2_pernament)
            else:
                self.name = self.name1
                self.base_stats = []
                self.base_stats.extend(self.base_stats1_pernament)
        elif isinstance(self, Stage1):
            if self.lvl > 5:
                self.name = self.name2
                self.base_stats = []
                self.base_stats.extend(self.base_stats2_pernament)
            else:
                self.name = self.name1
                self.base_stats = []
                self.base_stats.extend(self.base_stats1_pernament)
        else:
            self.name = self.name1
            self.base_stats = []
            self.base_stats.extend(self.base_stats1_pernament)

        self.b_hp = self.base_stats[0]
        self.b_att = self.base_stats[1]
        self.b_defense = self.base_stats[2]
        self.b_sp_att = self.base_stats[3]
        self.b_sp_def = self.base_stats[4]
        self.b_spd = self.base_stats[5]
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
        if self.set == True:
            self.set = False
            self.attack1 = random.choice(self.attack_list)
            self.attack_list.remove(self.attack1)
            if self.attack1 in self.status_attacks:
                self.attack2 = random.choice(self.dmg_attacks)
                self.attack_list.remove(self.attack2)
            else:
                self.attack2 = random.choice(self.attack_list)
                self.attack_list.remove(self.attack2)
        self.image = self.image1
        self.small_image = pygame.transform.scale(self.image, (57,50))
        if self.mega_evolved == False:
            if self.lvl > 5:
                if self.stage1_type1 != 0:
                    self.type1 = self.stage1_type1
                if self.stage1_type2 != 0:
                    self.type2 = self.stage1_type2
            if self.lvl == 10:
                if self.stage2_type1 != 0:
                    self.type1 = self.stage2_type1
                if self.stage2_type2 != 0:
                    self.type2 = self.stage2_type2
        else:
            self.image = pygame.image.load('pictures/mon_img/'+self.name+'.png')
            self.small_image = pygame.transform.scale(self.image, (57,50))
            self.max_hp = (((2*self.hp4+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
            self.hp = (((2*self.hp4+self.ivs[0]+21)*self.lvl)/100)+self.lvl + 10
            self.att = (((2*self.att4+self.ivs[1]+21)*self.lvl)/100)+5
            self.defense = (((2*self.def4+self.ivs[2]+21)*self.lvl)/100)+5
            self.sp_att = (((2*self.sp_att4+self.ivs[3]+21)*self.lvl)/100)+5
            self.sp_def = (((2*self.sp_def4+self.ivs[4]+21)*self.lvl)/100)+5
            self.spd = (((2*self.spd4+self.ivs[5]+21)*self.lvl)/100)+5
            self.type1 = self.type1m
            self.type2 = self.type2m

    def respawn_mon(self):
        self.set = True
        self.attack_list = []
        self.attack_list.extend(self.attacks_respawn)
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        for i in random.choices(range(1,11), weights=(33,20,15,10,7,5,4,3,2,1), k=1):
            self.lvl = i
        self.set_mon()


    def lvlup(self):
        if self.lvl < 10:
            self.lvl += 1
            self.set_mon()
        else:
            self.burn = False
            self.confuse = False
            self.hit_yourself = False
            self.poison = False
            self.flinch = False
            self.sleep = False
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

        for i in chance_list:
            if isinstance(i, UltraBeast):
                i.respawn_beast()
            

    def can_mega(self, name, stats, type1, type2):
        self.mega = True
        self.name4 = name
        self.base_stats4 = stats
        self.hp4 = stats[0]
        self.att4 = stats[1]
        self.def4 = stats[2]
        self.sp_att4 = stats[3]
        self.sp_def4 = stats[4]
        self.spd4 = stats[5]
        self.type1m = type1
        self.type2m = type2

    def mega_evolve(self):
        self.base_stats = []
        self.base_stats.extend(self.base_stats4)
        self.base_stats_pernament = []
        self.base_stats_pernament.extend(self.base_stats4)
        self.base_stats4_pernament = []
        self.base_stats4_pernament.extend(self.base_stats4)
        self.name = self.name4
        self.mega_evolved = True
        self.mega = False
        self.set_mon()

    def draw_spawn_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        SCREEN.blit(self.image, (pos[0]+70, pos[1]+60))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        text_lvl = FONT.render('lvl:'+str(self.lvl), True, (0, 0, 0))
        hp = round((100*self.hp)/self.max_hp)
        text_hp = FONT.render('HP: '+str(hp)+'%', True, (0, 0, 0))

        if ((100*self.hp)/self.max_hp) < 20:
            color = (225, 0, 0)
        elif ((100*self.hp)/self.max_hp) < 50:
            color = (225, 165, 0)
        else:
            color = (0, 225, 0)
        
        draw_status(self, pos)

        pygame.draw.rect(SCREEN, color, pygame.Rect(pos[0]+50, pos[1]+300, (((100*self.hp)/self.max_hp)*3), 60))
        SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
        SCREEN.blit(text_lvl, (pos[0]+270, pos[1]+10))
        SCREEN.blit(text_hp, (pos[0]+50, pos[1]+300))

        self.fight_rect = pygame.Rect(pos[0]+20, pos[1]+500, 150, 60)
        self.catch_rect = pygame.Rect(pos[0]+230, pos[1]+500, 150, 60)
        text_fight = FONT.render('Fight', True, (0, 0, 0))
        text_catch = FONT.render('Catch', True, (0, 0, 0))
        self.catch_visible = True
        self.fight_visible = True
        
        pygame.draw.rect(SCREEN, (0, 200, 0), self.catch_rect)
        SCREEN.blit(text_catch, (pos[0]+250, pos[1]+505))
        
        pygame.draw.rect(SCREEN, (200, 0, 0), self.fight_rect)
        SCREEN.blit(text_fight, (pos[0]+40, pos[1]+505))
        
        pygame.display.update()

    def draw_attack_card(self, owner, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        SCREEN.blit(self.image, (pos[0]+70, pos[1]+60))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        text_lvl = FONT.render('lvl:'+str(self.lvl), True, (0, 0, 0))
        hp = round((100*self.hp)/self.max_hp, 2)
        text_hp = FONT.render('HP: '+str(hp)+'%', True, (0, 0, 0))
        text_attack1 = FONT2.render(str(self.attack1.name), True, (0, 0, 0))
        text_dmg1 = FONT2.render(str(self.attack1.dmg), True, (0, 0, 0))
        text_attack2 = FONT2.render(str(self.attack2.name), True, (0, 0, 0))
        text_dmg2 = FONT2.render(str(self.attack2.dmg), True, (0, 0, 0))

        if ((100*self.hp)/self.max_hp) < 20:
            color = (225, 0, 0)
        elif ((100*self.hp)/self.max_hp) < 50:
            color = (225, 165, 0)
        else:
            color = (0, 225, 0)

        draw_status(self, pos)

        self.attack1_visible = True
        self.attack2_visible = True
        self.attack1_rect = pygame.Rect(pos[0]+20, pos[1]+366, 350, 60)
        self.attack2_rect = pygame.Rect(pos[0]+20, pos[1]+435, 350, 60)
        pygame.draw.rect(SCREEN, attack_color[self.attack1.type], self.attack1_rect)
        pygame.draw.rect(SCREEN, attack_color[self.attack2.type], self.attack2_rect)
        pygame.draw.rect(SCREEN, color, pygame.Rect(pos[0]+50, pos[1]+300, (((100*self.hp)/self.max_hp)*3), 60))
        SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
        SCREEN.blit(text_lvl, (pos[0]+270, pos[1]+10))
        SCREEN.blit(text_hp, (pos[0]+50, pos[1]+300))
        SCREEN.blit(text_attack1, (pos[0]+25, pos[1]+378))
        SCREEN.blit(text_dmg1, (pos[0]+300, pos[1]+378))
        SCREEN.blit(text_attack2, (pos[0]+25, pos[1]+447))
        SCREEN.blit(text_dmg2, (pos[0]+300, pos[1]+447))
        
        
        for i in owner.z_moves:
            if i.zname.type == self.attack1.type:
                self.z_move = i
                i.sp_atk = self.attack1.sp_atk
                text_zmove = FONT2.render(str(i.zname.name), True, (0, 0, 0))
                text_zdmg = FONT2.render(str(self.attack1.dmg+i.zname.dmg), True, (0, 0, 0))
                self.z_rect_visible = True
                self.z_rect = pygame.Rect(pos[0]+20, pos[1]+504, 350, 60)
                pygame.draw.rect(SCREEN, attack_color[i.zname.type], self.z_rect)
                SCREEN.blit(text_zmove, (pos[0]+25, pos[1]+516))
                SCREEN.blit(text_zdmg, (pos[0]+300, pos[1]+516))
        pygame.display.update()

    def draw_info_card(self, pos):
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 400, 600))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1], 1, 650))
        text_name = FONT.render(self.name, True, (0, 0, 0))
        text_lvl = FONT.render('lvl:'+str(self.lvl), True, (0, 0, 0))
        SCREEN.blit(text_name, (pos[0]+50, pos[1]+10))
        SCREEN.blit(text_lvl, (pos[0]+270, pos[1]+10))
        SCREEN.blit(FONT2.render('IVs:', True, (0, 0, 0)), (pos[0]+130, pos[1]+70))
        SCREEN.blit(FONT2.render('HP:         '+str(self.ivs[0]), True, (0, 0, 0)), (pos[0]+20, pos[1]+110))
        SCREEN.blit(FONT2.render('Att:        '+str(self.ivs[1]), True, (0, 0, 0)), (pos[0]+20, pos[1]+140))
        SCREEN.blit(FONT2.render('Def:        '+str(self.ivs[2]), True, (0, 0, 0)), (pos[0]+20, pos[1]+170))
        SCREEN.blit(FONT2.render('Sp Att:    '+str(self.ivs[3]), True, (0, 0, 0)), (pos[0]+20, pos[1]+200))
        SCREEN.blit(FONT2.render('Sp Def:    '+str(self.ivs[4]), True, (0, 0, 0)), (pos[0]+20, pos[1]+230))
        SCREEN.blit(FONT2.render('Spd:        '+str(self.ivs[5]), True, (0, 0, 0)), (pos[0]+20, pos[1]+260))

        SCREEN.blit(FONT2.render('stats:', True, (0, 0, 0)), (pos[0]+250, pos[1]+70))
        SCREEN.blit(FONT2.render(str(self.base_stats[0]), True, (0, 0, 0)), (pos[0]+260, pos[1]+110))
        SCREEN.blit(FONT2.render(str(self.base_stats[1]), True, (0, 0, 0)), (pos[0]+260, pos[1]+140))
        SCREEN.blit(FONT2.render(str(self.base_stats[2]), True, (0, 0, 0)), (pos[0]+260, pos[1]+170))
        SCREEN.blit(FONT2.render(str(self.base_stats[3]), True, (0, 0, 0)), (pos[0]+260, pos[1]+200))
        SCREEN.blit(FONT2.render(str(self.base_stats[4]), True, (0, 0, 0)), (pos[0]+260, pos[1]+230))
        SCREEN.blit(FONT2.render(str(self.base_stats[5]), True, (0, 0, 0)), (pos[0]+260, pos[1]+260))

        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1]+60, 400, 1))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1]+320, 400, 1))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1]+380, 400, 1))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0]+220, pos[1]+60, 1, 260))

        if self.type2 != '':
            SCREEN.blit(FONT2.render('Type:   '+str(self.type1)+', '+str(self.type2), True, (0, 0, 0)), (pos[0]+20, pos[1]+320))
        else:
            SCREEN.blit(FONT2.render('Type:   '+str(self.type1), True, (0, 0, 0)), (pos[0]+20, pos[1]+320))
        SCREEN.blit(FONT2.render('Attacks:', True, (0, 0, 0)), (pos[0]+20, pos[1]+400))
        SCREEN.blit(FONT2.render(str(self.attack1.name), True, (0, 0, 0)), (pos[0]+40, pos[1]+440))
        SCREEN.blit(FONT2.render(str(self.attack2.name), True, (0, 0, 0)), (pos[0]+40, pos[1]+480))

        SCREEN.blit(FONT2.render('Dmg:', True, (0, 0, 0)), (pos[0]+280, pos[1]+400))
        SCREEN.blit(FONT2.render(str(self.attack1.dmg), True, (0, 0, 0)), (pos[0]+300, pos[1]+440))
        SCREEN.blit(FONT2.render(str(self.attack2.dmg), True, (0, 0, 0)), (pos[0]+300, pos[1]+480))

        SCREEN.blit(FONT2.render('Basic:', True, (0, 0, 0)), (pos[0]+10, pos[1]+550))
        SCREEN.blit(FONT2.render('Stage1:', True, (0, 0, 0)), (pos[0]+110, pos[1]+550))
        SCREEN.blit(FONT2.render('Stage2:', True, (0, 0, 0)), (pos[0]+200, pos[1]+550))
        SCREEN.blit(FONT2.render('Mega:', True, (0, 0, 0)), (pos[0]+310, pos[1]+550))

        if self.mega == True:
            SCREEN.blit(check, (pos[0]+325,pos[1]+600))

        else:
            SCREEN.blit(cross, (pos[0]+325,pos[1]+600))

        if isinstance(self, Stage2):
            SCREEN.blit(check, (pos[0]+225,pos[1]+600))
            SCREEN.blit(check, (pos[0]+125,pos[1]+600))
            SCREEN.blit(check, (pos[0]+25,pos[1]+600))

        elif isinstance(self, Stage1):
            SCREEN.blit(cross, (pos[0]+225,pos[1]+600))
            SCREEN.blit(check, (pos[0]+125,pos[1]+600))
            SCREEN.blit(check, (pos[0]+25,pos[1]+600))
        
        else:
            SCREEN.blit(cross, (pos[0]+225,pos[1]+600))
            SCREEN.blit(cross, (pos[0]+125,pos[1]+600))
            SCREEN.blit(check, (pos[0]+25,pos[1]+600))

        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0], pos[1]+520, 400, 1))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0]+100, pos[1]+520, 1, 130))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0]+195, pos[1]+520, 1, 130))
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(pos[0]+300, pos[1]+520, 1, 130))

    def draw_team(self, pos):
        self.small_image = pygame.transform.scale(self.image, (57,50))
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(pos[0], pos[1], 240, 60))
        SCREEN.blit(self.small_image, (pos[0], pos[1]+5))
        if ((100*self.hp)/self.max_hp) < 0:
            hp = 0
        else:
            hp = round((100*self.hp)/self.max_hp, 2)
        text_hp = FONT2.render('HP: '+str(hp)+'%', True, (0, 0, 0))
        SCREEN.blit(text_hp, (pos[0]+90, pos[1]+5))
        pygame.display.update()

    def attack(self, move, enemy, turn_count):
        self.effectiveness1 = 1
        self.effectiveness2 = 1
        self.dmg = 0
        if move.type == 'zcrystal':
            for i in super_effective[move.zname.type]:
                if i == enemy.type1:
                    self.effectiveness1 = 2
                if enemy.type2 != '':
                    if i == enemy.type2:
                        self.effectiveness2 = 2

            for i in notvery_effective[move.zname.type]:
                if i == enemy.type1:
                    self.effectiveness1 = 0.5
                if enemy.type2 != '':
                    if i == enemy.type2:
                        self.effectiveness2 = 0.5
            
            for i in no_effect[move.zname.type]:
                if i == enemy.type1:
                    self.effectiveness1 = 0
                if enemy.type2 != '':
                    if i == enemy.type2:
                        self.effectiveness2 = 0

            if self.hit_yourself == True:
                if self.attack1.sp_atk == 'physical':
                    self.dmg = (((((2*self.lvl)/5)+2)*40*(self.att/self.defense)/50)+2)
                if self.attack1.sp_atk == 'special':
                    self.dmg = (((((2*self.lvl)/5)+2)*40*(self.sp_att/self.sp_def)/50)+2)
                self.hp = self.hp - self.dmg
            else:
                attack_effect(move, self, enemy, turn_count)
                if self.attack1.sp_atk == 'physical':
                    self.dmg = ((((((2*self.lvl)/5)+2)*(self.attack1.dmg+move.zname.dmg)*(self.att/enemy.defense)/50)+2)*self.effectiveness1*self.effectiveness2)
                if self.attack1.sp_atk == 'special':
                    self.dmg = ((((((2*self.lvl)/5)+2)*(self.attack1.dmg+move.zname.dmg)*(self.sp_att/enemy.sp_def)/50)+2)*self.effectiveness1*self.effectiveness2)
                if self.attack1.sp_atk == 'status':
                    self.dmg = ((((((2*self.lvl)/5)+2)*move.zname.dmg*(self.sp_att/enemy.sp_def)/50)+2)*self.effectiveness1*self.effectiveness2)
                self.dmg = self.dmg*move.multiplier
                for i in range(0, move.hit_number):
                    enemy.hp = enemy.hp - self.dmg
                self.hp = self.hp + (self.dmg*move.heal_multiplier)
                self.hp = self.hp - (self.dmg*move.selfhit_multiplier)
                if self.hp >= self.max_hp:
                    self.hp = self.max_hp

        else:
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
                
                

    def fight(self, player, move, turn_count):
        turn_count = turn_count
        text3, text4, text5, text6, text7, text8, text9, text10, text11 = 0,0,0,0,0,0,0,0,0
        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(300, 720, 900, 150))
        wait = True
        message = True
        message1 = False
        message2 = False
        message3 = False
        message4 = False
        if self.hp > 0:
            if player.active_mon.hp > 0:
                if self.spd > player.active_mon.spd:
                    used_move = random.choice((self.attack1, self.attack2))
                    if self.confuse == True and random.randrange(1,4) == 1:
                        self.hit_yourself = True
                    else:
                        self.hit_yourself = False

                    if self.hit_yourself == True: 
                        text1 = FONT.render(self.name+' hurt itself in its confusion!', True, (0, 0, 0))
                        self.attack(used_move, player.active_mon, turn_count)
                    elif self.flinch == True:
                        text1 = FONT.render(self.name+' flinched!', True, (0, 0, 0))
                    elif self.freeze == True:
                        if used_move.hit(self, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            self.freeze = False
                            self.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.name+' is frozen!', True, (0, 0, 0))
                    elif self.paralyze == True:
                        if used_move.hit(self, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            self.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                            text1 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.name+' is paralyzed!', True, (0, 0, 0))
                    elif used_move.hit(self, player.active_mon) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                    else:
                        self.attack(used_move, player.active_mon, turn_count)
                        if used_move.sp_atk == 'status':
                            text_self_efectivity = ''
                        elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                            text_self_efectivity = '(supereffective)'
                        elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                            text_self_efectivity = '(not very effective)'
                        elif self.effectiveness1 * self.effectiveness2 == 0:
                            text_self_efectivity = '(no effect)'
                        else:
                            text_self_efectivity = ''

                        text1 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                        
                    
                    if player.active_mon.hp > 0:
                        if player.active_mon.confuse == True and random.randrange(1,4) == 1:
                            player.active_mon.hit_yourself = True
                        else:
                            player.active_mon.hit_yourself = False
                        if player.active_mon.hit_yourself == True:
                            text2 = FONT.render(player.active_mon.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            player.active_mon.attack(move, self, turn_count)
                        elif player.active_mon.flinch == True:
                            text2 = FONT.render(player.active_mon.name+' flinched!', True, (0, 0, 0))
                        elif player.active_mon.freeze == True:
                            if move.hit(player.active_mon, self) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                player.active_mon.freeze = False
                                player.active_mon.attack(move, self, turn_count)
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
                            if move.hit(player.active_mon, self) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                player.active_mon.attack(move, self, turn_count)
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
                        elif move.hit(player.active_mon, self) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))

                        else:
                            player.active_mon.attack(move, self, turn_count)
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
                        

                    if self.hp < 0:
                        text3 = FONT.render(self.name+' fainted', True, (0, 0, 0))
                    else:
                        text3 = 0


                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.burn == True:
                        self.hp = (self.hp - (self.max_hp*(1/16)))
                        text5 = FONT.render(self.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.poison == True:
                        self.hp = (self.hp - (self.max_hp*(1/16)))
                        text7 = FONT.render(self.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if player.active_mon.confuse == True:
                        text8 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0
                    
                    if self.confuse == True:
                        text9 = FONT.render(self.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.hp < 0:
                        text10 = FONT.render(self.name+' fainted', True, (0, 0, 0))
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
                        player.active_mon.attack(move, self, turn_count)
                    elif player.active_mon.flinch == True:
                        text1 = FONT.render(player.active_name+' flinched!', True, (0, 0, 0))
                    elif player.active_mon.freeze == True:
                        if move.hit(player.active_mon, self) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,6) == 1:
                            player.active_mon.freeze = False
                            player.active_mon.attack(move, self, turn_count)
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
                        else:
                            text1 = FONT.render(player.active_mon.name+' is frozen!', True, (0, 0, 0))

                    elif player.active_mon.paralyze == True:
                        if move.hit(player.active_mon, self) == 0:
                            if random.randrange(1,3) == 1:
                                text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                            else:
                                text1 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))
                        elif random.randrange(1,5) != 1:
                            player.active_mon.attack(move, self, turn_count)
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
                        else:
                            text1 = FONT.render(player.active_mon.name+' is paralyzed!', True, (0, 0, 0))
                    elif move.hit(player.active_mon, self) == 0:
                        if random.randrange(1,3) == 1:
                            text1 = FONT.render(player.active_mon.name+' missed!', True, (0, 0, 0))
                        else:
                            text1 = FONT.render(self.name+' avoided the attack!', True, (0, 0, 0))
                    else:


                        player.active_mon.attack(move, self, turn_count)
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

                    if self.hp > 0:
                        used_move = random.choice((self.attack1, self.attack2))
                        if self.confuse == True and random.randrange(1,4) == 1:
                            self.hit_yourself = True
                        else:
                            self.hit_yourself = False
                        if self.hit_yourself == True:
                            text2 = FONT.render(self.name+' hurt itself in its confusion!', True, (0, 0, 0))
                            self.attack(used_move, player.active_mon, turn_count)
                        elif self.flinch == True:
                            text2 = FONT.render(self.name+' flinched!', True, (0, 0, 0))
                        elif self.freeze == True:
                            if used_move.hit(self, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,6) == 1:
                                self.freeze = False
                                self.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.effectiveness1 * self.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''
                                text2 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.name+' is frozen!', True, (0, 0, 0))

                        elif self.paralyze == True:
                            if used_move.hit(self, player.active_mon) == 0:
                                if random.randrange(1,3) == 1:
                                    text2 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                                else:
                                    text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))
                            elif random.randrange(1,5) != 1:
                                self.attack(used_move, player.active_mon, turn_count)
                                if used_move.sp_atk == 'status':
                                    text_self_efectivity = ''
                                elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                                    text_self_efectivity = '(supereffective)'
                                elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                                    text_self_efectivity = '(not very effective)'
                                elif self.effectiveness1 * self.effectiveness2 == 0:
                                    text_self_efectivity = '(no effect)'
                                else:
                                    text_self_efectivity = ''

                                text2 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))
                            else:
                                text2 = FONT.render(self.name+' is paralyzed!', True, (0, 0, 0))

                        elif used_move.hit(self, player.active_mon) == 0:
                            if random.randrange(1,3) == 1:
                                text2 = FONT.render(self.name+' missed!', True, (0, 0, 0))
                            else:
                                text2 = FONT.render(player.active_mon.name+' avoided the attack!', True, (0, 0, 0))

                        else:
                            self.attack(used_move, player.active_mon, turn_count)
                            if used_move.sp_atk == 'status':
                                text_self_efectivity = ''
                            elif self.effectiveness1 * self.effectiveness2 == 2 or self.effectiveness1 * self.effectiveness2 == 4:
                                text_self_efectivity = '(supereffective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0.5 or self.effectiveness1 * self.effectiveness2 == 0.25:
                                text_self_efectivity = '(not very effective)'
                            elif self.effectiveness1 * self.effectiveness2 == 0:
                                text_self_efectivity = '(no effect)'
                            else:
                                text_self_efectivity = ''
                        
                            text2 = FONT.render(self.name+' used '+str(used_move.name)+' '+text_self_efectivity, True, (0, 0, 0))

                    else:
                        text2 = FONT.render(self.name+' fainted', True, (0, 0, 0))
                        

                    if player.active_mon.hp < 0:
                        text3 = FONT.render(player.active_mon.name+' fainted', True, (0, 0, 0))
                    else:
                        text3 = 0


                    if player.active_mon.burn == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text4 = FONT.render(player.active_mon.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text4 = 0

                    if self.burn == True:
                        self.hp = (self.hp - (self.max_hp*(1/16)))
                        text5 = FONT.render(self.name+' is hurt by it´s burn', True, (0, 0, 0))
                    else:
                        text5 = 0

                    if player.active_mon.poison == True:
                        player.active_mon.hp = (player.active_mon.hp - (player.active_mon.max_hp*(1/16)))
                        text6 = FONT.render(player.active_mon.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text6 = 0
                    
                    if self.poison == True:
                        self.hp = (self.hp - (self.max_hp*(1/16)))
                        text7 = FONT.render(self.name+' is hurt by poison', True, (0, 0, 0))
                    else:
                        text7 = 0

                    if player.active_mon.confuse == True:
                        text8 = FONT.render(player.active_mon.name+' is confused!', True, (0, 0, 0))
                    else:
                        text8 = 0
                    
                    if self.confuse == True:
                        text9 = FONT.render(self.name+' is confused!', True, (0, 0, 0))
                    else:
                        text9 = 0

                    if self.hp < 0:
                        text10 = FONT.render(self.name+' fainted', True, (0, 0, 0))
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
                    self.flinch = False
                    player.active_mon.flinch = False
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
                    self.flinch = False
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

        if self.hp <= 0:
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


class Stage1(Basic):
    def __init__(self, name, name2, base_stats1, base_stats2, type):
        self.name2 = name2
        self.image2 = pygame.image.load('pictures/mon_img/' +self.name2+ '.png')
        super().__init__(name, base_stats1, type)
        self.base_stats_pernament = base_stats1
        self.base_stats2_pernament = base_stats2
        hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats2_pernament[0], self.base_stats2_pernament[1], self.base_stats2_pernament[2], self.base_stats2_pernament[3], self.base_stats2_pernament[4], self.base_stats2_pernament[5]

    def set_mon(self):
        if self.lvl > 5:
            self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats2_pernament[0], self.base_stats2_pernament[1], self.base_stats2_pernament[2], self.base_stats2_pernament[3], self.base_stats2_pernament[4], self.base_stats2_pernament[5]
            self.base_stats_pernament = self.base_stats2_pernament
            self.base_stats = self.base_stats2_pernament
            super().set_mon()
            if self.mega_evolved == False:
                self.image = self.image2
                self.name = self.name2
                self.small_image = pygame.transform.scale(self.image, (57,50))
        else:
            self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats_pernament[0], self.base_stats_pernament[1], self.base_stats_pernament[2], self.base_stats_pernament[3], self.base_stats_pernament[4], self.base_stats_pernament[5]
            super().set_mon()

class Stage2(Basic):
    def __init__(self, name, name2, name3, base_stats1, base_stats2, base_stats3, type):
        self.name2 = name2
        self.image2 = pygame.image.load('pictures/mon_img/' +self.name2+ '.png')
        self.name3 = name3
        self.image3 = pygame.image.load('pictures/mon_img/' +self.name3+ '.png')
        self.base_stats_pernament = base_stats1
        self.base_stats2_pernament = base_stats2
        self.base_stats3_pernament = base_stats3
        self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats2_pernament[0], self.base_stats2_pernament[1], self.base_stats2_pernament[2], self.base_stats2_pernament[3], self.base_stats2_pernament[4], self.base_stats2_pernament[5]
        self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats3_pernament[0], self.base_stats3_pernament[1], self.base_stats3_pernament[2], self.base_stats3_pernament[3], self.base_stats3_pernament[4], self.base_stats3_pernament[5]
        super().__init__(name, base_stats1, type)

    def set_mon(self):
        if self.lvl > 5 and self.lvl < 10:
            self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats2_pernament[0], self.base_stats2_pernament[1], self.base_stats2_pernament[2], self.base_stats2_pernament[3], self.base_stats2_pernament[4], self.base_stats2_pernament[5]
            self.base_stats_pernament = self.base_stats2_pernament
            self.base_stats = self.base_stats2_pernament
            super().set_mon()
            if self.mega_evolved == False:
                self.name = self.name2
                self.image = self.image2
                self.small_image = pygame.transform.scale(self.image, (57,50))
        elif self.lvl == 10:
            self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats3_pernament[0], self.base_stats3_pernament[1], self.base_stats3_pernament[2], self.base_stats3_pernament[3], self.base_stats3_pernament[4], self.base_stats3_pernament[5]
            self.base_stats_pernament = self.base_stats3_pernament
            self.base_stats = self.base_stats3_pernament
            super().set_mon()
            if self.mega_evolved == False:
                self.name = self.name3
                self.image = self.image3
                self.small_image = pygame.transform.scale(self.image, (57,50))
        else:
            self.b_hp, self.b_att, self.b_defense, self.b_sp_att, self.b_sp_def, self.b_spd = self.base_stats_pernament[0], self.base_stats_pernament[1], self.base_stats_pernament[2], self.base_stats_pernament[3], self.base_stats_pernament[4], self.base_stats_pernament[5]
            super().set_mon()

class Legendary(Basic):
    def __init__(self, name, base_stats, types=[]):
        self.name1 = name
        self.name = name
        self.lvl = 1
        self.base_stats = base_stats
        self.base_stats1 = base_stats
        self.base_stats1_pernament = base_stats
        self.base_stats_pernament = base_stats
        self.type = type
        self.type1 = types[0]
        self.type2 = types[1]
        self.stage1_type1 = types[2]
        self.stage1_type2 = types[3]
        self.stage2_type1 = types[4]
        self.stage2_type2 = types[5]
        self.image1 = pygame.image.load('pictures/mon_img/'+ self.name + '.png')
        self.b_hp = base_stats[0]
        self.pc_visible = False
        self.b_att = base_stats[1]
        self.b_defense = base_stats[2]
        self.b_sp_att = base_stats[3]
        self.b_sp_def = base_stats[4]
        self.b_spd = base_stats[5]
        self.set = True
        self.mega = False
        self.mega_evolved = False
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        legends.append(self)

class UltraBeast(Basic):
    def __init__(self, name, base_stats, types=[]):
        self.name1 = name
        self.name = name
        self.lvl = 1
        self.base_stats = base_stats
        self.base_stats1 = base_stats
        self.base_stats1_pernament = base_stats
        self.base_stats_pernament = base_stats
        self.type = type
        self.type1 = types[0]
        self.type2 = types[1]
        self.stage1_type1 = types[2]
        self.stage1_type2 = types[3]
        self.stage2_type1 = types[4]
        self.stage2_type2 = types[5]
        self.image1 = pygame.image.load('pictures/mon_img/'+ self.name + '.png')
        self.b_hp = base_stats[0]
        self.pc_visible = False
        self.b_att = base_stats[1]
        self.b_defense = base_stats[2]
        self.b_sp_att = base_stats[3]
        self.b_sp_def = base_stats[4]
        self.b_spd = base_stats[5]
        self.set = True
        self.mega = False
        self.mega_evolved = False
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        chance_list.append(self)
    
    def respawn_beast(self):
        self.set = True
        self.attack_list = []
        self.attack_list.extend(self.attacks_respawn)
        self.ivs = [random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31),random.randrange(0,31)]
        self.set_mon()


bulbasaur = Stage2('Bulbasaur', 'Ivysaur', 'Venusaur', [45, 49, 49, 65, 65, 45], [60, 62, 63, 80, 80, 60], [80, 82, 83, 100, 100, 80], ['grass', 'poison', 0, 0, 0, 0])
bulbasaur.set_attacks([razor_leaf, tackle, petal_blizzard, vine_whip, seed_bomb, take_down, double_edge], [growl, growth, poison_powder, sweet_scent])
bulbasaur.can_mega('M Venusaur', [80, 100, 123, 122, 120, 80], 'grass', 'poison')
charmander = Stage2('Charmander', 'Charmeleon', 'Charizard', [39, 52, 43, 60, 50, 65], [58, 64, 58, 80, 65, 80], [78, 84, 78, 109, 85, 100], ['fire', '', 0, 0, 0, 'flying'])
charmander.set_attacks([dragon_claw, ember, scratch, dragon_breath, fire_fang, slash, flamethrower, flame_burst, inferno, wing_attack, heat_wave, flare_blitz, air_slash],[growl, scary_face, smokescreen])
charmander.can_mega('M Charizard', [78, 130, 111, 130, 85, 100], 'fire', 'dragon')
squirtle = Stage2('Squirtle', 'Wartortle', 'Blastoise', [44, 48, 65, 50, 64, 43], [59, 63, 80, 65, 80, 58], [79, 83, 100, 85, 105, 78], ['water', '', 0, 0, 0, 0])
squirtle.set_attacks([flash_cannon, tackle, water_gun, rapid_spin, bite, water_pulse, aqua_tail, hydro_pump], [tail_whip, withdraw, iron_defense])
squirtle.can_mega('M Blastoise', [79, 103, 120, 135, 115, 78], 'water', '')
caterpie = Stage2('Caterpie', 'Metapod', 'Butterfree', [45, 30, 35, 20, 20, 45], [50, 20, 55, 25, 25, 30], [60, 45, 50, 90, 80, 70], ['bug', '', 0, 0, 0, 'flying'])
caterpie.set_attacks([bug_buzz, bug_bite, tackle, gust, confusion, psybeam, silver_wind, air_slash], [harden, poison_powder, stun_spore, supersonic, quilver_dance, string_shot])
weedle = Stage2('Weedle', 'Kakuna', 'Beedrill', [40, 35, 30, 20, 20, 50], [45, 25, 50, 25, 25, 35], [65, 90, 40, 45, 80, 75], ['bug', 'poison', 0, 0, 0, 0])
weedle.set_attacks([bug_bite, poison_sting, furry_cutter, venoshock, poison_jab, twineedle, fury_attack, pursuit, pin_missile], [harden, agility, string_shot])
weedle.can_mega('M Beedrill', [65, 150, 40, 15, 80, 145], 'bug', 'poison')
pidgey = Stage2('Pidgey', 'Pidgeotto', 'Pidgeot', [40, 45, 40, 35, 35, 56], [63, 60, 55, 50, 50, 71], [83, 80, 75, 70, 70, 101], ['normal', 'flying', 0, 0, 0, 0])
pidgey.set_attacks([gust, hurricane, quick_attack, tackle, twister, wing_attack, air_slash], [feather_dance, sand_attack, agility])
pidgey.can_mega('M Pidgeot', [83, 80, 80, 135, 80, 121], 'normal', 'flying')
rattata = Stage1('Rattata', 'Raticate', [30, 56, 35, 25, 35, 72], [55, 81, 60, 50, 70, 97], ['normal', '', 0, 0, 0, 0])
rattata.set_attacks([tackle, quick_attack, bite, pursuit, hyper_fang, crunch, double_edge], [tail_whip, swords_dance, scary_face])
a_rattata = Stage1('A.Rattata', 'A.Raticate', [30, 56, 35, 25, 35, 72], [75, 71, 70, 40, 80, 72], ['dark', 'normal', 0, 0, 0, 0])
a_rattata.set_attacks([tackle, quick_attack, bite, pursuit, hyper_fang, crunch, double_edge], [tail_whip, scary_face])
spearow = Stage1('Spearow', 'Fearow', [40, 60, 30, 31, 31, 70], [65, 90, 65, 61, 61, 100], ['normal', 'flying', 0, 0, 0, 0])
spearow.set_attacks([drill_run, peck, pursuit, aerial_ace, drill_peck, fury_attack], [growl, leer, agility])
ekans = Stage1('Ekans', 'Arbok', [35, 60, 44, 40, 54, 55], [60, 95, 69, 65, 79, 80], ['poison', '', 0, 0, 0, 0])
ekans.set_attacks([crunch, ice_fang, thunder_fang, fire_fang, poison_sting, bite, acid, mud_bomb, gunk_shot, acid_spray], [leer, screech, glare, coil])
pikachu = Stage1('Pikachu', 'Raichu', [35, 55, 40, 50, 50, 90], [60, 90, 55, 90, 80, 110], ['electric', '', 0, 0, 0, 0])
pikachu.set_attacks([thunder_shock, quick_attack, spark, discharge, slam, thunderbolt, thunder, nuzzle, wild_charge], [tail_whip, growl, thunder_wave, agility, double_team, play_nice])
sandshrew = Stage1('Sandshrew', 'Sandslash', [50, 75, 85, 20, 30, 40], [75, 100, 110, 45, 55, 65], ['ground', '', 0, 0, 0, 0])
sandshrew.set_attacks([scratch, poison_sting, rapid_spin, furry_cutter, swift, slash, earthquake, fury_swipes, crush_claw], [defense_curl, swords_dance, sand_attack])
a_sandshrew = Stage1('A.Sandshrew', 'A.Sandslash', [50, 75, 90, 10, 35, 40], [75, 100, 120, 25, 65, 65], ['ice', 'steel', 0, 0, 0, 0])
a_sandshrew.set_attacks([icicle_crash, slash, metal_claw, scratch, powder_snow, rapid_spin, furry_cutter, swift, iron_head, blizzard, fury_swipes, icicle_spear, ice_ball], [defense_curl, iron_defense, swords_dance])
nidoranf = Stage2('Nidoran F', 'Nidorina', 'Nidoqueen', [55, 47, 52, 40, 40, 41], [70, 62, 67, 55, 55, 56], [90, 92, 87, 75, 85, 76], ['poison', '', 0, 0, 0, 'ground'])
nidoranf.set_attacks([superpower, scratch, poison_sting, earth_power, body_slam, bite, crunch, poison_fang, double_kick, fury_swipes], [tail_whip, growl])
nidoranm = Stage2('Nidoran M', 'Nidorino', 'Nidoking', [46, 57, 40, 40, 40, 50], [61, 72, 57, 55, 55, 65], [81, 102, 77, 85, 75, 85], ['poison', '', 0, 0, 0, 'ground'])
nidoranm.set_attacks([megahorn, peck, poison_sting, earth_power, horn_attack, poison_jab, fury_attack, double_kick], [leer])
clefairy = Stage1('Clefairy', 'Clefable', [70, 45, 48, 60, 65, 35], [95, 70, 73, 95, 90, 60], ['fairy', '', 0, 0, 0, 0])
clefairy.set_attacks([disarming_voice, pound, wakeup_slap, moonblast, double_slap], [growl, defense_curl, cosmic_power, minimize])
vulpix = Stage1('Vulpix', 'Ninetales', [38, 41, 40, 50, 65, 65], [73, 76, 75, 81, 100, 100], ['fire', '', 0, 0, 0, 0])
vulpix.set_attacks([flamethrower, quick_attack, ember, payback, feint_attack, hex, flame_burst, fire_blast, inferno, extrasensory], [tail_whip, babydoll_eyes, confuse_ray, willowisp])
a_vulpix = Stage1('A.Vulpix', 'A.Ninetales', [38, 41, 40, 50, 65, 65], [73, 67, 75, 81, 100, 109], ['ice', '', 0, 'fairy', 0, 0])
a_vulpix.set_attacks([dazzling_gleam, ice_beam, ice_shard, powder_snow, icy_wind, payback, hex, feint_attack, blizzard, aurora_beam, extrasensory], [tail_whip, babydoll_eyes, confuse_ray, nasty_plot])
jigglypuff = Stage1('Jigglypuff', 'Wigglytuff', [115, 45, 20, 45, 25, 20], [140, 70, 45, 85, 50, 45], ['normal', 'fairy', 0, 0, 0, 0])
jigglypuff.set_attacks([disarming_voice, play_rough, pound, wakeup_slap, body_slam, hyper_voice, double_slap, double_edge], [defense_curl, play_nice])
zubat = Stage2('Zubat', 'Golbat', 'Crobat', [40, 45, 35, 30, 40, 55], [75, 80, 70, 65, 75, 90], [85, 90, 80, 70, 80, 130], ['poison', 'flying', 0, 0, 0, 0])
zubat.set_attacks([astonish, bite, wing_attack, swift, poison_fang, leech_life, venoshock, air_slash, absorb], [supersonic, confuse_ray, screech])
oddish = Stage2('Oddish', 'Gloom', 'Vileplume', [45, 50, 55, 75, 65, 30], [60, 65, 70, 85, 75, 40], [75, 80, 85, 110, 90, 50], ['grass', 'poison', 0, 0, 0, 0])
oddish.set_attacks([petal_blizzard, acid, moonblast, absorb, mega_drain, giga_drain], [growth, poison_powder, stun_spore, sweet_scent])
paras = Stage1('Paras', 'Parasect', [35, 70, 55, 45, 55, 25], [60, 95, 80, 60, 80, 30], ['bug', 'grass', 0, 0, 0, 0])
paras.set_attacks([scratch, furry_cutter, slash, giga_drain, xscissor, absorb, cross_poison], [stun_spore, poison_powder, growth])
venonat = Stage1('Venonat', 'Venomoth', [60, 55, 50, 40, 55, 45], [70, 65, 60, 90, 75, 90], ['bug', 'poison', 0, 0, 0, 0])
venonat.set_attacks([gust, bug_buzz, silver_wind, tackle, confusion, psybeam, signal_beam, leech_life, zen_headbutt, poison_fang, psychic], [supersonic, poison_powder, stun_spore, quilver_dance])
diglett = Stage1('Diglett', 'Dugtrio', [10, 55, 25, 35, 45, 95], [35, 100, 50, 50, 70, 120], ['ground', '', 0, 0, 0, 0])
diglett.set_attacks([night_slash, scratch, astonish, bulldoze, mud_bomb, earth_power, slash, earthquake, mud_slap], [growl, sand_attack])
a_diglett = Stage1('A.Diglett', 'A.Dugtrio', [10, 55, 30, 35, 45, 90], [35, 100, 60, 50, 70, 110], ['ground', 'steel', 0, 0, 0, 0])
a_diglett.set_attacks([night_slash, metal_claw, astonish, bulldoze, mud_bomb, earth_power, iron_head, earthquake, mud_slap], [growl, sand_attack])
meowth = Stage1('Meowth', 'Persian', [40, 45, 35, 40, 40, 90], [65, 70, 60, 65, 65, 115], ['normal', '', 0, 0, 0, 0])
meowth.set_attacks([swift, play_rough, scratch, bite, feint_attack, slash, night_slash, fury_swipes, power_gem], [growl, screech, nasty_plot])
a_meowth = Stage1('A.Meowth', 'A.Persian', [40, 35, 35, 50, 40, 90], [65, 60, 60, 75, 65, 115], ['dark', '', 0, 0, 0, 0])
a_meowth.set_attacks([swift, play_rough, scratch, bite, feint_attack, slash, night_slash, dark_pulse, fury_swipes, power_gem], [growl, screech, nasty_plot])
g_meowth = Stage1('G.Meowth', 'Perrserker', [50, 65, 55, 40, 40, 40], [70, 110, 100, 50, 60, 50], ['steel', '', 0, 0, 0, 0])
g_meowth.set_attacks([scratch, metal_claw, slash, iron_head, fury_swipes], [growl, swagger, metal_sound, screech, iron_defense])
psyduck = Stage1('Psyduck', 'Golduck', [50, 52, 48, 65, 50, 55], [80, 82, 78, 95, 80, 85], ['water', '', 0, 0, 0, 0])
psyduck.set_attacks([aqua_jet, scratch, water_gun, confusion, water_pulse, zen_headbutt, aqua_tail, hydro_pump, fury_swipes], [tail_whip, screech, amnesia])
mankey = Stage1('Mankey', 'Primeape', [40, 80, 35, 35, 45, 70], [65, 105, 60, 60, 70, 95], ['fighting', '', 0, 0, 0, 0])
mankey.set_attacks([scratch, karate_chop, pursuit, cross_chop, fury_swipes, close_combat], [leer, swagger, screech])
growlithe = Stage1('Growlithe', 'Arcanine', [55, 70, 45, 70, 50, 60], [90, 110, 80, 100, 80, 95], ['fire', '', 0, 0, 0, 0])
growlithe.set_attacks([fire_fang, crunch, thunder_fang, ember, bite, flamethrower, flame_wheel, take_down, flame_burst, heat_wave, flare_blitz], [leer, agility])
poliwag = Stage2('Poliwag', 'Poliwhirl', 'Poliwrath', [40, 50, 40, 40, 40, 90], [65, 65, 65, 50, 50, 90], [90, 95, 95, 70, 90, 70], ['water', '', 0, 0, 0, 'fighting'])
poliwag.set_attacks([dynamic_punch, Bubble_beam, body_slam, earth_power, hydro_pump, water_gun, pound, bubble, mud_bomb, wakeup_slap, double_slap, mud_shot, submission], [])
abra = Stage2('Abra', 'Kadabra', 'Alakazam', [25, 20, 15, 105, 55, 90], [40, 35, 30, 120, 70, 105], [55, 50, 45, 135, 95, 120], ['psychic', '', 0, 0, 0, 0])
abra.set_attacks([confusion, psybeam, psycho_cut, psychic], [calm_mind])
abra.can_mega('M Alakazam', [55, 50, 65, 175, 105, 150], 'psychic', '')
machop = Stage2('Machop', 'Machoke', 'Machamp', [70, 80, 50, 35, 35, 35], [80, 100, 70, 50, 60, 45], [90, 130, 80, 65, 85, 55], ['fighting', '', 0, 0, 0, 0])
machop.set_attacks([karate_chop, wakeup_slap, cross_chop, dynamic_punch, submission, strenght, knock_off, dual_chop], [leer, bulk_up, scary_face])
bellsprout = Stage2('Bellsprout', 'Weepinbell', 'Victreebel', [50, 75, 35, 70, 30, 40], [65, 90, 50, 85, 45, 55], [80, 105, 65, 100, 70, 70], ['grass', 'poison', 0, 0, 0, 0])
bellsprout.set_attacks([leaf_tornado, vine_whip, razor_leaf, leaf_blade, leaf_storm, acid, poison_jab, slam, knock_off], [growth, poison_powder, stun_spore, sweet_scent])
tentacool = Stage1('Tentacool', 'Tentacruel', [40, 40, 35, 50, 100, 70], [80, 70, 65, 80, 120, 100], ['water', 'poison', 0, 0, 0, 0])
tentacool.set_attacks([poison_sting, acid, water_pulse, Bubble_beam, poison_jab, brine, hex, sludge_wave, hydro_pump, acid_spray], [supersonic, screech])
geodude = Stage2('Geodude', 'Graveler', 'Golem', [40, 80, 100, 30, 30, 20], [55, 95, 115, 45, 45, 35], [80, 120, 130, 55, 65, 45], ['rock', 'ground', 0, 0, 0, 0])
geodude.set_attacks([tackle, rock_throw, bulldoze, earthquake, stone_edge, rock_blast, double_edge, steamroller], [defense_curl])
a_geodude = Stage2('A.Geodude', 'A.Graveler', 'A.Golem', [40, 80, 100, 30, 30, 20], [55, 95, 115, 45, 45, 35], [80, 120, 130, 55, 65, 45], ['rock', 'electric', 0, 0, 0, 0])
a_geodude.set_attacks([tackle, rock_throw, spark, thunder_punch, discharge, stone_edge, rock_blast, double_edge, steamroller], [defense_curl])
ponyta = Stage1('Ponyta', 'Rapidash', [50, 85, 55, 65, 65, 90], [65, 100, 70, 80, 80, 105], ['fire', '', 0, 0, 0, 0])
ponyta.set_attacks([poison_jab, megahorn, quick_attack, ember, fire_blast, flame_wheel, take_down, inferno, flare_blitz, fury_attack, stomp], [growl, tail_whip, agility])
g_ponyta = Stage1('G.Ponyta', 'G.Rapidash', [50, 85, 55, 65, 65, 90], [65, 100, 70, 80, 80, 105], ['psychic', '', 'psychic', 'fairy', 0, 0])
g_ponyta.set_attacks([psycho_cut, megahorn, quick_attack, tackle, confusion, fairy_wind, psybeam, dazzling_gleam, psychic, take_down, flame_charge], [growl, tail_whip])
slowpoke = Stage1('Slowpoke', 'Slowbro', [90, 65, 65, 40, 40, 15], [95, 75, 110, 100, 80, 30], ['water', 'psychic', 0, 0, 0, 0])
slowpoke.set_attacks([tackle, water_gun, confusion, headbutt, water_pulse, zen_headbutt, psychic], [growl, amnesia])
slowpoke.can_mega('M Slowbro', [95, 75, 180, 130, 80, 30], 'water', 'psychic')
g_slowpoke = Stage1('G.Slowpoke', 'G.Slowbro', [90, 65, 65, 40, 40, 15], [95, 100, 95, 100, 70, 30], ['psychic', '', 'poison', 'psychic', 0, 0])
g_slowpoke.set_attacks([tackle, acid, confusion, headbutt, water_pulse, zen_headbutt, psychic], [growl, amnesia])
magnemite = Stage2('Magnemite', 'Magneton', 'Magnezone', [25, 35, 70, 95, 55, 45], [50, 60, 95, 120, 70, 70], [70, 70, 115, 130, 90, 60], ['electric', 'steel', 0, 0, 0, 0])
magnemite.set_attacks([tackle, zap_cannon, thunder_shock, spark, flash_cannon, discharge, mirror_shot], [supersonic, thunder_wave, metal_sound, screech])
farfetchd = Basic('Farfetch´d', [52, 90, 55, 58, 62, 60], ['normal', 'flying', 0, 0, 0, 0])
farfetchd.set_attacks([poison_jab, peck, furry_cutter, aerial_ace, night_slash, air_slash, brave_bird, fury_attack, knock_off], [leer, swords_dance, sand_attack, agility])
g_farfetchd = Stage1('G.Farfetch´d', 'Sirfetch´d', [52, 95, 55, 58, 62, 55], [62, 135, 95, 68, 82, 65], ['fighting', '', 0, 0, 0, 0])
g_farfetchd.set_attacks([peck, furry_cutter, brick_break, slam, leaf_blade], [leer, swords_dance])
doduo = Stage1('Doduo', 'Dodrio', [35, 85, 45, 35, 35, 75], [60, 110, 70, 60, 60, 110], ['normal', 'flying', 0, 0, 0, 0])
doduo.set_attacks([peck, quick_attack, pursuit, drill_peck, fury_attack], [growl, swords_dance, agility])
seel = Stage1('Seel', 'Dewgong', [65, 45, 55, 45, 70, 45], [90, 70, 80, 70, 95, 70], ['water', '', 'water', 'ice', 0, 0])
seel.set_attacks([headbutt, signal_beam, icy_wind, ice_shard, aqua_jet, brine, aqua_tail, ice_beam, aurora_beam, take_down], [growl])
grimer = Stage1('Grimer', 'Muk', [80, 80, 50, 40, 50, 25], [105, 105, 75, 65, 100, 50], ['poison', '', 0, 0, 0, 0])
grimer.set_attacks([pound, sludge, mud_bomb, sludge_wave, gunk_shot, sludge_bomb, mud_slap], [poison_gas, screech, harden, minimize])
a_grimer = Stage1('A.Grimer', 'A.Muk', [80, 80, 50, 40, 50, 25], [105, 105, 75, 65, 100, 50], ['poison', 'dark', 0, 0, 0, 0])
a_grimer.set_attacks([pound, bite, poison_fang, crunch, acid_spray, gunk_shot, knock_off], [harden, poison_gas, screech, minimize])
shellder = Stage1('Shellder', 'Cloyster', [30, 65, 100, 45, 25, 40], [50, 95, 180, 85, 45, 70], ['water', '', 'water', 'ice', 0, 0])
shellder.set_attacks([hydro_pump, icicle_crash, water_gun, tackle, ice_shard, brine, ice_beam, icicle_spear, aurora_beam, spike_cannon, razor_shell], [withdraw, supersonic, leer, iron_defense])
gastly = Stage2('Gastly', 'Haunter', 'Gengar', [30, 35, 30, 100, 35, 80], [45, 50, 45, 115, 55, 95], [60, 65, 60, 130, 75, 110], ['ghost', 'poison', 0, 0, 0, 0])
gastly.set_attacks([shadow_punch, lick, payback, shadow_ball, hex, dark_pulse], [confuse_ray])
gastly.can_mega('M Gengar', [60, 65, 80, 170, 95, 130], 'ghost', 'poison')
onix = Stage1('Onix', 'Steelix', [35, 45, 160, 30, 45, 70], [75, 85, 200, 55, 65, 30], ['rock', 'ground', 'steel', 'ground', 0, 0])
onix.set_attacks([tackle, rock_throw, dragon_breath, slam, iron_tail, stone_edge, thunder_fang, ice_fang, fire_fang, double_edge, rock_slide, rock_tomb], [harden, screech])
onix.can_mega('M Steelix', [75, 125, 230, 55, 95, 30], 'steel', 'ground')
drowzee = Stage1('Drowzee', 'Hypno', [60, 48, 45, 43, 90, 42], [85, 73, 70, 73, 115, 67], ['psychic', '', 0, 0, 0, 0])
drowzee.set_attacks([pound, confusion, headbutt, psybeam, zen_headbutt, psychic], [poison_gas, swagger, nasty_plot, meditate])
krabby = Stage1('Krabby', 'Kingler', [30, 105, 90, 25, 25, 50], [55, 130, 115, 50, 50, 75], ['water', '', 0, 0, 0, 0])
krabby.set_attacks([bubble, Bubble_beam, metal_claw, slam, brine, mud_shot, vice_grip, stomp, crabhammer], [leer, harden])
voltorb = Stage1('Voltorb', 'Electrode', [40, 30, 50, 55, 55, 100], [60, 50, 70, 80, 80, 150], ['electric', '', 0, 0, 0, 0])
voltorb.set_attacks([tackle, spark, swift, discharge, charge_beam], [screech])
exeggcute = Stage1('Exeggcute', 'Exeggutor', [60, 40, 80, 60, 45, 40], [95, 95, 85, 125, 75, 55], ['grass', 'psychic', 0, 0, 0, 0])
exeggcute.set_attacks([seed_bomb, confusion, leaf_storm, wood_hammer, bullet_seed, stomp, extrasensory], [stun_spore, poison_powder])
cubone = Stage1('Cubone', 'Marowak', [50, 50, 95, 40, 50, 35], [60, 80, 110, 50, 80, 45], ['ground', '', 0, 0, 0, 0])
cubone.set_attacks([bone_club, headbutt, double_edge], [growl, tail_whip, leer])
a_cubone = Stage1('Cubone', 'A.Marowak', [50, 50, 95, 40, 50, 35], [60, 80, 110, 50, 80, 45], ['ground', '', 'fire', 'ghost', 0, 0])
a_cubone.set_attacks([bone_club, hex, flame_wheel, flare_blitz], [growl, tail_whip, leer, willowisp])
hitmonlee = Basic('Hitmonlee', [50, 120, 53, 35, 110, 87], ['fighting', '', 0, 0, 0, 0])
hitmonlee.set_attacks([brick_break, double_kick, double_kick, close_combat, mega_kick], [meditate])
hitmonchan = Basic('Hitmonchan', [50, 105, 79, 35, 110, 76], ['fighting', '', 0, 0, 0, 0])
hitmonchan.set_attacks([pursuit, thunder_punch, ice_punch, fire_punch, close_combat, mach_punch, bullet_punch, mega_punch], [agility])
lickitung = Stage1('Lickitung', 'Lickilicky', [90, 55, 75, 60, 75, 30], [110, 85, 95, 80, 95, 50], ['normal', '', 0, 0, 0, 0])
lickitung.set_attacks([lick, slam, stomp, knock_off, power_whip], [defense_curl, screech, supersonic])
koffing = Stage1('Koffing', 'Weezing', [40, 65, 95, 60, 45, 35], [65, 90, 120, 85, 70, 60], ['poison', '', 0, 0, 0, 0])
koffing.set_attacks([tackle, sludge, smog, sludge_bomb], [poison_gas, smokescreen])
rhyhorn = Stage2('Rhyhorn', 'Rhydon', 'Rhyperior', [80, 85, 90, 30, 30, 25], [105, 130, 120, 45, 45, 40], [115, 140, 130, 55, 55, 40], ['ground', 'rock', 0, 0, 0, 0])
rhyhorn.set_attacks([hammer_arm, poison_jab, horn_attack, bulldoze, drill_run, stone_edge, earthquake, megahorn, fury_attack, take_down, stomp], [tail_whip, scary_face])
chansey = Stage1('Chansey', 'Blissey', [250, 5, 5, 35, 105, 50], [255, 10, 10, 75, 135, 55], ['normal', '', 0, 0, 0, 0])
chansey.set_attacks([pound, egg_bomb, take_down, double_edge, double_slap], [growl, tail_whip, defense_curl, minimize])
tangela = Stage1('Tangela', 'Tangrowth', [65, 55, 115, 100, 40, 60], [100, 100, 125, 110, 50, 50], ['grass', '', 0, 0, 0, 0])
tangela.set_attacks([vine_whip, giga_drain, ancient_power, slam, absorb, mega_drain, knock_off, power_whip], [stun_spore, growth, poison_powder, tickle])
kangaskhan = Basic('Kangaskhan', [105, 95, 80, 40, 80, 90], ['normal', '', 0, 0, 0, 0])
kangaskhan.set_attacks([bite, crunch, dizzy_punch, mega_punch], [leer, tail_whip])
kangaskhan.can_mega('M Kangaskhan', [105, 125, 100, 60, 100, 100], 'normal', '')
horsea = Stage2('Horsea', 'Seadra', 'Kingdra', [30, 40, 70, 70, 25, 60], [55, 65, 95, 95, 45, 85], [75, 95, 95, 95, 95, 85], ['water', '', 0, 0, 'water', 'dragon'])
horsea.set_attacks([hydro_pump, bubble, water_gun, twister, Bubble_beam, brine, dragon_pulse], [leer, agility, dragon_dance, smokescreen])
goldeen = Stage1('Goldeen', 'Seaking', [45, 67, 60, 35, 50, 63], [80, 92, 65, 65, 80, 68], ['water', '', 0, 0, 0, 0])
goldeen.set_attacks([megahorn, poison_jab, peck, horn_attack, water_pulse, fury_attack, waterfall], [tail_whip, supersonic, agility])
staryu = Stage1('Staryu', 'Starmie', [30, 45, 55, 70, 55, 85], [60, 75, 85, 100, 85, 115], ['water', '', 'water', 'psychic', 0, 0])
staryu.set_attacks([hydro_pump, water_gun, rapid_spin, swift, tackle, Bubble_beam, brine, psychic, power_gem], [harden, confuse_ray, cosmic_power, minimize])
mr_mime = Basic('Mr. Mime', [40, 45, 65, 100, 120, 90], ['psychic', 'fairy', 0, 0, 0, 0])
mr_mime.set_attacks([magical_leaf, confusion, psybeam, psychic, double_slap], [meditate])
scyther = Stage1('Scyther', 'Scizor', [70, 110, 80, 55, 80, 105], [70, 130, 100, 55, 80, 65], ['bug', 'flying', 'bug', 'steel', 0, 0])
scyther.set_attacks([quick_attack, pursuit, metal_claw, furry_cutter, slash, xscissor, night_slash, iron_head, bullet_punch], [leer, swords_dance, iron_defense, agility, double_team])
scyther.can_mega('M Scizor', [70, 150, 140, 65, 100, 75], 'bug', 'steel')
jynx = Basic('Jynx', [65, 50, 35, 115, 95, 95], ['ice', 'psychic', 0, 0, 0, 0])
jynx.set_attacks([lick, powder_snow, ice_punch, wakeup_slap, avalanche, body_slam, blizzard, double_slap], [fake_tears])
electabuzz = Stage1('Electabuzz', 'Electivire', [65, 83, 57, 95, 85, 105], [75, 123, 67, 95, 85, 95], ['electric', '', 0, 0, 0, 0])
electabuzz.set_attacks([fire_punch, quick_attack, thunder_shock, swift, thunder_punch, discharge, thunderbolt, thunder], [leer, screech])
magmar = Stage1('Magmar', 'Magmortar', [65, 95, 57, 100, 85, 93], [75, 95, 67, 125, 95, 83], ['fire', '', 0, 0, 0, 0])
magmar.set_attacks([thunder_punch, ember, feint_attack, flame_burst, fire_punch, flamethrower, fire_blast, lava_plume], [leer, confuse_ray, smokescreen])
pinsir = Basic('Pinsir', [65, 125, 100, 55, 70, 85], ['bug', '', 0, 0, 0, 0])
pinsir.set_attacks([brick_break, xscissor, superpower, submission, vice_grip], [harden, swords_dance])
pinsir.can_mega('M Pinsir', [65, 155, 120, 65, 90, 105], 'bug', 'flying')
tauros = Basic('Tauros', [75, 100, 95, 40, 70, 110], ['normal', '', 0, 0, 0, 0])
tauros.set_attacks([tackle, horn_attack, pursuit, payback, zen_headbutt, take_down], [tail_whip, swagger, scary_face])
magikarp = Stage1('Magikarp', 'Gyarados', [20, 10, 55, 15, 20, 80], [95, 125, 79, 60, 100, 81], ['water', '', 'water', 'flying', 0, 0])
magikarp.set_attacks([bite, twister, tackle, ice_fang, aqua_tail, crunch, hydro_pump, hurricane], [leer, scary_face])
magikarp.can_mega('M Gyarados', [95, 155, 109, 70, 130, 81], 'water', 'dark')
lapras = Basic('Lapras', [130, 85, 80, 85, 95, 60], ['water', 'ice', 0, 0, 0, 0])
lapras.set_attacks([water_gun, ice_shard, water_pulse, body_slam, brine, ice_beam, hydro_pump], [growl, confuse_ray])
vaporeon = Stage1('Eevee', 'Vaporeon', [55, 55, 50, 45, 65, 55],[ 130, 65, 60, 110, 95, 65], ['normal', '', 'water', 0, 0, 0])
vaporeon.set_attacks([water_gun, tackle, quick_attack, water_pulse, hydro_pump, take_down, double_edge, aurora_beam, muddy_water], [growl, tail_whip, babydoll_eyes, charm, sand_attack])
jolteon = Stage1('Eevee', 'Jolteon', [55, 55, 50, 45, 65, 55], [65, 65, 65, 110, 95, 130], ['normal', '', 'electric', 0, 0, 0])
jolteon.set_attacks([thunder_shock, tackle, quick_attack, thunder_fang, discharge, thunder, take_down, double_edge, pin_missile, double_kick], [babydoll_eyes, growl, tail_whip, thunder_wave, charm, sand_attack, agility])
flareon = Stage1('Eevee', 'Flareon', [55, 55, 50, 45, 65, 55], [65, 130, 60, 95, 110, 65], ['normal', '', 'fire', 0, 0, 0])
flareon.set_attacks([ember, tackle, quick_attack, bite, fire_fang, flare_blitz, lava_plume], [growl, tail_whip, babydoll_eyes, charm, sand_attack, scary_face])
porygon = Stage2('Porygon', 'Porygon2', 'Porygon-Z', [65, 60, 70, 85, 75, 40], [85, 80, 90, 105, 95, 60], [85, 80, 70, 135, 75, 90], ['normal', '', 0, 0, 0, 0])
porygon.set_attacks([zap_cannon, tackle, psybeam, signal_beam, discharge], [agility])
omanyte = Stage1('Omanyte', 'Omastar', [35, 40, 100, 90, 55, 35], [70, 60, 125, 115, 70, 55], ['rock', 'water', 0, 0, 0, 0])
omanyte.set_attacks([water_gun, brine, bite, tackle, hydro_pump, ancient_power, mud_shot, rock_blast, spike_cannon], [withdraw, leer, tickle])
kabuto = Stage1('Kabuto', 'Kabutops', [30, 80, 90, 55, 45, 55], [60, 115, 105, 65, 70, 80], ['rock', 'water', 0, 0, 0, 0])
kabuto.set_attacks([slash, night_slash, scratch, mud_shot, aqua_jet, ancient_power, mud_shot, absorb, mega_drain], [harden, leer, metal_sound, sand_attack])
aerodactyl = Basic('Aerodactyl', [80, 105, 65, 60, 75, 130], ['rock', 'flying', 0, 0, 0, 0])
aerodactyl.set_attacks([iron_head, ice_fang, fire_fang, thunder_fang, wing_attack, bite, ancient_power, crunch, take_down, rock_slide], [supersonic, agility, scary_face])
aerodactyl.can_mega('M Aerodactyl', [80, 135, 85, 70, 95, 150], 'rock', 'flying')
snorlax = Basic('Snorlax', [160, 110, 65, 65, 110, 30], ['normal', '', 0, 0, 0, 0])
snorlax.set_attacks([tackle, lick, body_slam, crunch], [amnesia])
dratini = Stage2('Dratini', 'Dragonair', 'Dragonite', [41, 64, 45, 50, 50, 50], [61, 84, 65, 70, 70, 70], [91, 134, 95, 100, 100, 80], ['dragon', '', 0, 0, 0, 'flying'])
dratini.set_attacks([wing_attack, hurricane, fire_punch, thunder_punch, twister, slam, aqua_tail, dragon_rush], [leer, thunder_wave, agility, dragon_dance])
chikorita = Stage2('Chikorita', 'Bayleef', 'Meganium', [45, 49, 65, 49, 65, 45], [60, 62, 80, 63, 80, 60], [80, 82, 100, 83, 100, 80], ['grass', '', 0, 0, 0, 0])
chikorita.set_attacks([tackle, razor_leaf, magical_leaf, body_slam, petal_blizzard], [growl, poison_powder, sweet_scent])
cyndaquil = Stage2('Cyndaquil', 'Quilava', 'Typhlosion', [39, 52, 43, 60, 50, 65], [58, 64, 58, 80, 65, 80], [78, 84, 78, 109, 85, 100], ['fire', '', 0, 0, 0, 0])
cyndaquil.set_attacks([tackle, ember, quick_attack, flame_wheel, swift, flamethrower, inferno, double_edge, flame_charge, lava_plume], [leer, defense_curl, smokescreen])
totodile = Stage2('Totodile', 'Croconaw', 'Feraligatr', [50, 65, 64, 44, 48, 43], [65, 80, 80, 59, 63, 58], [85, 105, 100, 79, 83, 78], ['water', '', 0, 0, 0, 0])
totodile.set_attacks([scratch, water_gun, bite, ice_fang, crunch, slash, aqua_tail, superpower, hydro_pump], [leer, screech, agility, scary_face])
sentret = Stage1('Sentret', 'Furret', [35, 46, 34, 35, 45, 20], [85, 76, 64, 45, 55, 90], ['normal', '', 0, 0, 0, 0])
sentret.set_attacks([scratch, quick_attack, slam, hyper_voice, fury_swipes], [defense_curl, amnesia, agility, coil])
hoothoot = Stage1('Hoothoot', 'Noctowl', [60, 30, 30, 36, 56, 50], [100, 50, 50, 86, 96, 70], ['normal', 'flying', 0, 0, 0, 0])
hoothoot.set_attacks([tackle, peck, confusion, air_slash, zen_headbutt, take_down, extrasensory], [growl])
ledyba = Stage1('Ledyba', 'Ledian', [40, 20, 30, 40, 80, 55], [55, 35, 50, 55, 110, 85], ['bug', 'flying', 0, 0, 0, 0])
ledyba.set_attacks([tackle, silver_wind, swift, bug_buzz, double_edge, mach_punch], [supersonic, agility])
spinarak = Stage1('Spinarak', 'Ariados', [40, 60, 40, 40, 40, 30], [70, 90, 70, 60, 70, 40], ['bug', 'poison', 0, 0, 0, 0])
spinarak.set_attacks([poison_sting, bug_bite, leech_life, shadow_sneak, psychic, poison_jab, absorb, fury_swipes, pin_missile, cross_poison], [swords_dance, agility, scary_face, string_shot])
chinchou = Stage1('Chinchou', 'Lanturn', [75, 38, 38, 56, 56, 67], [125, 58, 58, 76, 76, 67], ['water', 'electric', 0, 0, 0, 0])
chinchou.set_attacks([bubble, water_gun, Bubble_beam, spark, signal_beam, discharge, hydro_pump, take_down], [supersonic, thunder_wave, confuse_ray])
togepi = Stage2('Togepi', 'Togetic', 'Togekiss', [35, 20, 65, 40, 65, 20], [55, 40, 85, 80, 105, 40], [85, 50, 95, 120, 115, 80], ['fairy', '', 0, 'flying', 'fairy', 'flying'])
togepi.set_attacks([air_slash, magical_leaf, fairy_wind, ancient_power, double_edge], [growl, charm])
natu = Stage1('Natu', 'Xatu', [40, 50, 45, 70, 45, 70], [65, 75, 70, 95, 70, 95], ['psychic', 'flying', 0, 0, 0, 0])
natu.set_attacks([peck, air_slash, psychic, ominous_wind], [leer, confuse_ray])
mareep = Stage2('Mareep', 'Flaaffy', 'Ampharos', [55, 40, 40, 65, 45, 35], [70, 55, 55, 80, 60, 45], [90, 75, 85, 115, 90, 55], ['electric', '', 0, 0, 0, 0])
mareep.set_attacks([fire_punch, tackle, zap_cannon, thunder_shock, thunder_punch, discharge, signal_beam, thunder, dragon_pulse, take_down, power_gem], [growl, confuse_ray, thunder_wave, cotton_guard])
mareep.can_mega('M Ampharos', [90, 95, 105, 165, 110, 45], 'electric', 'dragon')
marill = Stage1('Marill', 'Azumarill', [70, 20, 50, 20, 50, 40], [100, 50, 80, 60, 80, 50], ['water', 'fairy', 0, 0, 0, 0])
marill.set_attacks([tackle, water_gun, Bubble_beam, slam, aqua_tail, play_rough, hydro_pump, superpower, double_edge], [tail_whip, defense_curl])
sudowoodo = Basic('Sudowoodo', [70, 100, 115, 30, 65, 30], ['rock', '', 0, 0, 0, 0])
sudowoodo.set_attacks([stone_edge, hammer_arm, rock_throw, slam, wood_hammer, double_edge, head_smash, rock_slide, rock_tomb], [])
hoppip = Stage2('Hoppip', 'Skiploom', 'Jumpluff', [35, 35, 40, 35, 55, 50], [55, 45, 50, 45, 65, 80], [75, 55, 70, 55, 95, 110], ['grass', 'flying', 0, 0, 0, 0])
hoppip.set_attacks([tackle, fairy_wind, giga_drain, bullet_seed, mega_drain], [tail_whip, poison_powder, stun_spore])
aipom = Stage1('Aipom', 'Ambipom', [55, 70, 55, 40, 55, 85], [75, 100, 66, 60, 66, 115], ['normal', '', 0, 0, 0, 0])
aipom.set_attacks([scratch, astonish, swift, fury_swipes, dual_chop], [tail_whip, screech, nasty_plot, tickle, sand_attack, agility])
sunkern = Stage1('Sunkern', 'Sunflora', [30, 30, 30, 30, 30, 30], [75, 75, 55, 105, 85, 30], ['grass', '', 0, 0, 0, 0])
sunkern.set_attacks([tackle, pound, razor_leaf, giga_drain, leaf_storm, petal_blizzard, absorb, mega_drain, double_edge], [growth])
yanma = Stage1('Yanma', 'Yanmega', [65, 65, 45, 75, 45, 95], [86, 76, 86, 116, 56, 95], ['bug', 'flying', 0, 0, 0, 0])
yanma.set_attacks([bug_buzz, air_slash, night_slash, bug_bite, wing_attack, tackle, gust, quick_attack, aerial_ace, ancient_power, slash], [supersonic, screech, double_team])
wooper = Stage1('Wooper', 'Quagsire', [55, 45, 45, 25, 25, 15], [95, 85, 85, 65, 65, 35], ['water', 'ground', 0, 0, 0, 0])
wooper.set_attacks([water_gun, mud_shot, slam, aqua_tail, earthquake, mud_shot, muddy_water], [tail_whip, amnesia])
espeon = Stage1('Eevee', 'Espeon', [55, 55, 50, 45, 65, 55], [65, 65, 60, 130, 95, 110], ['normal', '', 'psychic', 0, 0, 0])
espeon.set_attacks([bite, tackle, confusion, quick_attack, swift, psybeam, psychic], [tail_whip, growl, babydoll_eyes, charm, sand_attack])
umbreon = Stage1('Eevee', 'Umbreon', [55, 55, 50, 45, 65, 55], [95, 65, 110, 60, 130, 65], ['normal', '', 'dark', 0, 0, 0])
umbreon.set_attacks([swift, bite, quick_attack, tackle, dark_pulse], [tail_whip, babydoll_eyes, growl, screech, confuse_ray, charm, sand_attack])
murkrow = Stage1('Murkrow', 'Honchkrow', [60, 85, 42, 85, 42, 91], [100, 125, 52, 105, 52, 71], ['dark', 'flying', 0, 0, 0, 0])
murkrow.set_attacks([night_slash, astonish, wing_attack, dark_pulse], [swagger])
misdreavus = Stage1('Misdreavus', 'Mismagius', [60, 60, 60, 85, 85, 85], [60, 60, 60, 105, 105, 105], ['ghost', '', 0, 0, 0, 0])
misdreavus.set_attacks([magical_leaf, astonish, hex, psybeam, payback, shadow_ball, power_gem], [growl, confuse_ray])
girafarig = Basic('Girafarig', [70, 80, 65, 90, 65, 85], ['normal', 'psychic', 0, 0, 0, 0])
girafarig.set_attacks([astonish, tackle, confusion, psybeam, crunch, psychic, stomp], [growl, nasty_plot, agility])
pineco = Stage1('Pineco', 'Forretress', [50, 65, 90, 35, 35, 15], [75, 90, 140, 60, 60, 40], ['bug', '', 0, 'steel', 0, 0])
pineco.set_attacks([zap_cannon, tackle, bug_bite, rapid_spin, payback, take_down, double_edge, mirror_shot], [iron_defense])
dunsparce = Basic('Dunsparce', [100, 70, 70, 65, 65, 45], ['normal', '', 0, 0, 0, 0])
dunsparce.set_attacks([ancient_power, drill_run, take_down, double_edge, dragon_rush], [defense_curl, screech, glare, coil])
gligar = Stage1('Gligar', 'Gliscor', [65, 75, 105, 35, 65, 85], [75, 95, 125, 45, 75, 95], ['ground', 'flying', 0, 0, 0, 0])
gligar.set_attacks([thunder_fang, ice_fang, fire_fang, poison_jab, night_slash, slash, poison_sting, quick_attack, furry_cutter, xscissor, earthquake, knock_off], [harden, screech, swords_dance, sand_attack])
snubbull = Stage1('Snubbull', 'Granbull', [60, 80, 50, 40, 40, 30], [90, 120, 75, 60, 60, 45], ['fairy', '', 0, 0, 0, 0])
snubbull.set_attacks([ice_fang, thunder_fang, fire_fang, tackle, bite, lick, headbutt, play_rough, payback, crunch], [tail_whip, charm, scary_face])
qwilfish = Basic('Qwilfish', [65, 95, 85, 55, 55, 85], ['water', 'poison', 0, 0, 0, 0])
qwilfish.set_attacks([poison_sting, water_gun, brine, poison_jab, aqua_tail, pin_missile, take_down], [harden, minimize])
shuckle = Basic('Shuckle', [20, 10, 230, 10, 230, 5], ['bug', 'rock', 0, 0, 0, 0])
shuckle.set_attacks([rock_throw, bug_bite, stone_edge, rock_slide], [withdraw])
heracross = Basic('Heracross', [80, 125, 75, 40, 95, 85], ['bug', 'fighting', 0, 0, 0, 0])
heracross.set_attacks([tackle, aerial_ace, horn_attack, brick_break, megahorn, bullet_seed, fury_attack, pin_missile, close_combat, arm_thrust], [leer])
heracross.can_mega('M Heracross', [80, 185, 115, 40, 105, 75], 'bug', 'fighting')
sneasel = Stage1('Sneasel', 'Weavile', [55, 95, 55, 35, 75, 115], [70, 120, 65, 45, 85, 125], ['dark', 'ice', 0, 0, 0, 0])
sneasel.set_attacks([quick_attack, scratch, slash, ice_shard, icy_wind, metal_claw, night_slash, dark_pulse, fury_swipes], [leer, screech, agility, hone_claws])
teddiursa = Stage1('Teddiursa', 'Ursaring', [60, 80, 50, 50, 50, 40], [90, 130, 75, 75, 75, 55], ['normal', '', 0, 0, 0, 0])
teddiursa.set_attacks([scratch, lick, payback, slash, play_rough, hammer_arm, fury_swipes], [babydoll_eyes, charm, fake_tears, play_nice, scary_face, sweet_scent])
slugma = Stage1('Slugma', 'Magcargo', [40, 40, 40, 70, 40, 20], [60, 50, 120, 90, 80, 30], ['fire', '', 0, 'rock', 0, 0])
slugma.set_attacks([earth_power, ember, rock_throw, ancient_power, flamethrower, smog, lava_plume, rock_slide], [harden, amnesia])
swinub = Stage2('Swinub', 'Piloswine', 'Mamoswine', [50, 50, 40, 30, 30, 50],[ 100, 100, 80, 60, 60, 50], [110, 130, 80, 70, 60, 80], ['ice', 'ground', 0, 0, 0, 0])
swinub.set_attacks([ice_fang, ancient_power, tackle, powder_snow, ice_shard, icy_wind, earthquake, blizzard, take_down, fury_attack, mud_slap], [amnesia, scary_face])
corsola = Basic('Corsola', [65, 55, 95, 65, 95, 35], ['water', 'rock', 0, 0, 0, 0])
corsola.set_attacks([tackle, water_gun, ancient_power, Bubble_beam, earth_power, power_gem, spike_cannon], [harden, iron_defense])
remoraid = Stage1('Remoraid', 'Octillery', [35, 65, 35, 65, 35, 65], [75, 105, 75, 105, 75, 45], ['water', '', 0, 0, 0, 0])
remoraid.set_attacks([water_gun, water_pulse, psybeam, Bubble_beam, ice_beam, hydro_pump, aurora_beam, bullet_seed, gunk_shot], [])
mantine = Basic('Mantine', [85, 40, 70, 80, 140, 70], ['water', 'flying', 0, 0, 0, 0])
mantine.set_attacks([tackle, psybeam, water_gun, wing_attack, water_pulse, Bubble_beam, headbutt, air_slash, hydro_pump, take_down, bullet_seed], [supersonic, confuse_ray, agility])
skarmory = Basic('Skarmory', [65, 80, 140, 40, 70, 70], ['steel', 'flying', 0, 0, 0, 0])
skarmory.set_attacks([peck, metal_claw, wing_attack, drill_peck, fury_attack, steel_wing], [leer, metal_sound, sand_attack, agility])
houndour = Stage1('Houndour', 'Houndoom', [45, 60, 30, 80, 50, 65], [75, 90, 50, 110, 80, 95], ['dark', 'fire', 0, 0, 0, 0])
houndour.set_attacks([thunder_fang, ember, bite, fire_fang, flamethrower, crunch, smog, inferno], [leer, nasty_plot, howl])
houndour.can_mega('M Houndoom', [75, 90, 90, 140, 90, 115], 'dark', 'fire')
phanpy = Stage1('Phanpy', 'Donphan', [90, 60, 60, 40, 40, 40], [90, 120, 120, 60, 60, 50], ['ground', '', 0, 0, 0, 0])
phanpy.set_attacks([thunder_fang, fire_fang, horn_attack, bulldoze, rapid_spin, slam, earthquake, take_down, double_edge, knock_off], [growl, defense_curl, charm, scary_face])
stantler = Basic('Stantler', [73, 95, 62, 85, 65, 85], ['normal', '', 0, 0, 0, 0])
stantler.set_attacks([tackle, astonish, zen_headbutt, take_down, stomp], [leer, confuse_ray, calm_mind, sand_attack])
miltank = Basic('Miltank', [95, 80, 105, 40, 70, 100], ['normal', '', 0, 0, 0, 0])
miltank.set_attacks([tackle, headbutt, zen_headbutt, body_slam, play_rough, stomp], [growl, defense_curl])
larvitar = Stage2('Larvitar', 'Pupitar', 'Tyranitar', [50, 64, 50, 45, 50, 41], [70, 84, 70, 65, 70, 51], [100, 134, 110, 95, 100, 61], ['rock', 'ground', 0, 0, 0, 'dark'])
larvitar.set_attacks([ice_fang, dark_pulse, thunder_fang, fire_fang, tackle, payback, bite, crunch, earthquake, stone_edge, rock_slide], [leer, screech, scary_face])
larvitar.can_mega('M Tyranitar', [100, 164, 150, 95, 120, 71], 'rock', 'dark')
treecko = Stage2('Treecko', 'Grovyle', 'Sceptile', [40, 45, 35, 65, 55, 70], [50, 65, 45, 85, 65, 95], [70, 85, 65, 105, 85, 120], ['grass', '', 0, 0, 0, 0])
treecko.set_attacks([pound, night_slash, quick_attack, furry_cutter, pursuit, leaf_blade, slam, xscissor, leaf_storm, absorb, mega_drain, dual_chop, energy_ball], [leer, screech, agility])
treecko.can_mega('M Sceptile', [70, 110, 75, 145, 85, 145], 'grass', 'dragon')
torchic = Stage2('Torchic', 'Combusken', 'Blaziken', [45, 60, 40, 70, 50, 45], [60, 85, 60, 85, 60, 55], [80, 120, 70, 110, 70, 80], ['fire', '', 0, 'fighting', 0, 'fighting'])
torchic.set_attacks([fire_punch, scratch, ember, peck, quick_attack, slash, double_kick, flare_blitz, flame_charge], [growl, bulk_up, sand_attack])
torchic.can_mega('M Blaziken', [80, 160, 80, 130, 80, 100], 'fire', 'fighting')
mudkip = Stage2('Mudkip', 'Marshtomp', 'Swampert', [50, 70, 50, 50, 50, 40], [70, 85, 70, 60, 70, 50], [100, 110, 90, 85, 90, 60], ['water', '', 0, 'ground', 0, 'ground'])
mudkip.set_attacks([tackle, water_gun, mud_shot, mud_bomb, earthquake, hammer_arm, take_down, mud_slap, muddy_water, rock_slide], [growl])
mudkip.can_mega('M Sceptile', [100, 150, 110, 95, 110, 70], 'water', 'ground')
poochyena = Stage1('Poochyena', 'Mightyena', [35, 55, 35, 30, 30, 35], [70, 90, 70, 60, 60, 70], ['dark', '', 0, 0, 0, 0])
poochyena.set_attacks([tackle, bite, crunch, take_down, fire_fang, thunder_fang, ice_fang], [swagger, sand_attack, howl, scary_face])
zigzagoon = Stage1('Zigzagoon', 'Linoone', [38, 30, 41, 30, 41, 60], [78, 70, 61, 50, 61, 100], ['normal', '', 0, 0, 0, 0])
zigzagoon.set_attacks([tackle, play_rough, headbutt, slash, pin_missile, take_down, fury_swipes, double_edge], [growl, tail_whip, babydoll_eyes, sand_attack])
g_zigzagoon = Stage2('G.Zigzagoon', 'G.Linoone', 'Obstagoon', [38, 30, 41, 30, 41, 60], [78, 70, 61, 50, 61, 100], [93, 90, 101, 60, 81, 95], ['dark', 'normal', 0, 0, 0, 0])
g_zigzagoon.set_attacks([night_slash, cross_chop, tackle, lick, headbutt, pin_missile, take_down, double_edge], [leer, babydoll_eyes])
beautifly = Stage2('Wurmple', 'Silcoon', 'Beautifly', [45, 45, 35, 20, 30, 20], [50, 35, 55, 25, 25, 15], [60, 70, 50, 100, 50, 65], ['bug', '', 0, 0, 0, 'flying'])
beautifly.set_attacks([gust, silver_wind, giga_drain, bug_buzz, absorb, mega_drain], [harden, stun_spore, quilver_dance, string_shot])
dustox = Stage2('Wurmple', 'Cascoon', 'Dustox', [45, 45, 35, 20, 30, 20], [50, 35, 55, 25, 25, 15], [60, 50, 70, 50, 90, 65], ['bug', '', 0, 0, 0, 'poison'])
dustox.set_attacks([gust, silver_wind, confusion, venoshock, psybeam, bug_buzz], [harden, poison_powder, quilver_dance, string_shot])
lotad = Stage2('Lotad', 'Lombre', 'Ludicolo', [40, 30, 30, 40, 50, 30], [60, 50, 50, 60, 70, 50], [80, 70, 70, 90, 100, 70], ['water', 'grass', 0, 0, 0, 0])
lotad.set_attacks([astonish, bubble, Bubble_beam, zen_headbutt, hydro_pump, giga_drain, absorb, mega_drain, fury_swipes, knock_off, energy_ball], [growl])
seedot = Stage2('Seedot', 'Nuzleaf', 'Shiftry', [40, 40, 50, 30, 30, 30], [70, 70, 40, 60, 40, 60], [90, 100, 60, 90, 60, 80], ['grass', '', 0, 'dark', 0, 'dark'])
seedot.set_attacks([razor_leaf, feint_attack, leaf_tornado, hurricane, leaf_storm, pound, extrasensory], [harden, growth, swagger])
taillow = Stage1('Taillow', 'Swellow', [40, 55, 30, 30, 30, 85], [60, 85, 60, 75, 50, 125], ['normal', 'flying', 0, 0, 0, 0])
taillow.set_attacks([air_slash, peck, quick_attack, wing_attack, aerial_ace, brave_bird], [growl, agility, double_team])
wingull = Stage1('Wingull', 'Pelipper', [40, 30, 30, 55, 30, 85], [60, 50, 100, 95, 70, 65], ['water', 'flying', 0, 0, 0, 0])
wingull.set_attacks([hurricane, hydro_pump, water_gun, wing_attack, water_pulse, payback, brine], [growl, supersonic, agility])
ralts = Stage2('Ralts', 'Kirlia', 'Gardevoir', [28, 25, 25, 45, 35, 40], [38, 35, 35, 65, 55, 50], [68, 65, 65, 125, 115, 80], ['psychic', 'fairy', 0, 0, 0, 0])
ralts.set_attacks([moonblast, confusion, disarming_voice, magical_leaf, psychic], [growl, calm_mind, charm, double_team])
ralts.can_mega('M Gardevoir', [68, 85, 65, 165, 135, 100], 'psychic', 'fairy')
surskit = Stage1('Surskit', 'Masquerain', [40, 30, 32, 50, 52, 65], [70, 60, 62, 100, 82, 80], ['bug', 'water', 0, 'flying', 0, 0])
surskit.set_attacks([bug_buzz, bubble, quick_attack, gust, air_slash, silver_wind, ominous_wind], [quilver_dance, stun_spore, agility, scary_face, sweet_scent])
shroomish = Stage1('Shroomish', 'Breloom', [60, 40, 60, 40, 60, 35], [60, 130, 80, 60, 60, 70], ['grass', '', 0, 'fighting', 0, 0])
shroomish.set_attacks([tackle, headbutt, seed_bomb, dynamic_punch, absorb, mega_drain, mach_punch, force_palm], [stun_spore, poison_powder, growth])
slakoth = Stage2('Slakoth', 'Vigoroth', 'Slaking', [60, 60, 60, 35, 35, 30], [80, 80, 80, 55, 55, 90], [150, 160, 100, 95, 65, 100], ['normal', '', 0, 0, 0, 0])
slakoth.set_attacks([hammer_arm, scratch, feint_attack, fury_swipes], [amnesia, swagger])
nincada = Stage1('Nincada', 'Ninjask', [31, 45, 90, 30, 30, 40], [61, 90, 45, 50, 50, 160], ['bug', 'ground', 0, 'flying', 0, 0])
nincada.set_attacks([furry_cutter, bug_bite, scratch, slash, xscissor, metal_claw, absorb, fury_swipes, mud_slap], [harden, screech, swords_dance, sand_attack, agility, double_team])
whismur = Stage2('Whismur', 'Loudred', 'Exploud', [64, 51, 23, 51, 23, 28], [84, 71, 43, 71, 43, 48], [104, 91, 63, 91, 73, 68], ['normal', '', 0, 0, 0, 0])
whismur.set_attacks([crunch, bite, ice_fang, fire_fang, thunder_fang, pound, astonish, hyper_voice, stomp], [screech, supersonic, howl])
makuhita = Stage1('Makuhita', 'Hariyama', [72, 60, 30, 20, 30, 25], [144, 120, 60, 40, 60, 50], ['fighting', '', 0, 0, 0, 0])
makuhita.set_attacks([brine, tackle, wakeup_slap, close_combat, knock_off, arm_thrust, force_palm], [sand_attack])
nosepass = Stage1('Nosepass', 'Probopass', [30, 45, 135, 45, 90, 30], [60, 55, 145, 75, 150, 40], ['rock', '', 0, 'steel', 0, 0])
nosepass.set_attacks([tackle, spark, discharge, earth_power, stone_edge, zap_cannon, power_gem, rock_slide], [harden, thunder_wave])
skitty = Stage1('Skitty', 'Delcatty', [50, 45, 45, 35, 35, 50], [70, 65, 65, 55, 55, 90], ['normal', '', 0, 0, 0, 0])
skitty.set_attacks([disarming_voice, tackle, feint_attack, wakeup_slap, play_rough, double_slap, double_edge], [growl, tail_whip, charm])
sableye = Basic('Sableye', [50, 75, 75, 65, 65, 50], ['dark', 'ghost', 0, 0, 0, 0])
sableye.set_attacks([scratch, astonish, shadow_sneak, feint_attack, zen_headbutt, shadow_ball, power_gem, fury_swipes, knock_off], [leer, confuse_ray])
sableye.can_mega('M Sableye', [50, 85, 125, 85, 115, 20], 'dark', 'ghost')
mawile = Basic('Mawile', [50, 85, 85, 55, 55, 50], ['steel', 'fairy', 0, 0, 0, 0])
mawile.set_attacks([play_rough, iron_head, fairy_wind, astonish, bite, feint_attack, crunch, vice_grip], [growl, iron_defense, fake_tears, sweet_scent])
mawile.can_mega('M Mawile', [50, 105, 125, 55, 95, 50], 'steel', 'fairy')
aron = Stage2('Aron', 'Lairon', 'Aggron', [50, 70, 100, 40, 40, 30], [60, 90, 140, 50, 50, 40], [70, 110, 180, 60, 60, 50], ['steel', 'rock', 0, 0, 0, 0])
aron.set_attacks([tackle, headbutt, metal_claw, iron_head, iron_tail, double_edge, mud_slap, rock_slide, rock_tomb], [harden, metal_sound, iron_defense])
aron.can_mega('M Aggron', [70, 140, 230, 60, 80, 50], 'steel', '')
meditite = Stage1('Meditite', 'Medicham', [30, 40, 55, 40, 55, 60], [60, 60, 75, 60, 75, 80], ['fighting', 'psychic', 0, 0, 0, 0])
meditite.set_attacks([zen_headbutt, fire_punch, thunder_punch, ice_punch, confusion, force_palm], [calm_mind, meditate])
meditite.can_mega('M Medicham', [60, 100, 85, 80, 85, 100], 'fighting', 'psychic')
electrike = Stage1('Electrike', 'Manectric', [40, 45, 40, 65, 40, 65], [70, 75, 60, 105, 60, 105], ['electric', '', 0, 0, 0, 0])
electrike.set_attacks([fire_fang, tackle, quick_attack, spark, thunder_fang, bite, discharge, thunder, wild_charge], [thunder_wave, leer, howl])
electrike.can_mega('M Manectric', [70, 75, 80, 135, 80, 135], 'electric', '')
plusle = Basic('Plusle', [60, 50, 40, 85, 75, 95], ['electric', '', 0, 0, 0, 0])
plusle.set_attacks([quick_attack, spark, swift, discharge, thunder, nuzzle], [growl, thunder_wave, nasty_plot, charm, agility, play_nice])
minun = Basic('Minun', [60, 40, 50, 75, 85, 95], ['electric', '', 0, 0, 0, 0])
minun.set_attacks([quick_attack, spark, swift, discharge, thunder, nuzzle], [growl, thunder_wave, nasty_plot, fake_tears, agility, play_nice])
volbeat = Basic('Volbeat', [65, 73, 75, 47, 85, 85], ['bug', '', 0, 0, 0, 0])
volbeat.set_attacks([tackle, quick_attack, signal_beam, zen_headbutt, bug_buzz, play_rough, double_edge], [confuse_ray, double_team])
illumise = Basic('Illumise', [65, 47, 75, 73, 85, 85], ['bug', '', 0, 0, 0, 0])
illumise.set_attacks([tackle, quick_attack, zen_headbutt, bug_buzz, play_rough], [charm, play_nice, sweet_scent])
roselia = Stage1('Roselia', 'Roserade', [50, 60, 45, 100, 80, 65], [60, 70, 65, 125, 105, 90], ['grass', 'poison', 0, 0, 0, 0])
roselia.set_attacks([poison_sting, magical_leaf, giga_drain, petal_blizzard, absorb, mega_drain], [growth, stun_spore, sweet_scent])
gulpin = Stage1('Gulpin', 'Swalot', [70, 43, 53, 43, 53, 40], [100, 73, 83, 73, 83, 55], ['poison', '', 0, 0, 0, 0])
gulpin.set_attacks([body_slam, pound, sludge, gunk_shot, acid_spray, sludge_bomb], [poison_gas, amnesia])
carvanha = Stage1('Carvanha', 'Sharpedo', [45, 90, 20, 65, 20, 65], [70, 120, 40, 95, 40, 95], ['water', 'dark', 0, 0, 0, 0])
carvanha.set_attacks([slash, night_slash, bite, aqua_jet, ice_fang, poison_fang, crunch, take_down], [leer, screech, swagger, agility, scary_face])
carvanha.can_mega('M Sharpedo', [70, 140, 70, 110, 65, 105], 'water', 'dark')
wailmer = Stage1('Wailmer', 'Wailord', [130, 70, 35, 70, 35, 60], [170, 90, 45, 90, 45, 60], ['water', '', 0, 0, 0, 0])
wailmer.set_attacks([water_gun, astonish, brine, hydro_pump], [growl, amnesia])
numel = Stage1('Numel', 'Camerupt', [60, 60, 40, 65, 45, 35], [70, 100, 70, 105, 75, 40], ['fire', 'ground', 0, 0, 0, 0])
numel.set_attacks([tackle, ember, flame_burst, earth_power, earthquake, take_down, double_edge, lava_plume, rock_slide], [growl, amnesia])
numel.can_mega('M Camerupt', [70, 120, 100, 145, 105, 20], 'fire', 'ground')
torkoal = Basic('Torkoal', [70, 85, 140, 85, 70, 20], ['fire', '', 0, 0, 0, 0])
torkoal.set_attacks([ember, rapid_spin, flame_wheel, body_slam, flamethrower, smog, heat_wave, inferno, lava_plume], [withdraw, iron_defense, amnesia, smokescreen])
spoink = Stage1('Spoink', 'Grumpig', [60, 25, 35, 70, 80, 60], [80, 45, 65, 90, 110, 80], ['psychic', '', 0, 0, 0, 0])
spoink.set_attacks([psybeam, zen_headbutt, payback, psychic, power_gem], [confuse_ray, teeter_dance])
spinda = Basic('Spinda', [60, 60, 60, 60, 60, 60], ['normal', '', 0, 0, 0, 0])
spinda.set_attacks([tackle, feint_attack, psybeam, double_edge, dizzy_punch], [teeter_dance])
trapinch = Stage2('Trapinch', 'Vibrava', 'Flygon', [45, 100, 45, 45, 45, 10], [50, 70, 50, 50, 50, 70], [80, 100, 80, 80, 80, 100], ['ground', '', 0, 'dragon', 0, 'dragon'])
trapinch.set_attacks([dragon_claw, dragon_breath, feint_attack, bulldoze, earth_power, earthquake, dragon_rush, mud_slap, rock_slide], [supersonic, screech, sand_attack, dragon_dance])
cacnea = Stage1('Cacnea', 'Cacturne', [50, 85, 40, 85, 40, 35], [70, 115, 60, 115, 60, 55], ['grass', '', 0, 'dark', 0, 0])
cacnea.set_attacks([poison_sting, feint_attack, payback, pin_missile, absorb, energy_ball, needle_arm], [leer, growth, sand_attack])
swablu = Stage1('Swablu', 'Altaria', [45, 40, 60, 40, 75, 50], [75, 70, 90, 70, 105, 80], ['normal', 'flying', 'dragon', 0, 0, 0])
swablu.set_attacks([dragon_breath, peck, astonish, disarming_voice, dragon_pulse, moonblast, fury_attack, take_down], [growl, cotton_guard, dragon_dance])
swablu.can_mega('M Altaria', [75, 110, 110, 110, 105, 80], 'dragon', 'fairy')
zangoose = Basic('Zangoose', [73, 115, 60, 60, 60, 90], ['normal', '', 0, 0, 0, 0])
zangoose.set_attacks([scratch, quick_attack, furry_cutter, pursuit, slash, xscissor], [leer, swords_dance, hone_claws])
seviper = Basic('Seviper', [73, 100, 60, 100, 60, 65], ['poison', '', 0, 0, 0, 0])
seviper.set_attacks([bite, lick, venoshock, poison_fang, night_slash, poison_jab, crunch], [swagger, screech, swords_dance, glare, coil])
lunatone = Basic('Lunatone', [90, 55, 65, 95, 85, 70], ['rock', 'psychic', 0, 0, 0, 0])
lunatone.set_attacks([psychic, moonblast, tackle, confusion, rock_throw, stone_edge, power_gem, rock_slide], [harden, cosmic_power])
solrock = Basic('Solrock', [90, 95, 85, 55, 65, 70], ['rock', 'psychic', 0, 0, 0, 0])
solrock.set_attacks([tackle, confusion, rock_throw, psychic, stone_edge, flare_blitz, rock_slide], [harden, cosmic_power])
barboach = Stage1('Barboach', 'Whiscash', [50, 48, 43, 46, 41, 60], [110, 78, 73, 76, 71, 60], ['water', 'ground', 0, 0, 0, 0])
barboach.set_attacks([zen_headbutt, water_gun, mud_bomb, aqua_tail, earthquake, mud_slap, muddy_water], [amnesia, tickle])
corphish = Stage1('Corphish', 'Crawdaunt', [43, 80, 65, 50, 35, 35], [63, 120, 85, 90, 55, 55], ['water', '', 0, 'dark', 0, 0])
corphish.set_attacks([crunch, night_slash, Bubble_beam, bubble, vice_grip, knock_off, crabhammer, razor_shell], [harden, leer, swords_dance])
baltoy = Stage1('Baltoy', 'Claydol', [40, 40, 55, 40, 70, 55], [60, 70, 105, 70, 120, 75], ['ground', 'psychic', 0, 0, 0, 0])
baltoy.set_attacks([confusion, rapid_spin, psybeam, ancient_power, earth_power, extrasensory, mud_slap, rock_tomb], [harden, cosmic_power])
lileep = Stage1('Lileep', 'Cradily', [66, 41, 77, 61, 87, 23], [86, 81, 97, 81, 107, 43], ['rock', 'grass', 0, 0, 0, 0])
lileep.set_attacks([astonish, acid, ancient_power, brine, giga_drain, energy_ball], [confuse_ray, amnesia])
anorith = Stage1('Anorith', 'Armaldo', [45, 95, 50, 40, 50, 75], [75, 125, 100, 70, 80, 45], ['rock', 'bug', 0, 0, 0, 0])
anorith.set_attacks([scratch, water_gun, furry_cutter, metal_claw, ancient_power, slash, brine, xscissor, rock_blast, bug_bite, crush_claw], [harden])
feebas = Stage1('Feebas', 'Milotic', [20, 15, 20, 10, 55, 80], [95, 60, 79, 100, 125, 81], ['water', '', 0, 0, 0, 0])
feebas.set_attacks([water_pulse, water_gun, disarming_voice, twister, hydro_pump, tackle], [coil])
kecleon = Basic('Kecleon', [60, 90, 70, 60, 120, 40], ['normal', '', 0, 0, 0, 0])
kecleon.set_attacks([astonish, lick, scratch, shadow_sneak, fury_swipes, feint_attack, psybeam, ancient_power, slash], [tail_whip, screech])
shuppet = Stage1('Shuppet', 'Banette', [44, 75, 35, 63, 33, 45], [64, 115, 65, 83, 63, 65], ['ghost', '', 0, 0, 0, 0])
shuppet.set_attacks([shadow_sneak, feint_attack, hex, shadow_ball, knock_off], [screech, willowisp])
shuppet.can_mega('M Banette', [64, 165, 75, 93, 83, 75], 'ghost', '')
duskull = Stage2('Duskull', 'Dusclops', 'Dusknoir', [20, 40, 90, 30, 90, 25], [40, 70, 130, 60, 130, 25], [45, 100, 135, 65, 135, 45], ['ghost', '', 0, 0, 0, 0])
duskull.set_attacks([shadow_punch, fire_punch, ice_punch, thunder_punch, astonish, shadow_sneak, pursuit, hex, shadow_ball, payback], [leer, willowisp, confuse_ray])
tropius = Basic('Tropius', [99, 68, 83, 72, 87, 51], ['grass', 'flying', 0, 0, 0, 0])
tropius.set_attacks([leaf_storm, gust, razor_leaf, magical_leaf, leaf_tornado, air_slash, body_slam, stomp], [leer, growth, sweet_scent])
chimecho = Basic('Chimecho', [75, 50, 80, 95, 90, 65], ['psychic', '', 0, 0, 0, 0])
chimecho.set_attacks([astonish, confusion, take_down, double_edge, extrasensory], [growl])
absol = Basic('Absol', [65, 130, 60, 75, 60, 75], ['dark', '', 0, 0, 0, 0])
absol.set_attacks([scratch, quick_attack, pursuit, bite, slash, night_slash], [leer, swords_dance, double_team])
absol.can_mega('M Absol', [65, 150, 60, 115, 60, 115], 'dark', '')
snorunt = Stage1('Snorunt', 'Glalie', [50, 50, 50, 50, 50, 50], [80, 80, 80, 80, 80, 80], ['ice', '', 0, 0, 0, 0])
snorunt.set_attacks([powder_snow, ice_shard, icy_wind, bite, ice_fang, headbutt, crunch, blizzard], [leer, double_team])
snorunt.can_mega('M Glalie', [80, 120, 80, 120, 80, 100], 'ice', '')
spheal = Stage2('Spheal', 'Sealeo', 'Walrein', [70, 40, 50, 55, 50, 25], [90, 60, 70, 75, 70, 45], [110, 80, 90, 95, 90, 65], ['ice', 'water', 0, 0, 0, 0])
spheal.set_attacks([ice_fang, crunch, powder_snow, water_gun, brine, aurora_beam, body_slam, blizzard, ice_ball], [swagger, defense_curl, growl])
huntail = Stage1('Clamperl', 'Huntail', [35, 64, 85, 74, 55, 32], [55, 104, 105, 94, 75, 52], ['water', '', 0, 0, 0, 0])
huntail.set_attacks([water_gun, bite, feint_attack, water_pulse, ice_fang, brine, crunch, aqua_tail, hydro_pump], [iron_defense, screech, coil, scary_face])
gorebyss = Stage1('Clamperl', 'Gorebyss', [35, 64, 85, 74, 55, 32], [55, 84, 105, 114, 75, 52], ['water', '', 0, 0, 0, 0])
gorebyss.set_attacks([water_gun, confusion, psychic, water_pulse, aqua_tail, hydro_pump], [iron_defense, amnesia, agility, coil])
relicanth = Basic('Relicanth', [100, 90, 130, 45, 65, 55], ['water', 'rock', 0, 0, 0, 0])
relicanth.set_attacks([tackle, water_gun, ancient_power, take_down, hydro_pump, double_edge, head_smash, rock_tomb], [harden])
luvdisc = Basic('Relicanth', [43, 30, 55, 40, 65, 97], ['water', '', 0, 0, 0, 0])
luvdisc.set_attacks([tackle, water_gun, water_pulse, take_down, hydro_pump], [charm, agility])
bagon = Stage2('Bagon', 'Shelgon', 'Salamence', [45, 75, 60, 40, 30, 50], [65, 95, 100, 60, 50, 50], [95, 135, 80, 110, 80, 100], ['dragon', '', 0, 0, 0, 'flying'])
bagon.set_attacks([fire_fang, thunder_fang, ember, bite, dragon_breath, headbutt, crunch, dragon_claw, zen_headbutt, flamethrower, double_edge], [leer, scary_face])
bagon.can_mega('M Salamence', [95, 145, 130, 120, 90, 120], 'dragon', 'flying')
beldum = Stage2('Beldum', 'Metang', 'Metagross', [40, 55, 80, 35, 60, 30], [60, 75, 100, 55, 80, 50], [80, 135, 130, 95, 90, 70], ['steel', 'psychic', 0, 0, 0, 0])
beldum.set_attacks([hammer_arm, confusion, metal_claw, take_down, pursuit, zen_headbutt, psychic, bullet_punch], [iron_defense, agility, scary_face])
beldum.can_mega('M Metagross', [80, 145, 130, 105, 110, 110], 'steel', 'psychic')
turtwig = Stage2('Turtwig', 'Grotle', 'Torterra', [55, 68, 64, 45, 55, 31], [75, 89, 85, 55, 65, 36], [95, 109, 105, 75, 85, 56], ['grass', '', 0, 0, 0, 'ground'])
turtwig.set_attacks([earthquake, wood_hammer, tackle, absorb, razor_leaf, bite, mega_drain, crunch, giga_drain, leaf_storm], [withdraw])
chimchar = Stage2('Chimchar', 'Monferno', 'Infernape', [44, 58, 44, 58, 44, 61], [64, 78, 52, 78, 52, 81], [76, 104, 71, 104, 71, 108], ['fire', '', 0, 'fighting', 0, 'fighting'])
chimchar.set_attacks([close_combat, flare_blitz, scratch, ember, fury_swipes, flame_wheel, mach_punch, facade], [leer, calm_mind])
piplup = Stage2('Piplup', 'Prinplup', 'Empoleon', [53, 51, 53, 61, 56, 40], [64, 66, 68, 81, 76, 50], [84, 86, 88, 111, 101, 60], ['water', '', 0, 0, 0, 'steel'])
piplup.set_attacks([aqua_jet, metal_claw, tackle, bubble, peck, Bubble_beam, fury_attack, brine, drill_peck, hydro_pump, pound], [growl, swords_dance, swagger])
starly = Stage2('Starly', 'Staravia', 'Staraptor', [40, 55, 30, 30, 30, 60], [55, 75, 50, 40, 40, 80], [85, 120, 70, 50, 60, 100], ['normal', 'flying', 0, 0, 0, 0])
starly.set_attacks([close_combat, tackle, quick_attack, wing_attack, aerial_ace, take_down, brave_bird], [growl, agility, double_team])
bidoof = Stage1('Bidoof', 'Bibarel', [59, 45, 40, 35, 40, 31], [79, 85, 60, 55, 60, 71], ['normal', '', 0, 'water', 0, 0])
bidoof.set_attacks([water_gun, aqua_jet, tackle, headbutt, hyper_fang, crunch, take_down, superpower], [growl, defense_curl, swords_dance, amnesia])
kricketot = Stage1('Kricketot', 'Kricketune', [37, 25, 41, 25, 41, 25], [77, 85, 51, 55, 51, 55], ['bug', '', 0, 0, 0, 0])
kricketot.set_attacks([bug_bite, furry_cutter, absorb, slash, xscissor, night_slash, bug_buzz], [growl, screech])
shinx = Stage2('Shinx', 'Luxio', 'Luxray', [45, 65, 34, 40, 34, 45], [60, 85, 49, 60, 49, 60], [80, 120, 79, 95, 79, 70], ['electric', '', 0, 0, 0, 0])
shinx.set_attacks([tackle, spark, bite, thunder_fang, crunch, discharge, wild_charge], [leer, swagger, babydoll_eyes, scary_face])
cranidos = Stage1('Cranidos', 'Rampardos', [67, 125, 40, 30, 30, 58], [97, 165, 60, 65, 50, 58], ['rock', '', 0, 0, 0, 0])
cranidos.set_attacks([headbutt, pursuit, take_down, ancient_power, zen_headbutt, head_smash], [leer, screech, scary_face])
shieldon = Stage1('Shieldon', 'Bastiodon', [30, 42, 118, 42, 88, 30], [60, 52, 168, 47, 138, 30], ['rock', 'steel', 0, 0, 0, 0])
shieldon.set_attacks([tackle, iron_head, take_down, ancient_power], [metal_sound, iron_defense, swagger])
combee = Stage1('Combee', 'Vespiquen', [30, 30, 42, 30, 42, 70], [70, 80, 102, 80, 102, 40], ['bug', 'flying', 0, 0, 0, 0])
combee.set_attacks([slash, gust, poison_sting, furry_cutter, pursuit, fury_swipes, power_gem, bug_bite, bug_buzz], [confuse_ray, swagger, sweet_scent])
pachirisu = Basic('Pachirisu', [60, 45, 70, 45, 90, 95], ['electric', '', 0, 0, 0, 0])
pachirisu.set_attacks([quick_attack, spark, swift, discharge, hyper_fang, nuzzle], [growl, thunder_wave, charm])
buizel = Stage1('Buizel', 'Floatzel', [55, 65, 35, 60, 30, 85], [85, 105, 55, 85, 50, 115], ['water', '', 0, 0, 0, 0])
buizel.set_attacks([ice_fang, crunch, quick_attack, water_gun, pursuit, swift, aqua_jet, aqua_tail, hydro_pump], [growl, agility])
drifloon = Stage1('Drifloon', 'Drifblim', [90, 50, 34, 60, 44, 70], [150, 80, 44, 90, 54, 80], ['ghost', 'flying', 0, 0, 0, 0])
drifloon.set_attacks([astonish, gust, payback, hex, shadow_ball, ominous_wind], [amnesia, minimize])
buneary = Stage1('Buneary', 'Lopunny', [55, 66, 44, 44, 56, 85], [65, 76, 84, 54, 96, 105], ['normal', '', 0, 0, 0, 0])
buneary.set_attacks([pound, quick_attack, dizzy_punch], [defense_curl, babydoll_eyes, charm, agility])
buneary.can_mega('M Lopunny', [65, 136, 94, 54, 96, 135], 'normal', 'fighting')
glameow = Stage1('Glameow', 'Purugly', [49, 55, 42, 42, 37, 85], [71, 82, 64, 64, 59, 112], ['normal', '', 0, 0, 0, 0])
glameow.set_attacks([scratch, feint_attack, fury_swipes, slash, body_slam], [growl, swagger, charm, hone_claws])
stunky = Stage1('Stunky', 'Skuntank', [63, 63, 47, 41, 41, 74], [103, 93, 67, 71, 61, 84], ['poison', 'dark', 0, 0, 0, 0])
stunky.set_attacks([flamethrower, scratch, fury_swipes, acid_spray, bite, night_slash], [poison_gas, screech])
bronzor = Stage1('Bronzor', 'Bronzong', [57, 24, 86, 24, 86, 23], [67, 89, 116, 79, 116, 33], ['steel', 'psychic', 0, 0, 0, 0])
bronzor.set_attacks([tackle, confusion, feint_attack, payback, extrasensory], [confuse_ray, iron_defense, metal_sound])
chatot = Basic('Chatot', [76, 65, 45, 92, 42, 91], ['normal', 'flying', 0, 0, 0, 0])
chatot.set_attacks([hyper_voice, peck, fury_attack], [growl, feather_dance])
spiritomb = Basic('Spiritomb', [50, 92, 108, 92, 108, 35], ['ghost', 'dark', 0, 0, 0, 0])
spiritomb.set_attacks([pursuit, shadow_sneak, feint_attack, dark_pulse, ominous_wind], [confuse_ray, nasty_plot])
gible = Stage2('Gible', 'Gabite', 'Garchomp', [58, 70, 45, 40, 45, 42], [68, 90, 65, 50, 55, 82], [108, 130, 95, 80, 85, 102], ['dragon', 'ground', 0, 0, 0, 0])
gible.set_attacks([crunch, fire_fang, tackle, take_down, slash, dragon_claw, dragon_rush, dual_chop], [sand_attack])
gible.can_mega('M Garchomp', [108, 170, 115, 120, 95, 92], 'dragon', 'ground')
riolu = Stage1('Riolu', 'Lucario', [40, 70, 40, 35, 40, 60], [70, 110, 70, 115, 70, 90], ['fighting', '', 0, 'steel', 0, 0])
riolu.set_attacks([metal_claw, quick_attack, close_combat, dragon_pulse, force_palm], [calm_mind, metal_sound, swords_dance, screech, nasty_plot])
riolu.can_mega('M Lucario', [70, 145, 88, 140, 70, 112], 'fighting', 'steel')
hippopotas = Stage1('Hippopotas', 'Hippowdon', [68, 72, 78, 38, 42, 32], [108, 112, 118, 68, 72, 47], ['ground', '', 0, 0, 0, 0])
hippopotas.set_attacks([ice_fang, fire_fang, thunder_fang, tackle, bite, take_down, crunch, earthquake, double_edge], [sand_attack])
skorupi = Stage1('Skorupi', 'Drapion', [40, 50, 90, 30, 55, 65], [70, 90, 110, 60, 75, 95], ['poison', 'bug', 0, 'dark', 0, 0])
skorupi.set_attacks([thunder_fang, fire_fang, ice_fang, poison_sting, bite, pin_missile, pursuit, bug_bite, venoshock, poison_fang, night_slash, crunch, cross_poison, knock_off], [leer, hone_claws, scary_face])
croagunk = Stage1('Croagunk', 'Toxicroak', [48, 61, 40, 61, 40, 50], [83, 106, 65, 86, 65, 85], ['poison', 'fighting', 0, 0, 0, 0])
croagunk.set_attacks([astonish, poison_sting, pursuit, feint_attack, mud_bomb, venoshock, poison_jab, sludge_bomb, mud_slap], [swagger, nasty_plot])
carnivine = Basic('Carnivine', [74, 100, 72, 90, 72, 46], ['grass', '', 0, 0, 0, 0])
carnivine.set_attacks([vine_whip, bite, feint_attack, leaf_tornado, crunch, power_whip], [growth, sweet_scent])
finneon = Stage1('Finneon', 'Lumineon', [49, 49, 56, 49, 61, 66], [69, 69, 76, 69, 86, 91], ['water', '', 0, 0, 0, 0])
finneon.set_attacks([gust, pound, water_gun, water_pulse, silver_wind], [])
snover = Stage1('Snover', 'Abomasnow', [60, 62, 50, 62, 60, 40], [90, 92, 75, 92, 85, 60], ['grass', 'ice', 0, 0, 0, 0])
snover.set_attacks([ice_punch, powder_snow, razor_leaf, icy_wind, ice_shard, wood_hammer, blizzard], [leer, swagger])
snover.can_mega('M Abomasnow', [90, 132, 105, 132, 105, 30], 'grass', 'ice')
leafeon = Stage1('Eevee', 'Leafeon', [55, 55, 50, 45, 65, 55], [65, 110, 130, 60, 65, 95], ['normal', '', 'grass', 0, 0, 0])
leafeon.set_attacks([bite, tackle, giga_drain, quick_attack, swift, razor_leaf, leaf_blade], [tail_whip, growl, babydoll_eyes, swords_dance, charm, sand_attack])
glaceon = Stage1('Eevee', 'Glaceon', [55, 55, 50, 45, 65, 55], [65, 60, 110, 130, 95, 65], ['normal', '', 'ice', 0, 0, 0])
glaceon.set_attacks([bite, tackle, icy_wind, quick_attack, ice_shard, ice_fang, blizzard], [tail_whip, growl, babydoll_eyes, charm, sand_attack])
snivy = Stage2('Snivy', 'Servine', 'Serperior', [45, 45, 55, 45, 55, 63], [60, 60, 75, 60, 75, 83], [75, 75, 95, 75, 95, 113], ['grass', '', 0, 0, 0, 0])
snivy.set_attacks([tackle, vine_whip, leaf_tornado, mega_drain, slam, giga_drain, leaf_storm], [leer, growth, coil])
tepig = Stage2('Tepig', 'Pignite', 'Emboar', [65, 63, 45, 45, 45, 45], [90, 93, 55, 70, 55, 55], [110, 123, 65, 100, 65, 65], ['fire', '', 0, 'fighting', 0, 'fighting'])
tepig.set_attacks([hammer_arm, tackle, ember, smog, take_down, flamethrower, flare_blitz, arm_thrust, flame_charge, head_smash], [tail_whip, defense_curl])
oshawott = Stage2('Oshawott', 'Dewott', 'Samurott', [55, 55, 45, 63, 45, 45], [75, 75, 60, 83, 60, 60], [95, 100, 85, 108, 70, 70], ['water', '', 0, 0, 0, 0])
oshawott.set_attacks([slash, megahorn, water_gun, water_pulse, furry_cutter, aqua_jet, aqua_tail, hydro_pump, razor_shell], [tail_whip, swords_dance])
patrat = Stage1('Patrat', 'Watchog', [45, 55, 39, 35, 39, 42], [60, 85, 69, 60, 69, 77], ['normal', '', 0, 0, 0, 0])
patrat.set_attacks([bite, tackle, crunch, hyper_fang, slam], [confuse_ray, leer, nasty_plot, sand_attack])
lillipup = Stage2('Lillipup', 'Herdier', 'Stoutland', [45, 60, 45, 25, 45, 55], [65, 80, 65, 35, 65, 60], [85, 110, 90, 45, 90, 80], ['normal', '', 0, 0, 0, 0])
lillipup.set_attacks([ice_fang, fire_fang, thunder_fang, tackle, bite, take_down, crunch, play_rough], [leer, babydoll_eyes])
purrloin = Stage1('Purrloin', 'Liepard', [41, 50, 37, 50, 37, 66], [64, 88, 50, 88, 50, 106], ['dark', '', 0, 0, 0, 0])
purrloin.set_attacks([scratch, fury_swipes, pursuit, slash, play_rough], [growl, nasty_plot, sand_attack, hone_claws])
pansage = Stage1('Pansage', 'Simisage', [50, 53, 48, 53, 48, 64], [75, 98, 63, 98, 63, 101], ['grass', '', 0, 0, 0, 0])
pansage.set_attacks([lick, seed_bomb, fury_swipes, scratch, vine_whip, bite, crunch], [leer, nasty_plot, play_nice])
pansear = Stage1('Pansear', 'Simisear', [50, 53, 48, 53, 48, 64], [75, 98, 63, 98, 63, 101], ['fire', '', 0, 0, 0, 0])
pansear.set_attacks([lick, flame_burst, fury_swipes, scratch, fire_blast, bite, crunch], [leer, amnesia, play_nice])
panpour = Stage1('Panpour', 'Simipour', [50, 53, 48, 53, 48, 64], [75, 98, 63, 98, 63, 101], ['water', '', 0, 0, 0, 0])
panpour.set_attacks([lick, water_gun, fury_swipes, scratch, brine, bite, crunch], [leer, play_nice])
munna = Stage1('Munna', 'Musharna', [76, 25, 45, 67, 55, 24], [116, 55, 85, 107, 95, 29], ['psychic', '', 0, 0, 0, 0])
munna.set_attacks([psybeam, zen_headbutt, psychic], [defense_curl, calm_mind])
pidove = Stage2('Pidove', 'Tranquill', 'Unfezant', [50, 55, 50, 36, 30, 43], [62, 77, 62, 50, 42, 65], [80, 115, 80, 65, 55, 93], ['normal', 'flying', 0, 0, 0, 0])
pidove.set_attacks([gust, quick_attack, air_slash, facade], [leer, growl, feather_dance, swagger])
blitzle = Stage1('Blitzle', 'Zebstrika', [45, 60, 32, 50, 32, 76], [75, 100, 63, 80, 63, 116], ['electric', '', 0, 0, 0, 0])
blitzle.set_attacks([quick_attack, pursuit, spark, discharge, stomp, flame_charge, wild_charge], [tail_whip, thunder_wave, agility])
roggenrola = Stage2('Roggenrola', 'Boldore', 'Gigalith', [55, 75, 85, 25, 25, 15], [70, 105, 105, 50, 40, 20], [85, 135, 130, 60, 80, 25], ['rock', '', 0, 0, 0, 0])
roggenrola.set_attacks([power_gem, tackle, headbutt, rock_blast, stone_edge, mud_slap, rock_slide], [harden, iron_defense, sand_attack])
woobat = Stage1('Woobat', 'Swoobat', [65, 45, 43, 55, 43, 72], [67, 57, 55, 77, 55, 114], ['psychic', 'flying', 0, 0, 0, 0])
woobat.set_attacks([confusion, gust, air_slash, psychic], [amnesia, calm_mind])
drilbur = Stage1('Drilbur', 'Excadrill', [60, 85, 40, 30, 45, 68], [110, 135, 60, 50, 65, 88], ['ground', '', 0, 'steel', 0, 0])
drilbur.set_attacks([scratch, rapid_spin, fury_swipes, metal_claw, earthquake, drill_run, mud_slap, rock_slide], [swords_dance, hone_claws])
audino = Basic('Audino', [103, 60, 86, 60, 86, 50], ['normal', '', 0, 0, 0, 0])
audino.set_attacks([hyper_voice, pound, disarming_voice, take_down, double_edge], [growl, babydoll_eyes, play_nice])
audino.can_mega('M Audino', [103, 60, 126, 80, 126, 50], 'normal', 'fairy')
timburr = Stage2('Timburr', 'Gurdurr', 'Conkeldurr', [75, 80, 55, 25, 35, 35], [85, 105, 85, 40, 50, 40], [105, 140, 95, 55, 65, 45], ['fighting', '', 0, 0, 0, 0])
timburr.set_attacks([pound, rock_throw, wakeup_slap, dynamic_punch, hammer_arm, stone_edge, superpower, rock_slide], [leer, bulk_up, scary_face])
tympole = Stage2('Tympole', 'Palpitoad', 'Seismitoad', [50, 50, 40, 50, 40, 64], [75, 65, 55, 65, 55, 69], [105, 95, 75, 85, 75, 74], ['water', '', 0, 'ground', 0, 'ground'])
tympole.set_attacks([acid, bubble, Bubble_beam, mud_shot, hydro_pump, hyper_voice, muddy_water], [growl, supersonic])
throh = Basic('Throh', [120, 100, 85, 30, 85, 45], ['fighting', '', 0, 0, 0, 0])
throh.set_attacks([body_slam, superpower], [leer, bulk_up])
sawk = Basic('Sawk', [75, 125, 75, 30, 75, 85], ['fighting', '', 0, 0, 0, 0])
sawk.set_attacks([double_kick, karate_chop, brick_break, close_combat, rock_smash], [leer, bulk_up])
sewaddle = Stage2('Sewaddle', 'Swadloon', 'Leavanny', [45, 53, 70, 40, 60, 42], [55, 63, 90, 50, 80, 42], [75, 103, 80, 70, 80, 92], ['bug', 'grass', 0, 0, 0, 0])
sewaddle.set_attacks([tackle, bug_bite, razor_leaf, leaf_blade, xscissor, leaf_storm], [swords_dance, string_shot])
venipede = Stage2('Venipede', 'Whirlipede', 'Scolipede', [30, 45, 59, 30, 39, 57], [40, 55, 99, 40, 79, 47], [60, 100, 89, 55, 69, 112], ['bug', 'poison', 0, 0, 0, 0])
venipede.set_attacks([poison_sting, megahorn, pursuit, bug_bite, venoshock, double_edge, rock_climb, steamroller], [iron_defense, defense_curl, screech, agility])
cottonee = Stage1('Cottonee', 'Whimsicott', [40, 27, 60, 37, 50, 66], [60, 67, 85, 77, 75, 116], ['grass', 'fairy', 0, 0, 0, 0])
cottonee.set_attacks([mega_drain, gust, hurricane, moonblast, fairy_wind, absorb, giga_drain, energy_ball], [growth, stun_spore, poison_powder, charm, cotton_guard])
petilil = Stage1('Petilil', 'Lilligant', [45, 35, 50, 70, 50, 30], [70, 60, 75, 110, 75, 90], ['grass', '', 0, 0, 0, 0])
petilil.set_attacks([absorb, mega_drain, magical_leaf, giga_drain, leaf_storm, energy_ball], [growth, stun_spore, teeter_dance])
basculin = Basic('Basculin', [70, 92, 65, 80, 55, 98], ['water', '', 0, 0, 0, 0])
basculin.set_attacks([tackle, water_gun, headbutt, bite, aqua_jet, take_down, crunch, take_down, aqua_tail, double_edge, head_smash], [tail_whip, scary_face])
sandile = Stage2('Sandile', 'Krokorok', 'Krookodile', [50, 72, 35, 35, 35, 65], [60, 82, 45, 45, 45, 74], [95, 117, 80, 65, 70, 92], ['ground', 'dark', 0, 0, 0, 0])
sandile.set_attacks([bite, crunch, earthquake, mud_slap], [leer, swagger, sand_attack, scary_face])
darumaka = Stage1('Darumaka', 'Darmanitan', [70, 90, 45, 15, 45, 50], [105, 140, 55, 30, 55, 95], ['fire', '', 0, 0, 0, 0])
darumaka.set_attacks([hammer_arm, tackle, fire_fang, headbutt, fire_punch, flare_blitz, superpower, facade], [swagger])
g_darumaka = Stage1('G.Darumaka', 'G.Darmanitan', [70, 90, 45, 15, 45, 50], [105, 140, 55, 30, 55, 95], ['ice', '', 0, 0, 0, 0])
g_darumaka.set_attacks([icicle_crash, powder_snow, tackle, headbutt, avalanche, ice_fang, superpower, ice_punch, blizzard], [])
maractus = Basic('Maractus', [75, 86, 67, 106, 67, 60], ['grass', '', 0, 0, 0, 0])
maractus.set_attacks([peck, absorb, pin_missile, mega_drain, giga_drain, petal_blizzard, needle_arm], [growth, cotton_guard, sweet_scent])
dwebble = Stage1('Dwebble', 'Crustle', [50, 65, 85, 35, 35, 55], [70, 105, 125, 65, 75, 45], ['bug', 'rock', 0, 0, 0, 0])
dwebble.set_attacks([rock_blast, feint_attack, bug_bite, slash, xscissor, rock_slide], [withdraw, sand_attack])
scraggy = Stage1('Scraggy', 'Scrafty', [50, 75, 70, 35, 70, 48], [65, 90, 115, 45, 115, 58], ['dark', 'fighting', 0, 0, 0, 0])
scraggy.set_attacks([headbutt, feint_attack, payback, brick_break, crunch, facade, head_smash, rock_climb], [leer, swagger, sand_attack, scary_face])
sigilyph = Basic('Sigilyph', [72, 58, 80, 103, 80, 97], ['psychic', 'flying', 0, 0, 0, 0])
sigilyph.set_attacks([gust, psybeam, air_slash, psychic], [cosmic_power])
yamask = Stage1('Yamask', 'Cofagrigus', [38, 30, 85, 55, 65, 30], [58, 50, 145, 95, 105, 30], ['ghost', '', 0, 0, 0, 0])
yamask.set_attacks([astonish, hex, shadow_ball, ominous_wind], [willowisp, scary_face])
g_yamask = Stage1('G.Yamask', 'Runerigus', [38, 55, 85, 30, 65, 30], [58, 95, 145, 50, 105, 30], ['ground', 'ghost', 0, 0, 0, 0])
g_yamask.set_attacks([astonish, hex, shadow_ball, slam, earthquake], [])
tirtouga = Stage1('Tirtouga', 'Carracosta', [54, 78, 103, 53, 45, 22], [74, 108, 133, 83, 65, 32], ['water', 'rock', 0, 0, 0, 0])
tirtouga.set_attacks([water_gun, bite, aqua_jet, ancient_power, crunch, brine, aqua_tail, hydro_pump, rock_slide], [withdraw])
archen = Stage1('Archen', 'Archeops', [55, 112, 45, 74, 45, 70], [75, 140, 65, 112, 65, 110], ['rock', 'flying', 0, 0, 0, 0])
archen.set_attacks([quick_attack, wing_attack, rock_throw, ancient_power, crunch, dragon_breath, dragon_claw, rock_slide], [leer, agility, double_team, scary_face])
trubbish = Stage1('Trubbish', 'Garbodor', [50, 50, 62, 40, 62, 65], [80, 95, 82, 60, 82, 75], ['poison', '', 0, 0, 0, 0])
trubbish.set_attacks([pound, acid_spray, double_slap, sludge, body_slam, gunk_shot, sludge_bomb], [poison_gas, amnesia])
zorua = Stage1('Zorua', 'Zoroark', [40, 65, 40, 80, 40, 65], [60, 105, 60, 120, 60, 105], ['dark', '', 0, 0, 0, 0])
zorua.set_attacks([night_slash, scratch, pursuit, fury_swipes, feint_attack], [leer, nasty_plot, fake_tears, agility, hone_claws, scary_face])
minccino = Stage1('Minccino', 'Cinccino', [55, 50, 40, 40, 40, 75], [75, 95, 60, 65, 60, 115], ['normal', '', 0, 0, 0, 0])
minccino.set_attacks([bullet_seed, rock_blast, pound, double_slap, swift, slam, wakeup_slap, hyper_voice], [babydoll_eyes, charm, tickle])
gothita = Stage2('Gothita', 'Gothorita', 'Gothitelle', [45, 30, 50, 55, 65, 45], [60, 45, 70, 75, 85, 55], [70, 55, 95, 95, 110, 65], ['psychic', '', 0, 0, 0, 0])
gothita.set_attacks([pound, confusion, double_slap, feint_attack, psychic], [charm, fake_tears, tickle, play_nice])
ducklett = Stage1('Ducklett', 'Swanna', [62, 44, 50, 44, 50, 55], [75, 87, 63, 87, 63, 98], ['water', 'flying', 0, 0, 0, 0])
ducklett.set_attacks([water_gun, wing_attack, water_pulse, aerial_ace, Bubble_beam, air_slash, brave_bird, hurricane], [feather_dance, defog])
vanillite = Stage2('Vanillite', 'Vanillish', 'Vanilluxe', [36, 50, 50, 65, 60, 44], [51, 65, 65, 80, 75, 59], [71, 95, 85, 110, 95, 79], ['ice', '', 0, 0, 0, 0])
vanillite.set_attacks([icicle_spear, astonish, icy_wind, avalanche, ice_beam, blizzard, mirror_shot], [harden])
deerling = Stage1('Deerling', 'Sawsbuck', [60, 60, 50, 40, 50, 75], [80, 100, 70, 60, 70, 95], ['normal', 'grass', 0, 0, 0, 0])
deerling.set_attacks([megahorn, tackle, double_kick, feint_attack, take_down, double_edge, energy_ball], [growl, charm, sand_attack])
emolga = Basic('Emolga', [55, 75, 60, 75, 60, 103], ['electric', 'flying', 0, 0, 0, 0])
emolga.set_attacks([thunder_shock, quick_attack, spark, pursuit, discharge, nuzzle], [tail_whip, agility, double_team])
karrablast = Stage1('Karrablast', 'Escavalier', [50, 75, 45, 40, 45, 60], [70, 135, 105, 60, 105, 20], ['bug', '', 0, 'steel', 0, 0])
karrablast.set_attacks([double_edge, peck, twineedle, fury_attack, bug_buzz, slash, iron_head, xscissor, headbutt, take_down], [leer, iron_defense, swords_dance, scary_face])
foongus = Stage1('Foongus', 'Amoonguss', [69, 55, 45, 55, 55, 15], [114, 85, 70, 85, 80, 30], ['grass', 'poison', 0, 0, 0, 0])
foongus.set_attacks([absorb, astonish, mega_drain, feint_attack, giga_drain], [growth, sweet_scent])
frillish = Stage1('Frillish', 'Jellicent', [55, 40, 50, 65, 85, 40], [100, 60, 70, 85, 105, 60], ['water', 'ghost', 0, 0, 0, 0])
frillish.set_attacks([bubble, absorb, Bubble_beam, water_pulse, hex, hydro_pump, ominous_wind], [])
alomomola = Basic('Alomomola', [165, 75, 80, 40, 45, 65], ['water', '', 0, 0, 0, 0])
alomomola.set_attacks([hydro_pump, pound, aqua_jet, double_slap, water_pulse, brine], [play_nice])
joltik = Stage1('Joltik', 'Galvantula', [50, 47, 50, 57, 50, 65], [70, 77, 60, 97, 60, 108], ['bug', 'electric', 0, 0, 0, 0])
joltik.set_attacks([absorb, furry_cutter, bug_bite, slash, signal_beam, discharge, bug_buzz], [thunder_wave, screech, agility, string_shot])
ferroseed = Stage1('Ferroseed', 'Ferrothorn', [44, 50, 91, 24, 86, 10], [74, 94, 131, 54, 116, 20], ['grass', 'steel', 0, 0, 0, 0])
ferroseed.set_attacks([tackle, metal_claw, pin_missile, iron_head, payback, flash_cannon, mirror_shot, power_whip, rock_climb], [harden, iron_defense])
klink = Stage2('Klink', 'Klang', 'Klinklang', [40, 55, 70, 45, 60, 30], [60, 80, 95, 70, 85, 50], [60, 100, 115, 70, 85, 90], ['steel', '', 0, 0, 0, 0])
klink.set_attacks([thunder_shock, discharge, zap_cannon, vice_grip, charge_beam, mirror_shot], [metal_sound, screech])
tynamo = Stage2('Tynamo', 'Eelektrik', 'Eelektross', [35, 55, 40, 45, 40, 60], [65, 85, 70, 75, 70, 40], [85, 115, 80, 105, 80, 50], ['electric', '', 0, 0, 0, 0])
tynamo.set_attacks([crunch, crush_claw, zap_cannon, headbutt, discharge, acid, spark, thunderbolt, acid_spray, charge_beam, wild_charge], [thunder_wave, coil])
elgyem = Stage1('Elgyem', 'Beheeyem', [55, 55, 55, 85, 55, 30], [75, 75, 75, 125, 95, 40], ['psychic', '', 0, 0, 0, 0])
elgyem.set_attacks([confusion, psybeam, headbutt, zen_headbutt, psychic], [growl, calm_mind])
litwick = Stage2('Litwick', 'Lampent', 'Chandelure', [50, 30, 55, 65, 55, 20], [60, 40, 60, 95, 60, 55], [60, 55, 90, 145, 90, 80], ['ghost', 'fire', 0, 0, 0, 0])
litwick.set_attacks([hex, smog, flame_burst, ember, astonish, inferno, shadow_ball], [confuse_ray, willowisp, minimize])
axew = Stage2('Axew', 'Fraxure', 'Haxorus', [46, 87, 60, 30, 40, 57], [66, 117, 70, 40, 50, 67], [76, 147, 90, 60, 70, 97], ['dragon', '', 0, 0, 0, 0])
axew.set_attacks([scratch, slash, dragon_claw, dragon_pulse, dual_chop], [leer, swords_dance, dragon_dance, scary_face])
cubchoo = Stage1('Cubchoo', 'Beartic', [55, 70, 40, 60, 40, 40], [95, 130, 80, 70, 80, 50], ['ice', '', 0, 0, 0, 0])
cubchoo.set_attacks([icicle_crash, superpower, aqua_jet, powder_snow, icy_wind, fury_swipes, brine, slash, blizzard], [growl, swagger, charm, play_nice])
cryogonal = Basic('Cryogonal', [80, 50, 50, 95, 135, 105], ['ice', '', 0, 0, 0, 0])
cryogonal.set_attacks([night_slash, ice_shard, rapid_spin, icy_wind, aurora_beam, ancient_power, ice_beam, slash], [confuse_ray])
shelmet = Stage1('Shelmet', 'Accelgor', [50, 40, 85, 40, 65, 25], [80, 70, 40, 100, 60, 145], ['bug', '', 0, 0, 0, 0])
shelmet.set_attacks([absorb, acid_spray, quick_attack, mega_drain, swift, giga_drain, bug_buzz, body_slam], [agility, double_team])
stunfisk = Basic('Stunfisk', [109, 66, 84, 81, 99, 32], ['ground', 'electric', 0, 0, 0, 0])
stunfisk.set_attacks([tackle, water_gun, thunder_shock, mud_bomb, discharge, thunderbolt, mud_slap, muddy_water], [])
mienfoo = Stage1('Mienfoo', 'Mienshao', [45, 85, 50, 55, 50, 65], [65, 125, 60, 95, 60, 105], ['fighting', '', 0, 0, 0, 0])
mienfoo.set_attacks([pound, double_slap, swift, force_palm], [calm_mind, meditate])
druddigon = Basic('Druddigon', [77, 120, 90, 60, 90, 48], ['dragon', '', 0, 0, 0, 0])
druddigon.set_attacks([scratch, bite, slash, crunch, dragon_claw, night_slash, superpower, rock_climb], [leer, hone_claws, scary_face])
golett = Stage1('Golett', 'Golurk', [59, 74, 50, 35, 50, 35], [89, 124, 80, 55, 80, 55], ['ground', 'ghost', 0, 0, 0, 0])
golett.set_attacks([pound, astonish, shadow_punch, earthquake, hammer_arm, mega_punch, mud_slap], [defense_curl, iron_defense])
pawniard = Stage1('Pawniard', 'Bisharp', [45, 85, 70, 40, 40, 60], [65, 125, 100, 60, 70, 70], ['dark', 'steel', 0, 0, 0, 0])
pawniard.set_attacks([iron_head, scratch, furry_cutter, feint_attack, slash, metal_claw], [leer, metal_sound, iron_defense, swords_dance, scary_face])
bouffalant = Basic('Bouffalant', [95, 110, 95, 40, 95, 55], ['normal', '', 0, 0, 0, 0])
bouffalant.set_attacks([pursuit, fury_attack, horn_attack, megahorn], [leer, swords_dance, scary_face])
rufflet = Stage1('Rufflet', 'Braviary', [70, 83, 50, 37, 50, 60], [100, 123, 75, 57, 75, 80], ['normal', 'flying', 0, 0, 0, 0])
rufflet.set_attacks([superpower, brave_bird, peck, fury_attack, wing_attack, aerial_ace, air_slash, crush_claw], [leer, defog, hone_claws, scary_face])
vullaby = Stage1('Vullaby', 'Mandibuzz', [70, 55, 75, 45, 65, 60], [110, 65, 105, 55, 95, 80], ['dark', 'flying', 0, 0, 0, 0])
vullaby.set_attacks([brave_bird, gust, fury_attack, feint_attack, air_slash, dark_pulse], [leer, nasty_plot, defog])
heatmor = Basic('Heatmor', [85, 97, 66, 105, 66, 65], ['fire', '', 0, 0, 0, 0])
heatmor.set_attacks([tackle, lick, fury_swipes, flame_burst, bug_bite, slash, flamethrower, flare_blitz, inferno], [amnesia, hone_claws])
durant = Basic('Durant', [58, 109, 112, 48, 48, 109], ['bug', 'steel', 0, 0, 0, 0])
durant.set_attacks([metal_claw, furry_cutter, bite, bug_bite, crunch, iron_head, xscissor, vice_grip], [iron_defense, metal_sound, sand_attack, agility])
deino = Stage2('Deino', 'Zweilous', 'Hydreigon', [52, 65, 50, 45, 50, 38], [72, 85, 70, 65, 70, 58], [92, 105, 90, 125, 90, 98], ['dark', 'dragon', 0, 0, 0, 0])
deino.set_attacks([hyper_voice, bite, dragon_breath, crunch, dragon_pulse, body_slam, tackle, headbutt, slam, dragon_rush], [scary_face])
larvesta = Stage1('Larvesta', 'Volcarona', [55, 85, 55, 50, 55, 60], [85, 60, 65, 135, 105, 100], ['bug', 'fire', 0, 0, 0, 0])
larvesta.set_attacks([hurricane, heat_wave, flare_blitz, flame_wheel, ember, absorb, gust, silver_wind, flame_charge], [quilver_dance, amnesia, string_shot])
chespin = Stage2('Chespin', 'Quilladin', 'Chesnaught', [56, 61, 65, 48, 45, 38], [61, 78, 95, 56, 58, 57], [88, 107, 122, 74, 75, 64], ['grass', '', 0, 0, 0, 'fighting'])
chespin.set_attacks([hammer_arm, tackle, vine_whip, bite, pin_missile, take_down, seed_bomb, mud_shot, body_slam, wood_hammer, needle_arm], [growl, bulk_up])
fennekin = Stage2('Fennekin', 'Braixen', 'Delphox', [40, 45, 40, 62, 60, 60], [59, 59, 58, 90, 70, 73], [75, 69, 72, 114, 100, 104], ['fire', '', 0, 0, 0, 'psychic'])
fennekin.set_attacks([shadow_ball, scratch, ember, psybeam, flamethrower, psychic, fire_blast, flame_charge], [tail_whip, willowisp, howl])
froakie = Stage2('Froakie', 'Frogadier', 'Greninja', [41, 56, 40, 62, 44, 71], [54, 63, 52, 83, 56, 97], [72, 95, 67, 103, 71, 122], ['water', '', 0, 0, 0, 'dark'])
froakie.set_attacks([night_slash, pound, bubble, quick_attack, lick, water_pulse, shadow_sneak, feint_attack, hydro_pump, extrasensory], [growl, double_team, smokescreen])
bunnelby = Stage1('Bunnelby', 'Diggersby', [38, 36, 38, 32, 36, 57], [85, 56, 77, 50, 77, 78], ['normal', '', 0, 'ground', 0, 0])
bunnelby.set_attacks([hammer_arm, bulldoze, tackle, quick_attack, take_down, mud_shot, double_kick, earthquake, facade, mud_slap], [swords_dance, leer, agility])
fletchling = Stage2('Fletchling', 'Fletchinder', 'Talonflame', [45, 50, 43, 40, 38, 62], [62, 73, 55, 56, 52, 84], [78, 81, 71, 74, 69, 126], ['normal', 'flying', 'fire', 'flying', 'fire', 'flying'])
fletchling.set_attacks([ember, brave_bird, flare_blitz, tackle, quick_attack, peck, flame_charge, steel_wing], [growl, agility])
scatterbug = Stage2('Scatterbug', 'Spewpa', 'Vivillon', [38, 35, 40, 27, 25, 35], [45, 22, 60, 27, 30, 29], [80, 52, 50, 90, 50, 89], ['bug', '', 0, 0, 0, 'flying'])
scatterbug.set_attacks([gust, psybeam, bug_buzz, hurricane, tackle, bug_bite], [stun_spore, poison_powder, supersonic, quilver_dance, string_shot])
litleo = Stage1('Litleo', 'Pyroar', [62, 50, 58, 73, 54, 72], [86, 68, 72, 109, 66, 106], ['fire', 'normal', 0, 0, 0, 0])
litleo.set_attacks([tackle, ember, headbutt, take_down, fire_fang, flamethrower, crunch, hyper_voice], [leer, amnesia])
flabebe = Stage2('Flabébé', 'Floette', 'Florges', [44, 38, 39, 61, 79, 42], [54, 45, 47, 75, 98, 52], [78, 65, 68, 112, 154, 75], ['fairy', 0, 0, 0, 0, 0])
flabebe.set_attacks([disarming_voice, magical_leaf, petal_blizzard, moonblast, vine_whip, fairy_wind, razor_leaf], [])
skiddo = Stage1('Skiddo', 'Gogoat', [66, 65, 48, 62, 57, 52], [123, 100, 62, 97, 81, 68], ['grass', '', 0, 0, 0, 0])
skiddo.set_attacks([aerial_ace, earthquake, tackle, vine_whip, razor_leaf, take_down, bulldoze, seed_bomb, double_edge, leaf_blade], [growth, tail_whip, bulk_up])
pancham = Stage1('Pancham', 'Pangoro', [67, 82, 62, 46, 48, 43], [95, 124, 78, 69, 71, 58], ['fighting', 'dark', 0, 0, 0, 0])
pancham.set_attacks([hammer_arm, tackle, karate_chop, slash, body_slam, crunch, arm_thrust, bullet_punch], [leer])
furfrou = Basic('Furfrou', [75, 80, 60, 65, 90, 102], ['normal', '', 0, 0, 0, 0])
furfrou.set_attacks([tackle, headbutt, bite, take_down], [growl, tail_whip, babydoll_eyes, charm, sand_attack, cotton_guard])
espurr = Stage1('Espurr', 'Meowstic', [62, 48, 54, 63, 60, 68], [74, 48, 76, 83, 81, 104], ['psychic', '', 0, 0, 0, 0])
espurr.set_attacks([scratch, confusion, psybeam, disarming_voice, psychic, extrasensory], [leer, charm])
honedge = Stage2('Honedge', 'Doublade', 'Aegislash', [45, 80, 100, 35, 37, 28], [59, 110, 150, 45, 49, 35], [60, 50, 150, 50, 150, 60], ['steel', 'ghost', 0, 0, 0, 0])
honedge.set_attacks([furry_cutter, pursuit, shadow_sneak, slash, night_slash, iron_head, aerial_ace, head_smash], [iron_defense, swords_dance])
spritzee = Stage1('Spritzee', 'Aromatisse', [78, 52, 60, 63, 65, 23], [101, 72, 72, 99, 89, 29], ['fairy', '', 0, 0, 0, 0])
spritzee.set_attacks([fairy_wind, moonblast, psychic, disarming_voice], [calm_mind, charm, sweet_scent])
swirlix = Stage1('Swirlix', 'Slurpuff', [62, 48, 66, 59, 57, 49], [82, 80, 86, 85, 75, 72], ['fairy', '', 0, 0, 0, 0])
swirlix.set_attacks([tackle, fairy_wind, play_rough, energy_ball], [fake_tears, cotton_guard, play_nice, sweet_scent])
inkay = Stage1('Inkay', 'Malamar', [53, 54, 53, 37, 46, 45], [86, 92, 88, 68, 75, 73], ['dark', 'psychic', 0, 0, 0, 0])
inkay.set_attacks([tackle, peck, psybeam, payback, slash, night_slash, superpower], [swagger])
binacle = Stage1('Binacle', 'Barbaracle', [42, 52, 67, 39, 56, 50], [72, 105, 115, 54, 86, 68], ['rock', 'water', 0, 0, 0, 0])
binacle.set_attacks([stone_edge, scratch, water_gun, slash, ancient_power, furry_cutter, night_slash, cross_chop, mud_slap, razor_shell], [withdraw, sand_attack, hone_claws])
skrelp = Stage1('Skrelp', 'Dragalge', [50, 60, 60, 60, 60, 30], [65, 75, 90, 97, 123, 44], ['poison', 'dragon', 0, 0, 0, 0])
skrelp.set_attacks([twister, tackle, water_gun, feint_attack, bubble, acid, water_pulse, aqua_tail, hydro_pump, dragon_pulse, sludge_bomb], [tail_whip, double_team, smokescreen])
clauncher = Stage1('Clauncher', 'Clawitzer', [50, 53, 62, 58, 63, 44], [71, 73, 88, 120, 89, 59], ['water', '', 0, 0, 0, 0])
clauncher.set_attacks([dark_pulse, dragon_pulse, water_gun, bubble, Bubble_beam, water_pulse, aqua_jet, vice_grip, crabhammer, muddy_water], [swords_dance])
helioptile = Stage1('Helioptile', 'Heliolisk', [44, 38, 33, 61, 43, 70], [62, 55, 52, 109, 94, 109], ['electric', 'normal', 0, 0, 0, 0])
helioptile.set_attacks([quick_attack, thunder, pound, thunder_shock, bulldoze, thunderbolt, mud_slap], [tail_whip, thunder_wave])
tyrunt = Stage1('Tyrunt', 'Tyrantrum', [58, 89, 77, 45, 45, 48], [82, 121, 119, 69, 59, 71], ['rock', 'dragon', 0, 0, 0, 0])
tyrunt.set_attacks([tackle, bite, ancient_power, crunch, dragon_claw, earthquake, stomp, head_smash, rock_slide], [tail_whip, charm])
amaura = Stage1('Amaura', 'Aurorus', [77, 59, 50, 67, 63, 46], [123, 77, 72, 99, 92, 58], ['rock', 'ice', 0, 0, 0, 0])
amaura.set_attacks([powder_snow, rock_throw, icy_wind, take_down, aurora_beam, ancient_power, avalanche, ice_beam, blizzard], [growl, thunder_wave])
sylveon = Stage1('Eevee', 'Sylveon', [55, 55, 50, 45, 65, 55], [95, 65, 65, 110, 130, 60], ['normal', '', 'fairy', 0, 0, 0])
sylveon.set_attacks([bite, tackle, fairy_wind, quick_attack, disarming_voice, moonblast, swift], [tail_whip, growl, babydoll_eyes, charm, sand_attack])
hawlucha = Basic('Hawlucha', [78, 92, 75, 74, 63, 118], ['fighting', 'flying', 0, 0, 0, 0])
hawlucha.set_attacks([tackle, karate_chop, wing_attack, aerial_ace], [feather_dance, swords_dance, hone_claws])
dedenne = Basic('Dedenne', [67, 58, 57, 81, 67, 101], ['electric', 'fairy', 0, 0, 0, 0])
dedenne.set_attacks([tackle, thunder_shock, play_rough, thunder, discharge, charge_beam, nuzzle], [thunder_wave, tail_whip, charm])
carbink = Basic('Carbink', [50, 50, 150, 50, 150, 50], ['rock', 'fairy', 0, 0, 0, 0])
carbink.set_attacks([tackle, rock_throw, ancient_power, power_gem, stone_edge, moonblast], [harden])
goomy = Stage2('Goomy', 'Sliggoo', 'Goodra', [45, 50, 35, 55, 75, 40], [68, 75, 53, 83, 113, 60], [90, 100, 70, 110, 150, 80], ['dragon', '', 0, 0, 0, 0])
goomy.set_attacks([aqua_tail, tackle, bubble, absorb, dragon_breath, body_slam, dragon_pulse, muddy_water, power_whip], [])
klefki = Basic('Klefki', [57, 80, 91, 80, 87, 75], ['steel', 'fairy', 0, 0, 0, 0])
klefki.set_attacks([tackle, astonish, play_rough, mirror_shot], [metal_sound])
phantump = Stage1('Phantump', 'Trevenant', [43, 70, 48, 50, 60, 38], [85, 110, 76, 65, 82, 56], ['ghost', 'grass', 0, 0, 0, 0])
phantump.set_attacks([tackle, astonish, feint_attack, wood_hammer], [confuse_ray, growth, willowisp])
pumpkaboo = Stage1('Pumpkaboo', 'Gourgeist', [49, 66, 70, 44, 55, 51], [65, 90, 122, 58, 75, 84], ['ghost', 'grass', 0, 0, 0, 0])
pumpkaboo.set_attacks([astonish, razor_leaf, bullet_seed, shadow_ball, seed_bomb], [confuse_ray, scary_face])
bergmite = Stage1('Bergmite', 'Avalugg', [55, 69, 85, 32, 35, 28], [95, 117, 184, 44, 46, 28], ['ice', '', 0, 0, 0, 0])
bergmite.set_attacks([body_slam, crunch, tackle, bite, powder_snow, icy_wind, take_down, rapid_spin, avalanche, blizzard, double_edge, ice_ball], [iron_defense, harden])
noibat = Stage1('Noibat', 'Noivern', [40, 30, 35, 45, 40, 55], [85, 70, 80, 97, 80, 123], ['flying', 'dragon', 0, 0, 0, 0])
noibat.set_attacks([tackle, dragon_pulse, hurricane, absorb, gust, bite, wing_attack, air_slash], [screech, supersonic, agility])
rowlet = Stage2('Rowlet', 'Dartrix', 'Decidueye', [68, 55, 55, 50, 50, 42], [78, 75, 75, 70, 70, 52], [78, 107, 75, 100, 100, 70], ['grass', 'flying', 0, 0, 0, 'ghost'])
rowlet.set_attacks([tackle, peck, astonish, razor_leaf, fury_attack, leaf_blade, brave_bird], [growl, nasty_plot, feather_dance])
litten = Stage2('Litten', 'Torracat', 'Incineroar', [45, 65, 40, 60, 40, 70], [65, 85, 50, 80, 50, 90], [95, 115, 90, 80, 90, 60], ['fire', '', 0, 0, 0, 'dark'])
litten.set_attacks([scratch, ember, lick, fire_fang, bite, fury_swipes, flamethrower, flare_blitz, cross_chop], [growl, bulk_up, leer, swagger, scary_face])
popplio = Stage2('Popplio', 'Brionne', 'Primarina', [50, 54, 54, 66, 56, 40], [60, 69, 69, 91, 81, 50], [80, 74, 74, 126, 116, 60], ['water', '', 0, 0, 0, 'fairy'])
popplio.set_attacks([pound, water_gun, disarming_voice, aqua_jet, Bubble_beam, double_slap, hyper_voice, moonblast, hydro_pump], [growl, babydoll_eyes])
pikipek = Stage2('Pikipek', 'Trumbeak', 'Toucannon', [35, 75, 30, 30, 30, 65], [55, 85, 50, 40, 50, 75], [80, 120, 75, 75, 75, 60], ['normal', 'flying', 0, 0, 0, 0])
pikipek.set_attacks([rock_blast, peck, fury_attack, drill_peck, bullet_seed, hyper_voice, rock_smash], [growl, supersonic, screech, feather_dance])
yungoos = Stage1('Yungoos', 'Gumshoos', [48, 70, 30, 30, 30, 45], [88, 110, 60, 55, 60, 45], ['normal', '', 0, 0, 0, 0])
yungoos.set_attacks([tackle, pursuit, bite, take_down, crunch, hyper_fang, mud_slap], [leer, sand_attack, scary_face])
grubbin = Stage2('Grubbin', 'Charjabug', 'Vikavolt', [47, 62, 45, 55, 45, 46], [57, 82, 95, 55, 75, 36], [77, 70, 90, 145, 75, 43], ['bug', '', 0, 'electric', 0, 'electric'])
grubbin.set_attacks([thunderbolt, air_slash, bite, bug_bite, spark, bug_buzz, zap_cannon, crunch, xscissor, discharge, vice_grip, mud_slap], [iron_defense, agility, string_shot])
crabrawler = Stage1('Crabrawler', 'Crabominable', [47, 82, 57, 42, 47, 63], [97, 132, 77, 62, 67, 43], ['fighting', '', 0, 'ice', 0, 0])
crabrawler.set_attacks([ice_punch, bubble, pursuit, Bubble_beam, avalanche, dynamic_punch, close_combat, payback, dizzy_punch, rock_smash, crabhammer], [leer, iron_defense])
oricorio_baile = Basic('B-Oricorio', [75, 70, 70, 98, 70, 93], ['fire', 'flying', 0, 0, 0, 0])
oricorio_baile.set_attacks([pound, peck, double_slap, air_slash, hurricane], [growl, feather_dance, agility, teeter_dance])
oricorio_pompom = Basic('P-Oricorio', [75, 70, 70, 98, 70, 93], ['electric', 'flying', 0, 0, 0, 0])
oricorio_pompom.set_attacks([pound, peck, double_slap, air_slash, hurricane], [growl, feather_dance, agility, teeter_dance])
oricorio_pau = Basic('Pa-Oricorio', [75, 70, 70, 98, 70, 93], ['psychic', 'flying', 0, 0, 0, 0])
oricorio_pau.set_attacks([pound, peck, double_slap, air_slash, hurricane], [growl, feather_dance, agility, teeter_dance])
oricorio_sensu = Basic('S-Oricorio', [75, 70, 70, 98, 70, 93], ['ghost', 'flying', 0, 0, 0, 0])
oricorio_sensu.set_attacks([pound, peck, double_slap, air_slash, hurricane], [growl, feather_dance, agility, teeter_dance])
cutiefly = Stage1('Cutiefly', 'Ribombee', [40, 45, 40, 55, 40, 84], [60, 55, 60, 95, 70, 124], ['bug', 'fairy', 0, 0, 0, 0])
cutiefly.set_attacks([absorb, fairy_wind, silver_wind, bug_buzz, dazzling_gleam], [stun_spore, quilver_dance, sweet_scent])
rockruff = Stage1('Rockruff', 'Lycanroc', [45, 65, 40, 30, 40, 60], [75, 115, 65, 55, 65, 112], ['rock', '', 0, 0, 0, 0])
rockruff.set_attacks([quick_attack, tackle, bite, rock_throw, crunch, stone_edge, rock_climb, rock_slide, rock_tomb], [leer, sand_attack, howl, scary_face])
wishiwashi = Basic('Wishiwashi', [45, 20, 20, 25, 25, 40], ['water', '', 0, 0, 0, 0])
wishiwashi.set_attacks([water_gun, feint_attack, brine, take_down, aqua_tail, double_edge, hydro_pump], [growl])
mareanie = Stage1('Mareanie', 'Toxapex', [50, 53, 62, 43, 52, 45], [50, 63, 152, 53, 142, 35], ['poison', 'water', 0, 0, 0, 0])
mareanie.set_attacks([poison_sting, bite, peck, venoshock, poison_jab, pin_missile, spike_cannon], [])
mudbray = Stage1('Mudbray', 'Mudsdale', [70, 100, 70, 45, 55, 45], [100, 125, 100, 55, 85, 35], ['ground', '', 0, 0, 0, 0])
mudbray.set_attacks([bulldoze, double_kick, earthquake, superpower, stomp, mega_kick, mud_slap], [iron_defense])
dewpider = Stage1('Dewpider', 'Araquanid', [38, 40, 52, 40, 72, 27], [68, 70, 92, 50, 132, 42], ['water', 'bug', 0, 0, 0, 0])
dewpider.set_attacks([bubble, bug_bite, Bubble_beam, bite, crunch, leech_life], [])
fomantis = Stage1('Fomantis', 'Lurantis', [40, 55, 35, 50, 35, 35], [70, 105, 90, 80, 90, 45], ['grass', '', 0, 0, 0, 0])
fomantis.set_attacks([petal_blizzard, xscissor, razor_leaf, night_slash, furry_cutter, leaf_blade, slash], [growth, sweet_scent])
morelull = Stage1('Morelull', 'Shiinotic', [40, 35, 55, 65, 75, 15], [60, 45, 80, 90, 100, 30], ['grass', 'fairy', 0, 0, 0, 0])
morelull.set_attacks([absorb, astonish, mega_drain, giga_drain, moonblast], [confuse_ray])
salandit = Stage1('Salandit', 'Salazzle', [48, 44, 40, 71, 40, 77], [68, 64, 60, 111, 60, 117], ['poison', 'fire', 0, 0, 0, 0])
salandit.set_attacks([ember, smog, double_slap, flame_burst, venoshock, flamethrower, dragon_pulse], [swagger, poison_gas, nasty_plot, sweet_scent])
stufful = Stage1('Stufful', 'Bewear', [70, 75, 50, 45, 50, 50], [120, 125, 80, 55, 60, 60], ['normal', 'fighting', 0, 0, 0, 0])
stufful.set_attacks([tackle, payback, take_down, hammer_arm, superpower, double_edge], [leer, babydoll_eyes])
bounsweet = Stage2('Bounsweet', 'Steenee', 'Tsareena', [42, 30, 38, 30, 38, 32], [52, 40, 48, 40, 48, 62], [72, 120, 98, 50, 98, 72], ['grass', '', 0, 0, 0, 0])
bounsweet.set_attacks([double_slap, rapid_spin, razor_leaf, magical_leaf, leaf_storm, stomp], [swagger, play_nice, sweet_scent, teeter_dance])
comfey = Basic('Comfey', [51, 52, 90, 82, 110, 100], ['fairy', '', 0, 0, 0, 0])
comfey.set_attacks([vine_whip, magical_leaf, petal_blizzard, play_rough], [growth, sweet_scent])
oranguru = Basic('Oranguru', [90, 60, 80, 90, 110, 60], ['normal', 'psychic', 0, 0, 0, 0])
oranguru.set_attacks([confusion, feint_attack, zen_headbutt, psychic], [nasty_plot, calm_mind])
wimpod = Stage1('Wimpod', 'Golisopod', [25, 35, 40, 20, 30, 80], [75, 125, 140, 60, 90, 40], ['bug', 'water', 0, 0, 0, 0])
wimpod.set_attacks([furry_cutter, bug_bite, slash, pin_missile, rock_smash, razor_shell], [swords_dance, iron_defense, sand_attack])
sandygast = Stage1('Sandygast', 'Palossand', [55, 55, 80, 70, 45, 15], [85, 75, 110, 100, 75, 35], ['ghost', 'ground', 0, 0, 0, 0])
sandygast.set_attacks([absorb, astonish, mega_drain, bulldoze, giga_drain, shadow_ball, earth_power], [harden, iron_defense, sand_attack])
minior = Basic('Pyukumuku', [60, 60, 100, 60, 100, 60], ['rock', 'flying', 0, 0, 0, 0])
minior.set_attacks([tackle, swift, ancient_power, take_down, power_gem, double_edge], [defense_curl, confuse_ray])
komala = Basic('Komala', [65, 115, 65, 75, 95, 65], ['normal', '', 0, 0, 0, 0])
komala.set_attacks([rapid_spin, slam, wood_hammer], [defense_curl])
turtonator = Basic('Turtonator', [60, 78, 135, 91, 85, 36], ['fire', 'dragon', 0, 0, 0, 0])
turtonator.set_attacks([ember, smog, tackle, flamethrower, body_slam, dragon_pulse], [iron_defense])
togedemaru = Basic('Togedemaru', [65, 98, 63, 40, 73, 96], ['electric', 'steel', 0, 0, 0, 0])
togedemaru.set_attacks([tackle, thunder_shock, spark, discharge, pin_missile, nuzzle, wild_charge], [defense_curl])
mimikyu = Basic('Mimikyu', [55, 90, 80, 50, 105, 96], ['ghost', 'fairy', 0, 0, 0, 0])
mimikyu.set_attacks([wood_hammer, scratch, astonish, shadow_sneak, feint_attack, slash, play_rough], [babydoll_eyes, charm, double_team, hone_claws])
bruxish = Basic('Bruxish', [68, 105, 70, 70, 70, 92], ['water', 'psychic', 0, 0, 0, 0])
bruxish.set_attacks([water_gun, confusion, astonish, bite, aqua_jet, crunch, aqua_tail], [])
drampa = Basic('Drampa', [78, 60, 85, 135, 91, 36], ['normal', 'dragon', 0, 0, 0, 0])
drampa.set_attacks([twister, dragon_breath, dragon_pulse, hyper_voice, extrasensory], [glare, play_nice])
dhelmise = Basic('Dhelmise', [70, 131, 100, 86, 90, 40], ['ghost', 'grass', 0, 0, 0, 0])
dhelmise.set_attacks([absorb, rapid_spin, astonish, mega_drain, giga_drain, shadow_ball, slam, energy_ball, power_whip], [growth, metal_sound])
jangmoo = Stage2('Jangmo-o', 'Hakamo-o', 'Kommo-o', [45, 55, 65, 45, 45, 45], [55, 75, 90, 65, 70, 65], [75, 110, 125, 100, 105, 85], ['dragon', '', 0, 'fighting', 0, 'fighting'])
jangmoo.set_attacks([tackle, headbutt, dragon_claw], [leer, screech, iron_defense, dragon_dance, scary_face])

articuno = Legendary('+ Articuno', [90, 85, 100, 95, 125, 85], ['ice', 'flying', 0, 0, 0, 0])
articuno.set_attacks([gust, powder_snow, ice_shard, ancient_power, ice_beam, blizzard, hurricane], [agility])
zapdos = Legendary('+ Zapdos', [90, 90, 85, 125, 90, 100], ['electric', 'flying', 0, 0, 0, 0])
zapdos.set_attacks([peck, thunder_shock, ancient_power, discharge, drill_peck, thunder, zap_cannon], [thunder_wave, agility])
moltres = Legendary('+ Moltres', [90, 100, 90, 125, 85, 90], ['fire', 'flying', 0, 0, 0, 0])
moltres.set_attacks([wing_attack, ember, flamethrower, ancient_power, air_slash, heat_wave, hurricane], [agility])
mewtwo = Legendary('+ Mewtwo', [106, 110, 90, 154, 90, 130], ['psychic', '', 0, 0, 0, 0])
mewtwo.set_attacks([confusion, swift, psycho_cut, psychic], [amnesia])
raikou = Legendary('+ Raikou', [90, 85, 75, 115, 100, 115], ['electric', '', 0, 0, 0, 0])
raikou.set_attacks([discharge, bite, thunder_shock, spark, quick_attack, crunch, thunder, thunder_fang, extrasensory], [leer, calm_mind])
entei = Legendary('+ Entei', [115, 115, 85, 90, 75, 100], ['fire', '', 0, 0, 0, 0])
entei.set_attacks([lava_plume, bite, ember, stomp, flamethrower, fire_blast, fire_fang, extrasensory], [leer, swagger, calm_mind])
suicune = Legendary('+ Suicune', [100, 75, 115, 90, 115, 85], ['water', '', 0, 0, 0, 0])
suicune.set_attacks([Bubble_beam, bite, gust, aurora_beam, ice_fang, extrasensory, hydro_pump, blizzard], [leer, calm_mind])
lugia = Legendary('+ Lugia', [106, 90, 130, 90, 154, 110], ['psychic', 'flying', 0, 0, 0, 0])
lugia.set_attacks([gust, dragon_rush, extrasensory, hydro_pump, ancient_power], [calm_mind])
hooh = Legendary('+ Ho-Oh', [106, 130, 90, 110, 154, 90], ['fire', 'flying', 0, 0, 0, 0])
hooh.set_attacks([gust, brave_bird, extrasensory, fire_blast, ancient_power], [calm_mind])
regirock = Legendary('+ Regirock', [80, 100, 200, 50, 100, 50], ['rock', '', 0, 0, 0, 0])
regirock.set_attacks([stomp, rock_throw, charge_beam, bulldoze, ancient_power, stone_edge, hammer_arm, superpower, zap_cannon], [iron_defense])
regice = Legendary('+ Regice', [80, 50, 100, 100, 200, 50], ['ice', '', 0, 0, 0, 0])
regice.set_attacks([stomp, icy_wind, charge_beam, bulldoze, ancient_power, ice_beam, hammer_arm, superpower, zap_cannon], [])
registeel = Legendary('+ Registeel', [80, 75, 150, 75, 150, 50], ['steel', '', 0, 0, 0, 0])
registeel.set_attacks([stomp, metal_claw, charge_beam, bulldoze, ancient_power, iron_head, hammer_arm, superpower, zap_cannon, flash_cannon], [iron_defense, amnesia])
latias = Legendary('+ Latias', [80, 80, 90, 110, 130, 110], ['dragon', 'psychic', 0, 0, 0, 0])
latias.set_attacks([dragon_breath, zen_headbutt, psychic, dragon_pulse], [charm])
latios = Legendary('+ Latios', [80, 90, 80, 130, 110, 110], ['dragon', 'psychic', 0, 0, 0, 0])
latios.set_attacks([dragon_breath, zen_headbutt, psychic, dragon_pulse], [dragon_dance])
kyogre = Legendary('+ Kyogre', [100, 100, 90, 150, 140, 90], ['water', '', 0, 0, 0, 0])
kyogre.set_attacks([ancient_power, water_pulse, body_slam, aqua_tail, ice_beam, muddy_water, hydro_pump, double_edge], [scary_face, calm_mind])
groudon = Legendary('+ Groudon', [100, 150, 140, 100, 90, 90], ['ground', '', 0, 0, 0, 0])
groudon.set_attacks([ancient_power, mud_shot, earth_power, lava_plume, earthquake, fire_blast, hammer_arm], [scary_face, bulk_up])
rayquaza = Legendary('+ Rayquaza', [105, 150, 90, 150, 90, 95], ['dragon', 'flying', 0, 0, 0, 0])
rayquaza.set_attacks([twister, ancient_power, crunch, air_slash, dragon_pulse, hyper_voice], [scary_face, dragon_dance])
uxie = Legendary('+ Uxie', [75, 75, 130, 75, 130, 95], ['psychic', '', 0, 0, 0, 0])
uxie.set_attacks([confusion, swift, extrasensory], [amnesia])
mesprit = Legendary('+ Mesprit', [80, 105, 105, 105, 105, 80], ['psychic', '', 0, 0, 0, 0])
mesprit.set_attacks([confusion, swift, extrasensory], [charm])
azelf = Legendary('+ Azelf', [75, 125, 70, 125, 70, 115], ['psychic', '', 0, 0, 0, 0])
azelf.set_attacks([confusion, swift, extrasensory], [nasty_plot])
dialga = Legendary('+ Dialga', [100, 120, 120, 150, 100, 90], ['steel', 'dragon', 0, 0, 0, 0])
dialga.set_attacks([dragon_breath, ancient_power, metal_claw, slash, power_gem, dragon_claw, earth_power, iron_tail, flash_cannon], [scary_face])
palkia = Legendary('+ Palkia', [90, 120, 100, 150, 120, 100], ['water', 'dragon', 0, 0, 0, 0])
palkia.set_attacks([dragon_breath, ancient_power, water_pulse, slash, power_gem, dragon_claw, earth_power, aqua_tail, hydro_pump], [scary_face])
heatran = Legendary('+ Heatran', [91, 90, 106, 130, 106, 77], ['fire', 'steel', 0, 0, 0, 0])
heatran.set_attacks([heat_wave, ancient_power, iron_head, fire_fang, crunch, lava_plume, earth_power, stone_edge], [scary_face, metal_sound, leer])
regigigas = Legendary('+ Regigigas', [110, 160, 110, 80, 110, 100], ['normal', '', 0, 0, 0, 0])
regigigas.set_attacks([fire_punch, ice_punch, thunder_punch, dizzy_punch, knock_off, zen_headbutt], [confuse_ray])
giratina = Legendary('+ Giratina', [150, 100, 120, 100, 120, 90], ['ghost', 'dragon', 0, 0, 0, 0])
giratina.set_attacks([dragon_breath, ominous_wind, ancient_power, slash, shadow_sneak, dragon_claw, earth_power, hex], [scary_face])
cresselia = Legendary('+ Cresselia', [120, 70, 120, 75, 130, 85], ['psychic', '', 0, 0, 0, 0])
cresselia.set_attacks([psycho_cut, confusion, aurora_beam, slash, psychic, moonblast], [double_team])
cobalion = Legendary('+ Cobalion', [91, 90, 129, 90, 72, 108], ['steel', 'fighting', 0, 0, 0, 0])
cobalion.set_attacks([close_combat, quick_attack, double_kick, metal_claw, take_down, iron_head], [leer, swords_dance])
terrakion = Legendary('+ Terrakion', [91, 129, 90, 72, 90, 108], ['rock', 'fighting', 0, 0, 0, 0])
terrakion.set_attacks([close_combat, quick_attack, double_kick, rock_slide, take_down, stone_edge], [leer, swords_dance])
virizion = Legendary('+ Virizion', [91, 90, 72, 90, 129, 108], ['grass', 'fighting', 0, 0, 0, 0])
virizion.set_attacks([close_combat, quick_attack, double_kick, leaf_blade, take_down, magical_leaf, giga_drain], [leer, swords_dance])
tornadus = Legendary('+ Tornadus', [79, 115, 70, 125, 80, 111], ['flying', '', 0, 0, 0, 0])
tornadus.set_attacks([hammer_arm, hurricane, astonish, gust, bite, extrasensory, air_slash, crunch, dark_pulse], [swagger, agility])
thundurus = Legendary('+ Thundurus', [79, 115, 70, 125, 80, 111], ['electric', 'flying', 0, 0, 0, 0])
thundurus.set_attacks([astonish, thunder_shock, discharge, bite, hammer_arm, thunder, crunch, dark_pulse], [nasty_plot, swagger, agility])
landorus = Legendary('+ Landorus', [89, 125, 90, 115, 80, 101], ['ground', 'flying', 0, 0, 0, 0])
landorus.set_attacks([hammer_arm, mud_shot, rock_tomb, bulldoze, rock_throw, extrasensory, earth_power, earthquake, rock_slide, stone_edge], [swords_dance])
reshiram = Legendary('+ Reshiram', [100, 120, 100, 150, 120, 90], ['dragon', 'fire', 0, 0, 0, 0])
reshiram.set_attacks([fire_fang, ancient_power, flamethrower, dragon_breath, slash, extrasensory, dragon_pulse, crunch, fire_blast, hyper_voice], [])
zekrom = Legendary('+ Zekrom', [100, 150, 120, 120, 100, 90], ['dragon', 'electric', 0, 0, 0, 0])
zekrom.set_attacks([thunder_fang, ancient_power, thunderbolt, dragon_breath, slash, zen_headbutt, dragon_claw, crunch, thunder, hyper_voice], [])
kyurem = Legendary('+ Kyurem', [125, 130, 90, 130, 90, 95], ['dragon', 'ice', 0, 0, 0, 0])
kyurem.set_attacks([icy_wind, ancient_power, ice_beam, dragon_breath, slash, blizzard, dragon_pulse, hyper_voice], [scary_face])
xerneas = Legendary('+ Xerneas', [126, 131, 95, 131, 98, 99], ['fairy', '', 0, 0, 0, 0])
xerneas.set_attacks([take_down, aurora_beam, moonblast, megahorn, night_slash, close_combat], [])
yveltal = Legendary('+ Yveltal', [126, 131, 95, 131, 98, 99], ['dark', 'flying', 0, 0, 0, 0])
yveltal.set_attacks([hurricane, air_slash, dark_pulse, psychic, dragon_rush], [double_team])
zygarde = Legendary('+ Zygarde', [108, 100, 121, 81, 95, 95], ['dragon', 'ground', 0, 0, 0, 0])
zygarde.set_attacks([bulldoze, dragon_breath, bite, crunch, earthquake, dragon_pulse], [glare, coil])
tapu_koko = Legendary('+ Tapu Koko', [70, 115, 85, 95, 75, 130], ['electric', 'fairy', 0, 0, 0, 0])
tapu_koko.set_attacks([brave_bird, quick_attack, thunder_shock, spark, wild_charge, discharge], [withdraw, screech, agility])
tapu_lele = Legendary('+ Tapu Lele', [70, 85, 75, 130, 115, 95], ['psychic', 'fairy', 0, 0, 0, 0])
tapu_lele.set_attacks([astonish, confusion, psybeam, extrasensory, moonblast], [withdraw, sweet_scent, tickle])
tapu_bulu = Legendary('+ Tapu Bulu', [70, 130, 115, 85, 95, 75], ['grass', 'fairy', 0, 0, 0, 0])
tapu_bulu.set_attacks([wood_hammer, superpower, horn_attack, giga_drain, zen_headbutt, megahorn], [withdraw, scary_face])
tapu_fini = Legendary('+ Tapu Fini', [70, 75, 115, 95, 130, 85], ['water', 'fairy', 0, 0, 0, 0])
tapu_fini.set_attacks([moonblast, water_gun, water_pulse, brine, muddy_water, hydro_pump], [withdraw, defog])
solgaleo = Legendary('+ Solgaleo', [137, 137, 107, 113, 89, 97], ['psychic', 'steel', 0, 0, 0, 0])
solgaleo.set_attacks([wakeup_slap, metal_claw, iron_head, zen_headbutt, flash_cannon, crunch, flare_blitz], [metal_sound, cosmic_power])
lunala = Legendary('+ Lunala', [137, 113, 89, 137, 107, 97], ['psychic', 'ghost', 0, 0, 0, 0])
lunala.set_attacks([confusion, air_slash, shadow_ball, moonblast], [cosmic_power, confuse_ray])
necrozma = Legendary('+ Necrozma', [97, 107, 101, 127, 89, 79], ['psychic', '', 0, 0, 0, 0])
necrozma.set_attacks([charge_beam, metal_claw, mirror_shot, confusion, slash, rock_blast, night_slash, power_gem, psycho_cut], [iron_defense])



legend1 = random.choice(legends)
legends.remove(legend1)
legend2 = random.choice(legends)
legends.remove(legend2)

for i in (legend1, legend2):
    if i.type1 in ['normal', 'flying', 'fairy']:
        white_spawn.append(i)
    elif i.type1 in ['fire', 'dark']:
        orange_spawn.append(i)
    elif i.type1 in ['poison', 'psychic', 'ghost']:
        purple_spawn.append(i)
    elif i.type1 in ['rock', 'steel']:
        gray_spawn.append(i)
    elif i.type1 in ['electric', 'ice']:
        yellow_spawn.append(i)
    elif i.type1 in ['water']:
        blue_spawn.append(i)
    elif i.type1 in ['grass', 'bug']:
        green_spawn.append(i)
    elif i.type1 in ['ground', 'dragon', 'fighting']:
        brown_spawn.append(i)