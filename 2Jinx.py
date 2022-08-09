from asyncio.windows_events import NULL
from turtle import distance
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import json, time, math
from commons.targit import *

winstealer_script_info = {
    "script": "SA1-Jinx",
    "author": "SA1",
    "description": "SA1-Jinx",
    "target_champ": "jinx",
}

FishStacks = 0
isFishBones = True

combo_key = 57
harass_key = 45
killsteal_key = 46
laneclear_key = 47
flee_key = 30

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

steal_kill_with_w = False
steal_kill_with_r = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False

laneclear_with_q = True

w = {"Range": 1400}
e = {"Range": 900} 


def winstealer_load_cfg(cfg):
    global combo_key, harass_key, laneclear_key, killsteal_key, flee_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global steal_kill_with_w, steal_kill_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global laneclear_with_q

    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    killsteal_key = cfg.get_int("killsteal_key", 46)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    flee_key = cfg.get_int("flee_key", 30)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    laneclear_with_q= cfg.get_bool("laneclear_with_q", True)

    steal_kill_with_w = cfg.get_bool("steal_kill_with_w", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)


def winstealer_save_cfg(cfg):
    global combo_key, harass_key, laneclear_key, killsteal_key, flee_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global steal_kill_with_w, steal_kill_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global laneclear_with_q

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("killsteal_key", killsteal_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("flee_key", flee_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("laneclear_with_q", laneclear_with_q)


    cfg.set_bool("steal_kill_with_w", steal_kill_with_w)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)


def winstealer_draw_settings(game, ui):
    global combo_key, harass_key, laneclear_key, killsteal_key, flee_key
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global steal_kill_with_w, steal_kill_with_r
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global laneclear_with_q


    combo_key = ui.keyselect("Combo key", combo_key)
    
    
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        laneclear_with_q = ui.checkbox("Laneclear with q", laneclear_with_q)

        ui.treepop()
    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)

        ui.treepop()
    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)

        ui.treepop()
    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)


        ui.treepop()


qDamages = [20, 40, 55]
rDamages = [250, 350, 450]

class Fake_target():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def CalcRDmg(game, unit):
    global qDamages
    damage = 0
    distance = game.player.pos.distance(unit.pos)
    mathdist = math.floor(math.floor(distance) / 100)
    level = game.player.R.level
    baseq = rDamages[level - 1] + 0.15 + game.player.bonus_atk
    qmissheal = qDamages[level - 1] / 100 * (unit.max_health - unit.health)
    if distance < 100:
        damage = baseq + qmissheal
    elif distance >= 1500:
        damage = baseq + 10 + qmissheal
    else:
        damage = ((((mathdist * 6) + 10) / 100) * baseq) + baseq + qmissheal
    return rDamages[level - 1] + game.player.bonus_atk


def GetEnemyCount(game, dist):
    count = 0
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
            count = count + 1
    return count


lastQ = 0
lastW = 0
lastE = 0
lastR = 0



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

def QActive(game):
    q_spell = getSkill(game, "Q")
    if not getBuff(game.player,"JinxQ"):
        q_spell.trigger(False)


def QNotActive(game):
    q_spell = getSkill(game, "Q")
    if getBuff(game.player,"JinxQ"):
        q_spell.trigger(False)


def Combo(game):
    global lastQ, lastW, lastE, lastR
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if (
        use_q_in_combo
        and IsReady(game, q_spell)
        and game.player.mana > 20
        
    ):
        
        target=TargetSelector(game, 900)
        if target:
            distanceToTarget=game.player.pos.distance(target.pos)

            if not getBuff(game.player,"JinxQ") and distanceToTarget>600:
                q_spell.trigger(False)
            if getBuff(game.player,"JinxQ") and distanceToTarget<600 :
               q_spell.trigger(False)     
            # if distanceToTarget<=600:
            #     QNotActive(game)

    if (use_w_in_combo 
        and IsReady(game, w_spell) 
            
    ):
        if game.player.mana>=90:
            target = TargetSelector(game, w['Range'])
            if target:
                dis=game.player.pos.distance (target.pos)
                if dis<=1450:
                    w_travel_time = (dis / 1200 )
                    predicted_pos = predict_pos(target,w_travel_time)
                # dis=game.player.pos.distance (target.pos)
                # w_travel_time = (w['Range'] / 3300 )
                # predicted_pos = predict_pos(target,w_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                game.draw_line(game.world_to_screen(target.pos),game.world_to_screen(predicted_pos),10,Color.BLUE)
                
                playerAAdist=game.player.atkRange + game.player.gameplay_radius +50
                if (game.player.pos.distance(predicted_target.pos) <= w['Range'] 
                and predicted_target.pos.distance(game.player.pos)>= playerAAdist
                and not IsCollisioned(game, predicted_target)):
                    if target.ai_server_pos.distance (target.ai_navEnd)<=350:
                        # w_spell.move_and_trigger(game.world_to_screen(target.ai_navEnd))
                        if predicted_target.pos.distance (target.ai_navEnd)<=200:
                            w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    if target.ai_server_pos.distance (target.ai_navEnd)>=650:
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
    if (
        use_e_in_combo
        and IsReady(game, e_spell)
        and game.player.mana > 90
        
    ):
        
        target = TargetSelector(game, 900)
        if target:
            if game.player.mana>=90:
                predicted_pos = game.GetPredication(target,e['Range'] ,1700,0.100)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if target.pos.distance (target.ai_navEnd)<=700:
                        e_spell.move_and_trigger(game.world_to_screen(target.ai_navEnd))
                
    if (
        use_r_in_combo
        and IsReady(game, r_spell)
        and game.player.mana > 100
        
    ):
        
        target = TargetSelector(game, 4000)
        if target:
            if game.player.mana>=90:
                disToPlayer=game.player.pos.distance (target.pos)
            
                e_travel_time = disToPlayer/1700
                predicted_pos = predict_pos (target, e_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)

                playerAAdist=game.player.atkRange + game.player.gameplay_radius +50
                
                if (game.player.pos.distance(predicted_target.pos) <= 4000 
                and predicted_target.pos.distance(game.player.pos)>= playerAAdist  
                and target.health < CalcRDmg(game, target)):
                    r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                    



def Laneclear(game):
    global lastQ
    q_spell = getSkill(game, "Q")
    if (
        laneclear_with_q
        and IsReady(game, q_spell)
        and (game.player.mana / game.player.max_mana * 100) > 40
        and lastQ + 1 < game.time
    ):
        minion = GetBestMinionsInRange(game, (game.player.Q.level * 25) + 75 + 600)
        if minion:
            if game.player.atkRange < 599:
                if (
                    game.player.pos.distance(minion.pos) > 600 + minion.gameplay_radius
                    and game.player.pos.distance(minion.pos)
                    < (game.player.Q.level * 25) + 75 + 600 + minion.gameplay_radius
                ):
                    q_spell.trigger(False)
                    lastQ = game.time
            elif (
                game.player.pos.distance(minion.pos) < 600 + minion.gameplay_radius
                and game.player.atkRange > 600
            ):
                q_spell.trigger(False)
                lastQ = game.time


def winstealer_update(game, ui):
    self = game.player
    target=TargetSelector(game,game.player.atkRange + game.player.gameplay_radius + 25)
    # item1 = getSkill(game, "item2")
    if self.is_alive :
        
        target = TargetSelector(game, w['Range'])
        if target:
                
                dis=game.player.pos.distance (target.pos)
                if dis<=50000:
                    w_travel_time = (dis / 1200 )
                    predicted_pos = predict_pos(target,w_travel_time)
                    predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                    game.draw_line(game.world_to_screen(target.pos),game.world_to_screen(predicted_pos),3,Color.RED)
                
        if game.was_key_pressed(combo_key):
            
            Combo(game)
            # for missile in game.missiles:
            #     # print(missile.name)
            #     if (missile.name == "jinxbasicattack2" 
            #     or missile.name == "jinxbasicattack" 
            #     or missile.name == "jinxqattack"
            #     or missile.name == "jinxqattack2"):
            #         if target:
            #             game.click_at(False, game.world_to_screen(target.pos))
                
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
