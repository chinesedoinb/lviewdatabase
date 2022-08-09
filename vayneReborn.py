
from winstealer import *
from commons.items import *
from commons.targeting import *
from commons.utils import *
import json, time, math
from commons.targit import *

winstealer_script_info = {
    "script": "SA1 Vayne",
    "author": "SA1",
    "description": "SA1 Vayne",
    "target_champ": "vayne",
}

lastQ = 0
lastE = 0

combo_key = 57
harass_key = 46

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

randomize_q_pos = True

anti_gap_q = True
anti_gap_e = True

use_q_on_evade = False

draw_q_range = False
draw_e_range = False

MaxRCountForUse = 0

e_range = 475

q = {"Range": 325}
e = {"Speed": 999, "Range": 650, "delay": 0.75, "radius": 120}


use_q_with_harass = True
use_e_with_harass = False


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range
    global combo_key, harass_key
    global anti_gap_q, anti_gap_e, use_q_on_evade
    global e_range
    global randomize_q_pos
    global MaxRCountForUse
    global use_q_with_harass, use_e_with_harass
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    use_q_with_harass = cfg.get_bool("use_q_with_harass", True)
    use_e_with_harass = cfg.get_bool("use_e_with_harass", False)

    randomize_q_pos = cfg.get_bool("use_q_for_gapcloser", True)

    anti_gap_q = cfg.get_bool("anti_gap_q", True)
    anti_gap_e = cfg.get_bool("anti_gap_e", True)

    use_q_on_evade = cfg.get_bool("use_q_on_evade", False)

    e_range = cfg.get_int("e_range", 475)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)

    MaxRCountForUse = cfg.get_float("MaxRCountForUse", 1)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range
    global combo_key, harass_key
    global anti_gap_q, anti_gap_e, use_q_on_evade
    global e_range
    global randomize_q_pos
    global MaxRCountForUse
    global use_q_with_harass, use_e_with_harass

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("use_q_with_harass", use_q_with_harass)
    cfg.set_bool("use_e_with_harass", use_e_with_harass)

    cfg.set_bool("use_q_for_gapcloser", randomize_q_pos)

    cfg.set_bool("anti_gap_q", anti_gap_q)
    cfg.set_bool("anti_gap_e", anti_gap_e)

    cfg.set_bool("use_q_on_evade", use_q_on_evade)

    cfg.set_int("e_range", e_range)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_e_range", draw_e_range)

    cfg.set_float("MaxRCountForUse", MaxRCountForUse)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range
    global combo_key, harass_key
    global anti_gap_q, anti_gap_e, use_q_on_evade
    global e_range
    global randomize_q_pos
    global MaxRCountForUse
    global use_q_with_harass, use_e_with_harass


    combo_key = ui.keyselect("Combo key", combo_key)
    

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        randomize_q_pos = ui.checkbox("[Q] Use Q for_Gap closer", randomize_q_pos)
        use_q_with_harass = ui.checkbox("Use Q with Harass", use_q_with_harass)
        use_q_on_evade = ui.checkbox("Use Q on Evade", use_q_on_evade)
        anti_gap_q = ui.checkbox("[Q] Anti-Gap closer", anti_gap_q)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_e_with_harass = ui.checkbox("Use E with Harass", use_e_with_harass)
        anti_gap_e = ui.checkbox("[E] Anti-Gap closer", anti_gap_e)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        MaxRCountForUse = ui.dragfloat ("Max targets use for R", MaxRCountForUse, 1, 3, 5)
        ui.treepop()




def CheckWallStun(game, unit, PredictedE):
    global e_range
    PredictedPos = unit.pos
    Direction = PredictedPos.sub(game.player.pos)
    if PredictedE == True:
        # Time = (mesafe(unit.pos, game.player.pos) / 2000) + 0.25
        PredictedPos = unit.pos
        Direction = PredictedPos.sub(game.player.pos)
    for i in range(1, 11):
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * i))
        # game.draw_line(game.world_to_screen(unit.pos), game.world_to_screen(ESpot), 1, Color.GREEN )
        if SRinWall(game, ESpot):
            return ESpot
    return None



def Evade(game):
    global lastQ
    q_spell = getSkill(game, 'Q')


    for missile in game.missiles:
        end_pos = missile.end_pos.clone ()
        start_pos = missile.start_pos.clone ()
        curr_pos = missile.pos.clone ()
        bounding = game.player.gameplay_radius
        spell = get_missile_parent_spell (missile.name)
        if is_skillshot (missile.name) and game.point_on_line(
                game.world_to_screen(start_pos),
                game.world_to_screen(end_pos),
                game.world_to_screen(game.player.pos),
                bounding) and game.is_point_on_screen(curr_pos):
                    pos = getEvadePos (game, game.player.pos, bounding, missile, spell)
                    if pos and lastQ + 1 < game.time :
                        q_spell.move_and_trigger(game.world_to_screen(pos))
                        lastQ = game.time


RTargetCount = 0


def getCountR(game, dist):
    global RTargetCount, MaxRCountForUse
    RTargetCount = 0
    for champ in game.champs:
        if (
            champ
            and champ.is_visible
            and champ.is_enemy_to(game.player)
            and champ.isTargetable
            and champ.is_alive
            and game.is_point_on_screen(champ.pos)
            and game.distance(game.player, champ) < dist
        ):
            RTargetCount = RTargetCount + 1
    if int(RTargetCount) >= MaxRCountForUse:
        return True
    else:
        return False


def EDamage(game, target):

    total_atk = game.player.base_atk + game.player.bonus_atk
    return total_atk
def DrawDMG(game, player):
    color = Color.RED
    player = game.player
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            if EDamage(game, champ) >= champ.health:
                p = game.hp_bar_pos(champ)
                color.a = 5.0
                game.draw_rect(
                    Vec4(p.x - 47, p.y - 27, p.x + 61, p.y - 12), color, 0, 5
                )
def getVayneAttack2(game):

    for missile in game.missiles:
            # print(missile.name)
            if (missile.name == "vaynebasicattack2" 
            or missile.name == "vaynebasicattack"
            or missile.name == "zyrapseedmis"
            or missile.name == "vaynecritattack"
            or missile.name == "vayneultattack"
            ) :
                return True
    return False
    
def Combo(game):
    global lastQ, lastE
    global e_range
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    isPressE = False
    g_time = game.time
    target = TargetSelector(game,e["Range"]+300)

    #------------------- Q ---------------
    if (
        use_q_in_combo
        and IsReady(game, q_spell)
        and game.player.mana >= 30
    ):
        if target  :

                if (game.player.pos.distance(target.pos)<700):
                    
                            for buff in target.buffs:
                                if game.player.lvl >= 2:
                                        if buff.name == "VayneSilveredDebuff" :
                                                if buff.countAlt > 1 and getVayneAttack2(game):
                                                    
                                                        q_spell.trigger(False)


                elif game.player.lvl <= 2:
                        q_spell.trigger (False)
    #----------------  E ----------------
    if (
        use_e_in_combo
        and lastE + 1 < g_time
        and IsReady(game, e_spell)
        and game.player.mana >= 90
    ):
        target = TargetSelector(game, e["Range"])
        if target:
            for buff in target.buffs:
                if buff.name == "VayneSilveredDebuff":
                    if buff.countAlt > 1 :


                        if EDamage(game,target)>= target.health:

                            e_spell.move_and_trigger (game.world_to_screen (target.pos))
            if CheckWallStun(game, target, True):
                lastE = game.time
                e_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_r_in_combo and IsReady(game,r_spell) and game.player.mana>=80:
        if getCountR(game,e["Range"]+300):
            r_spell.trigger (False)
def Harass(game):
    global use_q_with_harass, use_e_with_harass
    global lastQ, lastE
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")

    if (
        use_q_with_harass
        and IsReady(game, q_spell)
        and game.player.mana > 30
    ):
        target = TargetSelector(game,e["Range"]+300)
        if target:
            
            q_spell.trigger(False)
    if (
        use_e_with_harass
        and IsReady(game, e_spell)
        and game.player.mana > 90
    ):
        target = TargetSelector(game,e["Range"]+300)
        if target:
            if CheckWallStun(game, target, True):
                
                e_spell.move_and_trigger(game.world_to_screen(target.pos))


def AntiGap(game):
    global anti_gap_q, anti_gap_e
    global lastQ, lastE
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    target = TargetSelector(game, 375)
    if target and target.atkRange < 375:
        if (
            anti_gap_e
            and lastE + 1 < game.time
            and IsReady(game, e_spell)
            and game.player.mana > 90
        ):
            lastE = game.time
            e_spell.move_and_trigger(game.world_to_screen(target.pos))



def winstealer_update(game, ui):
    global draw_q_range, draw_e_range,lastQ
    global combo_key, harass_key
    self = game.player

    if self.is_alive and game.is_point_on_screen(self.pos):
        if anti_gap_e and anti_gap_q:
            AntiGap(game)
        if game.was_key_pressed(combo_key):
            Combo(game)
        # if game.was_key_pressed(harass_key):
        #     Harass(game)

        
