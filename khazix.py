from ctypes import cast
from Pyke import is_collisioned
from winstealer import *
import orb_walker
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from orb_walker import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 khazix",
    "author": "SA1",
    "description": "SA1 khazix",
    "target_champ": "khazix",
}

combo_key = 57
harass_key = 46
laneclear_key=47

use_q_in_lasthit = False

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

use_q_in_lane = True
use_w_in_lane = True
use_e_in_lane = True
use_r_in_lane = True

Flag_used=False

draw_q_range = False
draw_w_range = False
draw_e_range = False

evade_pos = 0
lastQ =0
Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 1180}
R = {"Slot": "R", "Range": 2500}



def winstealer_load_cfg(cfg):
    global use_q_in_lane,use_w_in_lane,use_e_in_lane,use_r_in_lane
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,laneclear_key

    combo_key = cfg.get_int ("combo_key", 57)
    laneclear_key=cfg.get_int ("laneclear_key", laneclear_key)

    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)


    use_q_in_lane = cfg.get_bool ("use_q_in_lane", True)
    use_w_in_lane = cfg.get_bool ("use_w_in_lane", True)
    use_e_in_lane = cfg.get_bool ("use_e_in_lane", True)
    use_r_in_lane = cfg.get_bool ("use_r_in_lane", True)


def winstealer_save_cfg(cfg):
    global use_q_in_lane,use_w_in_lane,use_e_in_lane,use_r_in_lane
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,laneclear_key

    cfg.set_int ("combo_key", combo_key)
    cfg.set_int ("laneclear_key", laneclear_key)

    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)
    cfg.set_bool ("use_r_in_combo", use_r_in_combo)

    cfg.set_bool ("use_q_in_lane", use_q_in_lane)
    cfg.set_bool ("use_w_in_lane", use_w_in_lane)
    cfg.set_bool ("use_e_in_lane", use_e_in_lane)
    cfg.set_bool ("use_r_in_lane", use_r_in_lane)
    

def winstealer_draw_settings(game, ui):
    global use_q_in_lane,use_w_in_lane,use_e_in_lane,use_r_in_lane
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,laneclear_key



    # ui.text("LifeSaver - khazix:1.0.0.0")
    ui.separator ()

    combo_key = ui.keyselect ("Combo Key", combo_key)
    laneclear_key=ui.keyselect ("Laneclear Key", laneclear_key)
    
    if ui.treenode ("Combo Setting "):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        ui.treepop()
    if ui.treenode ("Lane/Jungle Setting "):
        use_q_in_lane = ui.checkbox ("Use Q in Lane/Jungle", use_q_in_lane)
        use_w_in_lane = ui.checkbox ("Use W in Lane/Jungle", use_w_in_lane)
        use_e_in_lane = ui.checkbox ("Use E in Lane/Jungle", use_e_in_lane)
        ui.treepop()
def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 350 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.R.level == 2:
        damage = 500 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.R.level == 3:
        damage = 650 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    return damage

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


w_mana=[55,60,65,70,75]

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    player=game.player
    lastq=0
    global Flag_used

    
    if use_q_in_combo and IsReady(game,q_spell) and game.player.mana >= 20 :
        if player.Q.name=="khazixq":
            target=TargetSelector(game,325)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))

        elif player.Q.name=="khazixqlong":
            target=TargetSelector(game,375)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        
    if use_w_in_combo and IsReady(game,w_spell) and player.mana>=w_mana[player.W.level -1]:
            target=TargetSelector(game,1000)
            if ValidTarget(target):
                disToPlayer=game.player.pos.distance (target.pos)
                e_travel_time = disToPlayer/828
                predicted_pos = predict_pos (target, e_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if lastq+1<game.time and disToPlayer<900 and not IsCollisioned(game,predicted_target):
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        lastq=game.time
                        
    if use_e_in_combo and IsReady(game,e_spell) and player.mana>=50:
            if player.E.name =="khazixe":
                target=TargetSelector(game,700)
                if ValidTarget(target):
                    disToPlayer=game.player.pos.distance (target.pos)
                    if disToPlayer>500 :
                            e_spell.move_and_trigger(game.world_to_screen(target.pos))

            elif player.E.name =="khazixelong":
                target=TargetSelector(game,900)
                if ValidTarget(target):
                    disToPlayer=game.player.pos.distance (target.pos)
                    if disToPlayer>500 :
                            e_spell.move_and_trigger(game.world_to_screen(target.pos))              


    
def Harass(game):
    pass
def LaneClear(game):
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    player=game.player
    lastq=0

    if use_q_in_lane and IsReady(game,q_spell) and game.player.mana >= 20 :
        if player.Q.name=="khazixq":
            target=GetBestMinionsInRange(game,325)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))

        elif player.Q.name=="khazixqlong":
            target=GetBestMinionsInRange(game,375)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        
    if use_w_in_lane and IsReady(game,w_spell) and player.mana>=w_mana[player.W.level -1]:
            target=GetBestMinionsInRange(game,1000)
            if ValidTarget(target):
                if lastq+1<game.time :
                        w_spell.move_and_trigger(game.world_to_screen(target.pos))
                        lastq=game.time


    if use_q_in_lane and IsReady(game,q_spell) and game.player.mana >= 20 :
        if player.Q.name=="khazixq":
            target=GetBestJungleInRange(game,325)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))

        elif player.Q.name=="khazixqlong":
            target=GetBestJungleInRange(game,375)
            if ValidTarget(target) :
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))
        
        
    if use_w_in_lane and IsReady(game,w_spell) and player.mana>=w_mana[player.W.level -1]:
            target=GetBestJungleInRange(game,1000)
            if ValidTarget(target):
                if lastq+1<game.time:
                        w_spell.move_and_trigger(game.world_to_screen(target.pos))
                        lastq=game.time

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,laneclear_key
    global Q, W, E, R

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) :

        if game.is_key_down(combo_key):
            Combo(game)
        if game.is_key_down(laneclear_key): 
            LaneClear(game)
            