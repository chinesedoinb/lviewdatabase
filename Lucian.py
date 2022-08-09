from ctypes import cast
from winstealer import *
import orb_walker
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
from orb_walker import *
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": "SA1 Lucian",
    "author": "SA1",
    "description": "SA1 Lucian",
    "target_champ": "lucian",
}

combo_key = 57
LaneClear_key = 35

use_q_in_lasthit = False

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True


use_q_in_lane=True
use_e_in_lane=True
use_w_in_lane=True


draw_q_range = False
draw_w_range = False
draw_e_range = False

evade_pos = 0
lastQ =0
lastE=0
Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 1180}
R = {"Slot": "R", "Range": 2500}

mana_q = [50,60,70,80,90]
mana_e=[40,30,20,10,0]

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key

    combo_key = cfg.get_int ("combo_key", 57)


    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)

    LaneClear_key = cfg.get_int ("LaneClear_key", 46)

    use_q_in_lane = cfg.get_bool ("use_q_in_laneClear", True)
    use_w_in_lane = cfg.get_bool ("use_w_in_laneClear", True)
    use_e_in_lane = cfg.get_bool ("use_e_in_laneClear", True)






def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit
    global use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key

    cfg.set_int ("combo_key", combo_key)


    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)
    cfg.set_bool ("use_r_in_combo", use_r_in_combo)

    cfg.set_int ("LaneClear_key", LaneClear_key)
    cfg.set_bool ("use_q_in_laneClear", use_q_in_lane)
    cfg.set_bool ("use_w_in_laneClear", use_w_in_lane)
    cfg.set_bool ("use_e_in_laneClear", use_e_in_lane)


def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key



    ui.text("Lucian:1.0.0.0")
    ui.separator ()
    ui.text ("Combo mode : Q.W.E (R Manual)")

    ui.separator()

    combo_key = ui.keyselect ("Combo Key", combo_key)


    if ui.treenode ("Setting [Q]"):
        use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
        ui.treepop ()
    if ui.treenode ("Setting [W]"):
        use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
        ui.treepop ()
    if ui.treenode ("Setting [E]"):
        use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
        ui.treepop ()
    if ui.treenode ("Setting [R]"):
        use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo)
        ui.treepop ()


    ui.separator ()
    #Lane Clear
    LaneClear_key = ui.keyselect ("Lane Clear", LaneClear_key)
    if ui.treenode ("Setting [Q]"):
        use_q_in_lane = ui.checkbox ("Use Q in Lane Clear", use_q_in_lane)
        ui.treepop ()
    if ui.treenode ("Setting [W]"):
        use_w_in_lane = ui.checkbox ("Use W in Lane Clear", use_w_in_lane)
        ui.treepop ()
    if ui.treenode ("Setting [E]"):
        use_e_in_lane = ui.checkbox ("Use E in Lane Clear", use_e_in_lane)
        ui.treepop ()

Qing =True
spellTimer = Timer()
def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit, use_q_in_lane, use_w_in_lane, use_e_in_lane,lastQ,lastE
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global spellTimer
    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    


    if use_q_in_combo and  game.player.mana>=mana_q[game.player.Q.level -1]:
        if IsReady(game,q_spell)  :
            target = TargetSelector (game,game.player.atkRange + game.player.gameplay_radius+50)
            if not q_spell.isActive and not w_spell.isActive and not e_spell.isActive:

                if target :
                    if not getBuff(game.player,"LucianPassiveBuff") :
                        if  spellTimer.Timer():
                            q_spell.move_and_trigger(game.world_to_screen(target.pos))
                            spellTimer.SetTimer(0.4)
                        

    if use_w_in_combo and IsReady(game,w_spell) and game.player.mana>=60:
        target = TargetSelector (game,900)
        if target :
            if not q_spell.isActive and not w_spell.isActive and not e_spell.isActive:
                if not getBuff(game.player,"LucianPassiveBuff"):
                    if  spellTimer.Timer():
                        w_spell.move_and_trigger(game.world_to_screen(target.pos))
                        spellTimer.SetTimer(0.2)
    if use_e_in_combo and IsReady(game,e_spell) and game.player.mana>=mana_e[game.player.E.level -1]:
        target = TargetSelector (game,700)
        if target :
                if  not IsReady(game,w_spell) or IsReady(game,q_spell):
                    if not getBuff(game.player,"LucianPassiveBuff"):
                            e_spell.trigger (False)
 

def LaneClear(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane,lastQ
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")
 # --------------Lane Clear-----------------
    if use_q_in_lane and IsReady(game,q_spell):
        target = GetBestMinionsInRange (game,500)
        if target and lastQ + 1 < game.time and  game.player.mana>=mana_q[game.player.Q.level -1]:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
            lastQ = game.time
    if use_w_in_lane and IsReady(game,w_spell) and game.player.mana>=60:
        target = GetBestMinionsInRange (game,900)
        if target and lastQ + 1 < game.time:
            if not getBuff(game.player,"LucianPassiveBuff"):
                w_spell.move_and_trigger(game.world_to_screen(target.pos))
                lastQ = game.time
    if use_e_in_lane and IsReady(game,e_spell) and game.player.mana>=mana_e[game.player.E.level -1]:
        target = GetBestMinionsInRange (game,700)
        if target and lastQ + 1 < game.time:
            if not getBuff(game.player,"LucianPassiveBuff"):
                e_spell.trigger (False)
                lastQ = game.time 

#--------------jungle Clear-----------------
    if use_q_in_lane and IsReady(game,q_spell):
        target = GetBestJungleInRange (game,500)
        if target and lastQ + 1 < game.time and  game.player.mana>=mana_q[game.player.Q.level -1]:
            q_spell.move_and_trigger(game.world_to_screen(target.pos))
            lastQ = game.time
    if use_w_in_lane and IsReady(game,w_spell) and game.player.mana>=60:
        target = GetBestJungleInRange (game,900)
        if target and lastQ + 1 < game.time:
            if not getBuff(game.player,"LucianPassiveBuff"):
                w_spell.move_and_trigger(game.world_to_screen(target.pos))
                lastQ = game.time
    if use_e_in_lane and IsReady(game,e_spell) and game.player.mana>=mana_e[game.player.E.level -1]:
        target = GetBestJungleInRange (game,700)
        if target and lastQ + 1 < game.time:
            if not getBuff(game.player,"LucianPassiveBuff"):
                e_spell.trigger (False)
                lastQ = game.time 


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, LaneClear_key, lasthit_key
    global Q, W, E, R
    # for b in game.player.buffs:


    # for b in game.player.buffs:
    #     print(b.name)
    # cursor_pos_vec2 = game.player.navBegin
    # cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, cursor_pos_vec2.z)
    # print(cursor_pos_vec3)
    # q_spell.move_and_trigger (cursor_pos_vec3)
    # target=TargetSelector(game,2000)
    # if target:
    #     print(game.world_to_screen(target.getNavEnd).x)
    #     # game.draw_line(game.world_to_screen(game.player.pos),game.world_to_screen(target.getNavEnd),10,Color.RED)
    if game.player.is_alive and game.is_point_on_screen(game.player.pos) :
        if game.is_key_down(LaneClear_key):
            LaneClear(game)
        if game.is_key_down(combo_key):
            Combo(game)