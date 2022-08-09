from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 Samira",
    "author": "SA1",
    "description": "SA1 Samira",
    "target_champ": "samira",
}

combo_key = 57
harass_key = 45
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

lane_clear_with_q = False
lane_clear_with_q2 = False

steal_kill_with_q = False
steal_kill_with_e = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

use_w_on_evade = False
use_e_on_evade = False

LastR = 0

q = {"Range": 900.0, "MinRange": 325.0, "Mana": 30}
w = {"Range": 325.0, "Mana": 60}
e = {"Range": 550.0, "Mana": 40}
r = {"Range": 550.0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_q2
    global use_w_on_evade, use_e_on_evade
    global steal_kill_with_q, steal_kill_with_e
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    use_w_on_evade = cfg.get_bool("use_w_on_evade", False)
    use_e_on_evade = cfg.get_bool("use_e_on_evade", False)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lane_clear_with_q2 = cfg.get_bool("lane_clear_with_q2", False)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_q2
    global use_w_on_evade, use_e_on_evade
    global steal_kill_with_q, steal_kill_with_e

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

    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    cfg.set_bool("use_e_on_evade", use_e_on_evade)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_q2", lane_clear_with_q2)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_q2
    global use_w_on_evade, use_e_on_evade
    global steal_kill_with_q, steal_kill_with_e

    ui.begin("WS+ Samira")
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use [Q] in Combo", use_q_in_combo)
        steal_kill_with_q = ui.checkbox("Use [Q] with Killsteal", steal_kill_with_q)
        draw_q_range = ui.checkbox("Draw [Q] Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use [W] in Combo", use_w_in_combo)
        use_w_on_evade = ui.checkbox("Use [W] on Evade", use_w_on_evade)
        draw_w_range = ui.checkbox("Draw [W] Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use [E] in Combo", use_e_in_combo)
        steal_kill_with_e = ui.checkbox("Steal kill with [E]", steal_kill_with_e)
        draw_e_range = ui.checkbox("Draw [E] Range", draw_e_range)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use [R] in Combo", use_r_in_combo)
        draw_r_range = ui.checkbox("Draw [R] Range", draw_r_range)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with [Q]", lane_clear_with_q)
        lane_clear_with_q2 = ui.checkbox("Laneclear with [Q2]", lane_clear_with_q2)
        ui.treepop()
    ui.end()


RTargetCount = 0


def getCountR(game, dist):
    global RTargetCount
    RTargetCount = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) <= dist
        ):
            RTargetCount = RTargetCount + 1
    return RTargetCount


def EDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 50 + get_onhit_magical(game.player, target)
    elif game.player.E.level == 2:
        damage = 60 + get_onhit_magical(game.player, target)
    elif game.player.E.level == 3:
        damage = 70 + get_onhit_magical(game.player, target)
    elif game.player.E.level == 4:
        damage = 80 + get_onhit_magical(game.player, target)
    elif game.player.E.level == 5:
        damage = 90 + get_onhit_magical(game.player, target)
    return damage


def Combo(game):
    global q, w, e, r
    global LastR
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana > q["Mana"]:
        target = TargetSelector(game, (q["Range"] or q["MinRange"]))
        if target and not IsCollisioned(game, target):
            q_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, q_spell, game.player, target)
                )
            )
    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana > w["Mana"]:
        target = TargetSelector(game, w["Range"])
        if target:
            w_spell.trigger(False)
    if use_e_in_combo and IsReady(game, e_spell) and game.player.mana > e["Mana"]:
        target = TargetSelector(game, e["Range"])
        # if target and EDamage(game, target) + 80 >= target.health + (
        #     target.health_regen * 1.5
        # ):
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if (
        use_r_in_combo
        and LastR + 1 < game.time
        and (
            getBuff(game.player, "samirarreadybuff")
            or (getBuff(game.player, "samirapassivecombo"))
        )
        and IsReady(game, r_spell)
    ):
        target = TargetSelector(game, r["Range"])
        if target:
            LastR = game.time
            r_spell.trigger(False)


def Evade(game):
    global e, w
    global use_e_on_evade, use_w_on_evade
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    for missile in game.missiles:
        end_pos = missile.end_pos.clone()
        start_pos = missile.start_pos.clone()
        curr_pos = missile.pos.clone()
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
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
            if IsReady(game, e_spell) and use_e_on_evade:
                minion = GetBestMinionsInRange(game, e["Range"])
                if minion and not IsDanger(game, minion.pos):
                    turret = GetBestTurretInRange(game, minion.gameplay_radius * 2)
                    if turret:
                        continue
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            if IsReady(game, w_spell) and use_w_on_evade and spell.danger > 2:
                w_spell.trigger(False)


def Laneclear(game):
    q_spell = getSkill(game, "Q")
    if lane_clear_with_q and IsReady(game, q_spell) and game.player.mana > q["Mana"]:
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and is_last_hitable(game, game.player, minion):
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_q2 and IsReady(game, q_spell) and game.player.mana > q["Mana"]:
        minion = GetBestMinionsInRange(game, q["MinRange"])
        if minion and is_last_hitable(game, game.player, minion):
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))


def winstealer_update(game, ui):
    global combo_key, harass_key, laneclear_key

    self = game.player

    if self.is_alive:


        Evade(game)

        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
