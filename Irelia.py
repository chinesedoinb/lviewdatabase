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
    "script": "Irelia",
    "author": "SA1",
    "description": "Irelia",
    "target_champ": "irelia",
}

combo_key = 57
laneclear_key = 47

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

draw_q_dmg = False

q = {"Range": 600}
w = {"Range": 825}
e = {"Range": 775}
r = {"Range": 1000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

debug_hp = 0
debug_dmg = 0.0


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q
    global lane_clear_with_q
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

    draw_q_dmg = cfg.get_bool("draw_q_dmg", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", False)
    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    
    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q
    global lane_clear_with_q
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("draw_q_range", draw_q_range)

    cfg.set_bool("draw_q_dmg", draw_q_dmg)
    

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range, draw_q_dmg
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q
    global lane_clear_with_q
    ui.begin(" Irelia ")
##    ui.text(str(debug_hp))
##    ui.text(str(debug_dmg))
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        draw_q_dmg = ui.checkbox("Draw Q Dmg", draw_q_dmg)
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
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
        lane_clear_with_q = ui.checkbox("Laneclear with Q (LastHit)", lane_clear_with_q)
        ui.treepop()
    ui.end()


lastQ = 0

mana_q = 20
mana_w = [70, 75, 80, 85, 90]
mana_e = 50
mana_r = 100

def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )

qLvLDmg = [5, 25, 45, 65, 85]
qMinionDmg = 0
passiveDmg = 0
playerLvl = 0
Espot = 0
ir_q = {"Range": 600}

def GetClosestMobToEnemyForGap(game):
    global ir_q
    closestMinionDistance = float("inf")
    closestMinion = None
    enemy = GetBestTargetsInRange(game, 3000)
    if enemy:
        for minion in game.minions:
            if (
                minion
                and ValidTarget(minion)
                and game.is_point_on_screen(minion.pos)
                and minion.pos.distance(game.player.pos) <= 600
                and minion.is_enemy_to(game.player)
            ):
                # if not use_q_underTower:
                #     if minion.pos.distance(enemy.pos) <= ir_q["Range"] and not IsUnderTurretEnemy(game, minion) :
                        
                #             minionDistanceToMouse = minion.pos.distance(enemy.pos)
                #             if minionDistanceToMouse <= closestMinionDistance:
                #                 closestMinion = minion
                #                 closestMinionDistance = minionDistanceToMouse
                
                if minion.pos.distance(enemy.pos) <= ir_q["Range"]:
                        
                            minionDistanceToMouse = minion.pos.distance(enemy.pos)
                            if minionDistanceToMouse <= closestMinionDistance:
                                closestMinion = minion
                                closestMinionDistance = minionDistanceToMouse           
    return closestMinion

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


def qDmg(game, target):
    global qLvLDmg, qMinionDmg, passiveDmg, debug_dmg, playerLvl, totalatk

    playerLvl = game.player.Q.level + game.player.W.level + game.player.E.level + game.player.R.level
    totalatk = game.player.base_atk + game.player.bonus_atk
    qMinionDmg = (40 + (playerLvl * 12))

    
    
    if getBuff(game.player, "ireliapassivestacksmax"):
        passiveDmg = ((7 + (playerLvl * 3)) + (game.player.bonus_atk * 0.3))
    else:
        passiveDmg = 0

    debug_dmg = get_onhit_magical(game.player, target)

    return (
        qLvLDmg[game.player.Q.level - 1]
        + (
            (totalatk * 0.6)
            + passiveDmg
        )
        
    )


def CanQ (game,target) -> bool:
    global qMinionDmg
    if getBuff(target, "ireliamark"):
        return True
    if (qDmg(game, target) + qMinionDmg) > effHP(game, target):
        return True
    return False



def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo , ireliaPos
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i, Espot
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

   

    player = game.player
    i = 0
    target = TargetSelector(game, e["Range"])
    if target:
        PredictedPos = target.pos
        Direction = PredictedPos.sub(game.player.pos)
        ESpot = PredictedPos.add(Direction.normalize().scale(40 * 15))


    if use_r_in_combo:
        if IsReady(game, r_spell):
            if target and IsReady(game, r_spell) and game.player.mana >= 100:
                TargetHP = int(target.health / target.max_health * 100)

                q_travel_time = 950/2000
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if TargetHP<=40:
                    r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
            
    
    if use_e_in_combo :
            if target and IsReady(game, e_spell) :
                
                if not getBuff(target,"ireliamark") or not IsReady(game, r_spell) or not getBuff(target,"ireliarslow"):
                    if getBuff(game.player, "IreliaE") :
                        q_travel_time = 850/2000
                        predicted_pos = predict_pos (target, q_travel_time)
                        predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                        e_spell.move_and_trigger(game.world_to_screen((predicted_target.pos).add(Direction.normalize().scale(60 * 10))))
                    else:
                        if game.player.mana >= 50:
                            e_spell.move_and_trigger(game.world_to_screen(PredictedPos.add(Direction.normalize().scale(-80 * 11))))
                            # time.sleep (0.2)


# logic :
#    1. if target is near and E is not ready > if minion is near target > Q cast to minion
#    2. else if E is ready > Q cast to target
#    3  else if Target is not Near and Minion is near > Q to Minion > if minion is near Target and target has irelia mark > cast Q to target
    if use_q_in_combo and IsReady(game,q_spell) and game.player.mana >=20:
        #if target and getBuff(target, "ireliamark"):
        target = TargetSelector(game, 600)
        minion = GetBestMinionsInRange(game,3000)
        CloseMinion= GetClosestMobToEnemyForGap(game)
        if target:
            if minion and minion.pos.distance(game.player.pos)<=600 and minion.pos.distance(target.pos)<=600:
                if not CanQ(game,target):
                    if (qDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                            q_spell.move_and_trigger(game.world_to_screen(minion.pos))
                else:
                    if CanQ(game,target):
                        q_spell.move_and_trigger(game.world_to_screen(target.pos))
            else:
                if game.player.pos.distance(target.pos)<=600:
                    if CanQ(game,target):
                        q_spell.move_and_trigger(game.world_to_screen(target.pos))
                



    if use_w_in_combo:
        if target and IsReady(game, w_spell) and game.player.mana >= mana_w[game.player.W.level -1]:
            w_spell.move_and_trigger(
                game.world_to_screen(
                    castpoint_for_collision(game, w_spell, game.player, target)
                )
            )


def Laneclear(game):

    global debug_dmg
    
    q_spell = getSkill(game, "Q")
    if lane_clear_with_q:
        minion = GetBestMinionsInRange(game, q["Range"])

    
        if minion and IsReady(game, q_spell) and game.player.mana >= 20:
            if (qDmg(game, minion) + qMinionDmg) > effHP(game, minion):
                q_spell.move_and_trigger(game.world_to_screen(minion.pos))

                                
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg, player
    self = game.player

    target = GetBestTargetsInRange(game, e["Range"])
    player = game.player
   
    # for b in target.buffs:
    #     print(b.name)
    if self.is_alive  :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
