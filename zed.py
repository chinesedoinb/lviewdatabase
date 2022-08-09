import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Zed",
    "author": "SA1",
    "description": "SA1-Zed",
    "target_champ": "zed",
}

smartCombo=47
laneclear_key = 46
harass_key = 45 

autoQKey=48
use_q_stack=True

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = True
lane_clear_with_e = True

lasthit_with_q = False
flee=49
steal_kill_with_q = False

toggled = False

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True
e_harass = False
smart_combo=1
draw_q_dmg = False

rSwitch=True
rEvade=True

q = {"Range": 925}
w = {"Range": 650}
e = {"Range": 0}
r = {"Range": 625}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

lastQ=0

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, e_harass,rSwitch,rEvade
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg,flee
    global spell_priority, harass_key, laneclear_key,smart_combo,autoQKey,use_q_stack,smartCombo
    global steal_kill_with_q
    global lane_clear_with_q,lane_clear_with_e
    
    smartCombo = cfg.get_int("smartCombo", 47)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key=cfg.get_int("laneclear_key", 46)
    flee=cfg.get_int("flee", 49)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)
    rSwitch=cfg.get_bool("rSwitch",True)
    rEvade=cfg.get_bool("rEvade",rEvade)
    e_harass = cfg.get_bool("e_harass", True)


    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)

    smart_combo=cfg.get_int("smart_combo",smart_combo)

    draw_q_range = cfg.get_bool("draw_q_range", True)
    draw_w_range = cfg.get_bool("draw_w_range", True)
    draw_e_range = cfg.get_bool("draw_e_range", True)
    draw_r_range = cfg.get_bool("draw_r_range", True)

    draw_q_dmg = cfg.get_bool("draw_q_dmg", False)

    
    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_e =cfg.get_bool("lane_clear_with_e", True)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    
    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, harass_key, laneclear_key,use_q_stack,autoQKey,smartCombo
    global steal_kill_with_q, e_harass,smart_combo,rSwitch
    global lane_clear_with_q,lane_clear_with_e,flee,rEvade
    
    cfg.set_int("smartCombo", smartCombo)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key",laneclear_key)
    cfg.set_int("flee",flee)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("rSwitch",rSwitch)

    cfg.set_bool("e_harass", e_harass)

    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    cfg.set_int("smart_combo",smart_combo)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("draw_q_range", draw_q_range)

    cfg.set_bool("draw_q_dmg", draw_q_dmg)
    cfg.set_bool("rEvade",rEvade)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo,smartCombo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key,smart_combo,use_q_stack,autoQKey,rSwitch,rEvade
    global steal_kill_with_q
    global lane_clear_with_q, e_harass,lane_clear_with_e,flee
    
    ui.text("SA1-Zed 1.0.0.0")
    	
    ui.separator ()
    # ui.text("LifeSaver#3592")

    smartCombo = ui.keyselect("Combo", smartCombo)
    harass_key = ui.keyselect("Harass Key", harass_key)
    autoQKey=ui.keyselect("Auto E key",autoQKey)
    laneclear_key=ui.keyselect("Lane Clear",laneclear_key)
    flee=ui.keyselect("flee",flee)

    ui.separator ()
    ui.text("Mode:")
    smart_combo=ui.listbox("",["Smart","Line mode : R > W > Q/E","Simple : W > R / Q /E"],smart_combo)
    ui.separator ()
    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()
    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_q_stack=ui.checkbox("Auto E",use_q_stack)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        rSwitch=ui.checkbox("Switch back to R shadow when enemy is dead",rSwitch)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q (LastHit)", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with Q (LastHit)", lane_clear_with_e)
        ui.treepop()

    if ui.treenode("Evade"):
        rEvade = ui.checkbox("R Evade)", rEvade)
        ui.treepop()    
    ui.separator ()


lastQ = 0

mana_q = [75, 70, 65, 60, 55]
mana_w = [40, 35, 30, 25, 20]
mana_e = 50
mana_r = 0

def GetLowestHPTarget(game, range):
    lowest_target = None
    lowest_hp = 9999

    player = game.player

    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
            and champ.pos.distance(player.pos) <= range
        ):
            if(champ.health < lowest_hp):
                lowest_hp = champ.max_health
                lowest_target = champ

    return lowest_target

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def QDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.Q.level
    if r_lvl == 0:
        return 0
    
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [80,115,150,185,220]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 2.85  + 2.40 * ad)+ (get_onhit_physical(game.player, target))

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def EDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.E.level
    if r_lvl == 0:
        return 0
    
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [70,90,110,130,150]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 2.85  + 2.40 * ad) 

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

def Harass(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i, e_harass

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell=getSkill(game, "R")
    player = game.player

    target = GetLowestHPTarget(game, 650)
    target2=GetLowestHPTarget(game, 1200)


    if use_w_in_combo and IsReady(game, w_spell):
               if target2:
                   if not w_spell.name=="zedw2" :
                        w_spell.move_and_trigger(game.world_to_screen(target2.pos))
    
    if use_q_in_combo and IsReady(game, q_spell):
                if target2:
                        if game.player.mana >= mana_q[game.player.Q.level -1]:
                                                    q_travel_time = 920/1700
                                                    predicted_pos = predict_pos (target2, q_travel_time)
                                                    predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                                                    # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                                    if game.player.pos.distance (predicted_target.pos) <= 1200 :
                                                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
    if use_e_in_combo:
        targetLong= GetLowestHPTarget(game, 1200)
        targetNear = GetLowestHPTarget(game, 290)
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell) and IsReady(game, w_spell):
            if targetLong :
                if  w_spell.name=="zedw2":
                    if game.player.mana >= mana_e:
                        e_spell.trigger(False)


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



def Evade(game):
    global e, lastW,rEvade
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    r_spell = getSkill(game, "R")
    target=GetBestTargetsInRange(game,650)
    for missile in game.missiles:
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot( game, game.player.pos, missile, spell, game.player.gameplay_radius * 2) and game.is_point_on_screen(missile.pos):
        
            if use_w_in_combo and IsReady(game, w_spell):    
                if w_spell.name=="zedw2" and r_spell.name=="zedr2" :
                      w_spell.trigger(False)
            if rEvade and IsReady(game, r_spell):
                if target:
                    if not r_spell.name=="zedr2" :
                        r_spell.move_and_trigger(game.world_to_screen(target.pos))
               



def simpleMode(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo,rSwitch
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    player = game.player
    target = TargetSelector(game, 1000)
    target2=TargetSelector(game, 1000)    

    if not IsReady(game, r_spell):
        if use_w_in_combo and IsReady(game, w_spell):
               if target2:
                   if not w_spell.name=="zedw2" :
                        w_spell.move_and_trigger(game.world_to_screen(target2.pos))
    if not IsReady(game, r_spell):
            if use_q_in_combo and IsReady(game, q_spell):
                if target2:
                        if game.player.mana >= mana_q[game.player.Q.level -1]:
                                                    q_travel_time = 920/1700
                                                    predicted_pos = predict_pos (target2, q_travel_time)
                                                    predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                                                    # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                                    if game.player.pos.distance (predicted_target.pos) <= 1200 :
                                                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
    if use_e_in_combo:
        targetLong= TargetSelector(game, 1200)
        targetNear = TargetSelector(game, 290)
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell) and IsReady(game, w_spell):
            if targetLong :
                if  w_spell.name=="zedw2":
                    if game.player.mana >= mana_e:
                        e_spell.trigger(False)



    #------------------------- if R is ready ---------------------------                                                                     
    if use_r_in_combo and IsReady(game, r_spell):
        targetDEAR = TargetSelector(game, 1500)
        targetR = TargetSelector(game, 650)
        if targetR:
            if not r_spell.name=="zedr2" :
                if game.player.mana >= mana_q[game.player.Q.level -1] and game.player.mana >=mana_w[game.player.W.level -1]:
                    r_spell.move_and_trigger(game.world_to_screen(targetR.pos))
        if not targetDEAR and r_spell.name=="zedr2" and rSwitch:
                    r_spell.trigger(False)

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana >= mana_w[game.player.W.level -1]:
           if target:
                        w_spell.move_and_trigger(game.world_to_screen(target.pos)) 
    if use_q_in_combo and IsReady(game, q_spell):
        if target:
            if r_spell.name=="zedr2" :
                    
                            for champ in game.champs:
                                for buff in champ.buffs:
                                    if (buff.name == "zedrdeathmark"):
                                        target =  champ
                            if target and game.player.mana >= mana_q[game.player.Q.level -1]:
                                            q_travel_time = 920/1700
                                            predicted_pos = predict_pos (target, q_travel_time)
                                            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                            # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                            if game.player.pos.distance (predicted_target.pos) <= 650 :
                                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
               
    if use_e_in_combo:
        targetLong= TargetSelector(game, 920)
        targetNear = TargetSelector(game, 290)
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell) and IsReady(game, w_spell):
            if targetLong :
                if  w_spell.name=="zedw2":
                    if target and game.player.mana >= mana_e:
                        e_spell.trigger(False)
                    

def LineMode(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    player = game.player
    target = TargetSelector(game, 650)
    target2=TargetSelector(game, 1200)
#------------------------- if No R  ---------------------------    
    if not IsReady(game, r_spell):
        if use_w_in_combo and IsReady(game, w_spell):
               if target2:
                   if not w_spell.name=="zedw2" :
                        w_spell.move_and_trigger(game.world_to_screen(target2.pos))
    if not IsReady(game, r_spell):
            if use_q_in_combo and IsReady(game, q_spell):
                if target2:
                        if game.player.mana >= mana_q[game.player.Q.level -1]:
                                                    q_travel_time = 920/1700
                                                    predicted_pos = predict_pos (target2, q_travel_time)
                                                    predicted_target = Fake_target (target2.name, predicted_pos, target2.gameplay_radius)
                                                    # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                                    if game.player.pos.distance (predicted_target.pos) <= 1200 :
                                                            q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
    if use_e_in_combo:
        targetLong= TargetSelector(game, 1200)
        targetNear = TargetSelector(game, 290)
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell) and IsReady(game, w_spell):
            if targetLong :
                if  w_spell.name=="zedw2":
                    if game.player.mana >= mana_e:
                        e_spell.trigger(False)

    #------------------------- if R is ready ---------------------------                                                                     
    if use_r_in_combo and IsReady(game, r_spell):
        targetDEAR = TargetSelector(game, 1500)
        if target:
            if not r_spell.name=="zedr2" :
                if game.player.mana >= mana_q[game.player.Q.level -1] and game.player.mana >=mana_w[game.player.W.level -1]:
                    r_spell.move_and_trigger(game.world_to_screen(target.pos))
        if not targetDEAR and r_spell.name=="zedr2" and rSwitch:
                    r_spell.trigger(False)

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana >= mana_w[game.player.W.level -1]:
           if target:
               if r_spell.name=="zedr2" :
                    if not w_spell.name=="zedw2" :
                        w_spell.move_and_trigger(game.world_to_screen(target.pos).add(Vec2(170,0 ))) 
    if use_q_in_combo and IsReady(game, q_spell):
        if target:
            if r_spell.name=="zedr2" :
                    if w_spell.name=="zedw2" :
                            for champ in game.champs:
                                for buff in champ.buffs:
                                    if (buff.name == "zedrdeathmark"):
                                        target =  champ
                            if target and game.player.mana >= mana_q[game.player.Q.level -1]:
                                            q_travel_time = 920/1700
                                            predicted_pos = predict_pos (target, q_travel_time)
                                            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                            # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                            if game.player.pos.distance (predicted_target.pos) <= 650 :
                                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
               
    if use_e_in_combo:
        targetLong= TargetSelector(game, 920)
        targetNear = TargetSelector(game, 290)
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell) and IsReady(game, w_spell):
            if targetLong :
                if  w_spell.name=="zedw2":
                    if target and game.player.mana >= mana_e:
                        e_spell.trigger(False)


def SmartMode(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    lastQ=0
    player = game.player
    
    if use_r_in_combo and IsReady(game, r_spell):
        target = TargetSelector(game, 650)
        targetDEAR = TargetSelector(game, 1500)
        if target :
            
            if not r_spell.name=="zedr2":
                if QDamage(game, target) + EDamage(game, target) >= target.health:
                    if game.player.mana >= mana_q[game.player.Q.level -1] and game.player.mana >=mana_w[game.player.W.level -1]:
                        r_spell.move_and_trigger(game.world_to_screen(target.pos))
        if not targetDEAR and r_spell.name=="zedr2" and rSwitch:
                    r_spell.trigger(False)

    if use_w_in_combo:
            target = TargetSelector(game, 2000)
            if target and IsReady(game, w_spell) :
                if IsReady(game, q_spell) or IsReady(game, e_spell):
                    if game.player.mana >= mana_q[game.player.Q.level -1] and game.player.mana >= mana_w[game.player.W.level -1]:
                        if not w_spell.name=="zedw2" :
                            if not r_spell.name=="zedr2" :
                                w_spell.move_and_trigger(game.world_to_screen(target.pos))
                            else:
                                w_spell.move_and_trigger(game.world_to_screen(target.pos).add(Vec2(150,0 )))    
                if QDamage(game, target) >= target.health or EDamage(game, target) >= target.health:
                    if IsReady(game, q_spell) and IsReady(game, e_spell) and IsReady(game, r_spell):
                        if game.player.pos.distance (target.pos) <= 700 or game.player.pos.distance (target.pos) <= 1800:
                          if w_spell.name=="zedw2" :
                              w_spell.move_and_trigger(game.world_to_screen(target.pos))

###################################  Q mode   ################################################################
    if use_q_in_combo :
        if not w_spell.name=="zedw2" :
            target = TargetSelector(game, 920)
            if IsReady(game, q_spell):
                for champ in game.champs:
                    for buff in champ.buffs:
                        if (buff.name == "zedrdeathmark"):
                            target =  champ
                if target and game.player.mana >= mana_q[game.player.Q.level -1]:
                                q_travel_time = 920/1700
                                predicted_pos = predict_pos (target, q_travel_time)
                                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                if game.player.pos.distance (predicted_target.pos) <= 920 and lastQ + 1 < game.time:
                                        
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                        lastQ=game.time
        elif w_spell.name=="zedw2" :
            target = TargetSelector(game, 2500)
            if IsReady(game, q_spell):
                for champ in game.champs:
                    for buff in champ.buffs:
                        if (buff.name == "zedrdeathmark"):
                            target =  champ
                if target and game.player.mana >= mana_q[game.player.Q.level -1]:
                                q_travel_time = 920/1700
                                predicted_pos = predict_pos (target, q_travel_time)
                                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                if game.player.pos.distance (predicted_target.pos) <= 2500 and  lastQ + 2 < game.time:
                                        
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                        lastQ=game.time

########################################################################################################

    if use_e_in_combo:
        targetLong= TargetSelector(game, 10000)
        targetNear = TargetSelector(game, 290)

        # shadow=game.getObject(UnitTag.Unit_Champion,10000)
        
        if IsReady(game, e_spell) and not IsReady(game, w_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell):
            for shadow in game.others:
                if shadow and shadow.name =="zedshadow":
                        if target:
                            if targetLong.pos.distance (shadow.pos)<=290:
                                e_spell.trigger(False)
           

def AutoQ(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key,autoQKey,use_q_stack
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    player = game.player
    if use_q_stack:
        # shadow=game.getObject(UnitTag.Unit_Champion,10000)
        targetNear = TargetSelector(game, 290)
        target = TargetSelector(game, 10000)
        if IsReady(game, e_spell):
            if targetNear:
                e_spell.trigger(False)
        if IsReady(game, e_spell):
            for shadow in game.others:
                if shadow and shadow.name =="eezedshadow":
                        if target:
                            if target.pos.distance (shadow.pos)<=290:
                                e_spell.trigger(False)
                        
def Fly(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana >= mana_w[game.player.W.level -1]:
                        w_spell.trigger(False) 

def Laneclear(game):
    global lane_clear_with_e,lane_clear_with_q
    global lastQ
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    
    if lane_clear_with_e and IsReady(game, e_spell):
        target=GetBestMinionsInRange(game,290)
        if target:
            e_spell.trigger(False)
    if lane_clear_with_q and IsReady(game, q_spell):
        target=GetBestMinionsInRange(game,920)
        if target:
                                q_travel_time = 920/1700
                                predicted_pos = predict_pos (target, q_travel_time)
                                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                if game.player.pos.distance (predicted_target.pos) <= 920 and lastQ + 1 < game.time:
                                        
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                        lastQ=game.time 
def jungle(game):
    global lane_clear_with_e,lane_clear_with_q
    global lastQ
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    
    if lane_clear_with_e and IsReady(game, e_spell):
        target=GetBestJungleInRange(game,290)
        if target:
            e_spell.trigger(False)
    if lane_clear_with_q and IsReady(game, q_spell):
        target=GetBestJungleInRange(game,920)
        if target:
                                q_travel_time = 920/1700
                                predicted_pos = predict_pos (target, q_travel_time)
                                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                                # game.draw_circle_world(predicted_target.pos, 150, 100, 5, Color.RED)   
                                if game.player.pos.distance (predicted_target.pos) <= 920 and lastQ + 1 < game.time:
                                        
                                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                        lastQ=game.time                                        
def DrawAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto E: Enabled", Color.BLACK, Color.GREEN, 10.0)
def DrawNotAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto E: Disabled", Color.BLACK, Color.RED, 10.0)



def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range,smart_combo,autoQKey,use_q_stack,smartCombo
    global q, w, e, r
    global combo_key, laneclear_key, harass_key,flee
    global draw_e_dmg, player
    self = game.player
    w_spell = getSkill(game, "W")
    player = game.player
    e_spell = getSkill(game, "E")

    target = GetBestTargetsInRange (game, 8000)
    # if target:
    #        for missle in game.missiles:
    #            print(missle.currentDashSpeed)
    #            game.draw_circle_world(missle.pos, 150, 100, 1, Color.PURPLE)
    
    
    # shadow=game.getObject(UnitTag.Unit_Champion,10000)
    # if shadow and shadow.name =="zedshadow":
    #     game.draw_circle_world(shadow.pos, 150, 100, 3, Color.PURPLE)
        
    #----------------------------------------------------------------------------
    # for obj in game.others:
    #         if  obj and obj.name == "zedshadow" and obj.is_alive:
    #             game.draw_circle_world(obj.pos, 150, 100, 1, Color.PURPLE)
    #             if target:
    #                 if obj.pos.distance(target.pos) < 200:
    #                     e_spell.trigger(False)



    Evade(game)
    if self.is_alive :
        
        if game.was_key_pressed(smartCombo):
            if smart_combo ==0 :
                SmartMode(game)
            if smart_combo==1:
                LineMode(game)
            if smart_combo==2:
                simpleMode(game)        
        if game.was_key_pressed(harass_key):
            Harass(game)
            
        if use_q_stack:
            AutoQ(game)
            DrawAutoQ(game)
        if not use_q_stack:
            DrawNotAutoQ(game)
        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack      

        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            jungle(game)

        if game.was_key_pressed(flee):
            Fly(game)    
