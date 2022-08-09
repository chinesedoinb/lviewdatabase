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
    "script": "Caitlyn",
    "author": "Caitlyn",
    "description": "Caitlyn",
    "target_champ": "caitlyn"
}

lastE = 0

combo_key = 0

use_q_in_combo = True
use_w_on_immobile = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo = True

move_in_combo = True

use_e_evade = True

q = {'Range': 1300 }
w = {'Range': 800}
e = {'Range': 800}
r = {'Range': 3500}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade
    combo_key = cfg.get_int ("combo_key", 0)
    move_in_combo = cfg.get_bool ("move_in_combo", True)

    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_on_immobile = cfg.get_bool ("use_w_on_immobile", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)

    use_e_evade = cfg.get_bool ("use_e_evade", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade
    cfg.set_int ("combo_key", combo_key)

    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_on_immobile", use_w_on_immobile)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)

    cfg.set_bool ("use_r_in_combo", use_r_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)

    cfg.set_bool ("move_in_combo", move_in_combo)

    cfg.set_bool ("use_e_evade", use_e_evade)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_on_immobile, use_r_in_combo, use_e_in_combo, use_w_in_combo
    global combo_key, move_in_combo
    global use_e_evade
    ui.text("SA1")
    
    combo_key = ui.keyselect ("Combo key", combo_key)
    # move_in_combo = ui.checkbox ("Move in combo", move_in_combo)

    if ui.treenode ("Setting [Q]"):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        ui.treepop ()

    if ui.treenode ("Setting [W]"):
        use_w_on_immobile = ui.checkbox ("Use W on Immobile", use_w_on_immobile)
        # ui.text("Only choose one!")
        # use_w_in_combo =  ui.checkbox ("Use W in Combo", use_w_in_combo)
        ui.treepop ()

    if ui.treenode ("Setting [E]"):
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        use_e_evade = ui.checkbox ("Use E to escape if target is close", use_e_evade)
        ui.treepop ()
    if ui.treenode ("Setting [R]"):
        use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo)
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
Q_mana=[50,60,70,80,90]
lastq=0


def Combo(game):
    global lastq
    before_cpos = game.get_cursor ()
    q_spell = getSkill (game, 'Q')
    e_spell = getSkill (game, 'E')
    w_spell = getSkill (game, 'W')
    r_spell = getSkill (game, 'R')

    # if move_in_combo:
    #     game.press_right_click ()


#added for when the target get trapped or cait used her E :
    targetW = TargetSelector (game, 3000)
    if ValidTarget (targetW):
        if getBuff (targetW, "CaitlynEMissile") or getBuff (targetW, "CaitlynWSnare"):
            game.move_cursor (game.world_to_screen (targetW.pos))
            game.press_right_click ()
            game.move_cursor (before_cpos)
            game.press_right_click ()
#end
    
    if use_q_in_combo and IsReady (game, q_spell):
        target = TargetSelector (game, 1100)

        if target:
            disToPlayer=game.player.pos.distance (target.pos)
            q_travel_time = disToPlayer/ 2000
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.mana>=Q_mana[game.player.Q.level - 1] and lastq+2<=game.time:
                q_spell.move_and_trigger(game.world_to_screen (predicted_target.pos))
                lastq=game.time

    if use_w_on_immobile and IsReady (game, w_spell):
        
        target = TargetSelector (game, w["Range"])
        if target is not None:
            if is_immobile (game, target) and game.player.mana>=20:
                w_spell.move_and_trigger(game.world_to_screen (target.pos))

    if use_e_in_combo and IsReady (game, e_spell):
        target = TargetSelector (game, e['Range'])

        if target:
            disToPlayer=game.player.pos.distance (target.pos)
            e_travel_time = disToPlayer / 1600
            
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.mana>=75 and not IsCollisioned (game,predicted_target):
                e_spell.move_and_trigger(game.world_to_screen (predicted_target.pos))
                
    if use_r_in_combo and IsReady (game, r_spell):
        target = TargetSelector (game, r["Range"])
        playerAAdist=game.player.atkRange + game.player.gameplay_radius +100

        if ValidTarget (target):
            if target.pos.distance(game.player.pos)<= playerAAdist:
                if  getBuff(target,"CaitlynEMissile"):
                    if (RDamage (game, target) >= target.health):
                            r_spell.move_and_trigger(game.world_to_screen (target.pos))

            if target.pos.distance(game.player.pos)>= 1100:
                    if (RDamage (game, target) >= target.health):
                            r_spell.move_and_trigger(game.world_to_screen (target.pos))
    # if use_w_in_combo and IsReady (game,w_spell):
    #     target = TargetSelector (game, w['Range'])
    #     if ValidTarget (target):
    #         e_travel_time = w['Range'] / 2
    #         predicted_pos = predict_pos (target, e_travel_time)
    #         predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
    #         if  game.player.mana>=20:
    #              w_spell.move_and_trigger(game.world_to_screen (predicted_target.pos))



def Evade(game):
    global use_e_evade
    global lastE
    e_spell = getSkill (game, "E")
    target = TargetSelector (game, 375)
    if target and target.atkRange < 375:
        if (
                use_e_evade
                and lastE + 1 < game.time
                and IsReady (game, e_spell)
                and game.player.mana > 75
        ):
            lastE = game.time
            e_spell.move_and_trigger (game.world_to_screen (target.pos))


def winstealer_update(game, ui):
    self = game.player

    # target = TargetSelector (game, 1500)
    # if target:
    #     disToPlayer=game.player.pos.distance (target.pos)
    #     q_travel_time = 1250/2200
        
    #     predicted_pos = predict_pos (target, q_travel_time)
    #     predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
        
    #     game.draw_line(game.world_to_screen(target.pos), game.world_to_screen(predicted_target.pos), 2, Color.GREEN)
    # target= TargetSelector(game,1000)
    # if target:
    #     for b in game.player.buffs:
    #         # if  b.name =="CaitlynEMissile":
    #             print(b.name)
    if self.is_alive and self.is_visible :
        # print (w_spell.timeCharge)
        if use_e_evade:
            Evade (game)
        if game.was_key_pressed (combo_key):
            Combo (game)








