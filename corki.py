from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
import sys
from commons.damage_calculator import *
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-corki",
    "author": "SA1",
    "description": "SA1-corki",
    "target_champ": "corki",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_e_in_combo = True
use_w_in_combo = True
use_r_in_combo= True

lane_clear_with_q = True
lane_clear_with_e = True
lane_clear_with_r = True

jungle_clear_with_q = True
jungle_clear_with_r = True
jungle_clear_with_e = True

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 825}
w = {"Range": 800}
e = {"Range": 690}
r = {"Range": 1300}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e,jungle_clear_with_r
    global jungle_clear_with_q, jungle_clear_with_e,lane_clear_with_r
    
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo", True)
    
    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    lane_clear_with_r = cfg.get_bool("lane_clear_with_r", True)

    jungle_clear_with_q = cfg.get_bool("jungle_clear_with_q", True)
    jungle_clear_with_r = cfg.get_bool("jungle_clear_with_r", True)
    jungle_clear_with_e = cfg.get_bool("jungle_clear_with_e", True)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e,lane_clear_with_r
    global jungle_clear_with_q, jungle_clear_with_e,jungle_clear_with_r
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("jungle_clear_with_r", jungle_clear_with_r)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

    cfg.set_bool("jungle_clear_with_q", jungle_clear_with_q)
    cfg.set_bool("jungle_clear_with_r", jungle_clear_with_r)
    cfg.set_bool("jungle_clear_with_e", jungle_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_e,lane_clear_with_r
    global jungle_clear_with_q, jungle_clear_with_e,jungle_clear_with_r
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    ui.separator ()
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        lane_clear_with_r = ui.checkbox("Laneclear with R", lane_clear_with_r)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
        jungle_clear_with_r = ui.checkbox("Jungle with R", jungle_clear_with_r)
        ui.treepop()

    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()
    
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


mana_q=[60,70,80,90,100]
def Combo(game):
    global use_q_in_combo, use_e_in_combo,use_r_in_combo
    global q, w, e, r

    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    e_spell = getSkill(game, "E")

    
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana>=mana_q[game.player.Q.level -1]:
                
                targetQ = TargetSelector (game,825)
                
                if targetQ :
                            
                            q_travel_time = (825/9999) + 0.250
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 825 :
                                if  game.player.mana >= 70:
                                    if not q_spell.isActive and not r_spell.isActive and not e_spell.isActive:
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            
    
    if use_e_in_combo and IsReady(game, e_spell) :
                targetR=TargetSelector(game,690)
                if targetR:
                    if game.player.pos.distance (targetR.pos) <= 690 :
                        if  game.player.mana >= 50:
                            if not q_spell.isActive and not r_spell.isActive and not e_spell.isActive:
                                e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
    if use_r_in_combo and IsReady(game, r_spell) :
                
                targetR = TargetSelector (game,1300)
                if targetR :
                    if game.player.R.timeCharge >0:
                       if not IsCollisioned(game, targetR):
                            e_travel_time = (1300/2000) +0.250
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1300 :
                                if  game.player.mana >= 20:
                                    if not q_spell.isActive and not r_spell.isActive and not e_spell.isActive:
                                        r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    

        
    
def Laneclear(game):
    global q, w, e, r
    global lane_clear_with_q,lane_clear_with_e,lane_clear_with_r
    global combo_key, laneclear_key
    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    e_spell = getSkill(game, "E")

    
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) and game.player.mana>=mana_q[game.player.Q.level -1]:
                
                targetQ = GetBestMinionsInRange (game,825)
                
                if targetQ :
                            
                            q_travel_time = 825/1000
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 825 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            
    
    if lane_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestMinionsInRange(game,690)
                if targetR:
                    if game.player.pos.distance (targetR.pos) <= 690 :
                        if  game.player.mana >= 50:
                            e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
    if lane_clear_with_r and IsReady(game, r_spell) :
                targetR = GetBestMinionsInRange (game,1300)
                if targetR:
                    if game.player.pos.distance (targetR.pos) <= 1300 :
                        if  game.player.mana >= 20:
                            if game.player.R.timeCharge >0:
                                r_spell.move_and_trigger(game.world_to_screen(targetR.pos))


def Jungleclear(game):
    global q, w, e, r
    global combo_key, laneclear_key
    global jungle_clear_with_q, jungle_clear_with_e,jungle_clear_with_r
    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    e_spell = getSkill(game, "E")

    
    before_cpos = game.get_cursor()
    if jungle_clear_with_q and IsReady(game, q_spell) and game.player.mana>=mana_q[game.player.Q.level -1]:
                
                targetQ = GetBestJungleInRange (game,825)
                
                if targetQ :
                            
                            q_travel_time = 825/1000
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 825 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            
    
    if jungle_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestJungleInRange(game,690)
                if targetR:
                    if game.player.pos.distance (targetR.pos) <= 690 :
                        if  game.player.mana >= 50:
                            e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
    if jungle_clear_with_r and IsReady(game, r_spell) :
                targetR = GetBestJungleInRange (game,1300)
                if targetR:
                    if game.player.pos.distance (targetR.pos) <= 1300 :
                        if  game.player.mana >= 50:
                            if game.player.R.timeCharge >0:
                                r_spell.move_and_trigger(game.world_to_screen(targetR.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q
    global jungle_clear_with_q,jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player


    
    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
