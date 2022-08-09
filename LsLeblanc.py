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
    "script": "SA1-leblanc",
    "author": "SA1",
    "description": "SA1-leblanc",
    "target_champ": "leblanc",
}

combo_key = 57
harass_key = 46
LaneClear_key = 36

use_q_in_lasthit = False

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = True

use_q_in_lane=True
use_e_in_lane=True
use_w_in_lane=True


Flag_used=False

draw_q_range = False
draw_w_range = False
draw_e_range = False
smart_combo=1
evade_pos = 0
lastQ =0
Q = {"Slot": "Q", "Range": 750}
W = {"Slot": "W", "Range": 1180}
E = {"Slot": "E", "Range": 1180}
R = {"Slot": "R", "Range": 2500}

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,smart_combo,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,LaneClear_key

    combo_key = cfg.get_int ("combo_key", 57)
    use_q_in_combo = cfg.get_bool ("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool ("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool ("use_e_in_combo", True)
    use_r_in_combo = cfg.get_bool ("use_r_in_combo", True)

    LaneClear_key = cfg.get_int ("LaneClear_key", 36)
    use_q_in_lane = cfg.get_bool ("use_q_in_laneClear", True)
    use_w_in_lane = cfg.get_bool ("use_w_in_laneClear", True)
    use_e_in_lane = cfg.get_bool ("use_e_in_laneClear", True)

    smart_combo=cfg.get_int("smart_combo",smart_combo)



def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,smart_combo
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key,LaneClear_key

    cfg.set_int ("combo_key", combo_key)


    cfg.set_bool ("use_q_in_combo", use_q_in_combo)
    cfg.set_bool ("use_w_in_combo", use_w_in_combo)
    cfg.set_bool ("use_e_in_combo", use_e_in_combo)
    cfg.set_bool ("use_r_in_combo", use_r_in_combo)

    cfg.set_int ("LaneClear_key", LaneClear_key)
    cfg.set_bool ("use_q_in_laneClear", use_q_in_lane)
    cfg.set_bool ("use_w_in_laneClear", use_w_in_lane)
    cfg.set_bool ("use_e_in_laneClear", use_e_in_lane)

    cfg.set_int("smart_combo",smart_combo)



def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo, use_q_in_lasthit,smart_combo,use_q_in_lane,use_w_in_lane,use_e_in_lane
    global combo_key, harass_key, lasthit_key,LaneClear_key



    ui.text("Leblanc:1.0.0.1")
    ui.separator ()

    ui.text ("Combo Mode:")
    smart_combo=ui.listbox("",["Smart Combo","Q > R > W > E Combo"],smart_combo)

    ui.separator()
    combo_key = ui.keyselect ("Combo Key", combo_key)
    use_q_in_combo = ui.checkbox ("Use Q in Combo", use_q_in_combo)
    use_w_in_combo = ui.checkbox ("Use W in Combo", use_w_in_combo)
    use_e_in_combo = ui.checkbox ("Use E in Combo", use_e_in_combo)
    use_r_in_combo = ui.checkbox ("Use R in Combo", use_r_in_combo)

    ui.separator ()
    # Lane Clear
    LaneClear_key = ui.keyselect ("Lane Clear", LaneClear_key)
    use_q_in_lane = ui.checkbox ("Use Q in Lane Clear", use_q_in_lane)
    use_w_in_lane = ui.checkbox ("Use W in Lane Clear", use_w_in_lane)
    use_e_in_lane = ui.checkbox ("Use E in Lane Clear", use_e_in_lane)
spellTimer = Timer()
testerinio = Timer()

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo,lastQ,smart_combo
    global draw_q_range, draw_e_range, draw_w_range
    global combo_key, harass_key, lasthit_key
    global Q, W, E, R

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game,"E")
    r_spell = getSkill (game, "R")
    target = TargetSelector (game,750)

    global Flag_used

    if target :
        # -------- Combo mode : Q > R > W > E     i got headech for this :
        if smart_combo==1:
            # for buff in target.buffs:
            #     print(buff.name)
            if use_q_in_combo :
                if IsReady(game,q_spell) and  spellTimer.Timer():
                    q_spell.move_and_trigger (game.world_to_screen (target.pos))
                    spellTimer.SetTimer(0.4)
            
            if getBuff(target,"LeblancQMark") and IsReady(game,r_spell) and spellTimer.Timer():
                     r_spell.move_and_trigger(game.world_to_screen(target.pos))
                     spellTimer.SetTimer(0.2)   
            if getBuff (target,"LeblancRQMark")and use_w_in_combo or getBuff (target, "leblanceroot") :
                if not getBuff(game.player,"LeblancW"):
                    if IsReady (game, w_spell) and spellTimer.Timer():
                        w_spell.move_and_trigger (game.world_to_screen (target.pos)) 
                        spellTimer.SetTimer(0.4)   

            if  use_e_in_combo and getBuff(game.player,"LeblancW") and not IsCollisioned(game, target):
                if IsReady(game,e_spell) and spellTimer.Timer() :
                    e_spell.move_and_trigger (game.world_to_screen (target.pos)) 
                    spellTimer.SetTimer(0.4)   
        #-------------------Smart Combo mode :D---------------------------
        if smart_combo==0:
            if use_q_in_combo :
                if IsReady (game, q_spell) and IsReady(game,r_spell):
                    q_spell.move_and_trigger (game.world_to_screen (target.pos))
                if use_r_in_combo:
                    r_spell.move_and_trigger (game.world_to_screen (target.pos))
            if use_w_in_combo:
                if IsReady (game, w_spell)or IsReady(game,r_spell)  or getBuff (target, "leblanceroot"):
                    if not getBuff (game.player, "LeblancW"):
                        w_spell.move_and_trigger (game.world_to_screen (target.pos))
                        if use_r_in_combo:
                            r_spell.move_and_trigger (game.world_to_screen (target.pos))
            if  use_w_in_combo:
                if getBuff (target, "LeblancQMark") or IsReady(game,r_spell)and IsReady (game, w_spell)  or getBuff (target, "leblanceroot"):
                    if not getBuff (game.player, "LeblancW"):
                        w_spell.move_and_trigger (game.world_to_screen (target.pos))
                        if use_r_in_combo:
                            r_spell.move_and_trigger (game.world_to_screen (target.pos))
            if  use_e_in_combo :
                if IsReady (game, e_spell)or IsReady(game,r_spell) and not IsCollisioned(game, target) :
                    e_spell.move_and_trigger ( game.world_to_screen (castpoint_for_collision (game, q_spell, game.player, target)))
                    if use_r_in_combo:
                        r_spell.move_and_trigger (game.world_to_screen (target.pos))

def Harass(game):
    pass
def LaneClear(game):
    global use_q_in_lane,use_w_in_lane,use_e_in_lane

    q_spell = getSkill (game, "Q")
    w_spell = getSkill (game, "W")
    e_spell = getSkill (game, "E")
    r_spell = getSkill (game, "R")
    target = GetBestMinionsInRange (game, 750)
    if target:
        if use_q_in_lane :
            if IsReady (game, q_spell) or IsReady (game, r_spell):
                q_spell.move_and_trigger (game.world_to_screen (target.pos))
        if  use_w_in_lane:
           if IsReady (game, w_spell) or IsReady (game, r_spell)  :
                w_spell.move_and_trigger (game.world_to_screen (target.pos))
        if  use_w_in_lane :
            if IsReady (game, r_spell) and IsReady (game,w_spell)  :
                w_spell.move_and_trigger (game.world_to_screen (target.pos))
        if use_e_in_lane:
            if IsReady (game, e_spell) or IsReady (game, r_spell) :
                e_spell.move_and_trigger (game.world_to_screen (target.pos))


def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_r_in_combo, use_e_in_combo,smart_combo,lastQ,use_q_in_lane,use_w_in_lane,use_e_in_lane
    # print(game.player.W.isActive2)
    if game.player.is_alive and game.is_point_on_screen(game.player.pos) :
        if game.is_key_down(combo_key) :
            Combo(game)
            
        if game.is_key_down(laneclear_key):
            LaneClear(game)
           