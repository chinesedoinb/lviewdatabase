from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from orb_walker import *
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Yone",
    "author": "SA1",
    "description": "SA1-Yone",
    "target_champ": "yone",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46
autoQKey=1

use_q_in_combo = True
use_e_in_combo = True
use_r_in_combo = True
use_w_in_combo=True


use_w_on_evade = True

use_q_stack=True
use_e_underTower=True

flee=50

steal_kill_with_q = False
steal_kill_with_e = False
steal_kill_with_r = False

lane_clear_with_q = False
lasthit_with_q = False
lane_clear_with_w=False

lane_clear_with_eq = False
lane_clear_with_e = False

draw_q_range = False
draw_e_range = False
draw_r_range = False

q = {"Range": 450}
w = {"Range": 2500.0}
e = {"Range": 475}
r = {"Range": 1800}


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,use_w_in_combo
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e,lane_clear_with_w
    global use_w_on_evade,use_q_stack,use_e_underTower,flee
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)
    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)
    #flee=cfg.get_int("killsteal_key", 48)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", False)
    use_r_in_combo = cfg.get_bool("use_r_in_combo", True)
    use_w_in_combo=cfg.get_bool("use_w_in_combo",True)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)

    steal_kill_with_q = cfg.get_bool("steal_kill_with_q", False)
    steal_kill_with_e = cfg.get_bool("steal_kill_with_e", False)
    steal_kill_with_r = cfg.get_bool("steal_kill_with_r", False)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lasthit_with_q = cfg.get_bool("lasthit_with_q", False)
    lane_clear_with_w=cfg.get_bool("lane_clear_with_w", True)


    lane_clear_with_eq = cfg.get_bool("lane_clear_with_eq", False)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)

    use_w_on_evade = cfg.get_bool("use_w_on_evade", False)
    
    use_e_underTower=cfg.get_bool("use_e_underTower", False)

def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,use_w_in_combo
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee,lane_clear_with_w

    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("killsteal_key", killsteal_key)
    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    # cfg.set_int("flee", flee)
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)
    cfg.set_bool("use_w_in_combo",use_w_in_combo)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("steal_kill_with_q", steal_kill_with_q)
    cfg.set_bool("steal_kill_with_e", steal_kill_with_e)
    cfg.set_bool("steal_kill_with_r", steal_kill_with_r)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w",lane_clear_with_w)

    cfg.set_bool("lasthit_with_q", lasthit_with_q)
    cfg.set_bool("lane_clear_with_eq", lane_clear_with_eq)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)

    cfg.set_bool("use_w_on_evade", use_w_on_evade)
    
    cfg.set_bool("use_e_underTower", use_e_underTower)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey,lane_clear_with_w
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee,use_w_in_combo,lane_clear_with_w

    ui.text("SA1-Yone : 1.0.0.2")
    ui.separator ()
    # ui.text("LifeSaver#3592")
    ui.text("E manual")
    ################################
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    autoQKey=ui.keyselect("Auto Q key",autoQKey)
    
    
    # flee=ui.keyselect("Flee",flee)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_q_stack=ui.checkbox("Auto Q",use_q_stack)
        
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        ui.treepop()

    if ui.treenode("Setting [W]"):
        use_w_in_combo=ui.checkbox("Use W in Combo",use_w_in_combo)
        
        ui.treepop()

    if ui.treenode("Setting [R]"):
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        
        ui.treepop()

    if ui.treenode("Laneclear"):

        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w=ui.checkbox("Laneclear with W",lane_clear_with_w)
        lasthit_with_q = ui.checkbox("Lasthit with Q", lasthit_with_q)

        ui.treepop()
    


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


# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ad = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [200,400,600]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ad)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage
    


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
    before_cpos = game.get_cursor ()
    e_spell = getSkill(game, "E")
    q_spell = getSkill(game, "Q")
    if humanizer.Timer():
        game.press_right_click()
        humanizer.SetTimer(50 / 1000)
    minion=GetBestMinionsInRange(game,400)
    if minion :
        
        if IsReady(game, e_spell):
            game.move_cursor (game.world_to_screen (minion.pos))
            time.sleep (0.01)
            e_spell.trigger (False)
            q_spell.trigger(False)
            time.sleep (0.01)
            game.move_cursor (before_cpos)
spellTimer = Timer()        
def Combo(game):
    global q, e, r
    global lastE, lastQ, lastR
    global use_q_in_combo,use_w_in_combo,use_e_in_combo,spellTimer
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    w_spell = getSkill(game, "W")

    before_cpos = game.get_cursor ()
    
    if use_q_in_combo :
        target = TargetSelector (game,450)
        if target :
               
            # for b in target.buffs:
            #     print(b.name)
                if IsReady(game, q_spell) and q_spell.name=="yoneq" and not w_spell.isActive:
                    q_travel_time = 450 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.4)

    if use_q_in_combo :
        target = TargetSelector (game,1050)  
        if target :
                
                if IsReady(game, q_spell) and q_spell.name=="yoneq3" and not w_spell.isActive:
                    q_travel_time = 1050 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 1050 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.6)
                            # game.move_cursor (game.world_to_screen (predicted_target.pos))
                            # time.sleep (0.01)
                            # q_spell.trigger (False)
                            
    
    if use_w_in_combo :
        target = TargetSelector (game,700)  
        if target :
                if IsReady(game, w_spell) :
                    q_travel_time = 700 / 1800
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700 and spellTimer.Timer():
                        w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.4)

    if use_r_in_combo:
        target=TargetSelector(game,1000)
        if target:
            if IsReady(game, r_spell) :
                q_travel_time=1000/1500
                predicted_pos=predict_pos(target, q_travel_time)
                predicted_target=Fake_target(target.name, predicted_pos, target.gameplay_radius)
                if game.player.pos.distance(predicted_target.pos)<=950:
                    if  getBuff(target, "yoneq3knockup") or RDamage(game, target)>=target.health:
                        if  spellTimer.Timer():
                            r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                            spellTimer.SetTimer(0.3)
                    
                    
    # if use_e_in_combo :
    #     target = GetBestTargetsInRange (game,900)
    #     if target :
    #            if not getBuff(target, "YoneE"):
    #                     e_spell.move_and_trigger (game.world_to_screen (target.pos))
                
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
    global q, e, r,use_q_stack,autoQKey,spellTimer
    global lastE, lastQ, lastR
    global use_q_in_combo,use_w_in_combo,use_e_in_combo
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor ()
    
    if use_q_in_combo:
        target = GetBestTargetsInRange (game,450)
        if target :
                if IsReady(game, q_spell) and q_spell.name=="yoneq" and not q_spell.name=="yoneq3":
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.4)

                            
    if use_q_in_combo:
        Minion =  GetBestMinionsInRange(game,475)
        target = TargetSelector (game,500)
        jungle= GetBestJungleInRange(game,475)
        if Minion and not target:
                if IsReady(game, q_spell) and q_spell.name=="yoneq":
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (Minion, q_travel_time)
                    predicted_target = Fake_target (Minion.name, predicted_pos, Minion.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.4)
               
        if jungle and not target:
            if IsReady(game, q_spell) and q_spell.name=="yoneq":
                    q_travel_time = 475 / 1500
                    predicted_pos = predict_pos (jungle, q_travel_time)
                    predicted_target = Fake_target (jungle.name, predicted_pos, jungle.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475 and spellTimer.Timer():
                        q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
                        spellTimer.SetTimer(0.4)
def Laneclear(game):
    global q, e, r
    global lastE, lastQ, lastR,lane_clear_with_q,lane_clear_with_w
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    w_spell = getSkill(game, "W")

    before_cpos = game.get_cursor ()
    
    if lane_clear_with_q :
        target = GetBestMinionsInRange (game,450)

        if target:

                if IsReady(game, q_spell):
                    q_travel_time = 450 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.02)
                            game.move_cursor (before_cpos)
    
    if lane_clear_with_w:
        target = GetBestMinionsInRange(game,700)  
        if target :
                if IsReady(game, w_spell) :
                    q_travel_time = 700 / 1800
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            w_spell.trigger (False)
                            time.sleep (0.02)
                            game.move_cursor (before_cpos)
def jungle(game):
    global q, e, r
    global lastE, lastQ, lastR,lane_clear_with_q,lane_clear_with_w
    q_spell = getSkill(game, "Q")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    w_spell = getSkill(game, "W")

    before_cpos = game.get_cursor ()
    
    if lane_clear_with_q :
        target = GetBestJungleInRange (game,450)

        if target:

                if IsReady(game, q_spell):
                    q_travel_time = 450 / 1500
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 475:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            q_spell.trigger (False)
                            time.sleep (0.02)
                            game.move_cursor (before_cpos)
    
    if lane_clear_with_w:
        target = GetBestJungleInRange(game,700)  
        if target :
                if IsReady(game, w_spell) :
                    q_travel_time = 700 / 1800
                    predicted_pos = predict_pos (target, q_travel_time)
                    predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                    if game.player.pos.distance (predicted_target.pos) <= 700:
                            game.move_cursor (game.world_to_screen (predicted_target.pos))
                            time.sleep (0.01)
                            w_spell.trigger (False)
                            time.sleep (0.02)
                            game.move_cursor (before_cpos)

def winstealer_update(game, ui):
    global use_q_in_combo, use_e_in_combo, use_r_in_combo,autoQKey
    global draw_q_range, draw_e_range, draw_r_range
    global combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_q, steal_kill_with_e, steal_kill_with_r
    global lane_clear_with_q, lasthit_with_q, lane_clear_with_eq, lane_clear_with_e
    global use_w_on_evade,use_q_stack,use_e_underTower,flee
    global spellTimer
    self = game.player

    if self.is_alive and game.is_point_on_screen(self.pos) :

        
        if game.is_key_down(combo_key) :
            Combo(game)
            
        if game.is_key_down(laneclear_key):
            Laneclear(game)
            jungle(game)
        # if game.is_key_down(harass_key):
        #     Harass(game)
        if use_q_stack:
            AutoQ(game)  
            DrawAutoQ(game)
        if not use_q_stack:
            DrawNotAutoQ(game)    
        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack    
                

        # if game.is_key_down(flee):
        #     fleeOrb(game)