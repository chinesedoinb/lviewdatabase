from dis import dis
from msilib.schema import tables
from re import T
import sys
from turtle import distance
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
    "script": "SA1-katarina",
    "author": "SA1",
    "description": "SA1-katarina",
    "target_champ": "katarina",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True
smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 1000}
w = {"Range": 600}
e = {"Range": 600}
r = {"Range": 3000}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)


    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
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

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)


    ui.text("SA1-katarina : 1.0.0.0")
    # ui.text("Author : LifeSaver#3592")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo=ui.checkbox("User R in Combo",use_r_in_combo)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        lane_clear_with_w = ui.checkbox("Laneclear with W ", lane_clear_with_w)
        ui.treepop()

    if ui.treenode("Jungle Clear Settings"):
        jungle_clear_with_q = ui.checkbox("Jungle with Q", jungle_clear_with_q)
        jungle_clear_with_w = ui.checkbox("Jungle with W", jungle_clear_with_w)
        jungle_clear_with_e = ui.checkbox("Jungle with E", jungle_clear_with_e)
        ui.treepop()




########################
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


def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

lastq=0
lastDagger=0
daggers = []
lastDaggerPos=None
def CheckDaggers(game):
    global daggers, lastDaggerPos, lastDagger
    
    for missile in game.missiles:
        if missile.name == "katarinawdaggerarc" or missile.name == "katarinaqdaggerarc" or missile.name == "katarinaqdaggerarc2":
            lastDaggerPos = missile.end_pos

            


def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo,lastq
    global q, w, e, r
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    before_cpos = game.get_cursor()
    if not getBuff(game.player,"katarinarsound"):
        if use_q_in_combo and IsReady(game, q_spell):
                    targetQ = TargetSelector (game,625)

                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 625:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

        if use_e_in_combo and IsReady(game, e_spell)  :
                    
                    targetE=TargetSelector (game,720)
                    if targetE:
                        for missile in game.missiles:
                            if missile.name == "katarinaqdaggerarc" or missile.name == "katarinaqdaggerarc2"or missile.name == "katarinawdaggerarc":
                                lastDaggerPos = missile.end_pos
                                if lastDaggerPos:
                                    e_spell.move_and_trigger(game.world_to_screen(lastDaggerPos))


                        

                                        
        if use_w_in_combo and IsReady(game, w_spell) :
                    targetQ = TargetSelector (game,1150)
                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 370:
                            w_spell.trigger(False)

                        
    if use_r_in_combo and IsReady(game, r_spell) : 
                targetR=TargetSelector(game,370)
                
                if targetR:
                         r_spell.trigger(False)   
                                        

def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global spell_priority, combo_key, laneclear_key, killsteal_key
    #q = {"Range": 600}
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if not getBuff(game.player,"katarinarsound"):
        if lane_clear_with_q and IsReady(game, q_spell):
                    targetQ = GetBestMinionsInRange (game,625)

                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 625:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

        if lane_clear_with_e and IsReady(game, e_spell)  :
                    
                    targetE=GetBestMinionsInRange (game,720)
                    if targetE:
                        for missile in game.missiles:
                            if missile.name == "katarinaqdaggerarc" or missile.name == "katarinaqdaggerarc2"or missile.name == "katarinawdaggerarc":
                                lastDaggerPos = missile.end_pos
                                if lastDaggerPos:
                                    e_spell.move_and_trigger(game.world_to_screen(lastDaggerPos))


                        

                                        
        if lane_clear_with_w and IsReady(game, w_spell) :
                    targetQ = GetBestMinionsInRange (game,1150)
                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 370:
                            w_spell.trigger(False)

    
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if not getBuff(game.player,"katarinarsound"):
        if lane_clear_with_q and IsReady(game, q_spell):
                    targetQ = GetBestJungleInRange (game,625)

                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 625:
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))

        if lane_clear_with_e and IsReady(game, e_spell)  :
                    
                    targetE=GetBestJungleInRange (game,720)
                    if targetE:
                        for missile in game.missiles:
                            if missile.name == "katarinaqdaggerarc" or missile.name == "katarinaqdaggerarc2"or missile.name == "katarinawdaggerarc":
                                lastDaggerPos = missile.end_pos
                                if lastDaggerPos:
                                    e_spell.move_and_trigger(game.world_to_screen(lastDaggerPos))


                        

                                        
        if lane_clear_with_w and IsReady(game, w_spell) :
                    targetQ = GetBestJungleInRange (game,1150)
                    if targetQ:
                        if game.player.pos.distance(targetQ.pos) <= 370:
                            w_spell.trigger(False)


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e
    global q, w, e, r

    e_spell = getSkill(game, "E")

    # for missile in game.missiles:
    #         if missile.name == "katarinawdaggerarc" or missile.name == "katarinaqdaggerarc" or missile.name == "katarinaqdaggerarc2":
    #              kataDags.append(missile)
    # for i in kataDags:
    #     game.draw_circle_world(i.end_pos, 100, 100, 10, Color.GREEN)

    #     #if i:
    #     #             e_spell.move_and_trigger(game.world_to_screen(i.pos))
    #     #             kataDags=[]

    #     if len(kataDags)>20:            
    #         kataDags=[]
    # targetQ = TargetSelector (game,625)
    # if targetQ:
    #    for i in game.others:
    #         if i.id>151 and i.id<290 and i.is_alive:
    #             game.draw_circle_world(i.pos, 100, 100, 10, Color.GREEN)
    #             game.draw_text(game.world_to_screen(i.pos), ("{}_{} ({})".format(i.name, i.id, hex(i.address))), Color.GREEN)
    #             if ui.treenode("{}_{} ({})".format(i.name, i.id, hex(i.address))):
    #                 ui.labeltext("address", hex(i.address))
    #                 ui.labeltext("net_id", hex(i.net_id))
    #                 ui.labeltext("name", i.name, Color.ORANGE)
    #                 ui.labeltext("pos", f"x={i.pos.x:.2f}, y={i.pos.y:.2f}, z={i.pos.z:.2f}")
    #                 ui.dragint("id", i.id)
    
    self = game.player
    
    if self.is_alive :
        if game.was_key_pressed(combo_key):
            Combo(game)
            
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            
