from dis import dis
from msilib.schema import tables
from re import T
import sys
from turtle import distance
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
    "script": "SA1-velkoz",
    "author": "SA1",
    "description": "SA1-velkoz",
    "target_champ": "velkoz",
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


    ui.text("SA1-Velkoz : 1.0.0.0")
    # ui.text("Author : LifeSaver#3592")
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


def distanc(game,spell,target):
    dist=0
    disToPlayer=game.player.pos.distance (target.pos)
    if disToPlayer>0 and disToPlayer< spell.cast_range:
        dist=disToPlayer
        return dist
lastq=0
manaQ=[40,45,50,55,60]
manaW=[50,55,60,65,70]
manaE=[50,55,60,65,70]


def bffs(game, target):
    for buff in target.buffs:

        
        if 'stun' in buff.name.lower ():
            return True
      
        elif 'knockup' in buff.name.lower ():
            return True
        elif 'slow' in buff.name.lower ():
            return True    
    return False

spellTimer = Timer()
def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo,lastq,spellTimer
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana>=manaQ[game.player.Q.level -1] :
                targetQ = TargetSelector (game,1050)
                if targetQ and spellTimer.Timer():
                            
                            disToPlayer=game.player.pos.distance (targetQ.pos)
                            if disToPlayer>0 and disToPlayer< 1050:
                                e_travel_time = disToPlayer/1200
                            predicted_pos = game.GetPredication(targetQ,1050 ,1200,0.251)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (targetQ.pos)<=820 and not IsCollisioned(game,targetQ):
                                if not game.player.Q.name=="velkozqsplitactivate":
                                    if not q_spell.isActive and not w_spell.isActive and not e_spell.isActive:
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_pos))
                                        spellTimer.SetTimer(0.7)
                                        if get_distance(cursor_pos_vec3, game.world_to_screen(predicted_target.pos)) <20 :
                                            game.move_cursor(before_cpos)                                                                                       
                                            
    if use_e_in_combo and IsReady(game, e_spell) and game.player.mana>=manaE[game.player.E.level -1] :
                targetR=TargetSelector(game,810)
                e_travel_time=0
                if targetR:
                            # disToPlayer=game.player.pos.distance (targetR.pos)
                            # if disToPlayer>0 and disToPlayer< 810:
                            e_travel_time = (810/9999999 ) + 0.8
                            predicted_pos = predict_pos (targetR, e_travel_time)
                            predicted_target = Fake_target (targetR.name, predicted_pos, targetR.gameplay_radius)
                            if game.player.pos.distance (targetR.pos)<=780 and  spellTimer.Timer():
                                if not q_spell.isActive and not w_spell.isActive and not e_spell.isActive :
                                    if targetR.pos.distance (targetR.ai_navEnd)<=600 and game.player.pos.distance (targetR.ai_navEnd)<=810:
                                        e_spell.move_and_trigger(game.world_to_screen(targetR.ai_navEnd))
                                        spellTimer.SetTimer(0.4)
                                    else :
                                        e_spell.move_and_trigger(game.world_to_screen(predicted_pos))
                                        spellTimer.SetTimer(0.4)
                                    
    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1]:
                targetW = TargetSelector (game,1150)
                e_travel_time=0
                if targetW :
                            
                            disToPlayer=game.player.pos.distance (targetW.pos)
                            if disToPlayer>0 and disToPlayer< 1050:
                                e_travel_time = disToPlayer/1200
                            predicted_pos = predict_pos (targetW, e_travel_time)
                            predicted_target = Fake_target (targetW.name, predicted_pos, targetW.gameplay_radius)
                            

                            if  (
                                game.player.mana >= 70  
                                and game.player.pos.distance (targetW.pos)<=850 
                                and game.player.W.timeCharge>0) and  spellTimer.Timer():
                                    if not q_spell.isActive and not w_spell.isActive and not e_spell.isActive:

                                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                        spellTimer.SetTimer(0.4)

                        
    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana>=100: 
                targetR=TargetSelector(game,1575)
                if targetR:
                            hp = int(targetR.health / targetR.max_health * 100)
                            if game.player.pos.distance (targetR.pos) > 450 and hp<60:
                                if  game.player.mana >= 100:
                                        if not getBuff(game.player,"VelkozR"):
                                            game.move_cursor(game.world_to_screen(targetR.pos))
                                            r_spell.trigger(False)
                                        if getBuff(game.player,"VelkozR"):
                                            game.move_cursor(game.world_to_screen(targetR.pos))
                                        

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
    if lane_clear_with_q and IsReady(game, q_spell) and game.player.mana>=manaQ[game.player.Q.level -1] :
                targetQ = GetBestMinionsInRange (game,1050)
                if targetQ :
                                if not game.player.Q.name=="velkozqsplitactivate":
                                    q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                        

    if lane_clear_with_e and IsReady(game, e_spell) and game.player.mana>=manaE[game.player.E.level -1] :
                targetR=GetBestMinionsInRange(game,1250)
                if targetR:
                    e_spell.move_and_trigger(game.world_to_screen(targetR.pos))

                                    
    if lane_clear_with_w and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1]:
                targetW = GetBestMinionsInRange (game,1150)
                
                if targetW :
                        if  (
                                game.player.mana >= 70  
                                and game.player.W.timeCharge>0):
                                    w_spell.move_and_trigger(game.world_to_screen(targetW.pos))

    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if jungle_clear_with_q and IsReady(game, q_spell) and game.player.mana>=manaQ[game.player.Q.level -1] :
                targetQ = GetBestJungleInRange (game,1050)
                if targetQ :
                                if not game.player.Q.name=="velkozqsplitactivate":
                                    q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                        

    if jungle_clear_with_e and IsReady(game, e_spell) and game.player.mana>=manaE[game.player.E.level -1] :
                targetR=GetBestJungleInRange(game,1250)
                if targetR:
                    e_spell.move_and_trigger(game.world_to_screen(targetR.pos))

                                    
    if jungle_clear_with_w and IsReady(game, w_spell) and game.player.mana>= manaW[game.player.W.level -1]:
                targetW = GetBestJungleInRange (game,1150)
                
                if targetW :
                        if  (
                                game.player.mana >= 70  
                                and game.player.W.timeCharge>0):
                                    w_spell.move_and_trigger(game.world_to_screen(targetW.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r

    
    # target=TargetSelector(game,2000)
    # if target:
    #     if bffs(game,target):
    #         print("yes")
    #     else:
    #         print("no")
    
    self = game.player
    if self.is_alive :
        if game.is_key_down(combo_key):
            
            Combo(game)
            
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            
