from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "C.Annie",
    "author": "Carter",
    "description": "Burn, burn, burn!",
    "target_champ": "annie",
}

combo_key = 57
laneclear_key = 47
lasthit_key = 45

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lasthit_with_q = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

auto_e_shield = False

lastR = 0

auto_e_proximity = 400

q = {"Range": 625}
w = {"Range": 600}
e = {"Range": 800}
r = {"Range": 600}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q
    global auto_e_shield, auto_e_proximity

    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    lasthit_key = cfg.get_int("lasthit_key", 45)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)

    auto_e_shield = cfg.get_bool("auto_e_shield", False)
    auto_e_proximity = cfg.get_float("auto_e_proximity", 0)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q
    global auto_e_shield, auto_e_proximity

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("lasthit_key", lasthit_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)

    cfg.set_bool("auto_e_shield", auto_e_shield)

    cfg.set_float("auto_e_proximity", auto_e_proximity)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, lasthit_key
    global lane_clear_with_q, lasthit_with_q
    global auto_e_shield, auto_e_proximity

    ui.begin("C.Annie")
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    lasthit_key = ui.keyselect("Lasthit key", lasthit_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        auto_e_shield = ui.checkbox("Auto Shield Projectiles", auto_e_shield)
        use_e_in_combo = ui.checkbox("E if Enemy in Proximity:", use_e_in_combo)
        auto_e_proximity = ui.sliderfloat("", auto_e_proximity, 100, 800.0)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q (LastHit)", lane_clear_with_q)
        ui.treepop()

    if ui.treenode("Lasthit"):
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        ui.treepop()

    ui.end()

def Evade(game):
    global e, lastE
    e_spell = getSkill(game, "E")
    for missile in game.missiles:
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if (
            game.point_on_line(
                game.world_to_screen(start_pos),
                game.world_to_screen(end_pos),
                game.world_to_screen(game.player.pos),
                br,
            )
            and game.is_point_on_screen(curr_pos)
        ):
            if IsReady(game, e_spell) and auto_e_shield:
                e_spell.trigger(False)

qFlatDamage = [80, 115, 150, 185, 220]

def QDamage(game, target):
    global qFlatDamage
    raw_damage = qFlatDamage[game.player.Q.level - 1] + (game.player.ap * 0.75)
    true_damage = raw_damage
    # if(target.magic_resist > 0):
    #     true_damage = true_damage * (100/(100 + target.magic_resist))
    # elif(target.magic_resist < 0):
    #     true_damage = true_damage * (2 - (100/(100 + target.magic_resist)))
    return(true_damage)

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key
    global q, w, e, r
    global lastR
    global auto_e_proximity

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_r_in_combo
        and lastR + 3 < game.time
        and IsReady(game, r_spell)
    ):
        target = TargetSelector(game, r["Range"])
        if target:
            r_spell.move_and_trigger(game.world_to_screen(target.pos))
            lastR = game.time
    if (
        use_e_in_combo
        and IsReady(game, e_spell)
    ):
        target = TargetSelector(game, auto_e_proximity)
        if target:
            e_spell.trigger(False)
    if (
        use_q_in_combo
        and IsReady(game, q_spell)
    ):
        target = TargetSelector(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
    ):
        target = TargetSelector(game, w["Range"])
        if target:
            w_spell.move_and_trigger(game.world_to_screen(target.pos))

def Laneclear(game):
    global lane_clear_with_q
    q_spell = getSkill(game, "Q")
    if(lane_clear_with_q and IsReady(game, q_spell)):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and QDamage(game, minion) >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

def Lasthit(game):
    global lasthit_with_q
    q_spell = getSkill(game, "Q")
    if(lasthit_with_q and IsReady(game, q_spell)):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and QDamage(game, minion) >= minion.health:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, lasthit_key

    self = game.player

    player = game.player



    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
        if game.was_key_pressed(lasthit_key):
            Lasthit(game)
