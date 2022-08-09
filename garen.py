from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "C.Garen",
    "author": "SA1",
    "description": "DEMACIAAAAAA",
    "target_champ": "garen",
}

combo_key = 57

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lasthit_with_q = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

draw_r_dmg = False

lastE = 0

q = {"Range": 800}
w = {"Range": 600}
e = {"Range": 325}
r = {"Range": 400}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_r_range
    global spell_priority, combo_key
    global draw_r_dmg
    combo_key = cfg.get_int("combo_key", 57)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)
    draw_r_dmg = cfg.get_bool("draw_r_dmg", False)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_r_range
    global spell_priority, combo_key
    global draw_r_dmg

    cfg.set_int("combo_key", combo_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("draw_r_dmg", draw_r_dmg)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_r_range
    global spell_priority, combo_key
    global draw_r_dmg
    ui.begin("C.Garen")
    combo_key = ui.keyselect("Combo key", combo_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        draw_r_dmg = ui.checkbox("Draw When Executable With R", draw_r_dmg)
        ui.treepop()

    ui.end()

rFlatDamage = [150, 300, 450]
rPercDamage = [0.25, 0.30, 0.35]

def RDamage(game, target):
    global rFlatDamage
    global rPercDamage
    return(
        rFlatDamage[game.player.R.level -1] +
        (rPercDamage[game.player.R.level -1] * (target.max_health - target.health))
    )

def DrawRDamage(game, player):
    color = Color.YELLOW
    player = game.player
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            target = GetBestTargetsInRange(game, 2000)
            if target:
                if RDamage(game, target) > target.health:
                    p = game.hp_bar_pos(champ)
                    color.a = 5.0
                    game.draw_rect(
                        Vec4(p.x - 47, p.y - 27, p.x + 61, p.y - 12), color, 0, 2
                    )

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_r_range
    global combo_key
    global q, w, e, r
    global lastE

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_q_in_combo
        and IsReady(game, q_spell)
    ):
        target = TargetSelector(game, q["Range"])
        if target:
            q_spell.trigger(False)
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
    ):
        target = TargetSelector(game, w["Range"])
        if target:
            w_spell.trigger(False)

    if (
        use_e_in_combo
        and lastE + 1 < game.time
        and IsReady(game, e_spell)
    ):
        target = TargetSelector(game, e["Range"])
        if target and not IsReady(game, q_spell):
            e_spell.trigger(False)
            lastE = game.time

    if (
        use_r_in_combo
        and IsReady(game, r_spell)
    ):
        target = TargetSelector(game, r["Range"])
        if target and RDamage(game, target) > target.health:
            r_spell.move_and_trigger(game.world_to_screen(target.pos))

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key
    global draw_r_dmg

    self = game.player

    player = game.player

    if draw_r_dmg:
        DrawRDamage(game, player)


    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
