from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from commons.ByLib import *
from evade import checkEvade
import json, time, math
from commons.targit import *
winstealer_script_info = {
    "script": " Yuumi ",
    "author": "SA1",
    "description": "SA1",
    "target_champ": "yuumi",
}

combo_key = 57
harass_key = 45
laneclear_key = 47

qiyong = True
auto_e = True
auto_eHP = 0.0
auto_eMana = 0.0
auto_r = True
Rarea = 0
mainw = 0
subw = 0
wlist = []

q = {"Range": 1150}
w = {"Range": 700}
e = {"Range": 925}
r = {"Range": 1100}
x = {"Range": 99999}
				
def winstealer_load_cfg(cfg):
    global auto_e, auto_eHP, auto_eMana, r_combo, rc, auto_r, auto_w
    global drawQ, drawW, drawE, alert, draw_status, mainw, subw
    global combo_key, harass_key, laneclear_key
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    auto_w = cfg.get_bool("auto_w", True)
    auto_e = cfg.get_bool("auto_e", True)
    auto_eHP = cfg.get_float("auto_eHP", 60)
    auto_eMana = cfg.get_float("auto_eMana", 40)
    r_combo = cfg.get_bool("r_combo", True)
    auto_r = cfg.get_bool("auto_r", True)
    mainw = cfg.get_int("mainw", 0)
    subw = cfg.get_int("subw", 1)
    #rc = cfg.get_int("rc", 3)

	
def winstealer_save_cfg(cfg):
    global auto_e, auto_eHP, auto_eMana, r_combo, rc, auto_r, auto_w
    global drawQ, drawW, drawE, alert, draw_status, mainw, subw
    global combo_key, harass_key, laneclear_key
	
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)


    cfg.set_bool("auto_w", auto_w)
    cfg.set_bool("auto_e", auto_e)
    cfg.set_float("auto_eHP", auto_eHP)
    cfg.set_float("auto_eMana", auto_eMana)
    cfg.set_bool("r_combo", r_combo)
    cfg.set_int("auto_r", auto_r)
    cfg.set_int("mainw", mainw)
    cfg.set_int("mainw", subw)
    #cfg.set_int("rc", rc)

	
def winstealer_draw_settings(game, ui):
    global auto_e, auto_eHP, auto_eMana, r_combo, rc, auto_r, auto_w
    global drawQ, drawW, drawE, alert, draw_status, mainw, subw
    global combo_key, harass_key, laneclear_key
    global wlist
    
    for ally in game.champs:
        if ally.is_ally_to(game.player) and ally.name != game.player.name:
            #print("123" + ally.name)
            if not ally.name in wlist:
                wlist.append(ally.name)
    combo_key = ui.keyselect("Combo key", combo_key)
    harass_key = ui.keyselect("Harass key", harass_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)
	
	
	# ui.text()
    if ui.treenode("AFK-AT"):
		
        auto_w = ui.checkbox("Auto W", auto_w)
        auto_e = ui.checkbox("Auto E", auto_e)
        auto_eHP = ui.sliderfloat("HP to E", auto_eHP, 1,100)
        auto_eMana = ui.sliderfloat("Auto E Mana", auto_eMana, 1,100)
        ui.text("Will try auto AOE R when more than ONE enemy can be hit")
        ui.text("sometimes prediction can be off")
        auto_r = ui.checkbox("Auto try AOE R", auto_r)
        ui.treepop()
    if ui.treenode("W Setting"):
        ui.text("Main W Target")
        #print(wlist)
        mainw = ui.listbox( "Main W Ally", [str(target) for target in wlist], mainw)
        ui.separator()
        ui.text("Sub W Target")
        subw = ui.listbox( "Sub W Ally", [str(target) for target in wlist], subw)
        ui.text("If changed target while W, make sure to W out")
        ui.treepop()
    if ui.treenode("R Setting"):
        r_combo = ui.checkbox("Combo R", r_combo)
        #rc = ui.sliderint("Enemy count to R", int(rc), 1, 5)
        ui.treepop()
    ui.text("Report issues for suggestions to LOVETAIWAN#4123, Huge thx to azreal for many support.")


	
percentage = 0

def zaijia(game, unit) -> bool:
	champhead_pos = game.world_to_screen(game.player.pos)
	for turret in game.turrets:
		if turret.is_ally_to(game.player) and not str(turret.name).find("sruap_turret_order5"):
			range = turret.atk_range + 30
			dist = turret.pos.distance(game.player.pos) - range
			if dist <= game.player.gameplay_radius:
				#game.draw_text(champhead_pos, "HOME", Color.RED)
				return True
	return False

def insided(game, unit) -> bool:
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
			and champ.name == game.player.name
        ):
            if getBuff(champ, "YuumiWAttach"):
                return True
    return False
#YuumiWSpellPassive

	

def GetLowestHPTarget(game, range):
    lowest_target = None
    lowest_hp = 9999
	
    for champ in game.champs:
        if (
            champ.is_alive
            and champ.is_visible
            and champ.is_ally_to(game.player)
            #and game.is_point_on_screen(champ.pos) if move cam and target not on screen will cause crash on draw low HP ally alert
            and champ.pos.distance(game.player.pos) <= range
			and not champ.name == game.player.name
        ):
            if(champ.health < lowest_hp):
                lowest_hp = champ.health
                lowest_target = champ

    return lowest_target
	
def Healinside(game):
	global auto_e, auto_eHP, auto_eMana, ehpp, emanap
	ehpp = auto_eHP * 0.01
	emanap = auto_eMana * 0.01
	
	e_spell = getSkill(game, "E")
	enemy = TargetSelector(game, 1000)#need check if enemy around?
	
	for champ in game.champs:
		if champ.is_ally_to(game.player) and getBuff(champ, "YuumiWAlly"):
			if not champ == game.player:
				target = champ
				if auto_e and IsReady(game, e_spell):
					#print("Inside heal")
					if target.health < (ehpp * target.max_health) and game.player.mana > (emanap * game.player.max_mana) and not zaijia(game, target) and not getBuff(game.player, "recall") and target.is_alive:
						e_spell.trigger(False)

def Healoutside(game):
	global auto_e, auto_eHP, auto_eMana, ehpp, emanap
	ehpp = auto_eHP * 0.01
	emanap = auto_eMana * 0.01
	e_spell = getSkill(game, "E")
	
	if auto_e and IsReady(game, e_spell):
		#print("outside heal")
		if game.player.health < (ehpp * game.player.max_health) and game.player.mana > (emanap * game.player.max_mana) and not zaijia(game, game.player) and not getBuff(game.player, "recall"):
			e_spell.trigger(False)


def GetNearTarget(game, r_range=1100):
	global rc
	neartar = None
	worsttarget = None
	target1 = None
	target2 = None
	target3 = None
	target4 = None
	targetlist = []
	r_spell = getSkill(game, "R")
	i = 0
	
	enemy = TargetSelector(game, 1100)
	if enemy:
		for champ in game.champs:
			if (
				champ.is_alive
				and champ.is_visible
				and champ.is_enemy_to(game.player)
				and game.player.pos.distance(champ.pos) <= r_range
				and not champ.name == enemy.name
				and not neartar.name == champ.name
				):
					neartar = champ
					if neartar.pos.distance(enemy.pos) <= 100:
						print("100")
						r_spell.move_and_trigger(game.world_to_screen(enemy.pos))
					if neartar.pos.distance(enemy.pos) < 200:
						print("200")
						r_spell.move_and_trigger(game.world_to_screen(enemy.pos))



def Rtarget(game):
	global rcount
	global r_combo, rc, Rarea
	rcount = 0
	r_spell = getSkill(game, "R")
	#target = GetNearTarget(game, r["Range"])
	target = TargetSelector(game, r["Range"])
	
	if target and r_combo:
		r_spell.move_and_trigger(game.world_to_screen(target.pos))
		
	'''
	if target:
		tos = target.pos
		path = tos.sub(game.player.pos)
		Rarea = tos.add(path.normalize().scale(40 * 15))
	if IsReady(game, r_spell):
		r_spell.move_and_trigger(game.world_to_screen(tos.add(path.normalize().scale(40 * 11))))
	
	for target in game.champs:
		if (target and target.is_visible and target.is_enemy_to(game.player) and target.isTargetable and target.is_alive and game.is_point_on_screen(target.pos) and game.distance(game.player, target) < r["Range"]):
			rcount = rcount + 1
			if (r_combo and rcount <= rc):
				if rcount >= rc:
					#r_spell.move_and_trigger(game.world_to_screen(castpoint_for_collision(game, r_spell, game.player, target)))
					r_spell.move_and_trigger(game.world_to_screen(target.pos))
	'''

def meow(game, champ):
	global auto_r
	if (
        not champ.is_alive
        or champ.name == game.player.name
        or not champ.is_visible
        or champ.is_ally_to(game.player)
        or not game.is_point_on_screen(champ.pos)
	):
		return
	enemy = TargetSelector(game, 1100)
	if auto_r and enemy and champ:
		if enemy.pos.distance(champ.pos) <= 600:
			if game.player.pos.distance(enemy.pos) <= 1100 and game.player.pos.distance(champ.pos) <= 1100 and game.player.is_alive:
				dist = champ.pos.distance(enemy.pos)
				r_spell = getSkill(game, "R")
				pos = game.world_to_screen(
					champ.pos.sub(enemy.pos)
					.normalize()
					.scale(enemy.atk_range + enemy.gameplay_radius)
					.add(enemy.pos)
				)
				game.draw_line(
					game.world_to_screen(enemy.pos),
					game.world_to_screen(champ.pos),
					2,
					Color.BLUE,
				)
				if float(dist) <= 600 and float(dist) != 0.0:
					r_spell.move_and_trigger(game.world_to_screen(enemy.pos))
                    #print(float(dist))
def qTarget(game):
	q_spell = getSkill(game, "Q")
	enemy = TargetSelector(game, 1150)
	if enemy and game.player.mana>=90 and IsReady(game,q_spell):
		game.move_cursor(game.world_to_screen(enemy.pos))
		if game.hovered_obj:
				if game.is_point_on_screen(game.player.pos):
					if not IsCollisioned(game, enemy):
						q_spell.trigger(False)
						time.sleep(0.1)

def wtarget(game):
	global mainw, subw
	w_spell = getSkill(game, "W")
	#print(mainw)
	#print(wlist)
	targettow = wlist[mainw]
	subtow = wlist[subw]
	friend = None
	friend2 = None
	#print("target now " + targettow)
	#print("target 2 " + subtow)
	

	for champ in game.champs:
		if zaijia(game, champ):
			#print("NO")
			return
		else:
			if champ.is_ally_to(game.player) and champ.is_alive:
				if not champ == game.player:
					#if game.player.pos.distance(champ.pos) <= x["Range"]: make it auto bot? make find whoever low hp in whole map for w?
					if game.player.pos.distance(champ.pos) <= w["Range"]:
						friend = champ
						#print("friend 1" + friend.name)
						if friend and game.player.pos.distance(friend.pos) <= w["Range"]:
							#print("looking for " + friend.name)
							if friend.name == targettow and not insided(game, game.player) and not getBuff(friend, "recall") and friend.isTargetable:
								#print(targettow + "find")
								w_spell.move_and_trigger(game.world_to_screen(friend.pos))
								
								
					if game.player.pos.distance(champ.pos) <= w["Range"] and friend != friend2:
						friend2 = champ
						#print("friend 2 " + friend2.name)
						if friend2 and game.player.pos.distance(friend2.pos) <= w["Range"] or game.player.pos.distance(friend.pos) > w["Range"]:
							#print("looking for 2nd" + friend.name)
							if friend2.name == subtow and not insided(game, game.player) and not getBuff(friend, "recall") and friend2.isTargetable and game.player.pos.distance(friend2.pos) <= w["Range"] and not zaijia(game, friend2):
								#print("main guy dead find a new lover" + friend2.name)
								w_spell.move_and_trigger(game.world_to_screen(friend2.pos))
							

								
						
def targetR(game):
	r_spell = getSkill(game, "R")
	target=TargetSelector(game,1100)
	if auto_r and IsReady(game, r_spell) and game.player.mana>=100:
		if target:
			game.move_cursor(game.world_to_screen(target.pos))
			if game.hovered_obj:
				if game.is_point_on_screen(game.player.pos):
					r_spell.trigger(False)
					time.sleep(0.1)


clicking=True	
def winstealer_update(game, ui):
	global auto_e, auto_eHP, auto_eMana, auto_r, auto_w
	global combo_key, harass_key, laneclear_key, wlist ,clicking
	
	w_spell = getSkill(game, "W")
	clicked=False
	self = game.player
	player_pos = game.world_to_screen(game.player.pos)
	ally= GetAllyChampsInRange2(game)
	target=TargetSelector(game,1100)
	if self.is_alive :
		if ally :
				if insided(game, game.player):
					targetR(game)
					qTarget(game)
					
				if not insided(game, game.player) :
					if IsReady(game,w_spell) and clicking==True:
						game.move_cursor(game.world_to_screen(ally.pos))
						w_spell.trigger(False)
						time.sleep(0.1)
					
					if game.hovered_obj :
							# print(game.hovered_obj.name)
							clicking=False
					else:
							clicking=True
		if game.is_key_down(combo_key):
			#NearTarget(game)
			Rtarget(game)
		if insided(game, game.player):
			#game.draw_text(champhead_pos, "IN", Color.RED)
			Healinside(game)
		if not insided(game, game.player):
			Healoutside(game)
		# for champ in game.champs:
			
		# 	if len(wlist) > 0 and auto_w and not getBuff(self, "recall") and IsReady(game, w_spell):
		# 		wtarget(game)