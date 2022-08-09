from evade import checkEvade
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import time
from copy import deepcopy
import math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "jhin",
    "author": "life",
    "description": "life",
    "target_champ": "jhin"
}

lastE = 0

combo_key = 57
LaneClear_key = 35

use_q_in_combo = True
use_w_on_immobile = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

use_q_lane=True

use_e_evade = True

q = {'Range': 1200}
w = {'Range': 800}
e = {'Range': 700}
r = {'Range': 3500}

q_mana=[40,45,50,55,60]
w_mana=[50,60,70,80,90]


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo,LaneClear_key,use_q_lane
    global use_e_evade
    combo_key = cfg.get_int ("combo_key", combo_key)
    LaneClear_key=cfg.get_int("LaneClear_key",LaneClear_key)

    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)

    use_q_lane=cfg.get_bool ("use_q_lane", True)
    


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo,LaneClear_key
    global use_e_evade,use_q_lane
    cfg.set_int ("combo_key", combo_key)
    cfg.set_int ("LaneClear_key", LaneClear_key)
    
    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_r_in_combo", use_r_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)


    cfg.set_bool ("use_q_lane", use_q_lane)
    


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo,LaneClear_key
    global use_e_evade,use_q_lane

    
    combo_key = ui.keyselect ("Combo key", combo_key)
    LaneClear_key = ui.keyselect ("Lane Clear key", LaneClear_key)

    if ui.treenode ("Combo settings:"):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        use_w_in_combo =  ui.checkbox ("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo)
        ui.treepop ()
    if ui.treenode ("LaneClear settings:"):
        use_q_lane = ui.checkbox ("Use Q in LaneClear", use_q_lane)
        ui.treepop ()


def is_immobile(game, target):
    for buff in target.buffs:

        if 'snare' in buff.name.lower ():
            return True
        elif 'stun' in buff.name.lower ():
            return True
        elif 'suppress' in buff.name.lower ():
            return True
        elif 'root' in buff.name.lower ():
            return True
        elif 'taunt' in buff.name.lower ():
            return True
        elif 'sleep' in buff.name.lower ():
            return True
        elif 'knockup' in buff.name.lower ():
            return True
        elif 'binding' in buff.name.lower ():
            return True
        elif 'morganaq' in buff.name.lower ():
            return True
        elif 'jhinw' in buff.name.lower ():
            return True
    return False


class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target,casttime):
    """Predicts the target's new position after a duration"""
    target_direction = target.ai_navEnd.sub(target.ai_navBegin).normalize()

    veloc=target.ai_velocity
    orientation = veloc.normalize()
    if veloc.x ==0.0 and veloc.y == 0.0:
        return target.pos   

    # Target movement speed
    target_movement_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_movement_speed * casttime 
    # distance_to_travel2=(timetoimpact / 2.2)* 1.5 
    return target.pos.add(target_direction.scale(distance_to_travel))



def RDamage(game, target):
    # Calculate damage
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    lvl_damage = [300, 525, 750]
    r_damage = lvl_damage[r_lvl - 1] + 2*game.player.bonus_atk

    # Reduce damage
    target_armor = target.armour
    if target_armor >= 0:
        damage_multiplier = 100 / (100 + target_armor)
    else:
        damage_multiplier = 2 - 100 / (100 - target_armor)

    return r_damage * damage_multiplier

def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )
def QDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.Q.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [45,70,95,120,145]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def Combo(game):
    before_cpos = game.get_cursor ()
    q_spell = getSkill (game, 'Q')
    e_spell = getSkill (game, 'E')
    w_spell = getSkill (game, 'W')
    r_spell = getSkill (game, 'R')

    if use_q_in_combo and IsReady (game, q_spell) and game.player.mana>=q_mana[game.player.Q.level -1]:
        target = TargetSelector (game,550)
        if target:
            if getBuff(game.player,"JhinPassiveReload"):
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
            if QDamage(game,target)>=target.health or QDamage(game,target)>=target.armour:
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
    if use_w_in_combo and IsReady (game, w_spell) and game.player.mana>=w_mana[game.player.W.level -1]:
        target = TargetSelector (game,3000)
        if target:
            w_travel=3000/10000
            predicted_pos = predict_pos (target, w_travel)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if getBuff(target,"jhinespotteddebuff"):
                w_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
        


    if use_r_in_combo and IsReady (game, r_spell):
        target = TargetSelector (game, 3500)
        if target:
            w_travel=3500/5000
            predicted_pos = predict_pos (target, w_travel)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.R.name=="jhinrshot":
                r_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
            

        
def laneClear(game):
    
    q_spell = getSkill (game, 'Q')
    e_spell = getSkill (game, 'E')
    w_spell = getSkill (game, 'W')
    r_spell = getSkill (game, 'R')

    if use_q_lane and IsReady (game, q_spell) and game.player.mana>=q_mana[game.player.Q.level -1]:
        target = GetBestMinionsInRange (game,550)
        if target:
            if getBuff(game.player,"JhinPassiveReload"):
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
            if QDamage(game,target)>=effHP(game,target) :
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
                
    if use_q_lane and IsReady (game, q_spell) and game.player.mana>=q_mana[game.player.Q.level -1]:
        target = GetBestJungleInRange (game,550)
        if target:
            if getBuff(game.player,"JhinPassiveReload"):
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
            if QDamage(game,target)>=effHP(game,target) :
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
        


def getTargetsInRange(game, atk_range = 0) -> list:
    targets = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        targets.append(champ)

    return targets
def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

def getTargetsByClosenessToCursor(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the cursor'''

    targets = getTargetsInRange(game, atk_range)
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    return sorted(targets, key = lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))


def winstealer_update(game, ui):
    self = game.player
    r_spell = getSkill (game, 'R')
    if self.is_alive and self.is_visible :

        # print (w_spell.timeCharge)
        if game.was_key_pressed (combo_key):
            Combo (game)
        if game.was_key_pressed (LaneClear_key):
            laneClear (game)    

        if use_r_in_combo and IsReady (game, r_spell) and game.player.R.name=="jhinrshot" :
            targets_list = getTargetsByClosenessToCursor(game, 3500)
            game.draw_circle(game.get_cursor(), 120, 100, 2, Color.YELLOW)
            if targets_list:
                target = targets_list[0]
            else:
                target = None

            if target:
                w_travel=3500/5000
                predicted_pos = predict_pos (target, w_travel)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                cursor_pos_vec2 = game.get_cursor()
                cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0) 
                if get_distance(cursor_pos_vec3, game.world_to_screen(target.pos)) <=300:
                        r_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
                        





