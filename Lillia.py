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
    "script": "SA1-Lillia",
    "author": "SA1",
    "description": "SA1-Lillia",
    "target_champ": "lillia"
}

combo_key = 0
laneclear_key = 47

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

use_Qclear = True
use_Wclear = True
use_Eclear = True



q = {'Range': 1049} #1100, using safe range
w = {'Range': 350} 
e = {'Range': 350}
r = {'Range': 550}

MaxRCountForUse = 1

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, laneclear_key
    global use_Qclear, use_Wclear, use_Eclear
    global MaxRCountForUse
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("harass_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    use_Qclear = cfg.get_bool("use_Qclear", True)
    use_Wclear = cfg.get_bool("use_Wclear", True)
    use_Eclear = cfg.get_bool("use_Eclear", True)

    MaxRCountForUse = cfg.get_float("MaxRCountForUse", 1)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, laneclear_key
    global use_Qclear, use_Wclear, use_Eclear
    global MaxRCountForUse

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)    
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("use_Qclear", use_Qclear)
    cfg.set_bool("use_Wclear", use_Wclear)
    cfg.set_bool("use_Eclear", use_Eclear)

    cfg.set_float("MaxRCountForUse", MaxRCountForUse)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, laneclear_key
    global use_Qclear, use_Wclear, use_Eclear
    
    ui.text("SA1-Lillia : 1.0.0.0")
    ui.separator ()

    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Farm-Clear key", laneclear_key)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
        ui.treepop()

    if ui.treenode("Farm-clear settings"):
        use_Qclear = ui.checkbox("Farm-clear with Q", use_Qclear)
        use_Wclear = ui.checkbox("Farm-clear with W", use_Wclear)
        use_Eclear = ui.checkbox("Farm-clear with E", use_Eclear)
        ui.treepop()

RTargetCount = 0


def getCountR(game, dist):
    global RTargetCount, MaxRCountForUse
    RTargetCount = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist
        ):
            RTargetCount = RTargetCount + 1
    if int(RTargetCount) >= MaxRCountForUse:
        return True
    else:
        return False
    
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

def circle_on_line(A, B, C, R):
    x_diff = B.x - A.x
    y_diff = B.y - A.y
    LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)
    Dx = x_diff / LAB
    Dy = y_diff / LAB
    t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
    if not -R <= t <= LAB + R:
        return False
    Ex = t*Dx+A.x
    Ey = t*Dy+A.y
    x_diff1 = Ex - C.x
    y_diff1 = Ey - C.y
    LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)
    return LEC <= R


def is_collisioned(game, target, oType="minion", ability_width=0):
    player_pos = game.world_to_screen(game.player.pos)
    target_pos = game.world_to_screen(target.pos)

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                minion_pos = game.world_to_screen(minion.pos)
                total_radius = minion.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
                    return True
    
    if oType == "champ":
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
                champ_pos = game.world_to_screen(champ.pos)
                total_radius = champ.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
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



def Combo(game):
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    player=game.player

    if use_q_in_combo and IsReady(game, q_spell):
        target=TargetSelector(game,450)
        if target:
            if player.mana>=50:
                q_spell.trigger(False)

    if use_w_in_combo and IsReady(game, w_spell):
        target=TargetSelector(game,500)
        if target:
            if player.mana>=50:
                if IsReady(game, w_spell):
                    w_travel_time = 700 / 1000
                    predicted_pos = predict_pos (target, w_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700 :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            w_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)    

    if use_e_in_combo and IsReady(game, e_spell):
        target=TargetSelector(game,3000)
        if target:
            if player.mana>=70:
                
                    e_travel_time = 3000 / 3000
                    predicted_pos = predict_pos (target, e_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 3000 or is_immobile(game, predicted_target.pos) and not IsCollisioned(game, predicted_target) :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            e_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)   
                            
                               
def Farmclear(game):
    global use_Qclear, use_Wclear, use_Eclear
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")

    player=game.player
    if use_Qclear and IsReady(game, q_spell):
        target=GetBestMinionsInRange(game,450)
        if target:
            if player.mana>=50:
                q_spell.trigger(False)

    if use_Wclear and IsReady(game, w_spell):
        target=GetBestMinionsInRange(game,500)
        if target:
            if player.mana>=50:
                if IsReady(game, w_spell):
                    w_travel_time = 700 / 1000
                    predicted_pos = predict_pos (target, w_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700 :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            w_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)    

    if use_Eclear and IsReady(game, e_spell):
        target=GetBestMinionsInRange(game,800)
        if target:
            if player.mana>=70:
                if IsReady(game, e_spell):
                    if game.player.pos.distance (target.pos) <= 800 :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (target.pos))
                            time.sleep (0.01)
                            e_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)   
def jungleClear(game):
    
    global use_Qclear, use_Wclear, use_Eclear
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")

    player=game.player
    if use_Qclear and IsReady(game, q_spell):
        target=GetBestJungleInRange(game,450)
        if target:
            if player.mana>=50:
                q_spell.trigger(False)

    if use_Wclear and IsReady(game, w_spell):
        target=GetBestJungleInRange(game,500)
        if target:
            if player.mana>=50:
                if IsReady(game, w_spell):
                    w_travel_time = 700 / 1000
                    predicted_pos = predict_pos (target, w_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700 :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            w_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)    

    if use_Eclear and IsReady(game, e_spell):
        target=GetBestJungleInRange(game,800)
        if target:
            if player.mana>=70:
                if IsReady(game, e_spell):
                    if game.player.pos.distance (target.pos) <= 800 :
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (target.pos))
                            time.sleep (0.01)
                            e_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)   
def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, laneclear_key
    global use_Qclear, use_Wclear, use_Eclear
    global MaxRCountForUse

    if game.player.is_alive and game.is_point_on_screen(game.player.pos)  :
        if game.is_key_down(laneclear_key):
            Farmclear(game)
            jungleClear(game)
        if game.is_key_down(combo_key):
            Combo(game)



    

    
    





    
    
    

