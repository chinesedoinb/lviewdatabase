from ctypes import cast
from winstealer import *
import orb_walker
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from orb_walker import *
import json, time, math
import time
import urllib3, json, urllib, ssl
from commons.targit import *
# Get player stats from local server


winstealer_script_info = {
    "script": "SA1-Veigar",
    "author": "SA1",
    "description": "SA1-Veigar",
    "target_champ": "veigar",
}

combo_key = 57
LaneClear_key = 35

use_q_in_lasthit = False

use_q_in_combo = False
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

ewq=False

use_q_in_lane=True
use_e_in_lane=True
use_w_in_lane=True


draw_q_range = False
draw_w_range = False
draw_e_range = False

evade_pos = 0
lastQ =0
Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 100}
R = {"Slot": "R", "Range": 2500}



def winstealer_load_cfg(cfg):
    global ewq,use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key

    combo_key = cfg.get_int ("combo_key", 57)

    ewq=cfg.get_bool("ewq",False)
    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)

    LaneClear_key = cfg.get_int ("LaneClear_key", 46)

    use_q_in_lane = cfg.get_bool ("use_q_in_laneClear", True)
    use_w_in_lane = cfg.get_bool ("use_w_in_laneClear", True)
    use_e_in_lane = cfg.get_bool ("use_e_in_laneClear", True)



def winstealer_save_cfg(cfg):
    global ewq,use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key

    cfg.set_int ("combo_key", combo_key)

    cfg.set_bool("ewq",ewq)
    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)
    cfg.set_bool ("use_r_in_combo", use_r_in_combo)

    cfg.set_int ("LaneClear_key", LaneClear_key)
    cfg.set_bool ("use_q_in_laneClear", use_q_in_lane)
    cfg.set_bool ("use_w_in_laneClear", use_w_in_lane)
    cfg.set_bool ("use_e_in_laneClear", use_e_in_lane)


def winstealer_draw_settings(game, ui):
    global ewq,use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key


    ui.text("SA1-Veigar:1.0.0.0")
    ui.separator ()
    ewq=ui.checkbox("E/W Mode : E > W > Q",ewq)

    ui.separator()

    combo_key = ui.keyselect ("Combo Key", combo_key)
    use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
    use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
    use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)

    use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo) # not work atm


    ui.separator ()
    #Lane Clear
    LaneClear_key = ui.keyselect ("Lane Clear", LaneClear_key)
    use_q_in_lane = ui.checkbox ("Use Q in Lane Clear", use_q_in_lane)
    use_w_in_lane = ui.checkbox ("Use W in Lane Clear", use_w_in_lane)
    

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


# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats



def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [175, 250, 325]
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
    global ewq,use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    before_cpos = game.get_cursor ()
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")

    
    if ewq:
        if use_e_in_combo and IsReady(game, e_spell):
            targetE=TargetSelector (game,1000)
            
            if targetE:
                # for buff in targetE.buffs:
                #         print(buff.name)
                e_travel_time=800/200
                predicted_pos = predict_pos (targetE, e_travel_time)
                predicted_target = Fake_target (targetE.name, predicted_pos, targetE.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 800:
                    if game.player.mana >= 90:
                        game.move_cursor(game.world_to_screen(predicted_target.pos).add(Vec2(0, 150)))
                        time.sleep(0.01)
                        e_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)
            
        if use_w_in_combo and IsReady(game, w_spell) :
            targetW = TargetSelector (game,900)
            if targetW :
                w_travel_time = 900/ 20
                predicted_pos = predict_pos (targetW, w_travel_time)
                predicted_target = Fake_target (targetW.name, predicted_pos, targetW.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 900 and getBuff(targetW, "veigareventhorizonstun"):
                    if  game.player.mana >= 70:
                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                        time.sleep(0.01)
                        w_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)
        if use_q_in_combo and IsReady(game, q_spell) :
            targetQ = TargetSelector (game,900)
            if targetQ :
                q_travel_time = 900/1200
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 900 and not IsCollisioned(game, targetQ):
                    if  game.player.mana >= 50:
                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                        time.sleep(0.01)
                        q_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)                
    ###########################################################so_what######################################################################
    else:
    
        if use_e_in_combo and IsReady(game, e_spell):
            targetE=TargetSelector (game,1000)
            
            if targetE:
                # for buff in targetE.buffs:
                #         print(buff.name)
                e_travel_time=900/20
                predicted_pos = predict_pos (targetE, e_travel_time)
                predicted_target = Fake_target (targetE.name, predicted_pos, targetE.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 900:
                    if game.player.mana >= 90:
                        game.move_cursor(game.world_to_screen(predicted_target.pos).add(Vec2(0, 150)))
                        time.sleep(0.01)
                        e_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)

        if use_q_in_combo and IsReady(game, q_spell) :
            targetQ = TargetSelector (game,700)
            if targetQ :
                q_travel_time = 900/1200
                predicted_pos = predict_pos (targetQ, q_travel_time)
                predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 900 and not IsCollisioned(game, targetQ):
                    if  game.player.mana >= 50:
                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                        time.sleep(0.01)
                        q_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)
                    
        if use_w_in_combo and IsReady(game, w_spell) :
            targetW = TargetSelector (game,900)
            if targetW :
                w_travel_time = 900/ 20
                predicted_pos = predict_pos (targetW, w_travel_time)
                predicted_target = Fake_target (targetW.name, predicted_pos, targetW.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= 900 :
                    if  game.player.mana >= 70:
                        game.move_cursor(game.world_to_screen(predicted_target.pos))
                        time.sleep(0.01)
                        w_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)

    if use_r_in_combo and IsReady(game, r_spell) :
        targetR=TargetSelector(game,900)
        if targetR:
                if RDamage(game, targetR)>=targetR.health and game.player.mana >= 100:
                        game.move_cursor(game.world_to_screen(targetR.pos))
                        time.sleep(0.01)
                        r_spell.trigger(False)
                        time.sleep(0.01)
                        game.move_cursor(before_cpos)
            

def LaneClear(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")

 # --------------Lane Clear-----------------
    if use_q_in_lane and IsReady(game, q_spell) and game.player.mana >= 50 :
                minion = GetBestMinionsInRange(game, 900)
                if minion and minion.health <=100 :
                    q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if use_w_in_lane and IsReady(game, w_spell) and game.player.mana >= 70 :
                minion = GetBestMinionsInRange(game, 900)
                if minion:
                    w_spell.move_and_trigger(game.world_to_screen(minion.pos))


#--------------jungle Clear-----------------
    
    


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key
    global Q, W, E, R
    target = GetBestTargetsInRange (game, 2000)
    # if target:
    #     game.draw_circle_world (target.pos, 200, 100, 5, Color.GREEN)
    # playerStart = game.world_to_screen (game.player.pos)
    # before_cpos = game.get_cursor ()

    # game.draw_line (playerStart, before_cpos, 10, Color.WHITE)

    if game.player.is_alive and game.is_point_on_screen(game.player.pos) :
        if game.is_key_down(LaneClear_key):
            LaneClear(game)
            
        if game.is_key_down(combo_key):
            Combo(game)
            