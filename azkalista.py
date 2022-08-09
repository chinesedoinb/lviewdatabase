from commons.targit import TargetSelector
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
import json, time, math

winstealer_script_info = {
    "script": "SA1+ Kalista",
    "author": "SA1",
    "description": "SA1+ Kalista",
    "target_champ": "kalista",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46

use_q_in_combo = True
use_e_in_combo = True

lane_clear_with_e = False
lasthit_with_q = False
lasthit_with_e = False
auto_e = False

steal_kill_with_e = False
save_with_r = False

toggled = False

draw_q_range = False
draw_w_range = False
draw_e_range = False
draw_r_range = False
allytarget = 0
draw_e_dmg = False

q = {"Range": 1200}
w = {"Range": 5000}
e = {"Range": 1100}
r = {"Range": 1200}

debug_dmg = 0

EffJungleHP = 0
eStackTotal = 0
spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}
myAD = 0
buff_name = ""
debug_hp = 0
r_value = 0


def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_e_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e
    global auto_e
    global lane_clear_with_e
    global draw_e_dmg, save_with_r, r_value
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)

    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_e_dmg = cfg.get_bool("draw_e_dmg", False)
    draw_r_range = cfg.get_bool("draw_r_range", False)
    save_with_r = cfg.get_bool("draw_r_range", False)
    r_value = cfg.get_float("r_value", 0)

    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", False)
    auto_e = cfg.get_bool("auto_e", True)

    spell_priority = json.loads(
        cfg.get_str("spell_priority", json.dumps(spell_priority))
    )


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_e_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e, steal_kill_with_q
    global lane_clear_with_e
    global auto_e
    global draw_e_dmg, r_value, save_with_r
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)

    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_e_dmg", draw_e_dmg)
    cfg.set_bool("draw_r_range", draw_r_range)
    cfg.set_bool("save_with_r", save_with_r)
    cfg.set_float("r_value", r_value)

    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.get_bool("auto_e", auto_e)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_e_in_combo
    global draw_w_range, draw_e_range, draw_r_range, draw_q_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global steal_kill_with_e, steal_kill_with_q
    global lane_clear_with_e
    global auto_e
    global draw_e_dmg, allytarget
    global EffJungleHP, save_with_r, r_value

##    ui.text(str(debug_hp))
##    ui.text(str(debug_dmg))
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    if ui.treenode("Setting [Q]"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        
        ui.treepop()


    if ui.treenode("Setting [E]"):
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        draw_e_dmg = ui.checkbox("Draw When is Killeable By E DMG", draw_e_dmg)
        lane_clear_with_e = ui.checkbox("Kill minions with E", lane_clear_with_e)
        ui.treepop()

    if ui.treenode("Setting [R]"):
        save_with_r = ui.checkbox("Use R to save ally", save_with_r)
        r_value = ui.sliderfloat("Ally HP Threshold", r_value, 0, 100.0)
        ui.treepop()
        
        
    if ui.treenode("Auto Expunge"):
        auto_e = ui.checkbox("Auto E everything", auto_e)
        ui.treepop()


#AD Damage Dealer
def effHP(game, target):
    global unitArmour, unitHP, EffJungleHP

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour
    unitHP = target.health
    
    return (
        (((1+(unitArmour / 100))*unitHP))
        )

def jungeffHP(game, jungle):
    global unitArmour, unitHP, EffJungleHP

    #jungle = GetBestJungleInRange(game, 1200)
    unitArmour = jungle.armour
    unitHP = jungle.health
    if jungle.name == "sru_dragon_air" or jungle.name == "sru_dragon_earth" or jungle.name == "sru_dragon_fire" or jungle.name == "sru_dragon_water" or jungle.name == "sru_dragon_elder" or jungle.name == "sru_riftherald":
        unitHP = ((unitHP)*2)
    if jungle.name == "sru_baron":
        unitHP = ((unitHP)*4)
    EffJungleHP = (((1+(unitArmour / 100))*(unitHP)))
    return (
        (((1+(unitArmour / 100))*(unitHP)))
        )

#AP Damage Dealer
#def effHP(game, target):
#    global unitArmour, unitHP

#   target = GetBestTargetsInRange(game, e["Range"])
#    unitMR = target.magicResist
#    unitHP = target.health 
#    return (
#        (((1+(unitMR / 100))*unitHP))
#        )

eLvLDamage = [20, 30, 40, 50, 60]
eStackDamage = [5.0, 9.0, 14.0, 20.0, 27.0]
eStackDamageMulti = [0.20, 0.2375, 0.275, 0.3125, 0.35]

def minionEdmg(game, minion):
    global eLvLDamage, eStackDamageMulti, eStackDamage
    ecount = 0
    if getBuff(minion, "kalistaexpungemarker"):
        ecount = getBuff(minion, "kalistaexpungemarker").countAlt -1
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((eStackDamage[game.player.E.level - 1] + ((total_atk) *eStackDamageMulti[game.player.E.level - 1])) * ecount)
    return (
        damage_melee
        )

def jungEdmg(game, jungle):
    global eLvLDamage, eStackDamageMulti, eStackDamage, eStackTotal
    ecount = 0
    if getBuff(jungle, "kalistaexpungemarker"):
        ecount = getBuff(jungle, "kalistaexpungemarker").countAlt -1
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((eStackDamage[game.player.E.level - 1] + ((total_atk) *eStackDamageMulti[game.player.E.level - 1])) * ecount)
    eStackTotal = damage_melee
    return (
        damage_melee
        )
        
def EDamage(game, target):
    global eLvLDamage, eStackDamageMulti, eStackDamage, eStackTotal, myAD
    ecount = 0
    if getBuff(target, "kalistaexpungemarker"):
        ecount = getBuff(target, "kalistaexpungemarker").countAlt -1
    #unitArmour = target.armour
    #unitHP = target.maxHealth
    #effHP = ((1+(unitArmour / 100))*unitHP)
    total_atk = game.player.base_atk + game.player.bonus_atk
    damage_melee = (eLvLDamage[game.player.E.level - 1] + (total_atk * 0.6))
    damage_melee += ((eStackDamage[game.player.E.level - 1] + ((total_atk) *eStackDamageMulti[game.player.E.level - 1])) * ecount)
    eStackTotal = damage_melee
    myAD = get_onhit_physical(game.player, target)
    return (
        damage_melee
        )


def DrawEDMG(game, player):
    color = Color.BLUE
    player = game.player
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_enemy_to(player)
            and game.is_point_on_screen(champ.pos)
        ):
            target = TargetSelector(game, e["Range"])
            if target:
                if EDamage(game, target) >= effHP(game, target):
                    p = game.hp_bar_pos(target)
                    #color.a = 5.0
                    game.draw_rect(
                        Vec4(p.x - 47, p.y - 27, p.x + 61, p.y - 12), color, 0, 5
                    )


lastQ = 0
mana_q = [50, 55, 60, 65, 70]

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
    global use_q_in_combo, use_e_in_combo
    global draw_e_range, draw_w_range, draw_r_range, draw_q_range
    global combo_key, harass_key, laneclear_key
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, mana_q
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    if use_q_in_combo and IsReady(game, q_spell) and game.player.mana > mana_q[game.player.Q.level -1]:
        target = TargetSelector(game, q["Range"])
        if target and IsReady(game, q_spell):
                q_travel_time = 900/1300
                predicted_pos = predict_pos (target, q_travel_time)
                predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
                if not IsCollisioned(game, predicted_target):
                    q_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
##    #if use_e_in_combo and IsReady(game, e_spell) and game.player.mana > 30:
##        target = GetBestTargetsInRange(game, 1100)
##        #if target and getBuff(target, "kalistaexpungemarker"):
##            #if EDamage(game, target) >= effHP(game, target):
##                #e_spell.trigger(False)
            

def Laneclear(game):
    global lane_clear_with_e
    
    e_spell = getSkill(game, "E")
    
    if lane_clear_with_e:    
        if IsReady(game, e_spell):
            minion = GetBestMinionsInRange(game, 1200)
            if minion:
            #for jungle in game.jungle:
                    if getBuff(minion, "kalistaexpungemarker"):
                        if EDamage(game, minion) >= effHP(game, minion):
                            e_spell.trigger(False)
def AutoE(game):
    global buff_name
    e_spell = getSkill(game, "E")
    if auto_e and IsReady(game, e_spell):
        minion = GetBestMinionsInRange(game, 1200)
        target = TargetSelector(game, 3000)
        jungle = GetBestJungleInRange(game, 1200)
        if target:
            for champ in game.champs:
                target = champ
                if getBuff(target, "kalistaexpungemarker"):
                    if EDamage(game, target) >= effHP(game, target):
                        if game.player.mana>= 30:
                            e_spell.trigger(False)
        if jungle:
            for jungle in game.jungle:
                    if getBuff(jungle, "kalistaexpungemarker"):
                        if jungEdmg(game, jungle) >= jungeffHP(game, jungle):
                            if game.player.mana>= 30:
                                e_spell.trigger(False)
        if minion:
            #for jungle in game.jungle:
                    if getBuff(minion, "kalistaexpungemarker"):
                        if EDamage(game, minion) >= effHP(game, minion):
                            if game.player.mana>= 30:
                                e_spell.trigger(False)

def Rsave(game):
    global r_value, save_with_r, boundAlly, debug_dmg, debug_hp, allytarget

    percentage = (r_value * 0.01)
    r_spell = getSkill(game, "R")
    if save_with_r:
        for champ in game.champs:
            if getBuff(champ, "kalistacoopstrikeally"):
                allytarget = champ
                if allytarget.health < (percentage * allytarget.max_health):
                    if IsReady(game, r_spell):
                        r_spell.trigger(False)

def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global q, w, e, r
    global combo_key, laneclear_key, harass_key
    global draw_e_dmg
    self = game.player

    player = game.player
    
    if draw_e_dmg:
        DrawEDMG(game, player)


    if self.is_alive:
        if save_with_r:
            Rsave(game)
        if auto_e:
            AutoE(game)
        if game.was_key_pressed(combo_key):
            Combo(game)
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
