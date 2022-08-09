import sys

from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 Syndra",
    "author": "SA1",
    "description": "SA1 Syndra",
    "target_champ": "syndra",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46
autoQKey=3
use_q_stack=True

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

use_q_in_harass = True
use_w_in_harass = False
use_e_in_harass = False
use_r_in_harass = False

lane_clear_with_q = False
lane_clear_with_w = False
lasthit_with_q = False

steal_kill_with_e = False

toggled = False

draw_q_range = True
draw_w_range = False
draw_e_range = False
draw_r_range = False

draw_e_dmg = False

q = {"Range": 800}
w = {"Range": 925}
e = {"Range": 700}
r = {"Range": 750}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,use_q_stack
    global use_q_in_harass, use_w_in_harass, use_e_in_harass, use_r_in_harass
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global lane_clear_with_q,lane_clear_with_w
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)

    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", False)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,use_q_stack
    global use_q_in_harass, use_w_in_harass, use_e_in_harass, use_r_in_harass
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e

    global lane_clear_with_q,lane_clear_with_w 

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)


    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    # cfg.set_bool("lane_clear_with_e", lane_clear_with_e)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,use_q_stack
    global use_q_in_harass, use_w_in_harass, use_e_in_harass, use_r_in_harass
    global draw_q_range,draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global lane_clear_with_e
    global draw_e_dmg
    global lane_clear_with_q,lane_clear_with_w 

    ui.text("SA1-Syndra:1.0.0.0")
    ui.separator ()

    combo_key = ui.keyselect("Combo key", combo_key)
    # harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Lane clear key", laneclear_key)
    #killsteal_key = ui.keyselect("Killsteal key", killsteal_key)

    autoQKey=ui.keyselect("Auto Q key",autoQKey)

    if ui.treenode("Combo"):
        use_q_in_combo = ui.checkbox("Use Q", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R", use_r_in_combo)
        use_q_stack=ui.checkbox("Auto Q",use_q_stack)
        ui.treepop()

    if ui.treenode("LaneClear"):
        lane_clear_with_q = ui.checkbox("Use Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Use W", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Draw"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_e_range = ui.checkbox("Draw E Range", draw_e_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()


ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def BallDMG(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["abilityPower"]
    min_dmg = [90, 140, 190]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage


def countBalls(game):
    ball=0
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    targetQ = GetBestTargetsInRange (game,800)
    before_cpos = game.get_cursor()
    for object in game.others:
        if  object.name =="syndrasphere" and object.is_alive and game.is_point_on_screen(game.player.pos):
                ball+=1
    return ball                        
                         
def getBuff(target, name):
    buff = None
    for cBuff in target.buffs:
        if cBuff and cBuff.name == name:
            buff = cBuff
    return buff

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
    global q, w, e, r
    lastQ=0
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")


    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
                
                targetQ = TargetSelector (game,800)
                if targetQ :
                            q_travel_time = (800/1750 ) + q_spell.delay
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 800 :
                                
                                if  game.player.mana >= 70 and lastQ + 1 < game.time:
    
                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    # q_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, q_spell, game.player, targetQ,0.4)))
                                    lastQ = game.time


    if use_w_in_combo and IsReady(game, w_spell) :
                targetQ = TargetSelector (game,925)
                
                if targetQ :
                            disToPlayer=game.player.pos.distance (targetQ.pos)

                            q_travel_time = (disToPlayer/1450) + w_spell.delay
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 925 :
                                
                                if  game.player.mana >= 70 :
    
                                    w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))



    if use_e_in_combo and IsReady(game, e_spell) :
                targetQ = TargetSelector (game,1500)
                for ball in game.others:
                    if targetQ:
                        if ball.name =="syndrasphere" and ball.is_alive and game.is_point_on_screen(game.player.pos):
                            if game.player.pos.distance (ball.pos) <= 700 and targetQ.pos.distance (ball.pos) <=400: 
                                e_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

                # if targetQ :
                #             q_travel_time = 700/902
                #             predicted_pos = predict_pos (targetQ, q_travel_time)
                #             predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                #             if game.player.pos.distance (predicted_target.pos) <= 700 :
                                
                #                 if  game.player.mana >= 70 and lastQ + 1 < game.time:
                                    
                #                     e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    
                                         

    if use_r_in_combo and IsReady(game, r_spell) :
                # print(CastTogetBalls(game))
                targetQ = TargetSelector (game,750)
                
                if targetQ :
                        tragetHp = int(targetQ.health / targetQ.max_health * 100)
                        if  game.player.mana >= 100 :
                                if BallDMG(game, targetQ)>=targetQ.health:
                                    r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                if countBalls(game)>=3 and tragetHp<50:
                                    r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                if countBalls(game)>=2 and tragetHp<40:
                                    r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))        
                                if countBalls(game)>=1 and tragetHp<30:
                                    r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))



def Laneclear(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global q, w, e, r
    global lane_clear_with_q,lane_clear_with_w 
    lastQ=0
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")


    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                
                targetQ = GetBestMinionsInRange(game,800)
                if targetQ :
                            q_travel_time = 800/1750
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 800 :
                                
                                if  game.player.mana >= 70 and lastQ + 1 < game.time:
    
                                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                                    time.sleep (0.01)
                                    q_spell.trigger (False)
                                    time.sleep (0.01)
                                    game.move_cursor (before_cpos)
                                    lastQ = game.time


    if lane_clear_with_w and IsReady(game, w_spell) :
                targetQ = GetBestMinionsInRange (game,925)
                if targetQ :
                            q_travel_time = 925/1450
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 925 :
                                
                                if  game.player.mana >= 70 and lastQ + 1 < game.time:
    
                                    game.move_cursor (game.world_to_screen (predicted_target.pos))
                                    time.sleep (0.01)
                                    w_spell.trigger (False)
                                    time.sleep (0.01)
                                    game.move_cursor (before_cpos)
                                    lastQ = game.time 
                                 
def AutoQ(game):
    global q, e, r,use_q_stack,autoQKey
    global lastE, lastQ, lastR                                
    q_spell = getSkill(game, "Q")
    lastQ=0
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
                
                targetQ = GetBestTargetsInRange (game,800)
                if targetQ :
                            q_travel_time = (800/1750 ) + q_spell.delay
                            predicted_pos = predict_pos (targetQ, q_travel_time)
                            predicted_target = Fake_target (targetQ.name, predicted_pos, targetQ.gameplay_radius)
                            if game.player.pos.distance (predicted_target.pos) <= 800 :
                                if  game.player.mana >= 70 and lastQ + 1 < game.time:

                                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                                    lastQ = game.time
def Harass(game):
    global use_q_in_harass, use_w_in_harass, use_e_in_harass, use_r_in_harass
    global q, w, e, r

    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

def DrawAutoQ(game):
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Enabled", Color.BLACK, Color.GREEN, 10.0)   

def DrawNotAutoQ(game):
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto Q: Disabled", Color.BLACK, Color.RED, 10.0)


# def CheckWallStun(game, target):

    
#     return None

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_w_in_combo, use_r_in_combo,autoQKey,use_q_stack
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg
    self = game.player
    e_spell = getSkill(game, 'E')
    # player = game.player
    # target=TargetSelector(game,2000)  

    # if target:
        
        
    #     for ball in game.others:
    #         if ball.name =="syndrasphere" and ball.is_alive and game.is_point_on_screen(game.player.pos):
    #             TargetPos = ball.pos
    #             # if game.player.pos.distance (ball.pos) <= 700:
    #             targ=game.world_to_screen(TargetPos)
    #             player = game.world_to_screen(game.player.pos)
    #             playerDirection = TargetPos.sub(game.player.pos)
    #             for i in range(10, 200):
    #                 ESpot = TargetPos.add(playerDirection.normalize().scale(40 * i))
    #                 E = game.world_to_screen(ESpot)
    #                 # realTarget= game.world_to_screen(target.pos)
    #                 # if E == target.pos:
    #                 #     realTarget= game.world_to_screen(target.pos)
    #                 game.draw_line(targ,E,5,Color.RED)
    #                 print("Ball: " + str(E.x) + "   " + "Target: " + str(target.pos.x) )
    #                 return ESpot
        
    

    # for ball in game.others:
    #     if ball.name =="syndrasphere" and ball.is_alive and game.is_point_on_screen(game.player.pos):
    #         ball=game.world_to_screen(ball.pos)
    #         player=game.world_to_screen(game.player.pos)
    #         # if game.player.pos.distance (ball.pos) <= 700:
                        

    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
        if use_q_stack:
            AutoQ(game)  
            DrawAutoQ(game)
        if not use_q_stack:
            DrawNotAutoQ(game)  
        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack        

