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
    "script": "SA1-Brand",
    "author": "SA1",
    "description": "SA1-Brand",
    "target_champ": "brand",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True
smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 1000}
w = {"Range": 600}
e = {"Range": 600}
r = {"Range": 3000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

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
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)


    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
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
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)


    ui.text("Ls-Brand : 1.0.0.0")
    ui.text("LifeSaver#3592")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo=ui.checkbox("User R in Combo",use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        lane_clear_with_w = ui.checkbox("Laneclear with W ", lane_clear_with_w)
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

    

#mana_q = [50,60,70,80,90]
#mana_w = [70,80,90,100,110]
#mana_e = [50,48,46,44,42]
#mana_r = 100 ##for mana check later update???


########################
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




def basicPredication(game,target,spellRadius,missileSpeed,castDelay):
    
    player = game.player
    

    direction = target.pos.sub (target.prev_pos).normalize ()
    # In case the target wasn't moving
    if math.isnan (direction.x):
        direction.x = 0.0
    if math.isnan (direction.y):
        direction.y = 0.0
    if math.isnan (direction.z):
        direction.z = 0.0
    if direction.x == 0.0 and direction.z == 0.0:
        return target.pos


    extender=target.gameplay_radius
    distance=spellRadius
    steps= target.pos.distance(target.prev_pos) / distance
    if steps>0 and steps <1000:
        
            center= target.prev_pos  + direction * distance 
            pt_a= center - direction * extender
            pt_b=center + direction * extender

            if missileSpeed !=0:
                flytime= distance(player.pos,target.pos) / missileSpeed
            t = flytime + castDelay 
            arrive_time_a = distance(target.pos, pt_a) / target.movement_speed
            arrive_time_b = distance(target.pos, pt_b) / target.movement_speed


            predicted_pos = center
            if (min(arrive_time_a , arrive_time_b) <= t and max(arrive_time_a,arrive_time_b) >= t):
                return center

        
    # Target movement speed
    # target_speed = target.movement_speed

    # # The distance that the target will have traveled after the given duration
    # distance_to_travel = target_speed * duration

    # return target.pos.add (direction.scale (distance_to_travel))

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo
    global q, w, e, r,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = TargetSelector (game,1050)
                if targetQ :
                            q_travel_time = 1050/1200
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1050 and not IsCollisioned(game, targetQ):
                                if  game.player.mana >= 50 and lastQ + 2 < game.time:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    lastQ=game.time

    if use_e_in_combo and IsReady(game, e_spell) :
                targetR=TargetSelector(game,625)
                if targetR:
                            if game.player.pos.distance (targetR.pos) <= 625 :
                                if  game.player.mana >= 70:
                                    e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
    if use_w_in_combo and IsReady(game, w_spell) :
                targetQ = TargetSelector (game,900)
                if targetQ :
                            q_travel_time = 900/20
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            # p=basicPredication(game ,targetQ ,120.0 , 999999.f , 0.627)
                            if game.player.pos.distance (predicted_target.pos) <= 900 :
                                if  game.player.mana >= 70 and lastQ + 1 < game.time:
                                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    lastQ=game.time

    if use_r_in_combo and IsReady(game, r_spell) :
                targetR=TargetSelector(game,750)
                if targetR:
                            hp = int(targetR.health / targetR.max_health * 100)
                            if game.player.pos.distance (targetR.pos) <= 750 :
                                if  game.player.mana >= 100:
                                    if RDamage(game, targetR) >= targetR.health or hp<=30:
                                        r_spell.move_and_trigger(game.world_to_screen(targetR.pos))

def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global spell_priority, combo_key, laneclear_key, killsteal_key
    #q = {"Range": 600}
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestMinionsInRange(game,1050)
                if targetQ :
                            q_travel_time = 1050/1200
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1050 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            

    if lane_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestMinionsInRange(game,625)
                if targetR:
                                if  game.player.mana >= 90:
                                    e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                         
    if lane_clear_with_w and IsReady(game, w_spell)  :
                targetW = GetBestMinionsInRange (game,900)
                if targetW :
                            game.move_cursor(game.world_to_screen(targetW.pos))
                            time.sleep(0.01)
                            w_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if jungle_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestJungleInRange(game,1050)
                if targetQ :
                            q_travel_time = 1050/1200
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 1050 :
                                if  game.player.mana >= 70:
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            

    if jungle_clear_with_e and IsReady(game, e_spell) :
                targetR=GetBestJungleInRange(game,1100)
                if targetR:
                                if  game.player.mana >= 90:
                                    e_spell.move_and_trigger(game.world_to_screen(targetR.pos))
                        
    if jungle_clear_with_w and IsReady(game, w_spell):
                targetW = GetBestJungleInRange (game,900)
                if targetW :
                            game.move_cursor(game.world_to_screen(targetW.pos))
                            time.sleep(0.01)
                            w_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r
    
    self = game.player
    player = game.player



        # game.draw_circle(game.world_to_screen(p2),50 , 100 , 10 , Color.GREEN )
    if self.is_alive  :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            
