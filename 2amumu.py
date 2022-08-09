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
    "script": "Amumu",
    "author": "SA1",
    "description": "Amumu",
    "target_champ": "amumu"
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
    global MaxRCountForUse
    ui.text("Amumu")
    combo_key = ui.keyselect("Combo key", combo_key)
    
    
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    


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

    if ui.treenode("[R] Settings"):
        use_r_in_combo = ui.checkbox("Use R in combo", use_r_in_combo)
        MaxRCountForUse = ui.dragfloat ("Min targets use for R", MaxRCountForUse, 0,1,3)
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


    if use_q_in_combo :
        target = TargetSelector (game,q['Range'])
        
        if target :
            
            if game.player.Q.timeCharge >0:
                if IsReady(game, q_spell):
                    q_travel_time = q['Range'] / 2000
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range'] and not IsCollisioned(game, predicted_target):
                        if game.player.mana>=50:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.01)
                            game.move_cursor (before_cpos)
    
    if use_w_in_combo and IsReady(game, w_spell):
        target = TargetSelector (game, w["Range"])
        if target:
            if game.player.pos.distance(target.pos) <= w["Range"]:
                if not getBuff(game.player, "AuraofDespair")  :
                    if game.player.mana>=8:
                        w_spell.trigger(False)
        if not target:
            if getBuff(game.player, "AuraofDespair") :
                            w_spell.trigger(False)
    
    if use_e_in_combo and IsReady(game, e_spell):
        target = TargetSelector(game, e["Range"])
        
        if ValidTarget(target) and IsReady(game, e_spell):
            if game.player.mana>=30:
                game.move_cursor (game.world_to_screen (target.pos))
                time.sleep (0.01)
                e_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
    
    if (
        use_r_in_combo
        and getCountR(game, r["Range"])
        and IsReady(game, r_spell)
    ):
        target = TargetSelector(game, r["Range"])
        if target:
            if game.player.mana>=100:
                game.move_cursor (game.world_to_screen (target.pos))
                time.sleep (0.01)
                r_spell.trigger (False)
                time.sleep (0.01)
                game.move_cursor (before_cpos)
    
def Farmclear(game):
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")

    if use_Qclear and IsReady(game, q_spell) :
            target = GetBestJungleInRange(game, 1100)
            if target :
                if game.player.Q.timeCharge >0:
                  if IsReady(game, q_spell) and game.player.mana>=50:
                      game.move_cursor (game.world_to_screen (target.pos))
                      time.sleep (0.01)
                      q_spell.trigger(False)
                      time.sleep (0.01)
                      game.move_cursor (before_cpos)
    
    if use_Wclear and IsReady(game, w_spell) and game.player.mana>=8:
            target = GetBestJungleInRange (game, w["Range"])
            if target:
              if game.player.pos.distance(target.pos) <= w["Range"]:
                if not getBuff(game.player, "AuraofDespair")  :
                
                    w_spell.trigger(False)
            if not target:
                if getBuff(game.player, "AuraofDespair") :
                            w_spell.trigger(False)
    
    if use_Eclear and IsReady(game, e_spell):
        creep = GetBestJungleInRange(game, e["Range"])
        if creep:
            if game.player.mana>=30:
                e_spell.move_and_trigger(game.world_to_screen(creep.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo, use_w_in_combo
    global combo_key, laneclear_key
    global use_Qclear, use_Wclear, use_Eclear
    global MaxRCountForUse

    if game.player.is_alive and game.is_point_on_screen(game.player.pos)  :
        if game.was_key_pressed(laneclear_key):
            Farmclear(game)
        if game.was_key_pressed(combo_key):
            Combo(game)



    

    
    





    
    
    

