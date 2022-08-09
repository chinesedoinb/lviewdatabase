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
    "script": "Azir",
    "author": "Azir",
    "description": "Azir Azir",
    "target_champ": "azir",
}

combo_key = 57
laneclear_key = 47
harass_key = 45 

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lane_clear_with_e = False
lasthit_with_q = False

steal_kill_with_q = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False
e_harass = False

draw_q_dmg = False

q = {"Range": 740}
soldierAA = 370
w = {"Range": 500}
e = {"Range": 1100}
r = {"Range": 400}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

debug_hp = 0
buff_name = ""
debug_dmg = 0


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, q_harass
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q
    global lane_clear_with_q
    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    harass_key = cfg.get_int("harass_key", 45)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)
    q_harass = cfg.get_bool("q_harass", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    
    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, q_harass
    global lane_clear_with_q
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("harass_key", harass_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("q_harass", q_harass)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("draw_q_range", draw_q_range)
    

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q
    global lane_clear_with_q, q_harass
    ui.begin("Azir")
    debug_dmg = soldiercheck(game)
    ui.text(str(debug_dmg))
    combo_key = ui.keyselect("Revenant Shuffle", combo_key)
    laneclear_key = ui.keyselect("Shurima Shuffle", laneclear_key)
    harass_key = ui.keyselect("Harass Key", harass_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Shuffles", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        q_harass = ui.checkbox("Use Q in Harass", q_harass)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Shuffles", use_w_in_combo)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Shuffles", use_e_in_combo)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Shuffles", use_r_in_combo)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()
    ui.end()


lastQ = 0

mana_q = 55
mana_w = 40
mana_e = 60
mana_r = 100

#def effHP(game, target):
#    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
#    unitArmour = target.armour
#    unitHP = target.health

#    return (
##        (((1+(unitArmour / 100))*unitHP))
#       )


i = 0


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

def soldiercheck(game):
    i = 0
    for others in game.others:
        if i < 3 and others.name == "azirsoldier":
            i += 1
    return i


def Harass(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i, q_harass

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")

    player = game.player

    target = GetLowestHPTarget(game, (w["Range"] + 370))
    if target and IsReady(game, w_spell) and game.player.mana >= mana_w:
        if soldiercheck(game) < 3:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))
            target = GetLowestHPTarget(game, (q["Range"] + 370))

    if target and IsReady(game, q_spell) and game.player.mana >= mana_q:
        q_spell.move_and_trigger(game.world_to_screen(target.pos))



    

def Shurima(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i, prevPos, newPos, soldier, soldierDist
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    player = game.player
    target = GetLowestHPTarget(game, 1200)
    soldierDist = 0
    
    for others in game.others:
        if others.name == "azirsoldier" and soldierDist < 1100:
            if (game.player.pos.distance(others.pos) > soldierDist):
                soldierDist = game.player.pos.distance(others.pos)
                soldier = others

    PredictedPos = soldier.pos
    Direction = PredictedPos.sub(game.player.pos)
    QSpot = PredictedPos.sub(Direction.normalize().scale(40 * 50))

    if use_e_in_combo:
        if target and IsReady(game, e_spell) and game.player.mana >= mana_e:
            prevPos = player.pos
            e_spell.move_and_trigger(game.world_to_screen(soldier.pos))

    if use_q_in_combo:
        if target and IsReady(game, q_spell) and game.player.mana >= mana_q:
            soldierDist = game.player.pos.distance(soldier.pos)
            if soldierDist < 500:
                q_spell.move_and_trigger(game.world_to_screen(target.pos))

    if use_r_in_combo:
        if target and IsReady(game, r_spell) and game.player.mana >= mana_r and not IsReady(game, q_spell):
            r_spell.move_and_trigger(game.world_to_screen(QSpot))
    
                

def Revenant(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i, prevPos, newPos, soldier, soldierDist, QSpot
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    
    player = game.player
    soldierDist = 0
    soldier = game.player
    prevPos = player.pos

    
    
    for others in game.others:
        if others.name == "azirsoldier" and soldierDist < 2000:
            if (game.player.pos.distance(others.pos) > soldierDist):
                soldierDist = game.player.pos.distance(others.pos)
                soldier = others
                
    PredictedPos = soldier.pos
    Direction = PredictedPos.sub(game.player.pos)
    QSpot = PredictedPos.sub(Direction.normalize().scale(40 * 50))

    if use_e_in_combo:
        if IsReady(game, e_spell) and game.player.mana >= mana_e:
            prevPos = player.pos
            e_spell.move_and_trigger(game.world_to_screen(soldier.pos))


    if use_q_in_combo:
        if IsReady(game, q_spell) and game.player.mana >= mana_q:
            soldierDist = game.player.pos.distance(soldier.pos)
            if soldierDist < 400:
                q_spell.move_and_trigger(game.world_to_screen(QSpot))

    if use_r_in_combo:
        if IsReady(game, r_spell) and game.player.mana >= mana_r:
            QSpot = PredictedPos.add(Direction.normalize().scale(40 * 50))
            soldierDist = game.player.pos.distance(soldier.pos)
            if soldierDist < 400:
                r_spell.move_and_trigger(game.world_to_screen(QSpot))


    



def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg, player, soldier
    self = game.player

    player = game.player


    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Revenant(game)
        if game.was_key_pressed(laneclear_key):
            Shurima(game)
        if game.was_key_pressed(harass_key):
            Harass(game)
