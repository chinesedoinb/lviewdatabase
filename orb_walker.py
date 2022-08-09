from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
from commons.timer import Timer
import time, json, random
from API.summoner import *

winstealer_script_info = {
    "script": "Target-Selector",
    "author": "SA1",
    "description": "Target-Selector!",
}

lasthit_key = 45
harass_key = 46
key_orbwalk = 47
laneclear_key = 47

randomize_movement = False

draw_killable_minion = False
draw_killable_minion_fade = False

ResetAA = False

click_speed = 120
kite_ping = 50
windUpTime = 200

# lasthit_key = 45
# harass_key = 46
# key_orbwalk = 57
# laneclear_key = 47

randomize_movement = False

draw_killable_minion = False
draw_killable_minion_fade = False


smoothOrb=False


championInt=1

lowArmor=False
lowHealth=False
lowMr=False
autoPriority=True
closeToCursor=False
closeToplayer=False

sliderChampion1=0
sliderChampion2=0
sliderChampion3=0
sliderChampion4=0
sliderChampion5=0

c_atk_time=0

target1=None
target2=None
target3=None
target4=None
target5=None
def winstealer_load_cfg(cfg):
    global key_orbwalk, lasthit_key, harass_key, laneclear_key
    global randomize_movement,championInt,smoothOrb
    global click_speed, kite_ping,windup,lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global draw_killable_minion, draw_killable_minion_fade
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5

    lasthit_key = cfg.get_int("lasthit_key", 46)
    harass_key = cfg.get_int("harass_key", 45)
    key_orbwalk = cfg.get_int("key_orbwalk", 57)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    draw_killable_minion = cfg.get_bool("draw_killable_minion", False)
    randomize_movement = cfg.get_bool("randomize_movement", False)
    draw_killable_minion_fade = cfg.get_bool("draw_killable_minion_fade", False)
    click_speed = cfg.get_int("click_speed", click_speed)
    kite_ping = cfg.get_int("kite_ping", 15)
    windup=cfg.get_float("windup",1.7)

    championInt=cfg.get_int("championInt", championInt)

    smoothOrb=cfg.get_bool("smoothOrb",smoothOrb)

    autoPriority=cfg.get_bool("autoPriority",True)
    lowArmor=cfg.get_bool("lowArmor",False)
    lowHealth=cfg.get_bool("lowHealth",False)
    lowMr=cfg.get_bool("lowMr",False)
    closeToCursor=cfg.get_bool("closeToCursor",False)
    closeToplayer=cfg.get_bool("closeToplayer",False)

    sliderChampion1 = cfg.get_int("sliderChampion1", sliderChampion1)
    sliderChampion2 = cfg.get_int("sliderChampion2", sliderChampion2)
    sliderChampion3 = cfg.get_int("sliderChampion3", sliderChampion3)
    sliderChampion4 = cfg.get_int("sliderChampion4", sliderChampion4)
    sliderChampion5 = cfg.get_int("sliderChampion5", sliderChampion5)



def winstealer_save_cfg(cfg):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement,windup,smoothOrb
    global click_speed, kite_ping,championInt
    global draw_killable_minion, draw_killable_minion_fade
    global lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5

    cfg.set_int("lasthit_key", lasthit_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)
    cfg.set_int("key_orbwalk", key_orbwalk)
    cfg.set_bool("draw_killable_minion", draw_killable_minion)
    cfg.set_bool("randomize_movement", randomize_movement)
    cfg.set_bool("draw_killable_minion_fade", draw_killable_minion_fade)
    cfg.set_float("click_speed", click_speed)
    cfg.set_float("kite_ping", kite_ping)
    cfg.set_float("windup",windup)

    cfg.set_float("championInt",championInt)

    cfg.set_bool("autoPriority", autoPriority)
    cfg.set_bool("lowArmor", lowArmor)
    cfg.set_bool("lowHealth", lowHealth)
    cfg.set_bool("lowMr", lowMr)
    cfg.set_bool("closeToCursor", closeToCursor)
    cfg.set_bool("closeToplayer", closeToplayer)
    cfg.set_bool("smoothOrb", smoothOrb)



    cfg.set_float("sliderChampion1", sliderChampion1)
    cfg.set_float("sliderChampion2", sliderChampion2)
    cfg.set_float("sliderChampion3", sliderChampion3)
    cfg.set_float("sliderChampion4", sliderChampion4)
    cfg.set_float("sliderChampion5", sliderChampion5)


def winstealer_draw_settings(game, ui):
    global key_orbwalk, harass_key, lasthit_key, laneclear_key
    global randomize_movement,windup,smoothOrb
    global click_speed, kite_ping,championInt
    global draw_killable_minion, draw_killable_minion_fade
    global lowArmor,lowHealth,lowMr,autoPriority,closeToCursor,closeToplayer
    global sliderChampion1,sliderChampion2,sliderChampion3,sliderChampion4,sliderChampion5
    global target1,target2,target3,target4,target5,maxScore
    priority=0
    ui.text("Author: jiingz")
    ui.text("----------------------------------------------------------")
    ui.text("Select only 1 target selector")
    ui.text("----------------------------------------------------------")
    
    # lasthit_key = ui.keyselect("Last hit key", lasthit_key)
    # harass_key = ui.keyselect("Harass key", harass_key)
    # laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
    # key_orbwalk = ui.keyselect("Flee key", key_orbwalk)

    autoPriority = ui.checkbox("Auto Priority", autoPriority)
    lowArmor = ui.checkbox("Target Lowest Armor", lowArmor)
    lowHealth = ui.checkbox("Target Lowest Health", lowHealth)
    lowMr = ui.checkbox("Target Lowest Magic resist", lowMr)
    closeToCursor=ui.checkbox("close To Cursor", closeToCursor)
    closeToplayer=ui.checkbox("close To Player", closeToplayer)

    # click_speed = ui.sliderint("click_speed",int(click_speed) , 120, 500)


def drawKillableMinions(game, fade_effect):
    minion = game.GetBestTarget(
        UnitTag.Unit_Minion_Lane, game.player.atkRange + game.player.gameplay_radius
    )
    if minion:
        if fade_effect:
            percentHealth = (minion.health / minion.max_health) * 100
            value = 255 - (minion.health * 2)
            game.draw_circle_world(
                minion.pos,
                minion.gameplay_radius * 2,
                100,
                1,
                Color(0.0, 1.0, 1.0 - value, 1.0),
            )
        if not fade_effect:
            game.draw_circle_world(
                minion.pos, minion.gameplay_radius * 2, 100, 2, Color.ORANGE
            )




def autoAtkMissile(game) :
    global atkMissile
    atkMissile = None
    for missile in game.missiles:
        src = game.get_obj_by_id(missile.src_id)
        if missile and game.player.name in missile.name and 'attack' in missile.name:
            atkMissile = missile
    return atkMissile
            

def is_should_wait(game, player, enemy):
    missile_speed = player.basic_missile_speed + 1

    damageCalc.damage_type = damageType
    damageCalc.base_damage = 0

    hit_dmg = (
        damageCalc.calculate_damage(game, player, enemy)
        + items.get_onhit_physical(player, enemy)
        + items.get_onhit_magical(player, enemy)
    )

    hp = enemy.health + enemy.armour + (enemy.health_regen)
    t_until_basic_hits = game.distance(player, enemy) / missile_speed

    for missile in game.missiles:
        if missile.dest_id == enemy.id:
            src = game.get_obj_by_id(missile.src_id)
            if src:
                t_until_missile_hits = game.distance(missile, enemy) / (
                    missile.speed + 1
                )

                if t_until_missile_hits < t_until_basic_hits:
                    hp -= src.base_atk

    return hp - hit_dmg*1.5 <= 0

def ShouldWait(game, atk_range=0):
    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius + 25
    for minion in game.minions:
        if (
            not minion.is_alive
            or not minion.is_visible
            or not minion.isTargetable
            or minion.is_ally_to(game.player)
            or game.player.pos.distance(minion.pos) >= atk_range
        ):
            continue
        if is_should_wait(game, game.player, minion):
            target = minion
    return target

def can_attack(game) -> bool:
    global atk_speed
    #return int(game.time*1000) > last + (int(1000 / atk_speed) + kite_ping / 2)
    return HasResetSpells(game) or int(game.time*1000) + kite_ping / 2 + 25 >= last + int(1 / atk_speed) * 1000


def can_move(game, extra_windup = 0) -> bool:
    global atk_speed
    if autoAtkMissile(game):
        return True
    return int(game.time*1000) + kite_ping / 2 >= last + (1 /  atk_speed) * 1000 + extra_windup

def HasResetSpells(game)-> bool:
    if getBuff(game.player, "vaynetumblebonus"):
        last = int(game.time*1000) - kite_ping / 2
        return True
    return False

def ResetAutoAttack():
    global ResetAA

    return ResetAA

def OrbWalk(game, player, target):
    if target:
        if attackTimer.Timer() and can_attack(game):
            game.click_at(False, game.world_to_screen(target.pos))
            attackTimer.SetTimer(c_atk_time)
                    #moveTimer.SetTimer(b_windup_time)
            last = int(game.time*1000) - kite_ping / 2
        else:
            if humanizer.Timer():
                if autoAtkMissile(game):
                    game.press_right_click()
                    last = 0
                else:
                    if  can_move(game, windUpTime):
                        game.press_right_click()
                        last = 0
                humanizer.SetTimer(click_speed / 1000)
    else:
        if humanizer.Timer():
            game.press_right_click()
            last = int(game.time*1000) - kite_ping / 2
            humanizer.SetTimer(click_speed / 1000)

atk_range = 0
def winstealer_update(game, ui):
    global key_orbwalk, lasthit_key, laneclear_key
    global randomize_movement
    global click_speed, kite_ping
    global draw_killable_minion, draw_killable_minion_fade
    global attackTimer, moveTimer, humanizer
    global last, LastAttackCommandT
    global atk_range , atk_speed

    # atk_speed = GetAttackSpeed()

    # if draw_killable_minion_fade:
    #     drawKillableMinions(game, True)
    # elif draw_killable_minion:
    #     drawKillableMinions(game, False)

    # self = game.player

    # if (
    #     self.is_alive
    #     and game.is_point_on_screen(self.pos)
    #     and game.is_point_on_screen(game.get_cursor())
        
    #     #and not game.isChatOpen
    #     # and not checkEvade()
    # ):
    #     # if last + 0.2 < game.time:
    #     #     last = game.time
    #     #atk_speed = GetAttackSpeed()
    #     c_atk_time = max(1.0 / atk_speed, kite_ping / 1000)
    #     b_windup_time = (1.0 / atk_speed) * game.player.basic_atk_windup
        
    #     # for missile in game.missiles:
    #     #     src = game.get_obj_by_id(missile.src_id)
    #     #     if missile and game.player.name in missile.name and 'attack' in missile.name:
    #     #         print(missile.name)
    #     #         game.draw_circle_world(missile.pos,100, 100, 2, Color.GREEN)
    #     # if game.is_key_down(key_orbwalk) and not game.is_key_down(lasthit_key) and not game.is_key_down(laneclear_key):

    #     #     #for cBuff in game.player.buffs:
    #     #     #        if cBuff:
            
    #     #     target = game.GetBestTarget(
    #     #             UnitTag.Unit_Champion,
    #     #             game.player.atkRange + game.player.gameplay_radius,
    #     #         )
    #     #     #if (int(game.time*1000) - LastAttackCommandT > 100 + min(60, kite_ping)):
    #     #     if target:
    #     #         if attackTimer.Timer() and can_attack(game):
    #     #             game.click_at(False, game.world_to_screen(target.pos))
    #     #             attackTimer.SetTimer(c_atk_time)
    #     #             moveTimer.SetTimer(b_windup_time)
    #     #             last = int(game.time*1000) - kite_ping / 2
    #     #         else:
    #     #             if humanizer.Timer():
    #     #                 if can_move(game, windUpTime):
    #     #                     #game.click_at(False, game.get_cursor())
    #     #                     game.press_right_click()
    #     #                     last = 0
    #     #                 else:
    #     #                     if  moveTimer.Timer():
    #     #                         game.press_right_click()
    #     #                         last = 0
    #     #                 humanizer.SetTimer(click_speed / 1000)
    #     #     else:
    #     #         if humanizer.Timer():
    #     #             game.press_right_click()
    #     #             humanizer.SetTimer(click_speed / 1000)

    #     ShouldWaitTarget = ShouldWait(game)
    #     LastHittarget = LastHitMinions(game)
    #     if game.is_key_down(key_orbwalk):

    #             if humanizer.Timer():
    #                 game.press_right_click()
    #                 humanizer.SetTimer(click_speed / 1000)

    #     if game.is_key_down(lasthit_key):

    #         if ShouldWaitTarget:
    #             if  LastHittarget and attackTimer.Timer() and can_attack(game):
    #                     game.click_at(False, game.world_to_screen(LastHittarget.pos))
    #                     attackTimer.SetTimer(c_atk_time)
    #                     moveTimer.SetTimer(b_windup_time)
    #                     last = int(game.time*1000) - kite_ping / 2
    #             else:
    #                 if humanizer.Timer():
    #                     if can_move(game, windUpTime):
    #                         game.press_right_click()
    #                         last = 0
    #                     else:
    #                         if  moveTimer.Timer():# and can_move(game, windUpTime):
    #                             game.press_right_click()
    #                             last = 0
    #                     humanizer.SetTimer(click_speed / 1000)
    #         else:
    #             if humanizer.Timer():
    #                 game.press_right_click()
    #                 humanizer.SetTimer(click_speed / 1000)

        # if game.is_key_down(laneclear_key):

        #     target = (
        #         game.GetBestTarget(
        #             UnitTag.Unit_Minion_Lane,
        #             game.player.atkRange + game.player.gameplay_radius,
        #         )
        #         or game.GetBestTarget(
        #             UnitTag.Unit_Structure_Turret,
        #             game.player.atkRange + game.player.gameplay_radius,
        #         )
        #         or game.GetBestTarget(
        #             UnitTag.Unit_Structure_Inhibitor,
        #             game.player.atkRange + game.player.gameplay_radius,
        #         )
        #         or game.GetBestTarget(
        #             UnitTag.Unit_Structure_Nexus,
        #             game.player.atkRange + game.player.gameplay_radius,
        #         )
        #         or game.GetBestTarget(
        #             UnitTag.Unit_Monster,
        #             game.player.atkRange + game.player.gameplay_radius,
        #         )
        #     )

            #if ShouldWaitTarget:
            #    if  LastHittarget and attackTimer.Timer() and can_attack(game):
            #            game.click_at(False, game.world_to_screen(target.pos))
            #            attackTimer.SetTimer(c_atk_time)
            #            last = int(game.time*1000) - kite_ping / 2
            #    else:
            #        if humanizer.Timer():
            #            if autoAtkMissile(game):
            #                game.click_at(False, game.get_cursor())
            #                last = 0
            #            else:
            #                if  can_move(game, windUpTime):
            #                   game.click_at(False, game.get_cursor())
            #                   last = 0
            #            humanizer.SetTimer(click_speed / 1000)
            #else:
            #    if humanizer.Timer():
            #       game.click_at(False, game.get_cursor())
            #        humanizer.SetTimer(click_speed / 1000)

            # if target:
            #     if game.player.pos.distance(target.pos) <= game.player.atkRange + game.player.gameplay_radius + 25:
            #         if  attackTimer.Timer() and can_attack(game):
            #             game.click_at(False, game.world_to_screen(target.pos))
            #             attackTimer.SetTimer(c_atk_time)
            #             moveTimer.SetTimer(b_windup_time)
            #             last = int(game.time*1000)
            #         else:
            #             if humanizer.Timer():
            #                 if can_move(game, windUpTime):
            #                     game.press_right_click()
            #                     last = 0
            #                 else:
            #                     if  moveTimer.Timer():# and can_move(game, windUpTime):
            #                         game.press_right_click()
            #                         last = 0
            #                 humanizer.SetTimer(click_speed / 1000)
            # else:
            #     if humanizer.Timer():
            #         game.press_right_click()
            #         humanizer.SetTimer(click_speed / 1000)     
