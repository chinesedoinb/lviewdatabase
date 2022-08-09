import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "Cassio",
    "author": "SA1",
    "description": "Cassio",
    "target_champ": "cassiopeia",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lane_clear_with_e = False
lasthit_with_q = False

steal_kill_with_e = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

draw_e_dmg = False

q = {"Range": 850}
w = {"Range": 850}
e = {"Range": 750}
r = {"Range": 825}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
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

    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global draw_e_dmg
    
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
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
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_e = ui.checkbox("Laneclear with E (LastHit)", lane_clear_with_e)
        ui.treepop()
    


lastQ = 0

mana_q = [50,60,70,80,90]
mana_w = [70,80,90,100,110]
mana_e = [50,48,46,44,42]
mana_r = 100

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
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target

def GetLowestHPandPoisonTarget(game, range):
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
            and champ.buffs
        ):

            qpoison = getBuff(champ, "cassiopeiaqdebuff")
            wpoison = getBuff(champ, "cassiopeiawpoison")

            if(champ.health < lowest_hp) and (qpoison or wpoison):
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target

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


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    if (
        use_q_in_combo
        and game.player.mana > mana_q[game.player.Q.level-1]
    ):
        target = GetLowestHPTarget(game, q["Range"])
        if target and IsReady(game, q_spell):
                q_travel_time = 0.60
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= q["Range"]:
                    if  game.player.mana >= 40:
                        # q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        

    if (
        use_w_in_combo
        and game.player.mana > mana_w[game.player.W.level-1]
    ):
        target = TargetSelector(game, w["Range"]-100)
        if target and IsReady(game, w_spell):
                q_travel_time = 700/1500
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance (predicted_target.pos) <= w["Range"]-100:
                    if  game.player.mana >= 40:
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))

    if (
        use_e_in_combo
        and game.player.mana > mana_e[game.player.E.level-1]
    ):
        # target=GetBestTargetsInRange(game,e["Range"])
        target1 = GetLowestHPandPoisonTarget(game, 800)
        if target1 and IsReady(game, e_spell):
            e_spell.move_and_trigger(game.world_to_screen(target1.pos))

    if (
        use_r_in_combo
        and game.player.mana > mana_r
    ):
        
        target = GetLowestHPTarget(game, 600)
        if target and IsReady(game, r_spell):

            r_spell.move_and_trigger(game.world_to_screen(target.pos ))

eLvLDamage = [20, 40, 60, 80, 100]


def EDamage(game, target):
    global eLvLDamage
    ecount = 0
    damage = 0

    # if game.player.E.level == 1:
    #     damage = 20 + (
    #         get_onhit_magical(game.player, target)
    #         + (get_onhit_physical(game.player, target))
    #     )
    # elif game.player.E.level == 2:
    #     damage = 40 + (
    #         get_onhit_magical(game.player, target)
    #         + (get_onhit_physical(game.player, target))
    #     )
    # elif game.player.E.level == 3:
    #     damage = 60 + (
    #         get_onhit_magical(game.player, target)
    #         + (get_onhit_physical(game.player, target))
    #     )
    # elif game.player.E.level == 4:
    #      damage = 80 + (
    #         get_onhit_magical(game.player, target)
    #         + (get_onhit_physical(game.player, target))
    #     )
    # elif game.player.E.level == 5:
    #     damage = 100 + (
    #         get_onhit_magical(game.player, target)
    #         + (get_onhit_physical(game.player, target))
    #     )
    return (
        eLvLDamage[game.player.E.level - 1]
        + (
            get_onhit_magical(game.player, target)
            + (get_onhit_physical(game.player, target))
        )
        - 40
    )


def Laneclear(game):
    e_spell = getSkill(game, "E")
    if lane_clear_with_e and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"])
        if minion and EDamage(game, minion) >= minion.health:
        #if minion and is_last_hitable(game, game.player, minion):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg
    self = game.player
    target = GetLowestHPTarget(game, 1000)
    r_spell = getSkill(game, "Q")
    # if target :
    #     if target.isMoving:
    #         print("move")
    #     predict=game.world_to_screen(castpoint_for_collision(game, r_spell, game.player, target))
    #     targ=game.world_to_screen(target.pos)
    #     game.draw_line(targ,predict,5,Color.GREEN)

    player = game.player

    if self.is_alive :
        if game.was_key_pressed(combo_key) :
            Combo(game)
        if game.was_key_pressed(laneclear_key) :
            Laneclear(game)
