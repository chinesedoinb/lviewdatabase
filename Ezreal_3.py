from asyncio.windows_events import NULL
from dis import dis
from enum import auto
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
    "script": "Ezreal",
	"author": "SA1",
	"description": "SA1 Ezreal",
	"target_champ": "ezreal"
}


lastE = 0
lastQ = 0

last_attacked = 0

combo_key = 0
harass_key = 0
laneclear_key = 0
killsteal_key = 0

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True


auto_q = True


steal_kill_with_q = False
steal_kill_with_e = False
steal_kill_with_r = False

use_e_evade = True

lane_clear_with_q = False
lasthit_with_q = False

toggled = False

draw_q_range = False
draw_e_range = False
draw_r_range = False

q = { 'Range': 1150 }
w = { 'Range': 1150 }
e = { 'Range': 475 }
r = { 'Range': 25000 }

spell_priority = {
	'Q': 0,
    'W': 0,
	'E': 0,
	'R': 0
}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo
    global draw_q_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q
    global use_e_evade, auto_q
    combo_key = cfg.get_int("combo_key", 0)	
    harass_key = cfg.get_int("harass_key", 0)
    laneclear_key = cfg.get_int("laneclear_key", 0)
    killsteal_key = cfg.get_int("killsteal_key", 0)

    use_q_in_combo   = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo   = cfg.get_bool("use_w_in_combo", True)
    use_r_in_combo   = cfg.get_bool("use_r_in_combo", True)
    use_e_in_combo   = cfg.get_bool("use_e_in_combo", True)

    use_e_evade = cfg.get_bool("use_e_evade", False)
    auto_q = cfg.get_bool("auto_q", True)

    steal_kill_with_q   = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e   = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r   = cfg.get_bool("steal_kill_with_r", False)

    lane_clear_with_q   = cfg.get_bool("lane_clear_with_q", False)
    lasthit_with_q   = cfg.get_bool("lasthit_with_q", False)

    spell_priority = json.loads(cfg.get_str('spell_priority', json.dumps(spell_priority)))
	
def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo
    global draw_q_range, draw_r_range, draw_e_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q
    global use_e_evade
    global auto_q
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("killsteal_key", killsteal_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)

    cfg.set_bool("use_e_evade", use_e_evade)
    cfg.set_bool("auto_q", auto_q)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lasthit_with_q", lasthit_with_q)

    cfg.set_str('spell_priority', json.dumps(spell_priority))
	
def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo
    global draw_q_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q
    global use_e_evade
    global auto_q
    ui.text("SA1")
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    killsteal_key = ui.keyselect("Killsteal key", killsteal_key)
    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)

        auto_q = ui.checkbox("Auto use Q on target (beta)", auto_q)
        ui.text("EXPERIMENTAL!")
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        ui.treepop()

    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_e_evade = ui.checkbox("Use E on Evade", use_e_evade)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        ui.treepop()

    if ui.treenode("Laneclear"):
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        ui.treepop()

def fast_prediction(game, spell, caster, target, range):
	global Spells

	t = target.pos.sub(caster.pos).length() / spell.speed
	t += spell.travel_time

	target_dir = target.pos.sub(target.prev_pos).normalize()
	if math.isnan(target_dir.x):
		target_dir.x = 0.0
	if math.isnan(target_dir.y):
		target_dir.y = 0.0
	if math.isnan(target_dir.z):
		target_dir.z = 0.0

	if target_dir.x == 0.0 and target_dir.z == 0.0:
		return target.pos

	result = target.pos.add(target_dir.scale((t + spell.speed) * target.movement_speed))

	return result


def IsDangerousPosition(game, target):
    if game.is_point_on_screen(target.pos) and GetDistance(game.player.pos, target.pos) < 300:
        return True
    else: 
        return False

def getEvadePos1(game, current, br, missile, spell):
    self = game.player

    direction = missile.end_pos.sub(missile.start_pos)

    pos3 = missile.end_pos.add(Vec3(-direction.z, direction.y * 1.0, direction.x * 1.0))
    pos4 = missile.end_pos.add(Vec3(direction.z * 1.0, direction.y, -direction.x))

    direction2 = pos3.sub(pos4)
    direction2 = game.clamp2d(direction2, br)

    direction3 = Vec3(0, 0, 0)
    direction3.x = -direction2.x
    direction3.y = -direction2.y
    direction3.z = -direction2.z

    points = list()

    for k in range(-8, 8, 2):
        if game.is_left(
            game.world_to_screen(missile.start_pos),
            game.world_to_screen(missile.end_pos),
            game.world_to_screen(self.pos),
        ):
            test_pos = current.add(
                direction3.add(direction.normalize().scale(k * 70).add(Vec3(70, 0, 70)))
            )
            if not SRinWall(game, test_pos) and not IsDanger(game, test_pos):
                points.append(test_pos)
        else:
            test_pos = current.add(
                direction2.add(direction.normalize().scale(k * 70).add(Vec3(70, 0, 70)))
            )
            if not SRinWall(game, test_pos) and not IsDanger(game, test_pos):
                points.append(test_pos)
    if len(points) > 0:
        points = sorted(points, key=lambda a: self.pos.distance(a))
        return points[0]
    return None

def InSkillShot(game, pos, missile, spell, radius):
    pointSegment, pointLine, isOnSegment = VectorPointProjectionOnLineSegment(
        missile.start_pos, missile.end_pos, pos
    )
    if spell.flags & SFlag.Line or spell.flags & SFlag.SkillshotLine:
        return isOnSegment and pointSegment.distance(pos) <= game.player.gameplay_radius * 2
    if spell.flags & SFlag.Area:
        return game.point_on_line(
            game.world_to_screen(missile.start_pos),
            game.world_to_screen(missile.end_pos),
            game.world_to_screen(pos),
            radius,
        )
    return (
        isOnSegment
        and pointSegment.distance(pos)
        <= (missile.width or missile.cast_radius) + radius + game.player.gameplay_radius
    )

def Evade(game):
     global lastE, use_e_evade
     e_spell = getSkill(game, 'E')
     for missile in game.missiles:
         end_pos = missile.end_pos.clone()
         start_pos = missile.start_pos.clone()
         curr_pos = missile.pos.clone()
         bounding = game.player.gameplay_radius
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
                 bounding,
             )
             and game.is_point_on_screen(curr_pos)
         ):
             pos = getEvadePos1(game, game.player.pos, bounding, missile, spell)
             if pos:
                 if IsReady(game, e_spell) and use_e_evade and GetDistanceSqr(pos, game.player.pos)< 475 * 475 and not IsDanger(game, pos):
                     e_spell.move_and_trigger(game.world_to_screen(pos))

def GetDistanceSqr(p1, p2):
    p2 = p2
    d = p1.sub(p2)
    d.z = (p1.z or p1.y) - (p2.z or p2.y)
    return d.x * d.x + d.z * d.z

def GetDistance(p1, p2):
    squaredDistance = GetDistanceSqr(p1, p2)
    return math.sqrt(squaredDistance)

def TargetSelection(target, dist, range):
    global q
    if dist <= range:
        return True
    return False

def QDamage(game, target):
    damage = 0
    if game.player.Q.level == 1:
        damage = 20 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.Q.level == 2:
        damage = 45 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.Q.level == 3:
        damage = 70 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.Q.level == 4:
        damage = 95 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.Q.level == 5:
        damage = 120 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    return damage

def WDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 80 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) 
    elif game.player.E.level == 2:
        damage = 135 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.E.level == 3:
        damage = 190 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) 
    elif game.player.E.level == 4:
        damage = 245 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.E.level == 5:
        damage = 300 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    return damage


def EDamage(game, target):
    damage = 0
    if game.player.E.level == 1:
        damage = 80 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) 
    elif game.player.E.level == 2:
        damage = 150 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.E.level == 3:
        damage = 180 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target)) 
    elif game.player.E.level == 4:
        damage = 230 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    elif game.player.E.level == 5:
        damage = 280 + (get_onhit_physical(game.player, target) + get_onhit_magical(game.player, target))
    return damage


def RDamage(game, target):
    damage = 0
    if game.player.R.level == 1:
        damage = 350 
    elif game.player.R.level == 2:
        damage = 500 
    elif game.player.R.level == 3:
        damage = 650 
    return damage

def find_minion_target(game, min_range):
	target = None
	for minion in game.minions:
		if minion.is_enemy_to(game.player) and minion.is_alive and game.distance(game.player, minion) < min_range and game.is_point_on_screen(minion.pos):
			target = minion
		
	return target

def GetKitePosition(game, target):
    for i in range(0, 360, 22):
        angle = i * (math.pi/180)
  
        myPos = game.player.pos
        tPos = target.pos
  
        rot = RotateAroundPoint(tPos, myPos, angle)
        pos = myPos.add(myPos.sub(rot))
        if ValidTarget(target):
            for champ in game.champs:
                dist = GetDistance(target.pos, pos) / 2
                if (dist <500 and dist > 400):
                    return pos
                else:
                    dist = GetDistance(target.pos, pos)
                    if dist > 400 and dist < 500:
                        return pos
    return pos

def castE(game, target, pos):
    skill = getSkill(game, 'E')
    if IsReady(game, skill):
        before_pos = game.get_cursor()
        if GetKitePosition(game, target).distance(game.player.pos) <= 800:
            game.move_cursor(game.world_to_screen(GetKitePosition(game, target)))
            skill.trigger(False)

class Fake_target():
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

Q_mana= [28,31,34,37,40]
spellTimer = Timer()
def Combo(game, player):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo ,spellTimer
    global draw_q_range, draw_r_range, draw_e_range
    global   combo_key, harass_key, laneclear_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q
    global q, w, e, r
    global lastE, lastQ
    global use_e_evade
    global castE
    global last_attacked
    q_spell = getSkill(game, 'Q')
    w_spell = getSkill(game, 'W')
    e_spell = getSkill(game, 'E')
    r_spell = getSkill(game, 'R')
    #atk_speed = player.base_atk_speed * player.atk_speed_multi

    if use_w_in_combo and IsReady(game, w_spell) and game.player.mana>=50 :
        target = TargetSelector(game, w['Range'])
        if target:

            dis = game.player.pos.distance (target.pos)
            w_travel_time = dis/ 1200 


            predicted_pos = predict_pos(target,w_travel_time)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            if  spellTimer.Timer():
                if game.player.pos.distance (target.pos)<=1150 :
                        w_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
                        spellTimer.SetTimer(0.2)
    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana>= Q_mana[game.player.Q.level - 1]:
        target = TargetSelector(game, q['Range'])
        if target :
            dis=game.player.pos.distance (target.pos)

            q_travel_time = (dis/2000)
            predicted_pos = predict_pos(target,q_travel_time)
            #cast_point = castpoint_for_collision(game, q_spell, game.player, target)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            game.draw_line(game.world_to_screen(target.pos), game.world_to_screen(predicted_target.pos), 2, Color.GREEN)
            if  spellTimer.Timer():
                if game.player.pos.distance (target.pos)<=1150 :
                    if not IsCollisioned(game, predicted_target):
                        q_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
                        spellTimer.SetTimer(0.4)

    if use_r_in_combo and IsReady(game, r_spell) and game.player.mana>=100:
            target = TargetSelector(game, 3000)
            if target:
               r_travel_time = 3000 / 2000
               predicted_pos = predict_pos(target, r_travel_time)
               predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
               if game.player.pos.distance(predicted_target.pos) <= 3000 and target.health < RDamage(game, target):
                    if  spellTimer.Timer():
                        r_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
                        spellTimer.SetTimer(0.4)

    if use_e_in_combo and IsReady(game, e_spell):
        for champ in game.champs:
            for buff in champ.buffs:
             if(buff.name == "ezrealwattach"):
              target = champ
              if target and getBuff(target, "ezrealwattach"):
                    e_spell.trigger(False)
                        



def Auto(game):
        global spellTimer
        q_spell = getSkill(game, 'Q')
        before_cpos = game.get_cursor()
        target =  TargetSelector(game, q['Range'])
        if use_q_in_combo and IsReady(game, q_spell) and game.player.mana>= Q_mana[game.player.Q.level - 1]:
            
            if target:
                q_travel_time = q['Range'] / 2000
                predicted_pos = predict_pos(target, q_travel_time)
                predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos) <= q['Range'] and not IsCollisioned(game, predicted_target):
                    if spellTimer.Timer():
                        q_spell.move_and_trigger (game.world_to_screen (predicted_target.pos))
                        spellTimer.SetTimer(0.4)

def LaneClear(game):

    global debug_dmg, use_e_evade

    q_spell = getSkill(game, 'Q')
    before_cpos = game.get_cursor()
    num = 10000
    if q_spell and IsReady(game, q_spell ) and game.player.mana > 100:
        minion = GetBestMinionsInRange(game, 1100)
        if minion and is_last_hitable and not IsCollisioned(game, game.player, minion):
            q_spell.move_and_trigger (game.world_to_screen (minion.pos))

            
        elif minion and minion.health < num:
            num = minion.health
            q_spell.move_and_trigger (game.world_to_screen (minion.pos))
       # else:
           # game.move_cursor(game.world_to_screen(minion.pos))
           # game.press_right_click()
            # time.sleep(0.02)
            #return game.move_cursor(before_cpos)

def Harass(game):
    target =  TargetSelector(game, q['Range'])
    w_spell = getSkill(game, 'W')
    q_spell = getSkill(game, 'Q')
    before_cpos = game.get_cursor()
    if ValidTarget(target) and target and target.is_enemy_to(game.player) and game.is_point_on_screen(target.pos) and IsReady(game, w_spell) and not IsCollisioned(game, target):
        if game.player.pos.distance(target.pos) <= w['Range']:
            game.move_cursor(game.world_to_screen(target.pos))
            game.press_right_click()
            w_spell.trigger(False)
            time.sleep(0.02)
            game.move_cursor(before_cpos)
            game.press_right_click()
    if ValidTarget(target) and target and target.is_enemy_to(game.player) and game.is_point_on_screen(target.pos) and IsReady(game, q_spell) and not IsCollisioned(game, target):
        if game.player.pos.distance(target.pos) <= q['Range']:
            game.move_cursor(game.world_to_screen(target.pos))
            game.press_right_click()
            q_spell.trigger(False)
            time.sleep(0.02)
            game.move_cursor(before_cpos)
            game.press_right_click()
def PrediticTest(game, target,  radius,  spell_range,  spell_missile_speed,  spell_cast_delay):
		# //vars: obj_target_ptr, radius, spell_range, spell_missile_speed, spell_cast_delay
        missile_speed = 2100
        ping = 40
        flytime_max = 0.0
        
        if  missile_speed != 0 :
                
            flytime_max =  spell_range / spell_missile_speed 

        t_min = spell_cast_delay + ping / 2000.0
        t_max = flytime_max + spell_cast_delay + ping / 1000.0
        path_time = 0.0
        path_bounds=[NULL,NULL] 
        
        ppNavStart = target.ai_navBegin
        ppNavEnd = target.ai_navEnd
        for ppNavPtr in range(ppNavStart ,ppNavEnd):
            cur = game.world_to_screen(ppNavPtr)
            next = game.world_to_screen(ppNavPtr + 1)
            t = next.distance(cur)
            print(t)
        # if (path_time <= t_min and path_time + t >= t_min):

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_evade, use_e_in_combo
    global draw_q_range, draw_r_range, draw_e_range
    global q, e, r
    global combo_key, laneclear_key, harass_key, laneclear_key
    self = game.player

    target = TargetSelector(game, q['Range'])
    if target :
            dis=game.player.pos.distance (target.pos)

            q_travel_time = (dis/2000)
            predicted_pos = predict_pos(target,q_travel_time)
            #cast_point = castpoint_for_collision(game, q_spell, game.player, target)
            predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)
            game.draw_line(game.world_to_screen(target.pos), game.world_to_screen(predicted_target.pos), 2, Color.GREEN)
    if self.is_alive and self.is_visible :
        
        
        if auto_q:
            Auto(game)
        if game.was_key_pressed(combo_key):
            Combo(game, self)
        
        if game.was_key_pressed(laneclear_key):
            LaneClear(game)
        if game.was_key_pressed(harass_key):
            Harass(game)
        # if game.was_key_pressed(killsteal_key):
        #     if steal_kill_with_r:
        #         killStealR(game)