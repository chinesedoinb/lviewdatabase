from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
from commons.targit import *

winstealer_script_info = {
    "script": "SA1 Jarvan",
    "author": "SA1",
    "description": "SA1",
    "target_champ": "jarvaniv",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lane_clear_with_w = False
lane_clear_with_e = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

auto_w_proximity = 400

lastR = 0

q = {"Range": 850}
w = {"Range": 600}
e = {"Range": 860}
r = {"Range": 650}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity

    combo_key = cfg.get_int("combo_key", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_w", False)

    auto_w_proximity = cfg.get_float("auto_w_proximity", 0)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity

    cfg.set_int("combo_key", combo_key)
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

    cfg.set_float("auto_w_proximity", auto_w_proximity)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity

    ui.begin("C.Malphite")
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Jungleclear key", laneclear_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo, Range below:", use_w_in_combo)
        auto_w_proximity = ui.sliderfloat("", auto_w_proximity, 100, 600.0)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Jungle clear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Jungle clear with W", lane_clear_with_w)
        lane_clear_with_e = ui.checkbox("Jungle clear with E", lane_clear_with_e)
        ui.treepop()

    ui.end()

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key
    global q, w, e, r
    global lastR
    global auto_w_proximity

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_r_in_combo
        and lastR + 4 < game.time
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
        target = TargetSelector(game, e["Range"])
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_q_in_combo
        and IsReady(game, q_spell)
        and not IsReady(game, e_spell)
    ):
        target = TargetSelector(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
    ):
        target = TargetSelector(game, auto_w_proximity)
        if target:
            w_spell.trigger(False)

def Laneclear(game):
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if(lane_clear_with_w and IsReady(game, w_spell)):
        minion = GetBestJungleInRange(game, auto_w_proximity)
        if minion:
            w_spell.trigger(False)
    if(lane_clear_with_q and IsReady(game, q_spell) and not IsReady(game, e_spell)):
        minion = GetBestJungleInRange(game, q["Range"])
        if minion:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if(lane_clear_with_e and IsReady(game, e_spell)):
        minion = GetBestJungleInRange(game, e["Range"])
        if minion:
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key

    self = game.player

    player = game.player


    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
