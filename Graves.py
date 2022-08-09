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
    "script": "SA1-Graves",
    "author": "SA1",
    "description": "SA1-Graves",
    "target_champ": "graves",
}



combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

steal_kill_with_q = False
steal_kill_with_e = False
steal_kill_with_r = False

lane_clear_with_q = True
lane_clear_with_w=  True
lane_clear_with_e = True

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

max_mana_with_r = 40

lastQ = 0
lastE = 0
lastR = 0

q = {"Range": 1175}
e = {"Range": 1280}
r = {"Range": 0}

mana_w=[70,75,80,85,90]
def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q,lane_clear_with_w,lane_clear_with_e
    global max_mana_with_r
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)



    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    max_mana_with_r = cfg.get_float("max_mana_with_r", 40)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w=cfg.get_bool("lane_clear_with_w",True)
    lane_clear_with_e=cfg.get_bool("lane_clear_with_e",True)

    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q,lane_clear_with_w,lane_clear_with_e
    global max_mana_with_r
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("killsteal_key", killsteal_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    cfg.set_float("max_mana_with_r", max_mana_with_r)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w",lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e",lane_clear_with_e)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q,lane_clear_with_w,lane_clear_with_e
    global max_mana_with_r

    ui.text("SA1-Graves:1.0.0.0")
    ui.separator ()
    ui.text("Auth:Jingzz")
    ui.separator()


    combo_key = ui.keyselect("Combo key", combo_key)
    # harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    # killsteal_key = ui.keyselect("Killsteal key", killsteal_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        
        
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        
        
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        steal_kill_with_r = ui.checkbox("R when Enemy is killable", steal_kill_with_r)
        
        
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Laneclear with W", lane_clear_with_w)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
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


def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats



def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [250, 400, 550]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + ap)

    # Reduce damage based on target's magic resist
    mr = target.armour
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage
spellTimer = Timer()
spellTimerW=Timer()
def Combo(game):
    global q, e, r,steal_kill_with_r,spellTimer,spellTimerW
    global max_mana_with_r
    global lastQ, lastE, lastR
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    before_cpos = game.get_cursor()

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana>=mana_w[game.player.W.level -1]:
            target = TargetSelector(game,950)
            if target:

                q_travel_time = 950/ 1600
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if target:
                    if spellTimerW.Timer():
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimerW.SetTimer(0.4)   
            
    if (
        use_q_in_combo
        and game.player.mana >= 80
        and IsReady(game, q_spell)

    ):
        target = TargetSelector(game, 915)
        if target :

            q_travel_time = 925/ 920
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if target:
                if spellTimer.Timer():
                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    spellTimer.SetTimer(.4)   
              
                
    if (
        use_e_in_combo
        and game.player.mana >= 40
        and IsReady(game, e_spell) 
    ):
        target = TargetSelector(game, 925)
        if target :
            if not getBuff(game.player,"gravesbasicattackammo1"):
                e_spell.trigger(False)


    if use_r_in_combo and IsReady(game,r_spell) and game.player.mana>=100:
        target= game.GetBestTarget(UnitTag.Unit_Champion,1500)
        if target:
            q_travel_time = 1000/ 1400
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) >= 900:
                if RDamage(game,target)>=target.health:
                    r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))


# formula of w 610 + (20 * game.player.W.level) + game.player.gameplay_radius - 35
# formula of r damage baseRDmg = 60 + (40 * game.player.R.level) + (game.player.bonus_atk * 0.65) + (get_onhit_magical(game.player, target) * 0.25)

def Laneclear(game):
    global q, e, r,steal_kill_with_r
    global max_mana_with_r
    global lastQ, lastE, lastR
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()

    if lane_clear_with_w and IsReady(game, w_spell) and game.player.mana>=mana_w[game.player.W.level -1]:
            target = GetBestMinionsInRange(game,950)
            if target:

                
                if target:
                            game.move_cursor(game.world_to_screen(target.pos))
                            time.sleep(0.1)
                            w_spell.trigger(False)
                            time.sleep(0.1)
                            game.move_cursor(before_cpos) 
            
    if (
        lane_clear_with_q
        and game.player.mana >= 80
        and IsReady(game, q_spell)

    ):
        target = GetBestMinionsInRange(game, 915)
        if target :
            disToPlayer=game.player.pos.distance (target.pos)
            q_travel_time = disToPlayer/ 920
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if target:
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))  
              
                
    if (
        lane_clear_with_e
        and game.player.mana >= 40
        and IsReady(game, e_spell) 
    ):
        target = GetBestMinionsInRange(game, 925)
        if target :
            if not getBuff(game.player,"gravesbasicattackammo1"):
                e_spell.trigger(False)

    ####################################jungle:

    if lane_clear_with_w and IsReady(game, w_spell) and game.player.mana>=mana_w[game.player.W.level -1]:
            target = GetBestJungleInRange(game,950)
            if target:

                q_travel_time = 950/ 1600
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if target:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
            
    if (
        lane_clear_with_q
        and game.player.mana >= 80
        and IsReady(game, q_spell)

    ):
        target = GetBestJungleInRange(game, 915)
        if target :

            disToPlayer=game.player.pos.distance (target.pos)
            q_travel_time = disToPlayer/ 920
            predicted_pos = predict_pos (target, q_travel_time)
            predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
            if target:
                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos)) 
              
                
    if (
        lane_clear_with_e
        and game.player.mana >= 40
        and IsReady(game, e_spell) 
    ):
        target = GetBestJungleInRange(game, 925)
        if target :
            if not getBuff(game.player,"gravesbasicattackammo1"):
                e_spell.trigger(False)

def winstealer_update(game, ui):
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global lane_clear_with_q,lane_clear_with_w,lane_clear_with_e
    self = game.player

    if self.is_alive :
        

        if game.is_key_down(laneclear_key):
            Laneclear(game)
        if game.is_key_down(combo_key):
            Combo(game)
    