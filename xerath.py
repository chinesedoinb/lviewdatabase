from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
import time
import math
import urllib3, json, urllib, ssl
from commons.targit import *

winstealer_script_info = {
    "script": "SA1-Xerath",
	"author": "SA1",
	"description": "SA1-Xerath",
	"target_champ": "xerath"
}


# Keys
combo_key = 46
use_w_in_combo=True

# Range
def q_range(charge_time):
    if charge_time <= 0.4:
        return 400
    if charge_time >= 1:
        return 1450
    return 735 + 102.14*(charge_time - .25)*4
e_range = 550
r_range = 750
max_q_range = 1400


# Speed
q_speed = 1900


# Combo settings
combo_enabled = True
use_q_in_combo = True
grabs_only = False
use_e_in_combo = True
move_in_combo = False
grab_best_target_overall = True
grab_nearest_to_player = False
grab_nearest_to_cursor = False
grab_lowest_in_range = False


# Combo variables
charging_q = False


# Kill steal
r_kill_steal = True
disable_ks_key = 56
last_executed_target = None


# Aiborn duration of pyke's hook
q_airborn_duration = 1.1


# Last target grabbed
last_target_grabbed = None


# Used to prevent using ult right after grab
delay_r = False


# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats


# Calculate R execution damage
r_lvl_damage_list = [250, 290, 330, 370, 400, 430, 450, 470, 490, 510, 530, 540, 550]
def r_execution_threshold(game):
    level = getPlayerStats()["level"]
    if level < 6:
        return 0
    r_lvl_damage = r_lvl_damage_list[level - 6]
    bonus_damage = game.player.bonus_atk
    lethality = getPlayerStats()["championStats"]["physicalLethality"]
    return r_lvl_damage + 0.8*bonus_damage + 1.5*lethality


def winstealer_load_cfg(cfg):
    # Keys
    global combo_key,use_w_in_combo
    combo_key = cfg.get_int("combo_key", 57)

    # Combo settings
    global combo_enabled, use_q_in_combo, grabs_only, use_e_in_combo, move_in_combo
    combo_enabled = cfg.get_bool("combo_enabled", True)
    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    grabs_only = cfg.get_bool("grabs_only", False)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    move_in_combo = cfg.get_bool("move_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)

    global grab_best_target_overall, grab_nearest_to_player, grab_nearest_to_cursor, grab_lowest_in_range
    grab_best_target_overall = cfg.get_bool("grab_best_target_overall", True)
    grab_nearest_to_player = cfg.get_bool("grab_nearest_to_player", False)
    grab_nearest_to_cursor = cfg.get_bool("grab_nearest_to_cursor", False)
    grab_lowest_in_range = cfg.get_bool("grab_lowest_in_range", False)

    # Kill steal
    global r_kill_steal, disable_ks_key
    r_kill_steal = cfg.get_bool("r_kill_steal", True)
    disable_ks_key = cfg.get_int("disable_ks_key", 56)


def winstealer_save_cfg(cfg):
    # Keys
    cfg.set_int("combo_key", combo_key)

    # Combo settings
    cfg.set_bool("combo_enabled", combo_enabled)
    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("grabs_only", grabs_only)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("move_in_combo", move_in_combo)
    cfg.set_bool("grab_nearest_to_player", grab_nearest_to_player)
    cfg.set_bool("grab_nearest_to_cursor", grab_nearest_to_cursor)
    cfg.set_bool("grab_lowest_in_range", grab_lowest_in_range)
    cfg.set_bool("grab_best_target_overall", grab_best_target_overall)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)

    # Kill steal
    cfg.set_bool("r_kill_steal", r_kill_steal)
    cfg.set_int("disable_ks_key", disable_ks_key)


def winstealer_draw_settings(game, ui):
    # Keys
    global combo_key
    combo_key = ui.keyselect("Combo key", combo_key)

    # Combo settings
    if ui.treenode("Combo Settings"):
        global combo_enabled, move_in_combo,use_w_in_combo
        combo_enabled = ui.checkbox("Enable combo", combo_enabled)
        
        
        # if ui.treenode("Targeting"):
        #         global grab_best_target_overall, grab_nearest_to_player, grab_nearest_to_cursor, grab_lowest_in_range

        #         # Best target overall
        #         grab_best_target_overall = ui.checkbox("Best target overall (recommended)", grab_best_target_overall)
        #         if grab_best_target_overall:
        #             grab_nearest_to_player = False
        #             grab_nearest_to_cursor = False
        #             grab_lowest_in_range = False
        #         elif not grab_nearest_to_player and not grab_nearest_to_cursor and not grab_lowest_in_range:
        #             grab_best_target_overall = True

        #         # Nearest to player
        #         grab_nearest_to_player = ui.checkbox("Nearest to player", grab_nearest_to_player)
        #         if grab_nearest_to_player:
        #             grab_nearest_to_cursor = False
        #             grab_lowest_in_range = False
        #             grab_best_target_overall = False
        #         elif not grab_nearest_to_cursor and not grab_lowest_in_range and not grab_best_target_overall:
        #             grab_nearest_to_player = True

        #         # Nearest to cursor
        #         grab_nearest_to_cursor = ui.checkbox("Nearest to cursor", grab_nearest_to_cursor)
        #         if grab_nearest_to_cursor:
        #             grab_nearest_to_player = False
        #             grab_lowest_in_range = False
        #             grab_best_target_overall= False
        #         elif not grab_nearest_to_player and not grab_lowest_in_range and not grab_best_target_overall:
        #             grab_nearest_to_cursor = True

        #         # Lowest enemy in range
        #         grab_lowest_in_range = ui.checkbox("Lowest enemy in range", grab_lowest_in_range)
        #         if grab_lowest_in_range:
        #             grab_nearest_to_cursor = False
        #             grab_nearest_to_player = False
        #             grab_best_target_overall = False
        #         elif not grab_nearest_to_cursor and not grab_nearest_to_player and not grab_best_target_overall:
        #             grab_lowest_in_range = True

        #         ui.treepop()
            
        # Q Settings
        if ui.treenode("Q Settings"):
            global use_q_in_combo, grabs_only
            use_q_in_combo = ui.checkbox("Use Q in combo", use_q_in_combo)
            

            # Grab Preference
            

        # E Settings
        if ui.treenode("E Settings"):
            global use_e_in_combo
            use_e_in_combo = ui.checkbox("Use E in combo", use_e_in_combo)
            ui.treepop()
        

        if ui.treenode("W Settings"):
            
            use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
            ui.treepop()
        ui.treepop()
    # Kill steal
    if ui.treenode("R settings"):
        global r_kill_steal, disable_ks_key
        # r_kill_steal = ui.checkbox("Steal kills with R", r_kill_steal)
        disable_ks_key = ui.keyselect("Active R", disable_ks_key)
        ui.treepop()


def charge_q(game, q_spell):
    global charging_q, charge_start_time
    q_spell.trigger(True)
    charging_q = True
    charge_start_time = game.time

spellTimer = Timer()
def release_q(game, q_spell,target):
    global charging_q
    q_spell.move_and_trigger(game.world_to_screen(target))   
    charging_q = False


def GetLowestTargetInRange(game, atk_range=0):
    num = 999999999
    target = None
    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius
    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        if num >= champ.health:
            num = champ.health
            target = champ
    return target


def get_distance(pos1, pos2):
    x_distance = pos2.x - pos1.x
    y_distance = pos2.y - pos1.y
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance


def circle_on_line(A, B, C, R):
    # A: start of the line
    # B: end of the line
    # C: center of the circle
    # R: Radius of the circle

    # Compute the distance between A and B.
    x_diff = B.x - A.x
    y_diff = B.y - A.y
    LAB = math.sqrt(x_diff ** 2 + y_diff ** 2)

    # Compute the direction vector D from A to B.
    Dx = x_diff / LAB
    Dy = y_diff / LAB

    # The equation of the line AB is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= LAB.

    # Compute the distance between the points A and E, where
    # E is the point of AB closest the circle center (Cx, Cy)
    t = Dx*(C.x - A.x) + Dy*(C.y - A.y)
    if not -R <= t <= LAB + R:
        return False

    # Compute the coordinates of the point E using the equation of the line AB.
    Ex = t*Dx+A.x
    Ey = t*Dy+A.y

    # Compute the distance between E and C
    x_diff1 = Ex - C.x
    y_diff1 = Ey - C.y
    LEC = math.sqrt(x_diff1 ** 2 + y_diff1 ** 2)

    return LEC <= R


def is_collisioned(game, target, oType="minion", ability_width=0):
    player_pos = game.world_to_screen(game.player.pos)
    target_pos = game.world_to_screen(target.pos)

    if oType == "minion":
        for minion in game.minions:
            if minion.is_enemy_to(game.player) and minion.is_alive:
                minion_pos = game.world_to_screen(minion.pos)
                total_radius = minion.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, minion_pos, total_radius):
                    return True
    
    if oType == "champ":
        for champ in game.champs:
            if champ.is_enemy_to(game.player) and champ.is_alive and not champ.id == target.id:
                champ_pos = game.world_to_screen(champ.pos)
                total_radius = champ.gameplay_radius + ability_width / 2
                if circle_on_line(player_pos, target_pos, champ_pos, total_radius):
                    return True
    
    return False


def getTargetsInRange(game, atk_range = 0) -> list:
    targets = []

    if atk_range == 0:
        atk_range = game.player.atkRange + game.player.gameplay_radius

    for champ in game.champs:
        if champ.name in clones and champ.R.name == champ.D.name:
            continue
        if (
            not champ.is_alive
            or not champ.is_visible
            or not champ.isTargetable
            or champ.is_ally_to(game.player)
            or game.player.pos.distance(champ.pos) >= atk_range
        ):
            continue
        targets.append(champ)

    return targets


def getTargetsByHealth(game, atk_range = 0) -> list:
    '''Returns a sorted list of the targets in range from lowest to highest health'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: x.health)


def getTargetsByClosenessToPlayer(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the player'''

    targets = getTargetsInRange(game, atk_range)
    return sorted(targets, key = lambda x: game.player.pos.distance(x.pos))


def getTargetsByClosenessToCursor(game, atk_range = 0) -> list:
    '''Returns a sorted list of the closest targets (in range) to the cursor'''

    targets = getTargetsInRange(game, atk_range)
    cursor_pos_vec2 = game.get_cursor()
    cursor_pos_vec3 = Vec3(cursor_pos_vec2.x, cursor_pos_vec2.y, 0)
    return sorted(targets, key = lambda x: get_distance(cursor_pos_vec3, game.world_to_screen(x.pos)))

def castingQ(player):
	return True in ["xeratharcanopulsechargeup" in buff.name.lower() for buff in player.buffs]

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


manaQ=[80,90,100,110,120]
manaW=[70,80,90,100,110]
manaE=[60,65,70,75,80]
def combo(game):
		global spellTimer
		q_spell = getSkill(game, 'Q')
		e_spell = getSkill(game, 'E')
		w_spell= getSkill(game, 'W')
		old_cursor_pos = game.get_cursor()

		

		global last_target_grabbed
		if use_q_in_combo and IsReady(game, q_spell):
			target=TargetSelector(game,max_q_range)

			if target:
				if not charging_q:
				
						charge_q(game, q_spell)
						return
				current_charge_time = game.time - charge_start_time
				current_q_range = q_range(current_charge_time)
				current_q_travel_time = (current_q_range / q_speed ) 

				predicted_pos = predict_pos(target,  0.528 )
				# predicted_pos= game.GetPredication(target,current_q_travel_time,q_speed)
				predicted_target = Fake_target(target.name, predicted_pos, target.gameplay_radius)

				if game.player.pos.distance(predicted_target.pos) <= current_q_range - 50:
						if castingQ(game.player)  and spellTimer.Timer():
							release_q(game, q_spell,predicted_target.pos)
							spellTimer.SetTimer(0.4)
						elif game.player.mana>= manaQ[game.player.Q.level -1] and  spellTimer.Timer():
							release_q(game, q_spell,predicted_target.pos)
							spellTimer.SetTimer(0.4)

		if use_e_in_combo and IsReady(game, e_spell) :
			target = TargetSelector(game, 1050)
			if target:
				disToPlayer=game.player.pos.distance (target.pos)
				
				q_travel_time = (disToPlayer/1600) +0.100
				# q_travel_time = (1050/1600) +0.200
				predicted_pos = predict_pos (target, q_travel_time)
				predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
				if game.player.pos.distance (predicted_target.pos) <= 950 and not IsCollisioned(game, target):
						if  game.player.mana >= manaE[game.player.E.level -1] and spellTimer.Timer():
							e_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))   
							spellTimer.SetTimer(0.4)
							

		if use_w_in_combo and IsReady(game, w_spell) :
			target = TargetSelector(game, 1100)
			if target:
				q_travel_time = (1000/9999999) + 0.3
				predicted_pos = predict_pos (target, q_travel_time)
				predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
				if game.player.pos.distance (predicted_target.pos) <= 1100:
					if  game.player.mana >= manaW[game.player.W.level -1] and spellTimer.Timer():
						w_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
						spellTimer.SetTimer(0.2)

def hasQBuff(target):
    return True in ["pykeq" in buff.name.lower() for buff in target.buffs]


def isSlowed(target):
    return "slow" in [buff.name.lower() for buff in target.buffs]


def target_airborned(game, target):
    if not last_target_grabbed:
        return False
    return target.id == last_target_grabbed["id"] and game.time - last_target_grabbed["time"] <= q_airborn_duration


def steal_with_r(game):
		global last_executed_target,disable_ks_key,spellTimer
		r_spell= getSkill(game, 'R')

		old_cursor_pos = game.get_cursor()

		if disable_ks_key and IsReady(game, r_spell) and not charging_q:
			target = GetBestTargetsInRange(game, 5000)
			if target:
				predicted_pos = predict_pos (target, 0.5)
				predicted_target = Fake_target (target.name, predicted_pos, target.gameplay_radius)
				if game.player.pos.distance (predicted_target.pos) <= 5000:
					if  game.player.mana >= 70 and  spellTimer.Timer():
						r_spell.move_and_trigger(game.world_to_screen(predicted_target.pos))
						spellTimer.SetTimer(0.4)


def winstealer_update(game, ui):
    player = game.player

    # q_spell = getSkill(game, 'Q')
    # q_current_cooldown = round(q_spell.get_current_cooldown(game.time), 1)
    # if charging_q and q_current_cooldown != 0:
    #     release_q(game, q_spell)
    # for b in game.player.buffs:
    #     print(b.name)
    if player.is_alive and player.is_visible :
        if game.was_key_pressed(combo_key) and combo_enabled:
            combo(game)
        
        if game.was_key_pressed(disable_ks_key):
            steal_with_r(game)