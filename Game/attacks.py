import pygame
import random
pygame.init()

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)

FONT_attacks = pygame.font.Font('fonts/AntipastoPro_trial.ttf', 30)
FONT_number = pygame.font.Font('fonts/Regus-Brown.ttf', 30)

turn_count = 0

attack_color = {
    'normal': (168, 168, 120),
    'fire': (240, 128, 48),
    'water': (104, 144, 240),
    'grass': (120, 200, 80),
    'electric': (248, 208, 48),
    'ice': (152, 216, 216),
    'fighting': (192, 48, 40),
    'poison': (160, 64, 160),
    'ground': (224, 192, 104),
    'flying': (168, 144, 240),
    'psychic': (248, 88, 136),
    'bug': (168, 184, 32),
    'rock': (184, 160, 56),
    'ghost': (112, 88, 152),
    'dragon': (112, 56, 248),
    'dark': (112, 88, 72),
    'steel': (184, 184, 208),
    'fairy': (238, 153, 172)
}


list_of_attacks = []

class Attack:
    def __init__(self, name, type, sp_atk, dmg, acc, effect):
        self.name = name
        self.type = type
        self.sp_atk = sp_atk
        self.dmg = dmg
        self.acc = acc
        self.effect = effect
        self.color = attack_color[self.type]
        list_of_attacks.append(self)

        self.hit_number = 1
        self.multiplier = 1
        self.heal_multiplier = 0
        self.selfhit_multiplier = 0


    def hit(self, mon, enemy):
        if self.acc == 0:
            return 1
            
        elif random.randrange(0,100) < (self.acc*acc_stage_dict[mon.acc_stage]*evasion_stage_dict[enemy.evasion_stage]):
            return 1
        else:
            return 0
        
class ZMove:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.dmg = 70
        self.acc = 100

        self.hit_number = 1
        self.multiplier = 1
        self.heal_multiplier = 0
        self.selfhit_multiplier = 0
    
    def hit(self, mon, enemy):
        if self.acc == 0:
            return 1
            
        elif random.randrange(0,100) < (self.acc*acc_stage_dict[mon.acc_stage]*evasion_stage_dict[enemy.evasion_stage]):
            return 1
        else:
            return 0


def attacks_guide():
    list_of_attacks.sort(key=lambda x: x.name)
    turnoff_guide = pygame.image.load('pictures/maps/back_arrow.png')
    turnoff_guide_rect = pygame.Rect(0,0,100,100)
    guide = True
    posy = 140
    add_pos = 0
    while guide == True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if turnoff_guide_rect.collidepoint(mouse_pos):
                    guide = False
                    break    
                if event.button == 5:
                    posy -= 40
                if event.button == 4:
                    posy += 40
                    if posy >= 140:
                        posy = 140
            
        SCREEN.fill((0,0,0))    
        add_pos = 0
        for i in list_of_attacks:
            text_name = FONT_attacks.render(i.name, True, (i.color))
            SCREEN.blit(text_name, (10, add_pos+posy+2))
            text_type = FONT_attacks.render(i.type, True, (i.color))
            SCREEN.blit(text_type, (210, posy+add_pos+2))
            text_class = FONT_attacks.render(i.sp_atk, True, (i.color))
            SCREEN.blit(text_class, (310, posy+add_pos+2))
            text_power = FONT_number.render(str(i.dmg), True, (i.color))
            SCREEN.blit(text_power, (415, posy+add_pos+2))
            text_acc = FONT_number.render(str(i.acc), True, (i.color))
            SCREEN.blit(text_acc, (460, posy+add_pos+2))
            text_effect = FONT_number.render(i.effect, True, (i.color))
            SCREEN.blit(text_effect, (525, posy+add_pos+2))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(0, posy+add_pos, 2000, 1))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(205, 0, 1, 4000))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(305, 0, 1, 4000))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(410, 0, 1, 4000))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(455, 0, 1, 4000))
            pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(520, 0, 1, 4000))
            add_pos += 30

        pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(0,0,2000,130))
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(0,100,2000,1))
        pygame.draw.rect(SCREEN, (255,255,255), turnoff_guide_rect)
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(205, 100, 1, 30))
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(305, 100, 1, 30))
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(410, 100, 1, 30))
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(455, 100, 1, 30))
        pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(520, 100, 1, 30))
        SCREEN.blit(turnoff_guide, (0,0))
        text_title_name = FONT_attacks.render('Name', True, (0,0,0))
        text_title_type = FONT_attacks.render('Type', True, (0,0,0))
        text_title_class = FONT_attacks.render('Class', True, (0,0,0))
        text_title_power = FONT_attacks.render('Att', True, (0,0,0))
        text_title_acc = FONT_attacks.render('Acc', True, (0,0,0))
        text_title_effect = FONT_attacks.render('Effect', True, (0,0,0))
        SCREEN.blit(text_title_name, (10, 105))
        SCREEN.blit(text_title_type, (210, 105))
        SCREEN.blit(text_title_class, (310, 105))
        SCREEN.blit(text_title_power, (415, 105))
        SCREEN.blit(text_title_acc, (460, 105))
        SCREEN.blit(text_title_effect, (525, 105))
        pygame.display.update()

  
razor_leaf = Attack('Razor Leaf', 'grass', 'physical', 55, 95, '-')
tackle = Attack('Tackle', 'normal', 'physical', 40, 100, '-')
flamethrower = Attack('Flamethrower', 'fire', 'special', 90, 100, 'Has a 10% chance to burn the target')
petal_blizzard = Attack('Petal Blizzard', 'grass', 'physical', 90, 100, '-')
scratch = Attack('Scratch', 'normal', 'physical', 40, 100, '-')
ember = Attack('Ember', 'fire', 'special', 40, 100, 'Has a 10% chance to burn the target')
fire_fang = Attack('Fire Fang', 'fire', 'special', 65, 95, 'Has a 10% chance to burn the target and a 10% chance to make the target flinch')
flame_burst = Attack('Flame Burst', 'fire', 'special', 70, 100, '-')
slash = Attack('Slash', 'normal', 'physical', 70, 100, '-')
wing_attack = Attack('Wing Attack', 'flying', 'physical', 60, 100, '-')
dragon_claw = Attack('Dragon Claw', 'dragon', 'physical', 80, 100, '-')
air_slash = Attack('Air Slash', 'flying', 'special', 75, 95, 'Has a 30% chance to make the target flinch')
water_gun = Attack('Water Gun', 'water', 'special', 40, 100, '-')
bubble = Attack('Bubble', 'water', 'special', 40, 100, 'Has a 10% chance to lower the target´s Speed by one stage')
bite = Attack('Bite', 'dark', 'physical', 60, 100, 'Has a 30% chance to make the target flinch')
water_pulse = Attack('Water Pulse', 'water', 'special', 60, 100, 'Has a 20% chance to confuse the target')
dizzy_punch = Attack('Dizzy Punch', 'normal', 'physical', 70, 100, 'Has a 20% chance to confuse the target')
rapid_spin = Attack('Rapid Spin', 'normal', 'physical', 50, 100, '-')
aqua_tail = Attack('Aqua Tail', 'water', 'physical', 90, 90, '-')
flash_cannon = Attack('Flash Cannon', 'steel', 'special', 80, 100, 'Has a 10% chance to lower the target´s Sp.Def by one stage')
bug_bite = Attack('Bug Bite', 'bug', 'physical', 60, 100, '-')
confusion = Attack('Confusion', 'psychic', 'special', 50, 100, 'Has a 10% chance to confuse the target')
gust = Attack('Gust', 'flying', 'special', 40, 100, '-')
psybeam = Attack('Psybeam', 'psychic', 'special', 65, 100, 'Has a 10% chance to confuse the target')
silver_wind = Attack('Silver Wind', 'bug', 'special', 60, 100, 'Has a 10% chance to raise all of the user´s stats by one stage')
ominous_wind = Attack('Ominous Wind', 'ghost', 'special', 60, 100, 'Has a 10% chance to raise all of the user´s stats by one stage')
bug_buzz = Attack('Bug Buzz', 'bug', 'special', 90, 100, 'Has a 10% chance to lover the target´s Sp.Def by one stage')
poison_sting = Attack('Poison Sting', 'poison', 'physical', 15, 100, 'Has a 30% chance to poison the target')
twineedle = Attack('Twineedle', 'bug', 'physical', 25, 100, 'Hits twice. Has a 20% chance to poison the target')
pursuit = Attack('Pursuit', 'dark', 'physical', 40, 100, '-')
venoshock = Attack('Venoshock', 'poison', 'special', 65, 100, 'Inflicts double damage if the target is Poisoned')
quick_attack = Attack('Quick Attack', 'normal', 'physical', 40, 100, '-')
twister = Attack('Twister', 'dragon', 'special', 40, 100, 'Has a 20% chance to make the target flinch')
rock_slide = Attack('Rock_slide', 'rock', 'physical', 75, 90, 'Has a 30% chance to make the target flinch')
hurricane = Attack('Hurricane', 'flying', 'special', 110, 70, 'Has a 30% chance to confuse the target')
crunch = Attack('Crunch', 'dark', 'physical', 80, 100, 'Has a 20% chance to lower the target´s Def by one stage')
razor_shell = Attack('Razor Shell', 'water', 'physical', 75, 95, 'Has a 50% chance to lower the target´s Def by one stage')
rock_smash = Attack('Rock Smash', 'fighting', 'physical', 40, 100, 'Has a 50% chance to lower the target´s Def by one stage')
hyper_fang = Attack('Hyper Fang', 'normal', 'physical', 80, 90, 'Has a 10% chance to make the target flinch')
peck = Attack('Peck', 'flying', 'physical', 35, 100, '-')
aerial_ace = Attack('Aerial Ace', 'flying', 'physical', 60, 0, '-')
drill_run = Attack('Drill Run', 'ground', 'physical', 80, 95, '-')
acid = Attack('Acid', 'poison', 'special', 40, 100, 'Has a 10% chance to lower the target´s Sp.Def by one stage')
ice_fang = Attack('Ice Fang', 'ice', 'physical', 65, 95, 'Has a 10% chance to freeze the target and a 10% chance to make the target flinch')
thunder_fang = Attack('Thunder Fang', 'electric', 'atk', 65, 95, 'Has a 10% chance to paralyze the target and a 10% chance to make the target flinch')
mud_bomb = Attack('Mud Bomb', 'ground', 'special', 65, 85, '-')
thunder_shock = Attack('Thunder Shock', 'electric', 'special', 40, 100, 'Has a 10% chance tu paralyze the target')
spark = Attack('Spark', 'electric', 'physical', 65, 100, 'Has a 30% chance to paralyze the target')
discharge = Attack('Discharge', 'electric', 'special', 80, 100, 'Has a 30% chance to paralyze the target')
thunderbolt = Attack('Thunderbolt', 'electric', 'special', 90, 100, 'Has a 10% chance to paralyze the target')
furry_cutter = Attack('Fury Cutter', 'bug', 'physical', 40, 95, 'Power doubles every turn (max 4 turns)')
ice_ball = Attack('Ice Ball', 'ice', 'physical', 30, 90, 'Power doubles every turn (max 4 turns)')
swift = Attack('Swift', 'normal', 'special', 60, 0, '-')
earthquake = Attack('Earthquake', 'ground', 'physical', 100, 100, '-')
poison_fang = Attack('Poison Fang', 'poison', 'physical', 50, 100, 'Has a 50% chance to poison the target')
body_slam = Attack('Body Slam', 'normal', 'physical', 85, 100, 'Has a 30% chance to paralyze the target')
superpower = Attack('Superpower', 'fighting', 'physical', 120, 100, 'Lowers the user´s Att and Def by one stage')
horn_attack = Attack('Horn Attack', 'normal', 'physical', 65, 100, '-')
earth_power = Attack('Earth Power', 'ground', 'special', 90, 100, 'Has a 10% chance to lover the target´s Sp.Def by one stage')
megahorn = Attack('Megahorn', 'bug', 'physical', 120, 85, '-')
wakeup_slap = Attack('Wake-Up Slap', 'fighting', 'physical', 70, 100, '-')
moonblast = Attack('Moonblast', 'fairy', 'special', 95, 100, 'Has a 30% chance to lower the target´s Sp.Att by one stage')
pound = Attack('Pound', 'normal', 'physical', 40, 100, '-')
payback = Attack('Payback', 'dark', 'physical', 50, 100, 'Power is doubled if target is faster')
hex = Attack('Hex', 'ghost', 'special', 65, 100, 'Has double power if target is burned or poisoned')
fire_blast = Attack('Fire Blast', 'fire', 'special', 110, 85, 'Has a 10% chance to burn the target')
disarming_voice = Attack('Disarming Voice', 'fairy', 'special', 40, 0, '-')
hyper_voice = Attack('Hyper Voice', 'normal', 'special', 90, 100, '-')
astonish = Attack('Astonish', 'ghost', 'physical', 30, 100, 'Has a 30% chance to make the target flinch')
steamroller = Attack('Steamroller', 'bug', 'physical', 65, 100, 'Has a 30% chance to make the target flinch')
leech_life = Attack('Leech Life', 'bug', 'physical', 80, 100, 'Drains half the damage inflicted to healthe user')
giga_drain = Attack('Giga Drain', 'grass', 'special', 75, 100, 'Drains half the damage inflicted to healthe user')
xscissor = Attack('X-Scissor', 'bug', 'physical', 80, 100, '-')
psychic = Attack('Psychic', 'psychic', 'special', 90, 100, 'Has a 10% chance to lower the target´s Sp.Def by one stage')
signal_beam = Attack('Signal Beam', 'bug', 'special', 75, 100, 'Has a 10% chance to confuse the target')
bulldoze = Attack('Bulldoze', 'ground', 'physical', 60, 100, 'Has a 100% chance to lower the target´s Speed by one stage')
feint_attack = Attack('Feint Attack', 'dark', 'physical', 60, 0, '-')
zen_headbutt = Attack('Zen Headbutt', 'psychic', 'physical', 80, 90, 'Has a 20% chance to make the target flinch')
aqua_jet = Attack('Aqua Jet', 'water', 'physical', 40, 100, '-')
karate_chop = Attack('Karate Chop', 'fighting', 'physical', 50, 100, '-')
mach_punch = Attack('Mach Punch', 'fighting', 'physical', 40, 100, '-')
cross_chop = Attack('Cross Chop', 'fighting', 'physical', 100, 80, '-')
Bubble_beam = Attack('Bubble Beam', 'water', 'special', 65, 100, 'Has a 10% chance to lower the target´s Speed by one stage')
mud_shot = Attack('Mud Shot', 'ground', 'special', 55, 95, 'Has a 100% chance to lower the target´s Speed by one stage')
dynamic_punch = Attack('Dynamic Punch', 'fighting', 'physical', 100, 50, 'Has a 100% chance to confuse the target')
psycho_cut = Attack('Psycho Cut', 'psychic', 'physical', 70, 100, '-')
slam = Attack('Slam', 'normal', 'physical', 80, 75, '-')
leaf_blade = Attack('Leaf Blade', 'grass', 'physical', 90, 100, '-')
brine = Attack('Brine', 'water', 'special', 65, 100, 'Double damage if the target has less than half theit max HP remaining')
sludge_wave = Attack('Sludge Wave', 'poison', 'special', 95, 100, 'Has a 10% chance to poison the target')
sludge_bomb = Attack('Sludge Bomb', 'poison', 'special', 90, 100, 'Has a 30% chance to poison the target')
rock_throw = Attack('Rock Throw', 'rock', 'physical', 50, 90, '-')
stone_edge = Attack('Stone Edge', 'rock', 'physical', 100, 80, '-')
headbutt = Attack('Headbutt', 'normal', 'physical', 70, 100, 'Has a 30% chance to make the target flinch')
zap_cannon = Attack('Zap Cannon', 'electric', 'special', 120, 50, 'Has a 100% chance to paralyze the target')
night_slash = Attack('Night Slash', 'dark', 'physical', 70, 100, '-')
drill_peck = Attack('Drill Peck', 'flying', 'physical', 80, 100, '-')
icy_wind = Attack('Icy Wind', 'ice', 'special', 55, 95, 'Has a 100% chance to lower the target´s Speed by one stage')
ice_shard = Attack('Ice Shard', 'ice', 'physical', 40, 100, '-')
ice_beam = Attack('Ice Beam', 'ice', 'special', 90, 100, 'Has a 10% chance to freeze the target')
sludge = Attack('Sludge', 'poison', 'special', 65, 100, 'Has a 30% chance to poison the target')
lick = Attack('Lick', 'ghost', 'physical', 30, 100, 'Has a 30% chance to paralyze the target')
shadow_ball = Attack('Shadow Ball', 'ghost', 'special', 80, 100, 'Has a 20% chance to lower the target´s Sp.Def by one stage')
dark_pulse = Attack('Dark Pulse', 'dark', 'special', 80, 100, 'Has a 20% chance to make the target flinch')
shadow_punch = Attack('Shadow Punch', 'ghost', 'physical', 60, 0, '-')
dragon_breath = Attack('Dragon Breath', 'dragon', 'special', 60, 100, 'Has a 30% chance to paralyze the target')
iron_tail = Attack('Iron Tail', 'steel', 'physical', 100, 75, 'Has a 30% chance to lower the target´s Def by one stage')
metal_claw = Attack('Metal Claw', 'steel', 'physical', 50, 95, 'Has a 10% chance to raise the user´s Att by one stage')
seed_bomb = Attack('Seed Bomb', 'grass', 'physical', 80, 100, '-')
bone_club = Attack('Bone Club', 'ground', 'physical', 65, 85, 'Has a 10% chance to make the target flinch')
hammer_arm = Attack('Hammer Arm', 'fighting', 'physical', 100, 90, 'Lowers user´s Speed by one stage')
egg_bomb = Attack('Egg Bomb', 'normal', 'physical', 100, 75, '-')
ancient_power = Attack('Ancient Power', 'rock', 'special', 60, 100, 'Has a 10% chance to raise all of the user´s stats by one stage')
dragon_pulse = Attack('Dragon Pulse', 'dragon', 'special', 85, 100, '-')
magical_leaf = Attack('Magical Leaf', 'grass', 'special', 60, 0, '-')
powder_snow = Attack('Powder Snow', 'ice', 'special', 40, 100, 'Has a 10% chance to freeze the target')
blizzard = Attack('Blizzard', 'ice', 'special', 110, 70, 'Has a 10% chance to freeze the target')
avalanche = Attack('Avalanche', 'ice', 'physical', 60, 100, 'Double damage if the target is faster')
thunder = Attack('Thunder', 'electric', 'special', 110, 70, 'Has a 30% chance to paralyze the target')
brick_break = Attack('Brick Break', 'fighting', 'physical', 75, 100, '-')
iron_head = Attack('Iron Head', 'steel', 'physical', 80, 100, 'Has a 30% chance to make the target flinch')
needle_arm = Attack('Needle Arm', 'grass', 'physical', 60, 100, 'Has a 30% chance to make the target flinch')
play_rough = Attack('Play Rough', 'fairy', 'physical', 90, 90, 'Has a 10% chance to lower the target´s Att by one stage')
hydro_pump = Attack('Hydro Pump', 'water', 'special', 110, 80, '-')
vine_whip = Attack('Vine Whip', 'grass', 'physical', 45, 100, '-')
fairy_wind = Attack('Fairy Wind', 'fairy', 'special', 40, 100, '-')
leaf_tornado = Attack('Leaf Tornado', 'grass', 'special', 65, 90, '-')
leaf_storm = Attack('Leaf Storm', 'grass', 'special', 130, 90, 'Lowers the user´s Sp.Att by two stages')
poison_jab = Attack('Poison Jab', 'poison', 'physical', 80, 100, 'Has a 30% chance to poison the target')
shadow_sneak = Attack('Shadow Sneak', 'ghost', 'physical', 40, 100, '-')
fire_punch = Attack('Fire Punch', 'fire', 'physical', 75, 100, 'Has a 10% chance to burn the target')
ice_punch = Attack('Ice Punch', 'ice', 'physical', 75, 100, 'Has a 10% chance to freeze the target')
thunder_punch = Attack('Thunder Punch', 'electric', 'physical', 75, 100, 'Has a 10% chance to paralyze the target')
icicle_crash = Attack('Icicle Crash', 'ice', 'physical', 85, 90, 'Has a 30% chance to make the target flinch')
dazzling_gleam = Attack('Dazzling Gleam', 'fairy', 'special', 80, 100, '-')
flame_wheel = Attack('Flame Wheel', 'fire', 'physical', 60, 100, 'Has a 10% chance to burn the target')
double_kick = Attack('Double Kick', 'fighting', 'physical', 30, 100, 'Hits twice')
heat_wave = Attack('Heat Wave', 'fire', 'special', 95, 90, 'Has a 10% chance to burn the target')
inferno = Attack('Inferno', 'fire', 'special', 100, 50, 'Has a 100% chance to burn the target')
fury_attack = Attack('Fury Attack', 'normal', 'physical', 15, 85, 'Hits 2-5 times')
pin_missile = Attack('Pin Missile', 'bug', 'physical', 25, 95, 'Hits 2-5 times')
acid_spray = Attack('Acid Spray', 'poison', 'special', 40, 100, 'Lowers the target´s Sp.Def by two stages')
gunk_shot = Attack('Gunk Shot', 'poison', 'physical', 120, 80, 'Has a 30% chance to poison the target')
crush_claw = Attack('Crush Claw', 'normal', 'physical', 75, 95, 'Has a 50% chance to lower the target´s Def by one stage')
fury_swipes = Attack('Fury Swipes', 'normal', 'physical', 18, 80, 'Hits 2-5 times')
icicle_spear = Attack('Icicle Spear', 'ice', 'physical', 25, 100, 'Hits 2-5 times')
double_slap = Attack('Double Slap', 'normal', 'physical', 15, 85, 'Hits 2-5 times')
spike_cannon = Attack('Spike Cannon', 'normal', 'physical', 20, 100, 'Hits 2-5 times')
arm_thrust = Attack('Arm Thrust', 'fighting', 'physical', 15, 100, 'Hits 2-5 times')
aurora_beam = Attack('Aurora Beam', 'ice', 'special', 65, 100, 'Has a 10% chance to lower the target´s Att by one stage')
steel_wing = Attack('Steel Wing', 'steel', 'physical', 70, 90, 'Has a 10% chance to raise the user´s Def by one stage')
absorb = Attack('Absorb', 'grass', 'special', 20, 100, 'Drains half the damage inflicted to heal the user')
take_down = Attack('Take Down', 'normal', 'physical', 90, 85, 'User recieves 1/4 the damage it inflicts in recoil')
flare_blitz = Attack('Flare Blitz', 'fire', 'physical', 120, 100, 'User recieves 1/3 the damage it inflicts in recoil. Has a 10% chance to burn the target')
mega_drain = Attack('Mega Drain', 'grass', 'special', 40, 100, 'Drains half the damage inflicted to heal the user')
cross_poison = Attack('Cross Poison', 'poison', 'physical', 70, 100, 'Has a 10% chance to poison the target')
power_gem = Attack('Power Gem', 'rock', 'special', 80, 100, '-')
close_combat = Attack('Close Combat', 'fighting', 'physical', 120, 100, 'Lowers the user´s Def and Sp.Def by one stage')
submission = Attack('Submission', 'fighting', 'physical', 80, 80, 'User recieves 1/4 the damage it inflicts in recoil')
rock_blast = Attack('Rock Blast', 'rock', 'physical', 25, 90, 'Hits 2-5 times')
brave_bird = Attack('Brave Bird', 'flying', 'physical', 120, 100, 'User recieves 1/3 the damage it inflicts in recoil')
wood_hammer = Attack('Wood Hammer', 'grass', 'physical', 120, 100, 'User recieves 1/3 the damage it inflicts in recoil')
smog = Attack('Smog', 'poison', 'special', 30, 70, 'Has a 40% chance to poison the target')
double_edge = Attack('Double-Edge', 'normal', 'physical', 120, 100, 'User recieves 1/3 the damage it inflicts in recoil')
bullet_seed = Attack('Bullet Seed', 'grass', 'physical', 25, 100, 'Hits 2-5 times')
vice_grip = Attack('Vice Grip', 'normal', 'physical', 55, 100, '-')
stomp = Attack('Stomp', 'normal', 'physical', 65, 100, 'Has a 30% chance to make the target flinch')
strenght = Attack('Strenght', 'normal', 'physical', 80, 100, '-')
waterfall = Attack('Waterfall', 'water', 'physical', 80, 100, 'Has a 20% chance to make the target flinch')
facade = Attack('Facade', 'normal', 'physical', 70, 100, 'Power doubles if user is burned, paralyzed or poisoned')
knock_off = Attack('Knock Off', 'dark', 'physical', 65, 100, '-')
extrasensory = Attack('Extrasensory', 'psychic', 'special', 80, 100, 'Has a 10% chance to make the target flinch')
force_palm = Attack('Force Palm', 'fighting', 'physical', 60, 100, 'Has a 30% chance to paralyze the target')
bullet_punch = Attack('Bullet Punch', 'steel', 'physical', 40, 100, '-')
charge_beam = Attack('Charge Beam', 'electric', 'special', 50, 90, 'Has a 70% chance to raise the user´s Sp.Att by one stage')
crabhammer = Attack('Crabhammer', 'water', 'physical', 100, 90, '-')
dragon_rush = Attack('Dragon Rush', 'dragon', 'physical', 100, 75, 'Has a 20% chance to make the target flinch')
dual_chop = Attack('Dual Chop', 'dragon', 'physical', 40, 90, 'Hits twice in one turn')
energy_ball = Attack('Energy Ball', 'grass', 'special', 90, 100, 'Has a 10% chance to lower the target´s Sp.Def by one stage')
flame_charge = Attack('Flame Charge', 'fire', 'physical', 50, 100, 'Raises the user´s Speed by one stage')
head_smash = Attack('Head Smash', 'rock', 'physical', 150, 80, 'User recieves 1/2 the damage it inflicts in recoil')
lava_plume = Attack('Lava Plume', 'fire', 'special', 80, 100, 'Has a 20% chance to burn the target')
mega_kick = Attack('Mega Kick', 'normal', 'physical', 120, 75, '-')
mega_punch = Attack('Mega Punch', 'normal', 'physical', 80, 85, '-')
mirror_shot = Attack('Mirror Shot', 'steel', 'special', 65, 85, 'Has a 30% chance to lower the target´s accuracy by one stage')
mud_slap = Attack('Mud Slap', 'ground', 'special', 20, 100, 'Has a 100% chance to lower the target´s accuracy by one stage')
muddy_water = Attack('Muddy Water', 'water', 'special', 90, 85, 'Has a 30% chance to lower the target´s accuracy by one stage')
nuzzle = Attack('Nuzzle', 'electric', 'physical', 20, 100, 'Has a 100% chance tu paralyze the target')
power_whip = Attack('Power Whip', 'grass', 'physical', 120, 85, '-')
rock_climb = Attack('Rock Climb', 'normal', 'physical', 90, 85, 'Has a 20% chance to confuse the target')
rock_tomb = Attack('Rock Tomb', 'rock', 'physical', 60, 95, 'Has a 100% chance to lower the target´s Speed by one stage')
wild_charge = Attack('Wild Charge', 'electric', 'physical', 90, 100, 'User recieves 1/4 the damage it inflicts in recoil')


growl = Attack('Growl', 'normal', 'status', 0, 100, 'Lowers the target´s Att by one stage')
poison_powder = Attack('Poison Powder', 'poison', 'status', 0, 75, 'Poisons the target')
growth = Attack('Growth', 'normal', 'status', 0, 100, 'Raises the user´s Att and Sp.Att by one stage')
tail_whip = Attack('Tail Whip', 'normal', 'status', 0, 100, 'Lowers the target´s Def by one stage')
withdraw = Attack('Withdraw', 'water', 'status', 0, 100, 'Raises the user´s Def by one stage')
iron_defense = Attack('Iron Defense', 'steel', 'status', 0, 100, 'Raises the user´s Def by two stages')
stun_spore = Attack('Stun Spore', 'grass', 'status', 0, 75, 'Paralyzes the target')
supersonic = Attack('Supersonic', 'normal', 'status', 0, 55, 'Confuses the target')
quilver_dance = Attack('Quilver Dance', 'bug', 'status', 0, 100, 'Raises the user´s Sp.Att, Sp.Def and Speed by one stage each')
feather_dance = Attack('Feather Dance', 'flying', 'status', 0, 100, 'Lowers the target´s Att by two stages')
swords_dance = Attack('Swords Dance', 'normal', 'status', 0, 100, 'Raises the user´s Att by two stages')
leer = Attack('Leer', 'normal', 'status', 0, 100, 'Lowers the target´s Def by one stage')
screech = Attack('Screech', 'normal', 'status', 0, 85, 'Lowers the target´s Def by two stages')
thunder_wave = Attack('Thunder Wave', 'electric', 'status', 0, 90, 'Paralyzes the target')
defense_curl = Attack('Defense Curl', 'normal', 'status', 0, 100, 'Raises the user´s Def by one stage')
cosmic_power = Attack('Cosmic Power', 'psychic', 'status', 0, 100, 'Raises the user´s Def anf Sp.Def by one stage')
nasty_plot = Attack('Nasty Plot', 'dark', 'status', 0, 100, 'Raises the user´s Sp.Att by two stages')
confuse_ray = Attack('Confuse Ray', 'ghost', 'status', 0, 100, 'Confuses the target')
babydoll_eyes = Attack('Baby-Doll Eyes', 'fairy', 'status', 0, 100, 'Lowers the target´s Att by one stage')
willowisp = Attack('Will-O-Wisp', 'fire', 'status', 0, 85, 'Burns the target')
amnesia = Attack('Amnesia', 'psychic', 'status', 0, 100, 'Raises the user´s Sp.Def by two stages')
swagger = Attack('Swagger', 'normal', 'status', 0, 85, 'Raises the target´s Att by two stages and confuses the target')
calm_mind = Attack('Calm Mind', 'psychic', 'status', 0, 100, 'Raises the user´s Sp.Att and Sp.Def by one stage')
bulk_up = Attack('Bulk Up', 'fighting', 'status', 0, 100, 'Raises the user´s Att and Def by one stage')
metal_sound = Attack('Metal Sound', 'steel', 'status', 0, 85, 'Lowers the target´s Sp.Def by two stages')
fake_tears = Attack('Fake Tears', 'dark', 'status', 0, 100, 'Lowers the target´s Sp.Def by two stages')
poison_gas = Attack('Poison Gas', 'poison', 'status', 0, 90, 'Poisons the target')
harden = Attack('Harden', 'normal', 'status', 0, 100, 'Raises the user´s Def by one stage')
charm = Attack('Charm', 'fairy', 'status', 0, 100, 'Lowers the target´s Att by two stages')
glare = Attack('Glare', 'normal', 'status', 0, 100, 'Paralyzes the target')
tickle = Attack('Tickle', 'normal', 'status', 0, 100, 'Lowers the target´s Att and Def by one stage')
sand_attack = Attack('Sand Attack', 'ground', 'status', 0, 100, 'Lowers the target´s accuracy by one stage')
agility = Attack('Agility', 'psychic', 'status', 0, 0, 'Raises the users´s Speed by two stages')
coil = Attack('Coil', 'poison', 'status', 0, 0, 'Raises the users´s Att, Def and accuracy by one stage each')
cotton_guard = Attack('Cotton Guard', 'grass', 'status', 0, 0, 'Raises the users´s Def by three stages')
defog = Attack('Defog', 'flying', 'status', 0, 0, 'Lowers the target´s evasion by one stage')
double_team = Attack('Double Team', 'normal', 'status', 0, 0, 'Raises the user´s evasion by one stage')
dragon_dance = Attack('Dragon Dance', 'dragon', 'status', 0, 0, 'Raises the users´s Att and Speed by one stage')
hone_claws = Attack('Hone Claws', 'dark', 'status', 0, 0, 'Raises the users´s Att and accuracy by one stage')
howl = Attack('Howl', 'normal', 'status', 0, 0, 'Raises the users´s Att by one stage')
meditate = Attack('Meditate', 'psychic', 'status', 0, 0, 'Raises the users´s Att by one stage')
minimize = Attack('Minimize', 'normal', 'status', 0, 0, 'Raises the users´s evasion by two stages')
play_nice = Attack('Play Nice', 'normal', 'status', 0, 0, 'Lowers the target´s Att by one stage')
scary_face = Attack('Scary Face', 'normal', 'status', 0, 100, 'Lowers the target´s Speed by two stages')
smokescreen = Attack('Smokescreen', 'normal', 'status', 0, 100, 'Lowers the target´s accuracy by one stage')
string_shot = Attack('String Shot', 'bug', 'status', 0, 95, 'Lowers the target´s Speed by one stage')
sweet_scent = Attack('Sweet Scent', 'normal', 'status', 0, 100, 'Lowers the target´s evasion by one stage')
teeter_dance = Attack('Teeter Dance', 'normal', 'status', 0, 100, 'Confuses the target')



breakneck_blitz = ZMove('Breakneck Blitz', 'normal')
allout_pummeling = ZMove('All-Out Pummeling', 'fighting')
supersonic_skystrike = ZMove('Supersonic Skystrike', 'flying')
acid_downpour = ZMove('Acid Downpour', 'poison')
tectonic_rage = ZMove('Tectonic Rage', 'ground')
continental_crush = ZMove('Continental Crush', 'rock')
savage_spinout = ZMove('Savage Spin-Out', 'bug')
neverending_nightmare = ZMove('Never-Ending Nightmare', 'ghost')
corkscrew_crash = ZMove('Corkscrew Crash', 'steel')
inferno_overdrive = ZMove('Inferno Overdrive', 'fire')
hydro_vortex = ZMove('Hydro Vortex', 'water')
bloom_doom = ZMove('Bloom Doom', 'grass')
gigavolt_havoc = ZMove('Gigavolt Havoc', 'electric')
shattered_psyche = ZMove('Shattered Psyche', 'psychic')
subzero_slammer = ZMove('Subzerro Slammer', 'ice')
devastating_drake = ZMove('Devastating Drake', 'dragon')
black_hole_eclipse = ZMove('Black Hole Eclipse', 'dark')
twinkle_tackle = ZMove('Twinkle Tackle', 'fairy')


stage_multiplier_dict = {
    (-6):(2/8),
    (-5):(2/7),
    (-4):(2/6),
    (-3):(2/5),
    (-2):(2/4),
    (-1):(2/3),
    (0):(2/2),
    (1):(3/2),
    (2):(4/2),
    (3):(5/2),
    (4):(6/2),
    (5):(7/2),
    (6):(8/2)
}

acc_stage_dict = {
    (-6):(0.33),
    (-5):(0.375),
    (-4):(0.428),
    (-3):(0.5),
    (-2):(0.6),
    (-1):(0.75),
    (0):(1),
    (1):(1.33),
    (2):(1.66),
    (3):(2),
    (4):(2.33),
    (5):(2.66),
    (6):(3)
}

evasion_stage_dict = {
    (-6):(3),
    (-5):(2.66),
    (-4):(2.33),
    (-3):(2),
    (-2):(1.66),
    (-1):(1.33),
    (0):(1),
    (1):(0.75),
    (2):(0.6),
    (3):(0.5),
    (4):(0.428),
    (5):(0.375),
    (6):(0.33)
}


def attack_effect(move, mon, enemy, turn_count):
    move.multiplier = 1
    move.heal_multiplier = 0
    move.hit_number = 1
    move.selfhit_multiplier = 0
    if move == flamethrower:
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == ember:
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == fire_fang:
        if random.randrange(1,11) == 1:
            enemy.burn = True
        if random.randrange(1,11) == 1:
            enemy.flinch = True
    if move == extrasensory:
        if random.randrange(1,11) == 1:
            enemy.flinch = True
    if move == air_slash:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == force_palm:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True
    if move == bubble:
        if random.randrange(1,11) == 1:
            enemy.spd_stage -= 1
    if move == bite:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == water_pulse:
        if random.randrange(1,11) in [1,2]:
            enemy.confuse = True
    if move == dizzy_punch:
        if random.randrange(1,11) in [1,2]:
            enemy.confuse = True
    if move == rock_climb:
        if random.randrange(1,11) in [1,2]:
            enemy.confuse = True
    if move == twineedle:
        if random.randrange(1,11) in [1,2]:
            enemy.poison = True
        move.hit_number = 2
    if move == double_kick:
        move.hit_number = 2
    if move == flash_cannon:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == confusion:
        if random.randrange(1,11) == 1:
            enemy.confuse = True
    if move == psybeam:
        if random.randrange(1,11) == 1:
            enemy.confuse = True
    if move == silver_wind:
        if random.randrange(1,11) == 1:
            mon.att_stage += 1
            mon.defense_stage += 1
            mon.sp_att_stage += 1
            mon.sp_def_stage += 1
            mon.spd_stage += 1
    if move == ominous_wind:
        if random.randrange(1,11) == 1:
            mon.att_stage += 1
            mon.defense_stage += 1
            mon.sp_att_stage += 1
            mon.sp_def_stage += 1
            mon.spd_stage += 1
    if move == bug_buzz:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == poison_sting:
        if random.randrange(1,11) in [1,2,3]:
            enemy.poison = True
    if move == venoshock:
        if enemy.poison == True:
            move.multiplier = 2
    if move == twister:
        if random.randrange(1,11) in [1,2]:
            enemy.flinch = True
    if move == rock_slide:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == hurricane:
        if random.randrange(1,11) in [1,2,3]:
            enemy.confuse = True
    if move == crunch:
        if random.randrange(1,11) in [1,2]:
            enemy.defense_stage -= 1
    if move == rock_smash:
        if random.randrange(1,3) == 1:
            enemy.defense_stage -= 1
    if move == hyper_fang:
        if random.randrange(1,11) == 1:
            enemy.flinch = True
    if move == acid:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == ice_fang:
        if random.randrange(1,11) == 1:
            enemy.flinch = True
        if random.randrange(1,11) == 1:
            enemy.freeze = True
    if move == thunder_fang:
        if random.randrange(1,11) == 1:
            enemy.flinch = True
        if random.randrange(1,11) == 1:
            enemy.paralyze = True
    if move == thunder_shock:
        if random.randrange(1,11) == 1:
            enemy.paralyze = True
    if move == spark:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True
    if move == discharge:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True
    if move == thunderbolt:
        if random.randrange(1,11) == 1:
            enemy.paralyze = True
    if move == furry_cutter:
        if turn_count == 1:
            move.multiplier = 1
        if turn_count == 2:
            move.multiplier = 2
        if turn_count == 3:
            move.multiplier = 4
        if turn_count >= 4:
            move.multiplier = 8
    if move == ice_ball:
        if turn_count == 1:
            move.multiplier = 1
        if turn_count == 2:
            move.multiplier = 2
        if turn_count == 3:
            move.multiplier = 4
        if turn_count >= 4:
            move.multiplier = 8
    if move == poison_fang:
        if random.randrange(1,3) == 1:
            enemy.poison = True
    if move == body_slam:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True
    if move == superpower:
        mon.att_stage -= 1
        mon.defense_stage -= 1
    if move == earth_power:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == moonblast:
        if random.randrange(1,11) in [1,2,3]:
            enemy.sp_att_stage -= 1
    if move == payback:
        if mon.spd < enemy.spd:
            move.multiplier = 2
    if move == hex:
        if enemy.burn == True or enemy.poison == True:
            move.multiplier = 2
    if move == fire_blast:
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == astonish:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == steamroller:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == leech_life:
        move.heal_multiplier = 0.5
    if move == giga_drain:
        move.heal_multiplier = 0.5
    if move == psychic:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == signal_beam:
        if random.randrange(1,11) == 1:
            enemy.confuse = True
    if move == bulldoze:
        enemy.spd_stage -= 1   
    if move == zen_headbutt:
        if random.randrange(1,11) in [1,2]:
            enemy.flinch = True 
    if move == lava_plume:
        if random.randrange(1,11) in [1,2]:
            enemy.burn = True 
    if move == Bubble_beam:
        if random.randrange(1,11) == 1:
            enemy.spd_stage -= 1
    if move == mud_shot:
        enemy.spd_stage -= 1
    if move == mud_slap:
        enemy.acc_stage -= 1
    if move == dynamic_punch:
        enemy.confuse = True
    if move == brine:
        if enemy.hp < (enemy.max_hp/2):
            move.multiplier = 2
    if move == sludge_wave:
        if random.randrange(1,11) == 1:
            enemy.poison = True
    if move == sludge_wave:
        if random.randrange(1,11) in [1,2,3]:
            enemy.poison = True
    if move == headbutt:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True 
    if move == zap_cannon:
        enemy.paralyze = True
    if move == icy_wind:
        enemy.spd_stage -= 1
    if move == ice_beam:
        if random.randrange(1,11) == 1:
            enemy.freeze = True
    if move == sludge:
        if random.randrange(1,11) in [1,2,3]:
            enemy.poison = True 
    if move == lick:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True 
    if move == zen_headbutt:
        if random.randrange(1,11) in [1,2]:
            enemy.sp_def_stage -= 1 
    if move == dark_pulse:
        if random.randrange(1,11) in [1,2]:
            enemy.flinch = True
    if move == dragon_breath:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True  
    if move == iron_tail:
        if random.randrange(1,11) in [1,2,3]:
            enemy.defense_stage -= 1 
    if move == mirror_shot:
        if random.randrange(1,11) in [1,2,3]:
            enemy.acc_stage -= 1 
    if move == muddy_water:
        if random.randrange(1,11) in [1,2,3]:
            enemy.acc_stage -= 1 
    if move == metal_claw:
        if random.randrange(1,11) == 1:
            mon.att_stage += 1 
    if move == bone_club:
        if random.randrange(1,11) == 1:
            enemy.flinch = True 
    if move == hammer_arm:
        enemy.spd_stage -= 1
    if move == ancient_power:
        if random.randrange(1,11) == 1:
            mon.att_stage += 1
            mon.defense_stage += 1
            mon.sp_att_stage += 1
            mon.sp_def_stage += 1
            mon.spd_stage += 1
    if move == powder_snow:
        if random.randrange(1,11) == 1:
            enemy.freeze = True 
    if move == blizzard:
        if random.randrange(1,11) == 1:
            enemy.freeze = True 
    if move == avalanche:
        if mon.spd < enemy.spd:
            move.multiplier = 2
    if move == thunder:
        if random.randrange(1,11) in [1,2,3]:
            enemy.paralyze = True  
    if move == iron_head:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == needle_arm:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True    
    if move == play_rough:
        if random.randrange(1,11) == 1:
            enemy.att_stage -= 1 
    if move == leaf_storm:
        enemy.sp_att_stage -= 2
    if move == poison_jab:
        if random.randrange(1,11) in [1,2,3]:
            enemy.poison = True 
    if move == fire_punch:
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == ice_punch:
        if random.randrange(1,11) == 1:
            enemy.freeze = True
    if move == thunder_punch:
        if random.randrange(1,11) == 1:
            enemy.paralyze = True
    if move == icicle_crash:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == stomp:
        if random.randrange(1,11) in [1,2,3]:
            enemy.flinch = True
    if move == waterfall:
        if random.randrange(1,11) in [1,2]:
            enemy.flinch = True
    if move == dragon_rush:
        if random.randrange(1,11) in [1,2]:
            enemy.flinch = True
    if move == flame_wheel:
        if random.randrange(1,11) == 1:
            enemy.burn = True
        enemy.freeze = False
    if move == growl:
        enemy.att_stage -= 1
    if move == tickle:
        enemy.att_stage -= 1
        enemy.defense_stage -= 1
    if move == poison_powder:
        enemy.poison = True
    if move == growth:
        mon.att_stage += 1
        mon.sp_att_stage += 1
    if move == heat_wave:
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == inferno:
        enemy.burn = True
    if move == tail_whip:
        enemy.defense_stage -= 1
    if move == withdraw:
        mon.defense_stage += 1
    if move == iron_defense:
        mon.defense_stage += 2
    if move == stun_spore:
        enemy.paralyze = True
    if move == glare:
        enemy.paralyze = True
    if move == supersonic:
        enemy.confuse = True
    if move == quilver_dance:
        mon.sp_def_stage += 1
        mon.sp_att_stage += 1
        mon.spd_stage += 1
    if move == fury_attack:
        move.hit_number = random.choice([2,3,4,5])
    if move == pin_missile:
        move.hit_number = random.choice([2,3,4,5])
    if move == feather_dance:
        enemy.att_stage -= 2
    if move == swords_dance:
        mon.att_stage += 2
    if move == leer:
        enemy.defense_stage -= 1
    if move == screech:
        enemy.defense_stage -= 2
    if move == charm:
        enemy.att_stage -= 2
    if move == acid_spray:
        enemy.sp_def_stage -= 2
    if move == gunk_shot:
        if random.randrange(1,11) in [1,2,3]:
            enemy.poison = True
    if move == thunder_wave:
        enemy.paralyze = True
    if move == crush_claw:
        if random.randrange(1,3) == 1:
            enemy.defense_stage -= 1
    if move == razor_shell:
        if random.randrange(1,3) == 1:
            enemy.defense_stage -= 1
    if move == defense_curl:
        mon.defense_stage += 1
    if move == fury_swipes:
        move.hit_number = random.choice([2,3,4,5])
    if move == icicle_spear:
        move.hit_number = random.choice([2,3,4,5])
    if move == double_slap:
        move.hit_number = random.choice([2,3,4,5])
    if move == spike_cannon:
        move.hit_number = random.choice([2,3,4,5])
    if move == arm_thrust:
        move.hit_number = random.choice([2,3,4,5])
    if move == rock_blast:
        move.hit_number = random.choice([2,3,4,5])
    if move == bullet_seed:
        move.hit_number = random.choice([2,3,4,5])
    if move == cosmic_power:
        mon.defense_stage += 1
        mon.sp_def_stage += 1
    if move == nasty_plot:
        mon.sp_att_stage += 2
    if move == confuse_ray:
        enemy.confuse = True
    if move == babydoll_eyes:
        enemy.att_stage -= 1
    if move == willowisp:
        enemy.burn = True
    if move == aurora_beam:
        if random.randrange(1,11) == 1:
            enemy.att_stage -= 1
    if move == energy_ball:
        if random.randrange(1,11) == 1:
            enemy.sp_def_stage -= 1
    if move == steel_wing:
        if random.randrange(1,11) == 1:
            mon.def_stage += 1
    if move == absorb:
        move.heal_multiplier = 0.5
    if move == take_down:
        move.selfhit_multiplier = 0.25
    if move == wild_charge:
        move.selfhit_multiplier = 0.25
    if move == flare_blitz:
        move.selfhit_multiplier = 0.33
        if random.randrange(1,11) == 1:
            enemy.burn = True
    if move == mega_drain:
        move.heal_multiplier = 0.5
    if move == cross_poison:
        if random.randrange(1,11) == 1:
            enemy.poison = True
    if move == amnesia:
        mon.sp_def_stage += 2
    if move == swagger:
        enemy.att_stage += 2
        enemy.confuse = True
    if move == close_combat:
        mon.defense_stage -= 1
        mon.sp_def_stage -= 1
    if move == submission:
        move.selfhit_multiplier = 0.25
    if move == calm_mind:
        mon.sp_att_stage += 1
        mon.sp_def_stage += 1
    if move == bulk_up:
        mon.att_stage += 1
        mon.defense_stage += 1
    if move == metal_sound:
        enemy.sp_def_stage -= 2
    if move == fake_tears:
        enemy.sp_def_stage -= 2
    if move == brave_bird:
        move.selfhit_multiplier = 0.33
    if move == poison_gas:
        enemy.poison = True
    if move == harden:
        mon.defense_stage += 1
    if move == wood_hammer:
        move.selfhit_multiplier = 0.33
    if move == double_edge:
        move.selfhit_multiplier = 0.33
    if move == head_smash:
        move.selfhit_multiplier = 0.5
    if move == gunk_shot:
        if random.randrange(1,11) in [1,2,3,4]:
            enemy.poison = True
    if move == facade:
        if mon.burn == True or mon.paralyze == True or mon.poison == True:
            move.multiplier = 2
    if move == sand_attack:
        enemy.acc_stage -= 1
    if move == agility:
        mon.spd_stage += 2
    if move == charge_beam:
        if random.randrange(1,11) in [1,2,3,4,5,6,7]:
            mon.sp_att_stage += 1
    if move == coil:
        mon.att_stage += 1
        mon.defense_stage += 1
        mon.acc_stage += 1
    if move == cotton_guard:
        mon.defense_stage += 3
    if move == defog:
        enemy.evasion_stage -= 1
    if move == double_team:
        mon.evasion_stage += 1
    if move == dragon_dance:
        mon.spd_stage += 1
        mon.att_stage += 1
    if move == hone_claws:
        mon.acc_stage += 1
        mon.att_stage += 1
    if move == howl:
        mon.att_stage += 1
    if move == meditate:
        mon.att_stage += 1
    if move == dual_chop:
        move.hit_number = 2
    if move == flame_charge:
        mon.spd_stage += 1
    if move == minimize:
        mon.evasion_stage += 2
    if move == nuzzle:
        enemy.paralyze = True
    if move == play_nice:
        enemy.att_stage -= 1
    if move == rock_tomb:
        enemy.spd_stage -= 1
    if move == scary_face:
        enemy.spd_stage -= 2
    if move == smokescreen:
        enemy.acc_stage -= 1
    if move == string_shot:
        enemy.spd_stage -= 1
    if move == sweet_scent:
        enemy.evasion_stage -= 1
    if move == teeter_dance:
        enemy.confusion = True





    if enemy.hp_stage < -6:
        enemy.hp_stage = -6
    if enemy.hp_stage > 6:
        enemy.hp_stage = 6
    
    if enemy.att_stage < -6:
        enemy.att_stage = -6
    if enemy.att_stage > 6:
        enemy.att_stage = 6
    
    if enemy.defense_stage < -6:
        enemy.defense_stage = -6
    if enemy.defense_stage > 6:
        enemy.defense_stage = 6
    
    if enemy.sp_att_stage < -6:
        enemy.sp_att_stage = -6
    if enemy.sp_att_stage > 6:
        enemy.sp_att_stage = 6
    
    if enemy.sp_def_stage < -6:
        enemy.sp_def_stage = -6
    if enemy.sp_def_stage > 6:
        enemy.sp_def_stage = 6
    
    if enemy.spd_stage < -6:
        enemy.spd_stage = -6
    if enemy.spd_stage > 6:
        enemy.spd_stage = 6

    if mon.hp_stage < -6:
        mon.hp_stage = -6
    if mon.hp_stage > 6:
        mon.hp_stage = 6
    
    if mon.att_stage < -6:
        mon.att_stage = -6
    if mon.att_stage > 6:
        mon.att_stage = 6
    
    if mon.defense_stage < -6:
        mon.defense_stage = -6
    if mon.defense_stage > 6:
        mon.defense_stage = 6
    
    if mon.sp_att_stage < -6:
        mon.sp_att_stage = -6
    if mon.sp_att_stage > 6:
        mon.sp_att_stage = 6
    
    if mon.sp_def_stage < -6:
        mon.sp_def_stage = -6
    if mon.sp_def_stage > 6:
        mon.sp_def_stage = 6
    
    if mon.spd_stage < -6:
        mon.spd_stage = -6
    if mon.spd_stage > 6:
        mon.spd_stage = 6

    if mon.acc_stage < -6:
        mon.acc_stage = -6
    if mon.acc_stage > 6:
        mon.acc_stage = 6

    if enemy.acc_stage < -6:
        enemy.acc_stage = -6
    if enemy.acc_stage > 6:
        enemy.acc_stage = 6
    
    if enemy.evasion_stage < -6:
        enemy.evasion_stage = -6
    if enemy.evasion_stage > 6:
        enemy.evasion_stage = 6

    if mon.evasion_stage < -6:
        mon.evasion_stage = -6
    if mon.evasion_stage > 6:
        mon.evasion_stage = 6

    
    enemy.hp = (enemy.hp * stage_multiplier_dict[enemy.hp_stage])
    enemy.att = (enemy.att * stage_multiplier_dict[enemy.att_stage])
    enemy.defense = (enemy.defense * stage_multiplier_dict[enemy.defense_stage])
    enemy.sp_att = (enemy.sp_att * stage_multiplier_dict[enemy.sp_att_stage])
    enemy.sp_def = (enemy.sp_def * stage_multiplier_dict[enemy.sp_def_stage])
    enemy.spd = (enemy.spd * stage_multiplier_dict[enemy.spd_stage])

    mon.hp = (mon.hp * stage_multiplier_dict[mon.hp_stage])
    mon.att = (mon.att * stage_multiplier_dict[mon.att_stage])
    mon.defense = (mon.defense * stage_multiplier_dict[mon.defense_stage])
    mon.sp_att = (mon.sp_att * stage_multiplier_dict[mon.sp_att_stage])
    mon.sp_def = (mon.sp_def * stage_multiplier_dict[mon.sp_def_stage])
    mon.spd = (mon.spd * stage_multiplier_dict[mon.spd_stage])