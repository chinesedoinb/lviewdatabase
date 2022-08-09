import sys
from commons.damage_calculator import *
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Draven",
    "author": "SA1",
    "description": "Draven",
    "target_champ": "draven",
}

combo_key = 57
laneclear_key = 47
changeCombo=1
use_q_in_combo = True
use_e_in_combo = True
use_w_in_combo = True
use_r_in_combo=True

forceAXE=True

lane_clear_with_q = True
lane_clear_with_w = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 900}
w = {"Range": 800}
e = {"Range": 800}
r = {"Range": 450}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,changeCombo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range,forceAXE
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,use_r_in_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    forceAXE=cfg.get_bool("forceAXE",True)

    changeCombo=cfg.get_int("changeCombo",changeCombo)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", True)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)

    jungle_clear_with_q = cfg.get_bool("jungle_clear_with_q", True)
    jungle_clear_with_w = cfg.get_bool("jungle_clear_with_w", True)
    jungle_clear_with_e = cfg.get_bool("jungle_clear_with_e", True)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,changeCombo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w,forceAXE
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,use_r_in_combo
    

    cfg.set_int("changeCombo",changeCombo)

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("forceAXE",forceAXE)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)

    cfg.set_bool("jungle_clear_with_q", jungle_clear_with_q)
    cfg.set_bool("jungle_clear_with_w", jungle_clear_with_w)
    cfg.set_bool("jungle_clear_with_e", jungle_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,changeCombo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,forceAXE,use_r_in_combo

    ui.text("Ls-Draven 1.0.0.0")
    ui.separator ()
    ui.text("LifeSaver#3592")
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    ui.separator ()

    forceAXE=ui.checkbox("Force To catch Axe",forceAXE)
    changeCombo=ui.listbox("",["Force To catch Axe","Smooth catch Axe"],changeCombo)

    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo=ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Laneclear with W", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        jungle_clear_with_w = ui.checkbox("Jungle with W", jungle_clear_with_w)
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
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


# def catchAXE(game):
#     global forceAXE

#     for missle in game.missiles:

#         if missle.name=="dravenspinningreturncatch"  or missle.name=="dravenspinningreturn" and game.is_point_on_screen(game.player.pos):
#             if forceAXE:
#                     game.move_cursor(game.world_to_screen(missle.end_pos))
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
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [175,275,375]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ad)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage
t =0
def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range,changeCombo
    global combo_key, laneclear_key,forceAXE,t
    global q, w, e, r,lastQ
    before_cpos = game.get_cursor()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell=getSkill(game, "R")
    Qspin0=getBuff(game.player, "DravenSpinning")==False
    Qspin1=getBuff(game.player, "DravenSpinning")==True
    if use_q_in_combo:
            targetAXE=TargetSelector(game,800)

            

            for missle in game.missiles:
                if missle.name=="DravenSpinningAttack"  or missle.name=="dravenspinningreturn"  and game.is_point_on_screen(game.player.pos):
                    
                    
                            if targetAXE:
                                        if changeCombo == 1:
                                            if game.player.pos.distance(missle.end_pos) <=120:
                                                if use_w_in_combo and IsReady(game, w_spell):
                                                    w_spell.trigger(False)     
                                                game.move_cursor(game.world_to_screen(missle.end_pos))
                                            else:
                                                game.move_cursor(game.world_to_screen(missle.end_pos))
                                                time.sleep(0.01)
                                                game.move_cursor(before_cpos)
                                        if changeCombo ==0 :
                                            game.move_cursor(game.world_to_screen(missle.end_pos))
            if targetAXE:                                            
                if not getBuff(game.player, "DravenSpinning") and not getBuff(game.player, "dravenspinningattack"):
                        if IsReady(game, q_spell) :
                                q_spell.trigger(False)
                            
                
    if use_e_in_combo and IsReady(game, e_spell) :
                targetR=TargetSelector(game,1050)
                if targetR:
                    
                            e_travel_time = 1050/1600
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) >= 600 or game.player.pos.distance (predicted_target.pos) <= 350:
                                if  game.player.mana >= 70:
                                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        
    if use_w_in_combo and IsReady(game, w_spell) :
                targetW = TargetSelector (game,800)
                if targetW :
                    if game.player.mana>=150:
                        if game.player.pos.distance (targetW.pos) >= 650 :
                            w_spell.trigger(False)     
    if use_r_in_combo and IsReady(game, r_spell):
        target=TargetSelector(game,4000)
        if target:
            e_travel_time = 1050/1600
            predicted_pos = predict_pos (target, e_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance (predicted_target.pos) >= 800 :
                if  game.player.mana >= 100 and RDamage(game, target)>=target.health:
                    r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
def Laneclear(game):
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w,forceAXE
    global combo_key, laneclear_key
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")

    targetAXE=GetBestMinionsInRange(game,800)
    if lane_clear_with_q:

            for missle in game.missiles:
                if missle.name=="dravenspinningreturncatch"  or missle.name=="dravenspinningreturn" and game.is_point_on_screen(game.player.pos):
                    
                    if forceAXE:
                        if targetAXE:
                            game.move_cursor(game.world_to_screen(missle.end_pos))
            if not getBuff(game.player, "DravenSpinning") and not getBuff(game.player, "dravenspinningattack"):
                    if IsReady(game, q_spell) :
                            q_spell.trigger(False)
                           
                
                        
    if lane_clear_with_w and IsReady(game, w_spell) :
                targetW = GetBestJungleInRange (game,800)
                if targetW :
                    if game.player.mana>=150:
                        if game.player.pos.distance (targetW.pos) <= 650 :
                            w_spell.trigger(False)    

def Jungleclear(game):
    global q, w, e, r
    global combo_key, laneclear_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,forceAXE
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    targetAXE=GetBestJungleInRange(game,800)
    if jungle_clear_with_q:
        
            for missle in game.missiles:
                if missle.name=="dravenspinningreturncatch"  or missle.name=="dravenspinningreturn" and game.is_point_on_screen(game.player.pos):
                    
                    if forceAXE:
                        if targetAXE:
                            game.move_cursor(game.world_to_screen(missle.end_pos))
            if not getBuff(game.player, "DravenSpinning") and not getBuff(game.player, "dravenspinningattack"):
                    if IsReady(game, q_spell) :
                            q_spell.trigger(False)
                           
                
    if jungle_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestJungleInRange(game,1050)
                if targetR:
                    
                            e_travel_time = 1050/1600
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) >= 700 :
                                if  game.player.mana >= 70:
                                    e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        
    if jungle_clear_with_w and IsReady(game, w_spell) :
                targetW = GetBestJungleInRange (game,800)
                if targetW :
                    if game.player.mana>=150:
                        if game.player.pos.distance (targetW.pos) <= 650 :
                            w_spell.trigger(False)    

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player
    before_cpos = game.get_cursor()
    target=GetBestMinionsInRange(game,800)
    for missle in game.missiles:
        # d

        if missle.name=="dravenspinningreturncatch" and game.is_point_on_screen(game.player.pos):
            if forceAXE:
                    game.draw_circle_world(missle.end_pos, 100, 50, 1, Color.PURPLE)
                    # game.move_cursor(game.world_to_screen(missle.end_pos))
   
  
    if self.is_alive:
        if game.was_key_pressed(combo_key):
            Combo(game)
            
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
