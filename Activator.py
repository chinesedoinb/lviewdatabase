from distutils.command.clean import clean
from commons.targit import TargetSelector
from winstealer import *
from evade import checkEvade
from commons.items import *
from commons.skills import *
from commons.utils import *
from commons.targeting import *
import time, json, random
from API.summoner import *
from commons.timer import Timer

smite_key = 0
draw_smite_range = False
is_smiteable = False
auto_smiting = False
smite_buffs = False
smite_krugs = False
smite_wolves = False
smite_raptors = False
smite_gromp = False
smite_scuttle = False
smite_drake = False
smite_baron = False
smite_herald = False

auto_ignite=True
auto_heal=True
auto_barrier=True
auto_potion=True
auto_cleans=True
auto_Qss=True
auto_zhonya=True
auto_GoreDrink=True
auto_Yuomus=True
auto_Prowler=True

postion_slider = 70

winstealer_script_info = {
    "script": "Activator",
    "author": "Nick",
    "description": "Activator"
}

potions = {
    "item2003",
    "itemcrystalflask",
    "itemdarkcrystalflask",
}

QSSs = {
    "itemmercurial",
    "quicksilversash",  
}

Glass={
    "zhonyashourglass",
    "item2420",
}

GoreDrink={
    "6029active",
    "6630active",
    "6631active",
}

def IsReady(game, skill):
    return skill and skill.get_current_cooldown(game.time) == 0.0 and skill.level > 0

def winstealer_load_cfg(cfg):
    global auto_GoreDrink,auto_Yuomus,auto_Prowler
    global auto_Qss, auto_zhonya,postion_slider
    global auto_cleans,smite_key,auto_potion,auto_potion,auto_ignite,auto_heal,auto_barrier, draw_smite_range, auto_smiting, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    smite_key = cfg.get_int("smite_key", 0)
    auto_smiting = cfg.get_bool("auto_smiting", True)
    draw_smite_range = cfg.get_bool("draw_smite_range", True)
    smite_buffs = cfg.get_bool("smite_buffs", True)
    smite_krugs = cfg.get_bool("smite_krugs", True)
    smite_wolves = cfg.get_bool("smite_wolves", True)
    smite_raptors = cfg.get_bool("smite_raptors", True)
    smite_gromp = cfg.get_bool("smite_gromp", True)
    smite_scuttle = cfg.get_bool("smite_scuttle", True)
    smite_drake = cfg.get_bool("smite_drake", True)
    smite_baron = cfg.get_bool("smite_baron", True)
    smite_herald = cfg.get_bool("smite_herald", True)

    auto_ignite=cfg.get_bool("auto_ignite",True)

    auto_potion=cfg.get_bool("auto_potion",True)
    postion_slider=cfg.get_int("postion_slider", postion_slider)
    auto_cleans=cfg.get_bool("auto_cleans",True)

    auto_heal=cfg.get_bool("auto_heal",True)

    auto_barrier=cfg.get_bool("auto_barrier",True)
    
    auto_Qss =cfg.get_bool("auto_Qss",True)

    auto_zhonya =cfg.get_bool("auto_zhonya",True)

    auto_GoreDrink =cfg.get_bool("auto_GoreDrink",True)

    auto_Yuomus=cfg.get_bool("auto_Yuomus",True)

    auto_Prowler=cfg.get_bool("auto_Prowler",True)


def winstealer_save_cfg(cfg):
    global auto_cleans,smite_key, auto_potion,draw_smite_range, auto_ignite,auto_heal,auto_barrier,auto_smiting, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    global auto_Qss, auto_zhonya,postion_slider
    global auto_GoreDrink,auto_Yuomus,auto_Prowler

    cfg.set_int("smite_key", smite_key)
    cfg.set_bool("auto_smiting", auto_smiting)
    cfg.set_bool("draw_smite_range", draw_smite_range)
    cfg.set_bool("smite_buffs", smite_buffs)
    cfg.set_bool("smite_krugs", smite_krugs)
    cfg.set_bool("smite_wolves", smite_wolves)
    cfg.set_bool("smite_raptors", smite_raptors)
    cfg.set_bool("smite_gromp", smite_gromp)
    cfg.set_bool("smite_scuttle", smite_scuttle)
    cfg.set_bool("smite_drake", smite_drake)
    cfg.set_bool("smite_baron", smite_baron)
    cfg.set_bool("smite_herald", smite_herald)

    #ignite
    cfg.set_bool("auto_ignite",auto_ignite)

    #heal
    cfg.set_bool("auto_heal",auto_heal)

    #barrier
    cfg.set_bool("auto_barrier",auto_barrier)

    #potion
    cfg.set_bool("auto_potion",auto_potion)
    cfg.set_float("postion_slider", postion_slider)

    #Cleans
    cfg.set_bool("auto_cleans",auto_cleans)

    #Qss
    cfg.set_bool("auto_Qss",auto_Qss)

    #Zhonyas
    cfg.set_bool("auto_zhonya",auto_zhonya)

    #GoreDrink
    cfg.set_bool("auto_GoreDrink",auto_GoreDrink)

    #Yummous
    cfg.set_bool("auto_Yuomus",auto_Yuomus)

    #Prowler
    cfg.set_bool("auto_Prowler",auto_Prowler)

def winstealer_draw_settings(game, ui):
    global auto_cleans,smite_key, draw_smite_range,auto_potion, auto_smiting,auto_ignite,auto_heal,auto_barrier, smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    global auto_Qss, auto_zhonya,postion_slider
    global auto_GoreDrink,auto_Yuomus,auto_Prowler

    smite = game.player.get_summoner_spell(SummonerSpellType.Smite)

    ui.text("Activator by Nick: 1.0.0.1")
    ui.text("Author: Nick")
    ui.separator ()
    if ui.treenode("Auto Smite"):
        smite_key = ui.keyselect("Auto Smite Toggle Key", smite_key)
        draw_smite_range = ui.checkbox("Draw Smite Range", draw_smite_range)
        smite_buffs = ui.checkbox("Smite Buffs", smite_buffs)
        smite_krugs = ui.checkbox("Smite Krugs", smite_krugs)
        smite_wolves = ui.checkbox("Smite Wolves", smite_wolves)
        smite_raptors = ui.checkbox("Smite Raptors", smite_raptors)
        smite_gromp = ui.checkbox("Smite Gromp", smite_gromp)
        smite_scuttle = ui.checkbox("Smite Scuttle", smite_scuttle)
        smite_drake = ui.checkbox("Smite Drake", smite_drake)
        smite_baron = ui.checkbox("Smite Baron", smite_baron)
        smite_herald = ui.checkbox("Smite Herald", smite_herald)
        ui.treepop()

    if ui.treenode("Auto Ignite"):
        auto_ignite=ui.checkbox("Auto Ignite",auto_ignite)
        ui.treepop()

    if ui.treenode("Auto Heal"):
        auto_heal=ui.checkbox("Auto Heal",auto_heal)
        ui.treepop()

    if ui.treenode("Auto barrier"):
        auto_barrier=ui.checkbox("Auto barrier",auto_barrier)
        ui.treepop()
    if ui.treenode("Auto Cleans"):
        auto_cleans=ui.checkbox("Auto Cleans",auto_cleans)
        ui.treepop()
    if ui.treenode("Items"):
        if ui.treenode("Auto Potion"):
            auto_potion=ui.checkbox("Auto Potion",auto_potion)
            postion_slider=ui.sliderint("Health % ",int(postion_slider) , 0, 100)
            ui.text("(Put this item on on item slot 1 , 2 or 3)")
            ui.treepop() 

        if ui.treenode("Auto QSS/ Mercurial"):
            auto_Qss=ui.checkbox("Auto QSS",auto_Qss)
            ui.text("(Put this item on item slot 1 , 2 or 3)")
            ui.treepop()

        if ui.treenode("Auto Zhonyas/Stop Watch"):
            auto_zhonya=ui.checkbox("Zhonyas/Stop Watch",auto_zhonya)
            ui.text("(Put this item on item slot 1 , 2 or 3)")
            ui.treepop()

        if ui.treenode("Auto Goredrinker/ IronSpike /StrideBreaker "):
            auto_GoreDrink=ui.checkbox("Activate",auto_GoreDrink)
            ui.text("(Put this item on item slot 1 , 2 or 3)")
            ui.treepop()  

        if ui.treenode("Auto Youmuu's Ghostblade "):
            auto_Yuomus=ui.checkbox("Activate",auto_Yuomus)
            ui.text("(Put this item on item slot 1 , 2 or 3)")
            ui.treepop()

        if ui.treenode("Auto Prowler's Claw "):
            auto_Prowler=ui.checkbox("Activate",auto_Prowler)
            ui.text("(Put this item on item slot 1 , 2 or 3)")
            ui.treepop()    

        ui.treepop() 
    ui.separator ()


def GetBestJungleInRange(game, atk_range):
    global smite_buffs, smite_krugs, smite_wolves, smite_raptors, smite_gromp, smite_scuttle, smite_drake, smite_baron, smite_herald
    atk_range = 565
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    target = None
    for jungle in game.jungle:
        if game.player.pos.distance(jungle.pos) < atk_range:
            if smite_buffs == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Buff):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_krugs == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Krug):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_wolves == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Wolf):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_raptors == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Raptor):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_gromp == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Gromp):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_scuttle == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Large) and jungle.has_tags(UnitTag.Unit_Monster_Crab):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_drake == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic) and jungle.has_tags(UnitTag.Unit_Monster_Dragon):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)
            if smite_baron or smite_herald == True:
                if jungle.has_tags(UnitTag.Unit_Monster_Epic):
                    if (
                        not jungle.isTargetable
                        or not jungle.is_visible
                        or not jungle.is_alive
                        or jungle.name=="sru_riftherald_mercenary"
                        ):
                            continue
                    target = jungle
                    if spell and IsReady(game, spell):
                        SmiteMonster(game, target)

def auto_ign(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    target = TargetSelector(game, 600)
    ignite = game.player.get_summoner_spell(SummonerSpellType.Ignite)
    if target :
        if not getBuff(target,"illaoiespirit"):
            if ignite and IsReady(game, ignite):
                if target.health - ignite.value <= 0:
                        ignite.move_and_trigger(game.world_to_screen(target.pos))
def auto_hil(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    player = game.player
    heal = game.player.get_summoner_spell(SummonerSpellType.Heal)
    if heal and IsReady(game, heal):
                hp = int(player.health / player.max_health * 100)
                if hp < 28 and player.is_alive and heal.get_current_cooldown(game.time) == 0.0:
                     heal.trigger(False)
def auto_barr(game):
    global smite_key, draw_smite_range, auto_smiting,auto_ignite,auto_heal,auto_barrier
    player = game.player
    barrier = game.player.get_summoner_spell(SummonerSpellType.Barrier)
    if barrier and IsReady(game, barrier):
                hp = int(player.health / player.max_health * 100)
                if hp < 20 and player.is_alive and barrier.get_current_cooldown(game.time) == 0.0:
                     barrier.trigger(False)  

def bffs(game, player):
    for buff in game.player.buffs:
        # print(buff.name)
        if 'nasusw' in buff.name.lower ():
            return True
        elif 'exhaust' in buff.name.lower ():
            return True
        elif 'ignite' in buff.name.lower ():
            return True
        elif 'slow' in buff.name.lower ():
            return True     
        elif 'silence' in buff.name.lower ():
            return True      
        elif 'deathmark' in buff.name.lower ():
            return True
        elif 'blind' in buff.name.lower ():
            return True
        elif 'deathsentence' in buff.name.lower ():  #Threash Q 
            return True    
        elif 'hemoplague' in buff.name.lower ():
            return True    
        elif 'fear' in buff.name.lower ():
            return True
        elif 'charm' in buff.name.lower ():
            return True
        elif 'snare' in buff.name.lower ():
            return True
        elif 'stun' in buff.name.lower ():
            return True
        elif 'suppress' in buff.name.lower ():
            return True
        elif 'root' in buff.name.lower ():
            return True
        elif 'taunt' in buff.name.lower ():
            return True
        elif 'sleep' in buff.name.lower ():
            return True
        elif 'knockup' in buff.name.lower ():
            return True
        elif 'binding' in buff.name.lower ():
            return True
        elif 'morganaq' in buff.name.lower ():
            return True
        elif 'jhinw' in buff.name.lower ():
            return True
    return False

def cleans(game):
    global auto_cleans
    player = game.player
    cleans = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
    if bffs(game, player):
            
        if cleans and IsReady(game, cleans):
                    hp = int(player.health / player.max_health * 100)
                    if player.is_alive and cleans.get_current_cooldown(game.time) == 0.0:

                            # print("yes")
                            cleans.trigger(False)  

def auto_pot(game):

    global potions,postion_slider
    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    hp = int(player.health / player.max_health * 100)
    if hp < postion_slider :   
        for item in items:
            if item.name in potions and item.level>0:
                if getBuff(player, "Item2003") or getBuff(player, "ItemCrystalFlask") or getBuff(player, "ItemDarkCrystalFlask"):
                    continue
                elif IsReady(game,item):
                    item.trigger(False)

                                     
def DrawSmiteRange(game):
    color = Color.ORANGE
    color.a = 0.1
    game.draw_circle_world_filled(game.player.pos, 565, 50, color)
    color = Color.WHITE
    color.a = 5.0
    game.draw_circle_world(game.player.pos, 565, 100, 3, color)

def DrawSmiting(game):
    color = Color.ORANGE
    color.a = 5.0
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos), "AutoSmite: Enabled", Color.ORANGE, Color.BLACK, 4.0)
def SmiteMonster(game, target):
    global is_smiteable, auto_smiting
    spell = game.player.get_summoner_spell(SummonerSpellType.Smite)
    if auto_smiting:
        if target.health - spell.value <= 0:
            game.draw_circle_world(target.pos, 200, 100, 1, Color.RED)
 
            smite=str(spell.slot.name)
            if smite == "F":
                 if game.player.F.timeCharge>0 :
                    spell.move_and_trigger(game.world_to_screen(target.pos))
            else:
                if game.player.D.timeCharge>0 :
                    spell.move_and_trigger(game.world_to_screen(target.pos))


def UseQss(game):
    global potions, QSSs
    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    
    cleans = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
    target=TargetSelector(game,900)

    if target:
        if bffs(game, player) and not IsReady(game,cleans):
                for item in items:
                    if item.name in QSSs and item.level>0 :
                        # print(item.slot)
                        if IsReady(game,item):
                            item.trigger(False)

def UseZhonyas(game):
    global Glass
    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    player=game.player
    hp = int(player.health / player.max_health * 100)
    cleans = game.player.get_summoner_spell(SummonerSpellType.Cleanse)
    target=TargetSelector(game,900)
    # zhonyashourglass
    # item2420
    if target  :
        for item in items:
            if item.name in Glass and item.level>0 :
                if IsReady(game,item):
                    if bffs(game, player) and not IsReady(game,cleans) and hp<50:
                        item.trigger(False)
                    if hp<=30 and player.pos.distance(target.pos) <= 400:
                        item.trigger(False)
                        
def autoYuomus(game):
    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")

    target=TargetSelector(game,game.player.atkRange + game.player.gameplay_radius + 400)
    if target:
        for item in items :
            if item.name =="youmusblade" and  item.level>0:
                if IsReady(game,item):
                    if (q_spell.isActive
                    or w_spell.isActive
                    or e_spell.isActive
                    or r_spell.isActive
                    ) :
                        item.trigger(False)

def autoGoreDrink(game):
    global GoreDrink

    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    target=TargetSelector(game,400 )
    if target:
        for item in items :
            if item.name in GoreDrink and  item.level>0:
                if IsReady(game,item):
                    item.trigger(False)
def autoProwler(game):

    items = [getSkill(game, "item1"),
    getSkill(game, "item2"),
    getSkill(game, "item3"),]
    player=game.player
    target=TargetSelector(game,400 )
    q_spell = getSkill(game, "Q")
    r_spell = getSkill(game, "R")
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    if target:
        for item in items :
            if item.name =="6693active" and item.level>0:
                if IsReady(game,item):
                    if (q_spell.isActive
                    or w_spell.isActive
                    or e_spell.isActive
                    or r_spell.isActive) :
                        item.move_and_trigger(game.world_to_screen(target.pos))

def winstealer_update(game, ui):
    global auto_cleans,smite_key, draw_smite_range, auto_smiting,auto_potion
    global auto_Qss, auto_zhonya
    global auto_GoreDrink,auto_Yuomus,auto_Prowler

    player=game.player
    # print(game.player.item1.name)
    if player.is_alive and player.is_visible and game.is_point_on_screen(player.pos):
        # items------------------------------
        # if auto_Prowler:
        #     autoProwler(game)
        # if auto_Yuomus:
        #     autoYuomus(game)
        # if auto_GoreDrink:
        #     autoGoreDrink(game)

        # if auto_zhonya:
        #     UseZhonyas(game)

        # if auto_Qss:
        #     UseQss(game)
        # if auto_potion:
        #     auto_pot(game)
        #/------------------------------

        if draw_smite_range:
            DrawSmiteRange(game)

        if auto_smiting:
            DrawSmiting(game)
            GetBestJungleInRange(game, 0)
            
        if game.was_key_pressed(smite_key):
            auto_smiting = not auto_smiting
        if auto_ignite:
            auto_ign(game)  
        if auto_heal:
            auto_hil(game) 
        if auto_barrier:
            auto_barr(game)
        
        if auto_cleans:
            cleans(game)