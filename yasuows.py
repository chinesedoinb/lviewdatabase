from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from orb_walker import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Yasuo",
    "author": "SA1",
    "description": "SA1-Yasuo",
    "target_champ": "yasuo",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46
autoQKey=1

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

AutoR=True

use_w_on_evade = True

use_q_stack=True
use_e_underTower=True

flee=50

steal_kill_with_q = False
steal_kill_with_e = False
steal_kill_with_r = False

lane_clear_with_q = False
lasthit_with_q = False
lane_clear_with_eq = False
lane_clear_with_e = False

draw_q_range = False
draw_e_range = False
draw_r_range = False

q = {"Range": 450}
w = {"Range": 2500.0}
e = {"Range": 475}
r = {"Range": 1800}

e_RangeSlider=150

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,AutoR
    global draw_q_range, draw_e_range, draw_r_range,e_RangeSlider
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)
    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)
    flee=cfg.get_int("flee", flee)

    e_RangeSlider=cfg.get_int("e_RangeSlider", e_RangeSlider)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    AutoR=cfg.get_bool("AutoR", AutoR)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)
    lane_clear_with_eq = cfg.get_bool("lane_clear_with_eq", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)

    use_w_on_evade = cfg.get_bool("use_w_on_evade", True)
    
    use_e_underTower=cfg.get_bool("use_e_underTower", True)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range,e_RangeSlider
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee,AutoR

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("killsteal_key", killsteal_key)
    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    cfg.set_int("flee", flee)
    cfg.set_float("e_RangeSlider", e_RangeSlider)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("AutoR", AutoR)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)
    cfg.set_bool("lane_clear_with_eq", lane_clear_with_eq)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    
    cfg.set_bool("use_e_underTower", use_e_underTower)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range,e_RangeSlider
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee,AutoR

    ui.text("SA1-Yasuo : 1.0.0.0")
    ui.separator ()

    ################################
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    

    autoQKey=ui.keyselect("Auto Q key",autoQKey)
    
    
    flee=ui.keyselect("Flee",flee)
    e_RangeSlider = ui.sliderint("E Spell flee Cast Area",int(e_RangeSlider) , 70, 500)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_q_stack=ui.checkbox("Auto Q",use_q_stack)
        
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_on_evade = ui.checkbox("Use W on Evade", use_w_on_evade)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        
        use_e_underTower=ui.checkbox("Use E under Tower",use_e_underTower)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        AutoR=ui.checkbox("R toggel key", AutoR)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_eq = ui.checkbox("Lasthit with EQ", lane_clear_with_eq)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        ui.treepop()
    
def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance
def bffs(game, target):
    for buff in target.buffs:
        if 'knockup' in buff.name.lower ():
            return True

    return False
def GetClosestMobToEnemyForGap(game):
    global use_e_underTower
    closestMinionDistance = float("inf")
    closestMinion = None
    enemy = GetBestTargetsInRange(game, 5000)
    if enemy:
        for minion in game.minions:
            
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 475
                and not getBuff(minion, "YasuoE")
            ):
                if not use_e_underTower:
                    if minion.pos.distance(enemy.pos) <= e["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse
                if use_e_underTower:
                    if minion.pos.distance(enemy.pos) <= e["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse           
    return closestMinion


def QDamage(game, target):
    damage = 0
    if game.player.Q.level == 1:
        damage = 20 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 2:
        damage = 45 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 3:
        damage = 70 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 4:
        damage = 95 + (get_onhit_physical(game.player, target))
    elif game.player.Q.level == 5:
        damage = 120 + (get_onhit_physical(game.player, target))
    return damage


def EDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 60 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 2:
        damage = 70 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 3:
        damage = 80 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 4:
        damage = 90 + (get_onhit_magical(game.player, target))
    elif game.player.E.level == 5:
        damage = 100 + (get_onhit_magical(game.player, target))
    return damage


def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 200 + (get_onhit_physical(game.player, target))
    elif game.player.R.level == 2:
        damage = 350 + (get_onhit_physical(game.player, target))
    elif game.player.R.level == 3:
        damage = 500 + (get_onhit_physical(game.player, target))
    return damage


lastW = 0


def Evade(game):
    global e, lastW
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    for missile in game.missiles:
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot(
            game, game.player.pos, missile, spell, game.player.gameplay_radius * 2
        ) and game.is_point_on_screen(missile.pos):
            minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
                game, e["Range"]
            )
            if (
                minion
                and not InSkillShot(
                    game, minion.pos, missile, spell, minion.gameplay_radius * 2
                )
                and game.is_point_on_screen(missile.pos)
                and not IsUnderTurretEnemy(game, minion)
            ):
                if getBuff(minion, "YasuoE"):
                    continue
                if not IsDanger(game, minion.pos):
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            elif IsReady(game, w_spell):
                w_spell.move_and_trigger(game.world_to_screen(missile.pos))

lastE = 0
lastQ = 0
lastR = 0


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



def fleeOrb(game):
    target = None
    e_spell = getSkill(game, "E")
    q_spell = getSkill(game, "Q")
    TargetEnemy=TargetSelector(game,475)
    for minion in game.minions:
            if (
                not minion.is_alive
                or not minion.is_visible
                
                or minion.is_ally_to(game.player)
                or game.player.pos.distance(minion.pos) > 475
                or getBuff(minion,"YasuoE")
            ):
                continue
            target=minion
            cursor_pos_vec2 = game.get_cursor()
            cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
            if target:
                if get_distance(cursor_pos_vec3, game.world_to_screen(minion.pos)) <e_RangeSlider:
                    if IsReady(game, e_spell):
                            e_spell.move_and_trigger(game.world_to_screen(target.pos))

            # if TargetEnemy :
            #     if get_distance(cursor_pos_vec3, game.world_to_screen(TargetEnemy.pos)) <150:
            #         if IsReady(game, e_spell):
            #                 e_spell.move_and_trigger(game.world_to_screen(TargetEnemy.pos))
            # if IsReady(game, q_spell):
            #     q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    
spellTimer = Timer()
def Combo(game):
    global q, e, r
    global lastE, lastQ, lastR,spellTimer
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")


    before_cpos = game.get_cursor ()
    
    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        target = TargetSelector (game,475)
        if target :
            # for b in target.buffs:
            #     print(b.name)
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range'] and  spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)

    if use_q_in_combo and q_spell.name=="yasuoq3wrapper":
        target = TargetSelector (game,1000)
        if target :
            
                if IsReady(game, q_spell):
                    q_travel_time = 1000 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1000 and  spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)
    
            
    if use_r_in_combo and IsReady(game, r_spell):
        target = TargetSelector(game, r["Range"])
        minion = GetBestMinionsInRange(game, e["Range"])
        if target:
            if getBuff(target, "YasuoQ3Mis"):  
                if minion:
                    lastQ = game.time
                    lastE = game.time
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
                    q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                r_spell.trigger(False)
    if use_e_in_combo and lastE + 0.3 < game.time and IsReady(game, e_spell):
        target = TargetSelector(game, 475)
        minion = GetClosestMobToEnemyForGap(game)
        if target and not getBuff(target, "YasuoE"):
            if game.player.pos.distance (target.pos)>=300:
                e_spell.move_and_trigger(game.world_to_screen(target.pos))
        if minion and not target:
            
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))


def Harass(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    if (
        use_e_in_combo
        and lastE + 0.5 < game.time
        and IsReady(game, e_spell)
        and IsReady(game, q_spell)
    ):
        target = TargetSelector(game, e["Range"])
        if target and not buffIsAlive(game, getBuff(target, "YasuoE")):
            turret = GetBestTurretInRange(game, target.gameplay_radius * 2)
            if turret:
                return
            lastE = game.time
            e_spell.move_and_trigger(game.world_to_screen(target.pos))
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
    if use_e_in_combo and lastE + 0.5 < game.time and IsReady(game, e_spell):
        target = TargetSelector(game, r["Range"])
        if target:
            if target.pos.distance(game.player.pos) > q["Range"]:
                minion = GetClosestMobToEnemyForGap(game)
                if (
                    minion
                    and game.distance(minion, target) < e["Range"]
                    and not IsUnderTurretEnemy(game, minion)
                ):
                    lastE = game.time
                    e_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if use_q_in_combo and IsReady(game, q_spell):
        target = TargetSelector(game, q["Range"])
        if target:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))

def DrawAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Enabled", Color.BLACK, Color.GREEN, 10.0)
def DrawNotAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Disabled", Color.BLACK, Color.RED, 10.0)

def AutoQ(game):
    global q, e, r,use_q_stack,autoQKey ,spellTimer
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor ()
    
    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        target = GetBestTargetsInRange (game,475)
        if target :
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range'] and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)

    if use_q_stack and q_spell.name=="yasuoq3wrapper":
        target = TargetSelector (game,1000)
        if target :
                if IsReady(game, q_spell):
                    q_travel_time = 1000 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1000 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)
    if use_q_in_combo and q_spell.name=="yasuoq1wrapper" or q_spell.name=="yasuoq2wrapper":
        Minion =  GetBestMinionsInRange(game,475)
        target = TargetSelector (game,500)
        jungle= GetBestJungleInRange(game,475)
        if Minion and not target:
                if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (Minion, q_travel_time)
                    predicted_target = Fake_target (Minion.name, predicted_pos, Minion.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= q['Range'] and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)             
        if jungle and not target:
            if IsReady(game, q_spell):
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (jungle, q_travel_time)
                    predicted_target = Fake_target (jungle.name, predicted_pos, jungle.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1000 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
                        spellTimer.SetTimer(0.4)

def AutoRcast(game):
    r_spell = getSkill(game, "R")
    if use_r_in_combo and IsReady(game, r_spell):
        target = TargetSelector(game, r["Range"])
        if target:
            if bffs(game,target) or getBuff(target,"YasuoQ3Mis"): 
                
                r_spell.trigger(False)                


def Laneclear(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    if (
        lane_clear_with_q
        and IsReady(game, q_spell)
        and q_spell.name == "yasuoq3wrapper"
    ):
        minion = GetBestMinionsInRange(game, 1060) or GetBestJungleInRange(
            game, e["Range"]
        )
        if minion:
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_q and lastQ + 1 < game.time and IsReady(game, q_spell):
        minion = GetBestMinionsInRange(game, q["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if minion:
            lastQ = game.time
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
    if lane_clear_with_e and lastE + 0.5 < game.time and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if (
            minion
            and EDamage(game, minion) >= minion.health
            and not IsUnderTurretEnemy(game, minion)
        ):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            lastE = game.time
    if (
        lane_clear_with_eq
        and lastE + 0.5 < game.time
        and IsReady(game, e_spell)
        and IsReady(game, q_spell)
    ):
        minion = GetBestMinionsInRange(game, e["Range"]) or GetBestJungleInRange(
            game, e["Range"]
        )
        if (
            minion
            and (
                EDamage(game, minion) >= minion.health
                or QDamage(game, minion) >= minion.health
            )
            and not IsUnderTurretEnemy(game, minion)
        ):
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))
            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
def flee2(game):
    before_cpos = game.get_cursor ()
    e_spell = getSkill(game, "E")
    q_spell = getSkill(game, "Q")
    minion=fleeOrb(game,1000)
    if minion:
            
            e_spell.move_and_trigger(game.world_to_screen(minion.pos))

def FleeHelper(game):
    global q, e, r
    global lastE, lastQ, lastR
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
              
    if use_e_in_combo and IsReady(game, e_spell):
        target = TargetSelector(game, 475)
        minion = GetClosestMobToEnemyForGap(game)
        if target and not getBuff(target, "YasuoE"):
                e_spell.move_and_trigger(game.world_to_screen(target.pos))


 

def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee

    cursor_pos_vec2 = game.get_cursor()
    game.draw_circle(cursor_pos_vec2,e_RangeSlider,100,1,Color.GREEN)

    self=game.player
           
    if self.is_alive and game.is_point_on_screen(self.pos) :
        AutoRcast(game)
        if game.was_key_pressed(flee):
            
            fleeOrb(game)
            FleeHelper(game)
        if game.was_key_pressed(combo_key):
            Combo(game)
            
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            
        if game.was_key_pressed(harass_key):
            Harass(game)

        if use_w_on_evade:
            Evade(game)  

        if use_q_stack:
            AutoQ(game)  
            DrawAutoQ(game)

        if not use_q_stack:
            DrawNotAutoQ(game) 

        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack  
              
       