import pygame
from fields import *
from mons import *

player_list = []
class Player:
    def __init__(self, color):
        self.pos = [field158]
        self.now_on = field158
        self.color = color
        self.mons = []
        self.inventory = []
        self.backpack = []
        self.z_moves = []
        self.badge_case = []
        self.zmove_used = False
        self.alive = 0
        self.mega_count = 0
        self.lvl = 0
        player_list.append(self)
        

    def draw_player(self):
        pygame.draw.rect(SCREEN, (self.color), (self.now_on.center[0]-10, self.now_on.center[1]-10, 25,25))

    def draw_fight_mon(self, pos):
        self.alive = 0
        if len(self.mons) > 5:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 5:
                    self.alive = 0
                    return 0

        elif len(self.mons) > 4:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 4:
                    self.alive = 0
                    return 0

        elif len(self.mons) > 3:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 3:
                    self.alive = 0
                    return 0

        elif len(self.mons) > 2:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 2:
                    self.alive = 0
                    return 0

        elif len(self.mons) > 1:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 1:
                    self.alive = 0
                    return 0

        elif len(self.mons) > 0:
            while True:
                i = self.alive
                self.active_mon = self.mons[i]
                if self.active_mon.hp > 0:
                    self.mons[i].draw_attack_card(self, pos)
                    break
                else:
                    self.alive += 1
                if self.alive > 0:
                    self.alive = 0
                    return 0
  
        else:
            return True  
            
     
class NPC:
    def __init__(self):
        self.mons = []
        self.pos = []
        
        
Player1 = Player((255,0,0))
Player2 = Player((0,0,255))

npc = NPC()
