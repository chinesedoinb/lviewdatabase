from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
from commons.ByLib import *
from evade import checkEvade
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 Tristana",
    "author": "SA1",
    "description": "SA1",
    "target_champ": "tristana",
}

combo_key = 57
harass_key = 45
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = False
use_r_in_combo = True

lane_clear_with_q = False

use_q_in_harass = True
use_e_in_harass = True
w_combo_count=1
draw_e_dmg = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

w = {"Range": 900.0, "Mana": 60}
e = {"Range": 661.0}
e_mana = [55,55,60,65,70]
r = {"Range": 661.0, "Mana": 100}
e_lc_mana = 0.0
e_harass_mana = 0.0

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, use_r_ks, w_combo_count
    global use_q_in_harass, use_e_in_harass, e_harass_mana
    global lane_clear_with_q, lane_clear_with_q, lane_clear_with_e, e_lc_mana
    global combo_key, harass_key, laneclear_key
    global draw_w_range, draw_e_range, draw_r_range, draw_e_dmg
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", False)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)
    use_r_ks = cfg.get_bool("use_r_ks", False)
    use_q_in_harass = cfg.get_bool("use_q_in_harass", True)
    use_e_in_harass = cfg.get_bool("use_e_in_harass", True)
    e_harass_mana = cfg.get_float("e_harass_mana", 40)
    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    e_lc_mana = cfg.get_float("e_harass_mana", 40)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)
    #draw_e_dmg = cfg.get_bool("draw_e_dmg", True)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, use_r_ks, w_combo_count
    global use_q_in_harass, use_e_in_harass, e_harass_mana
    global lane_clear_with_q, lane_clear_with_e, e_lc_mana
    global combo_key, harass_key, laneclear_key
    global draw_w_range, draw_e_range, draw_r_range, draw_e_dmg
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)

    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("use_r_ks", use_r_ks)
    cfg.set_bool("use_q_in_harass", use_q_in_harass)
    cfg.set_bool("use_e_in_harass", use_e_in_harass)

    cfg.set_float("e_harass_mana", e_harass_mana)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_float("e_lc_mana", e_lc_mana)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.get_bool("draw_e_range", draw_e_range)
    cfg.get_bool("draw_r_range", draw_r_range)
    #cfg.set_bool("draw_e_dmg", draw_e_dmg)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, use_r_ks, w_combo_count
    global use_q_in_harass, use_e_in_harass, e_harass_mana
    global lane_clear_with_q, lane_clear_with_e, e_lc_mana
    global combo_key, harass_key, laneclear_key
    global draw_w_range, draw_e_range, draw_r_range, draw_e_dmg
    
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Combo"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo if can kill", use_r_in_combo)
        use_r_ks = ui.checkbox("Use R KS", use_r_ks)
        ui.treepop()

    if ui.treenode("Harass"):
        use_q_in_harass = ui.checkbox("Use Q in Harass", use_q_in_combo)
        use_e_in_harass = ui.checkbox("Use E in Harass", use_e_in_combo)
        e_harass_mana = ui.sliderfloat("E Mana", int(e_harass_mana), 1, 100)
        ui.treepop()

    if ui.treenode("Clear"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        e_lc_mana = ui.sliderfloat("E Mana", int(e_lc_mana), 1, 100)
        ui.treepop()
    if ui.treenode("Draw Settings"):
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
		#draw_e_dmg = ui.checkbox("Draw E DMG", draw_e_dmg)
        ui.treepop()
    

def Ks(game):
	global use_r_ks
	r_spell = getSkill(game, "R")
	target = GetBestTargetsInRange(game, r["Range"])
	if (use_r_ks and IsReady(game, r_spell)):
		if (target and RDamage(game, target) >= target.health):
			r_spell.move_and_trigger(game.world_to_screen(target.pos))


manaE=[50,55,60,70,75]
def Combo(game):
	global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, use_r_ks
	global use_q_in_harass, use_e_in_harass, e_harass_mana
	global lane_clear_with_q, lane_clear_with_e
	global draw_e_dmg
	global combo_key, harass_key, laneclear_key
	global q, w, e, r
	q_spell = getSkill(game, "Q")
	w_spell = getSkill(game, "W")
	e_spell = getSkill(game, "E")
	r_spell = getSkill(game, "R")
	if (use_q_in_combo and IsReady(game, q_spell)):
		target = TargetSelector(game, game.player.atkRange)
		if (target ):
			q_spell.trigger(False)
    
	if use_e_in_combo and IsReady(game, e_spell):
		target = TargetSelector(game, e["Range"])
		if (target and game.player.mana>= manaE[game.player.E.level -1]):
			e_spell.move_and_trigger(game.world_to_screen(target.pos))
    
	if use_r_in_combo and IsReady(game, r_spell) and game.player.mana>=100:
		target = TargetSelector(game, r["Range"])
		if (target and getBuff(target, "tristanaecharge") and RDamage(game, target) + EDamage(game,target) >= target.health + (1.5 * target.health_regen)):
			ecount = getBuff(target, "tristanaecharge").countAlt
			if (ecount == 3):
				r_spell.move_and_trigger(game.world_to_screen(target.pos))
    
def Harass(game):
	global q, e
	global use_q_in_harass, use_e_in_harass, e_harass_mana
	q_spell = getSkill(game, "Q")
	e_spell = getSkill(game, "E")
	hrpercentage = e_harass_mana * 0.01

	target = GetBestTargetsInRange(game, e["Range"])
	if (use_e_in_harass and game.player.mana > (hrpercentage * game.player.max_mana) and IsReady(game, e_spell)):
		if (target):
			e_spell.move_and_trigger(game.world_to_screen(target.pos))
	if (use_q_in_harass and IsReady(game, q_spell)):
		if (target):
			q_spell.trigger(False)

def Laneclear(game):
	global q, e
	global lane_clear_with_q, lane_clear_with_e, e_lc_mana
	q_spell = getSkill(game, "Q")
	e_spell = getSkill(game, "E")
	target = GetBestJungleInRange(game)
	minion = GetBestMinionsInRange(game, e["Range"])
	lcpercentage = e_lc_mana * 0.01

	if lane_clear_with_q and IsReady(game, q_spell) or lane_clear_with_e and IsReady(game, e_spell) and game.player.mana > (lcpercentage * game.player.max_mana):
		if (target):
			q_spell.trigger(False)
			e_spell.move_and_trigger(game.world_to_screen(target.pos))
		if (minion):
			q_spell.trigger(False)
			e_spell.move_and_trigger(game.world_to_screen(minion.pos))


def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 300 + (get_onhit_magical(game.player, target))
    elif game.player.R.level == 2:
        damage = 400 + (get_onhit_magical(game.player, target))
    elif game.player.R.level == 3:
        damage = 500 + (get_onhit_magical(game.player, target))
    return damage



def EDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 70 + (get_onhit_physical(game.player, target))
    elif game.player.E.level == 2:
        damage = 80 + (get_onhit_physical(game.player, target))
    elif game.player.E.level == 3:
        damage = 90 + (get_onhit_physical(game.player, target))
    elif game.player.E.level == 4:
        damage = 100 + (get_onhit_physical(game.player, target))
    elif game.player.E.level == 5:
        damage = 110 + (get_onhit_physical(game.player, target))
    return damage


def winstealer_update(game, ui):
	global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo, use_r_ks
	global use_q_in_harass, use_e_in_harass, e_harass_mana
	global lane_clear_with_q, lane_clear_with_e, e_lc_mana
	global draw_e_dmg
	global combo_key, harass_key, laneclear_key


	self = game.player
	player = game.player
	w_spell = getSkill(game, "W")
	e_spell = getSkill(game, "E")
	r_spell = getSkill(game, "R")
	if self.is_alive and draw_w_range and IsReady(game, w_spell):
		game.draw_circle_world(game.player.pos, w["Range"], 100, 1, Color.BLUE)
	if self.is_alive and draw_e_range and IsReady(game, e_spell):
		game.draw_circle_world(game.player.pos, e["Range"], 100, 1, Color.BLUE)
	if self.is_alive and draw_r_range and IsReady(game, r_spell):
		game.draw_circle_world(game.player.pos, r["Range"], 100, 1, Color.YELLOW)

	if use_r_ks:
		Ks(game)

	if self.is_alive and game.is_point_on_screen(self.pos) :
		if game.is_key_down(combo_key):
			Combo(game)
			
		if game.is_key_down(harass_key):
			Harass(game)
		if game.is_key_down(laneclear_key):
			Laneclear(game)
