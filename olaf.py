from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-olaf",
    "author": "SA1",
    "description": "Olaf",
    "target_champ": "olaf",
}

combo_key = 57
laneclear_key = 47

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True


lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False


auto_w_proximity = 400

lastR = 0

q = {"Range": 1000}
w = {"Range": 200}
e = {"Range": 320}


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


    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)


    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_w", True)

 

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


    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)


    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)



def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity

    ui.text("SA1-Olaf : 1.0.0.0")
    ui.text("R manual")
    ui.separator ()
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Jungleclear key", laneclear_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo, Range below:", use_w_in_combo)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        ui.treepop()


    if ui.treenode("Laneclear"):
        lane_clear_with_q = ui.checkbox("Jungle/lane clear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Jungle/lane clear with W", lane_clear_with_w)
        lane_clear_with_e = ui.checkbox("Jungle/lane clear with E", lane_clear_with_e)
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



def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global combo_key
    global q, w, e, r
    global lastR
    global auto_w_proximity
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_e_in_combo
        and IsReady(game, e_spell)
    ):
        target = TargetSelector(game, 325)
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if use_q_in_combo and IsReady(game, q_spell) :
                targetQ = TargetSelector (game,1000)
                if targetQ :
                    q_travel_time = 1000/1600
                    predicted_pos = predict_pos (targetQ, q_travel_time)
                    predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 950:
                        if  game.player.mana >= 50:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.01)
                            q_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
    if (
        use_w_in_combo
        and IsReady(game, w_spell)
    ):
        target = TargetSelector(game, 250)
        if target:
            w_spell.trigger(False)

def jungle(game):
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if (
        lane_clear_with_e
        and IsReady(game, e_spell)
    ):
        target = GetBestJungleInRange(game, 325)
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if lane_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestJungleInRange (game,1000)
                if targetQ :
                    q_travel_time = 1000/1600
                    predicted_pos = predict_pos (targetQ, q_travel_time)
                    predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 950:
                        if  game.player.mana >= 50:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.01)
                            q_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
    if (
        lane_clear_with_w
        and IsReady(game, w_spell)
    ):
        target = GetBestJungleInRange(game, 250)
        if target:
            w_spell.trigger(False)
def Laneclear(game):
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global auto_w_proximity
    before_cpos = game.get_cursor ()
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    if (
        lane_clear_with_e
        and IsReady(game, e_spell)
    ):
        target = GetBestMinionsInRange(game, 325)
        if target:
            e_spell.move_and_trigger(game.world_to_screen(target.pos))

    if lane_clear_with_q and IsReady(game, q_spell) :
                targetQ = GetBestMinionsInRange (game,1000)
                if targetQ :
                    q_travel_time = 1000/1600
                    predicted_pos = predict_pos (targetQ, q_travel_time)
                    predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 950:
                        if  game.player.mana >= 50:
                            game.move_cursor(game.world_to_screen(predicted_target.pos))
                            time.sleep(0.01)
                            q_spell.trigger(False)
                            time.sleep(0.01)
                            game.move_cursor(before_cpos)
    if (
        lane_clear_with_w
        and IsReady(game, w_spell)
    ):
        target = GetBestMinionsInRange(game, 250)
        if target:
            w_spell.trigger(False)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key

    self = game.player

    player = game.player

    if player.is_alive  :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            jungle(game)