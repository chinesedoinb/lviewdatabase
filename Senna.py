import sys
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Senna",
    "author": "SA1",
    "description": "SA1-Senna",
    "target_champ": "senna",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True

use_r_in_combo = False

lane_clear_with_q = True
lane_clear_with_w = True


jungle_clear_with_q = True
jungle_clear_with_w = True

smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 700}
w = {"Range": 370}

r = {"Range": 500}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}
mana_q = [70, 80, 90, 100, 110]
mana_w = [50, 55, 60, 65, 70]
r_range = [400, 650, 900]
# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)


    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)

    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w,smart_combo
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)

    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w,smart_combo
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)


    ui.text("SA1-Senna : 1.0.0.0")
    ui.text("E manual")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Use Q in Lane/Jungle", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Use W in Lane/Jungle", lane_clear_with_w)
        ui.treepop()


    

#mana_q = [50,60,70,80,90]
#mana_w = [70,80,90,100,110]
#mana_e = [50,48,46,44,42]
#mana_r = 100 ##for mana check later update???


########################
class Fake_target():
    def __init__(self, id_, name, pos, gameplay_radius):
        self.id = id_
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
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [100,200,300]
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

lastQ=0


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
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [250,375,500]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.armour
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage                
            
def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo
    global q, w, e, r,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
            target=TargetSelector(game,600)
            
            if target:
                if game.player.mana>=mana_q[game.player.Q.level -1]:
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))   

    if use_w_in_combo and IsReady(game, w_spell) :
                target=TargetSelector(game,1250)
                if target:
                    current_q_travel_time=1250/1000
                    predicted_pos = predict_pos(target, current_q_travel_time)
                    predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)

                    if game.player.pos.distance (predicted_target.pos)<=1000 :
                        if game.player.mana>=mana_w[game.player.W.level -1]:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))                           


    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana>=100:
            target=TargetSelector(game,25000)
            if target:
                    current_q_travel_time=25000/2000
                    predicted_pos = predict_pos(target, current_q_travel_time)
                    predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)

                    if game.player.pos.distance (predicted_target.pos)<=25000 :
                        if QDamage(game, target) > effHP(game, target):
                            r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    
    
def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w
    global spell_priority, combo_key, laneclear_key, killsteal_key,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()

    if lane_clear_with_q and IsReady(game, q_spell) :
            target=GetBestMinionsInRange(game,600)
            
            if target:
                if game.player.mana>=mana_q[game.player.Q.level -1]:
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))   

    if lane_clear_with_w and IsReady(game, w_spell) :
                target=GetBestMinionsInRange(game,1250)
                if target:
                    current_q_travel_time=1250/1000
                    predicted_pos = predict_pos(target, current_q_travel_time)
                    predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)

                    if game.player.pos.distance (predicted_target.pos)<=1000 :
                        if game.player.mana>=mana_w[game.player.W.level -1]:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos)) 


    
    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()

    if lane_clear_with_q and IsReady(game, q_spell) :
            target=GetBestJungleInRange(game,600)
            
            if target:
                if game.player.mana>=mana_q[game.player.Q.level -1]:
                    q_spell.move_and_trigger(game.world_to_screen(target.pos))   

    if lane_clear_with_w and IsReady(game, w_spell) :
                target=GetBestJungleInRange(game,1250)
                if target:
                    current_q_travel_time=1250/1000
                    predicted_pos = predict_pos(target, current_q_travel_time)
                    predicted_target = Fake_target(target.id, target.name, predicted_pos, target.gameplay_radius)

                    if game.player.pos.distance (predicted_target.pos)<=1000 and not IsCollisioned(game, predicted_target):
                        if game.player.mana>=mana_w[game.player.W.level -1]:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))  
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w
    global jungle_clear_with_q, jungle_clear_with_w
    global q, w, e, r
    r_spell = getSkill(game, "R")
    self = game.player
    player = game.player

 

        
    if self.is_alive:
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            
