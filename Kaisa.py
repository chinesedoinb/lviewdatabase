from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 Kai'sa",
    "author": "SA1",
    "description": "SA1 Kai'sa",
    "target_champ": "kaisa",
}

lasthit_key = 45
harass_key = 46
key_orbwalk = 57
laneclear_key = 47

## Combo
use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

# Evade
use_q_on_evade = True
use_w_on_evade = True
use_e_on_evade = True
use_r_on_evade = True

# KS
steal_kill_with_q = False
steal_kill_with_w = False
steal_kill_with_e = False
steal_kill_with_r = False

# Laneclear
lane_clear_with_q = False
lane_clear_with_w = False
lane_clear_with_e = False
lane_clear_with_r = False

# Drawings
draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

q = {"Range": 660}
w = {"Range": 3000}
e = {"Range": 0}
r = {"Range": 750}

qLvLDamage = [40, 55, 70, 85, 100]
wLvLDamage = [30, 55, 80, 105, 130]


def winstealer_load_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ## Keys
    lasthit_key = cfg.get_int("lasthit_key", 46)
    harass_key = cfg.get_int("harass_key", 45)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)

    ## Combo
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    ## Evade
    use_q_on_evade = cfg.get_bool("use_q_on_evade", True)
    use_w_on_evade = cfg.get_bool("use_w_on_evade", True)
    use_e_on_evade = cfg.get_bool("use_e_on_evade", True)
    use_r_on_evade = cfg.get_bool("use_r_on_evade", True)

    ## KS
    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_w = cfg.get_bool("steal_kill_with_w", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    ## Laneclear
    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)
    lane_clear_with_r = cfg.get_bool("lane_clear_with_r", False)

    ## Drawings
    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)


def winstealer_save_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range

    ## Keys
    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("key_orbwalk", key_orbwalk)

    ## Combo
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    ## Evade
    cfg.set_bool("use_q_on_evade", use_q_on_evade)
    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    cfg.set_bool("use_e_on_evade", use_e_on_evade)
    cfg.set_bool("use_r_on_evade", use_r_on_evade)

    ## KS
    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_w", steal_kill_with_w)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    ## Laneclear
    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_bool("lane_clear_with_r", lane_clear_with_r)

    ## Drawings
    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_e_range)
    cfg.set_bool("draw_e_range", draw_w_range)
    cfg.set_bool("draw_r_range", draw_r_range)

def winstealer_draw_settings(game, ui):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    

    ui.begin("WS+ Kai'sa")
    key_orbwalk = ui.keyselect("Combo key", key_orbwalk)
    #harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    lasthit_key = ui.keyselect("LastHit key", lasthit_key)
    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        #steal_kill_with_q = ui.checkbox("Steal kill with Q", steal_kill_with_q)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        #steal_kill_with_w = ui.checkbox("Steal kill with W", steal_kill_with_w)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        #steal_kill_with_e = ui.checkbox("Steal kill with E", steal_kill_with_e)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        #draw_e_dmg = ui.checkbox("Draw When is Killeable By E DMG", draw_e_dmg)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        #steal_kill_with_r = ui.checkbox("Steal kill with R", steal_kill_with_r)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Laneclear with E", lane_clear_with_w)
        ui.treepop()
    ui.end()

def QDamage(game, target):
    global qLvLDamage
    return (
        qLvLDamage[game.player.Q.level - 1] + (get_onhit_physical(game.player, target))
    )

def WDamage(game, target):
    global wLvLDamage
    return (
        wLvLDamage[game.player.W.level - 1] + (get_onhit_magical(game.player, target))
    )

def Combo(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    if use_w_in_combo and IsReady(game, w_spell):
        target = TargetSelector(game, w["Range"])
        if target and ValidTarget(target) and not IsCollisioned(game, target):
            w_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_q_in_combo and IsReady(game, q_spell):
        target = TargetSelector(game, q["Range"])
        if target and ValidTarget(target):
            q_spell.move_and_trigger(game.world_to_screen(target.pos))


def Laneclear(game):
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    if lane_clear_with_q and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"])
        if minion and ValidTarget(minion):
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_w and IsReady(game, w_spell):
        minion = GetBestMinionsInRange(game, w["Range"])
        if minion and ValidTarget(minion): #and not IsCollisioned(game, minion)
            w_spell.move_and_trigger(game.world_to_screen(minion.pos))


def winstealer_update(game, ui):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global use_q_on_evade, use_w_on_evade, use_e_on_evade, use_r_on_evade
    global steal_kill_with_q, steal_kill_with_w, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e, lane_clear_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    

    self = game.player
    #player = game.player
    #if draw_e_dmg:
        #DrawEDMG(game, player)
    if (
        self.is_alive
        and game.is_point_on_screen(game.player.pos)

    ):

        if game.is_key_down(laneclear_key):
            Laneclear(game)
        if game.is_key_down(key_orbwalk):
            Combo(game)
