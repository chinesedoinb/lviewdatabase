from winstealer import *
# from commons.utils import *
# from commons.skills import *
# from commons.items import *
# from commons.targeting import *
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *

winstealer_script_info = {
    "script": " Ashe",
    "author": "Ashe",
    "description": "sbtw",
    "target_champ": "ashe",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_r_in_combo = True

use_r_ks = True

lane_clear_with_q = False

q = {"Range": 650}
w = {"Range": 1150}
r = {"Range": 25000}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    use_r_ks = cfg.get_bool("use_r_ks", True)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("use_r_ks", use_r_ks)



    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_r_ks
    global combo_key, laneclear_key
    global lane_clear_with_q
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    if ui.treenode("[Combo Settings]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("[Laneclear Settings]"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        ui.treepop()

    if ui.treenode("[Killsteal settings]"):
        
        use_r_ks = ui.checkbox("Use R auto ks", use_r_ks)
        ui.treepop()

    if ui.treenode("[Laneclear settings]"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        ui.treepop()

class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

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


def Combo(game):
    global w, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()

    if (
        use_r_in_combo
        and IsReady(game, r_spell)
        and game.player.mana>=100
    ):
        target = TargetSelector(game, 1000)
        if target and not IsCollisioned(game, target):
            r_travel_time = 1000 / 1600
            predicted_pos = predict_pos(target, r_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= 1000:
               r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    if ( 
        use_w_in_combo
        and IsReady(game, w_spell)
        and game.player.mana>=70
    ):
        target = TargetSelector(game, w["Range"])
        if target:
            w_travel_time = w["Range"] / 2000
            predicted_pos = predict_pos(target, w_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if game.player.pos.distance(predicted_target.pos) <= 900 and not IsCollisioned(game, predicted_target):
             w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    if (
        use_q_in_combo
        and getBuff(game.player, "asheqcastready")
        and IsReady(game, q_spell) and game.player.mana>=50
    ):
        target = TargetSelector(game, q["Range"])
        if target:
            q_spell.trigger(False)

def Laneclear(game):
    q_spell = getSkill(game, "Q")
    if (
        lane_clear_with_q
        and getBuff(game.player, "asheqcastready")
        and IsReady(game, q_spell)
    ):
        minion = GetBestMinionsInRange(game)
        if minion:
            q_spell.trigger(False)

def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [200,400,600]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 1.0 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage
    



def KillSteal(game):
    R = getSkill(game, "R")
    before_cpos = game.get_cursor()        
    target = TargetSelector(game, 2000)
    if target and IsReady(game,R) and game.player.mana >=100:
       r_travel_time = 2000 / 1600
       predicted_pos = predict_pos(target, r_travel_time)
       predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
       if target.health < RDamage(game, target) :
          R.move_and_trigger(game.world_to_screen(predicted_target.pos))

def winstealer_update(game, ui):
    global combo_key, laneclear_key
    target=TargetSelector(game,game.player.atkRange + game.player.gameplay_radius + 25)

    self = game.player

    if self.is_alive :

        if game.was_key_pressed(combo_key):
            Combo(game)
            # for missile in game.missiles:
            #     # print(missile.name)
            #     if (missile.name == "ashebasicattack" 
            #     or missile.name == "asheqattack" 
            #     or missile.name == "asheqattacknoonhit"
            #     ):
            #         if target:
            #             game.click_at(False, game.world_to_screen(target.pos))
        elif game.was_key_pressed(laneclear_key):
            Laneclear(game)
        if use_r_ks:
            KillSteal(game)