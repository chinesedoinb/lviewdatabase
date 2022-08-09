from winstealer import *
from win32api import GetSystemMetrics
from commons.utils import *
from commons.timer import *
show_local_champ = False
show_allies = False
show_enemies = False
show_hud_right = True
show_hud_left = False

show_info= True

winstealer_script_info = {
    "script": "Skills utillity",
    "author": "SA1",
    "description": "Tracks spell cooldowns and levels",
}


def winstealer_load_cfg(cfg):
    global show_allies, show_enemies, show_local_champ,show_hud_right,show_hud_left,show_info

    show_allies = cfg.get_bool("show_allies", False)
    show_enemies = cfg.get_bool("show_enemies", True)
    show_local_champ = cfg.get_bool("show_local_champ", False)
    show_hud_right = cfg.get_bool("show_hud_right", show_hud_right)
    show_hud_left = cfg.get_bool("show_hud_left", show_hud_left)
    show_info = cfg.get_bool("show_info", show_info)

def winstealer_save_cfg(cfg):
    global show_allies, show_enemies, show_local_champ,show_hud_right,show_hud_left,show_info

    cfg.set_bool("show_allies", show_allies)
    cfg.set_bool("show_enemies", show_enemies)
    cfg.set_bool("show_local_champ", show_local_champ)
    cfg.set_bool("show_hud_right", show_hud_right)
    cfg.set_bool("show_hud_left", show_hud_left)
    cfg.set_bool("show_info", show_info)

def winstealer_draw_settings(game, ui):
    global show_allies, show_enemies, show_local_champ, show_hud_right,show_hud_left,show_info
    show_info=ui.checkbox("Show enemies ready spells top of the screen", show_info)
    show_allies = ui.checkbox("Show overlay on allies", show_allies)
    show_enemies = ui.checkbox("Show overlay on enemies", show_enemies)
    show_local_champ = ui.checkbox("Show overlay on self", show_local_champ)

    
    # ui.text(str( game.time - game.player.W.ready_at ))
    if ui.treenode("Show HUD"):
        
        show_hud_right = ui.checkbox("Show Right Hud", show_hud_right)
        show_hud_left = ui.checkbox("Show Left Hud", show_hud_left)
        ui.treepop()
def get_color_for_cooldown(cooldown):
    if cooldown > 0.0:
        return Color.RED
    else:
        return Color(1, 1, 1, 1)


def draw_spell(game, spell, pos, size, show_lvl=True, show_cd=True):

        cooldown = spell.get_current_cooldown(game.time)
        color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY

        game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 0)
        if show_cd and cooldown > 0.0:
            x = 0
            if int(cooldown < 10):
                x = 10.5
            elif int(cooldown) >= 10 and int(cooldown) < 100:
                x = 6.5

            game.draw_text(pos.add(Vec2(x, 6)), str(int(cooldown)), Color.WHITE)
        if show_lvl:
            for i in range(spell.level):
                offset = i*4
                game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.RED)
                
def draw_overlay_on_champ(game, champ):

    p = game.hp_bar_pos(champ)
    p.x -= 60
    if not game.is_point_on_screen(p):
        return

    p.x += 15
    draw_spell(game, champ.Q, p, 20 )
    p.x += 25
    draw_spell(game, champ.W, p, 20)
    p.x += 25
    draw_spell(game, champ.E, p, 20)
    p.x += 25
    draw_spell(game, champ.R, p, 20)
    p.x += 33
    p.y -= 30
    draw_spell(game, champ.D, p, 20)
    p.x += 0
    p.y += 25
    draw_spell(game, champ.F, p, 20)

# def get_color_for_cooldown(cooldown):
# 	if cooldown > 0.0:
# 		return Color.ORANGE
# 	else:
# 		return Color(1, 1, 1, 1)

def get_color_for_cooldown_minimal(cooldown):
	if cooldown > 0.0:
		return Color.ORANGE
	else:
		return Color.GREEN

def draw_spell2(game, spell, pos, size, show_lvl = False, show_cd = True):

        cooldown = spell.get_current_cooldown(game.time)
        color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.RED

        game.draw_image(spell.icon, pos, pos.add(Vec2(size + 4, size + 4)), color, 1.0)
        if show_cd and cooldown > 0.0:
            game.draw_text(pos.add(Vec2(7, 25)), str(int(cooldown)), Color.RED)
        
        if show_lvl:
            for i in range(spell.level):
                offset = i*4
                game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 22, pos.x + offset + 3, pos.y + 26), Color.RED)
def draw_minimalspell(game,mana , spell, pos, show_lvl):
        cooldown = spell.get_current_cooldown(game.time)
        # else Color.BLACK
        color = get_color_for_cooldown_minimal(cooldown) 
        if spell.level > 0 :
            if mana < skillMana(game,spell,spell.level) :
                 color = Color.BLUE
        else:
            color = Color.BLACK
        game.draw_rect_filled(Vec4(pos.x -12, pos.y -1, pos.x + 10, pos.y + 3), color)
        for i in range(int(cooldown)):
            game.draw_text(pos.add(Vec2(-3, 15)), str(int(cooldown)), Color.WHITE)
        if show_lvl:
            for i in range(spell.level):
                offset = i*4
                game.draw_rect_filled(Vec4(pos.x + offset-12, pos.y + 7, pos.x + offset -11 , pos.y +12), Color.GREEN)
def draw_innerbox(game, pos, size):

	game.draw_rect_filled(Vec4(pos.x + 23, pos.y - 2, pos.x + 130, pos.y + 6), Color.GRAY)

def draw_overlay_on_champ2(game, champ):

	p = game.hp_bar_pos(champ)
	p.x -= 70
	if not game.is_point_on_screen(p):
		return

	draw_innerbox(game, p, 24)
	p.x += 39
	draw_minimalspell(game,champ.mana, champ.Q, p,True)
	p.x += 26
	draw_minimalspell(game, champ.mana,champ.W, p,True)
	p.x += 26
	draw_minimalspell(game, champ.mana,champ.E, p,True)
	p.x += 26
	draw_minimalspell(game, champ.mana,champ.R, p,True)

	p.x += 16
	p.y -= 27
	draw_spell(game, champ.D, p, 15, False, False)
	p.y += 17
	draw_spell(game, champ.F, p, 15, False, False)

spellTimer = Timer()   
showed=False
last=0
def show_ready_spells(game):
    global showed,last
    x = ((GetSystemMetrics(0) / 2) * 2) - 1150
    y = GetSystemMetrics(1) / 2 - 355
    i=0
    player=game.player
    heroColor = Color.WHITE
    for champ in game.champs:
       
            if champ.health>0.0:
                if IsReady(game,player.D) :
                    
                        game.draw_image(
                        player.D.icon,
                        Vec2(x + 100, y + i ),
                        Vec2(x + 100, y + i ).add(Vec2(70, 70)),
                        Color.WHITE,
                        150 )
                
                        game.draw_image(
                            player.name.lower() + "_square",
                            Vec2(x + 4.5, y + i ),
                            Vec2(x + 10, y + i ).add(Vec2(70, 70)),
                            heroColor,
                            150)
                        showed=True
                       
                else:
                    showed=False



def draw_right_hud(game):
    i = 0
    
    x = ((GetSystemMetrics(0) / 2) * 2) - 175
    y = GetSystemMetrics(1) / 2 - 355

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.health>0.0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 95 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hpbare",
                Vec2(x + 66, y + i - 15),
                Vec2(x + 99, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 66, y + i - 11.5),
                Vec2(x + width, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 95 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hpbare",
                    Vec2(x + 55, y + i + 7),
                    Vec2(x + 99, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 66, y + i + 10.5),
                    Vec2(x + width2, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(46, 2.7)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 4.5, y + i - 25),
                Vec2(x + 10, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud",
                Vec2(x, y + i - 30),
                Vec2(x, y + i - 30).add(Vec2(70, 70)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 82, y + i + 33),
                Vec2(x + 80, y + i + 33).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(13, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "spellslot",
                Vec2(x + 80, y + i + 33),
                Vec2(x + 80, y + i + 33).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 126, y + i + 33),
                Vec2(x + 124, y + i + 33).add(Vec2(35, 35)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(13, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "spellslot",
                Vec2(x + 124, y + i + 33),
                Vec2(x + 124, y + i + 33).add(Vec2(35, 35)),
                Color.WHITE,
            )
            # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 46, y + i + 16),
                Vec2(x + 20, y + i - 8).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(46, 2.7)), hpword, Color.GRAY)

            # game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 110

def draw_left_hud(game):
    i = 0
    
    x = ((GetSystemMetrics(0) / 2) * 2) - 1920
    y = GetSystemMetrics(1) / 2 - 355

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            if champ.health>0:
                heroColor = Color.WHITE
            else:
                heroColor = Color.RED
            hp = champ.max_health / 100
            hpyuzde = champ.health / hp
            yuzde = 95 / 100
            width = yuzde * hpyuzde
            hpword = str(int(hpyuzde)) + " %"
            hpbarcoord = Vec2(x + 55, y + i - 15)
            IsUltReady = IsReady(game, champ.R)
            Icon = champ.R.icon

            ##HpBar
            game.draw_image(
                "hpbare",
                Vec2(x + 66, y + i - 15),
                Vec2(x + 99, y + i - 63.5).add(Vec2(70, 70)),
                Color.WHITE,
            )
            ##HpInner
            game.draw_image(
                "hpgreen",
                Vec2(x + 66, y + i - 11.5),
                Vec2(x + width, y + i - 67).add(Vec2(70, 70)),
                Color.WHITE,
            )

            if champ.max_mana > 0:
                mana = champ.max_mana / 100
                manayuzde = champ.mana / mana
                yuzde2 = 95 / 100
                width2 = yuzde2 * manayuzde
                manaword = str(int(manayuzde)) + " %"
                manabarcoord = Vec2(x + 55, y + i + 7)

                ##manaBar
                game.draw_image(
                    "hpbare",
                    Vec2(x + 55, y + i + 7),
                    Vec2(x + 99, y + i - 40.5).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                ##ManaInner
                game.draw_image(
                    "manablue",
                    Vec2(x + 66, y + i + 10.5),
                    Vec2(x + width2, y + i - 44).add(Vec2(70, 70)),
                    Color.WHITE,
                )
                game.draw_text(manabarcoord.add(Vec2(46, 2.7)), manaword, Color.WHITE)

            game.draw_image(
                champ.name.lower() + "_square",
                Vec2(x + 4.5, y + i - 25),
                Vec2(x + 10, y + i - 20).add(Vec2(55, 55)),
                heroColor,
                150,
            )

            game.draw_image(
                "hud",
                Vec2(x, y + i - 30),
                Vec2(x, y + i - 30).add(Vec2(70, 70)),
                Color.WHITE,
            )
            CDd = champ.D.get_current_cooldown(game.time)
            dColor = Color.WHITE
            if CDd > 0:
                dColor = Color.RED

            else:
                dColor = Color.WHITE

            game.draw_image(
                champ.D.icon,
                Vec2(x + 82, y + i + 33),
                Vec2(x + 80, y + i + 33).add(Vec2(35, 35)),
                dColor,
            )

            if CDd > 0:
                dx = x + 78
                if CDd > 10 and CDd < 100:
                    dx = x + 76
                elif CDd > 99:
                    dx = x + 74
                game.draw_text(
                    Vec2(dx, y + i + 33).add(Vec2(13, 11)), str(int(CDd)), Color.WHITE
                )
            game.draw_image(
                "spellslot",
                Vec2(x + 80, y + i + 33),
                Vec2(x + 80, y + i + 33).add(Vec2(35, 35)),
                Color.WHITE,
            )
            CDf = champ.F.get_current_cooldown(game.time)
            fColor = Color.WHITE
            if CDf > 0:
                fColor = Color.RED
            else:
                fColor = Color.WHITE
            game.draw_image(
                champ.F.icon,
                Vec2(x + 126, y + i + 33),
                Vec2(x + 124, y + i + 33).add(Vec2(35, 35)),
                fColor,
            )
            if CDf > 0:
                fx = x + 122
                if CDf > 10 and CDf < 100:
                    fx = x + 120
                elif CDf > 99:
                    fx = x + 118
                game.draw_text(
                    Vec2(fx, y + i + 33).add(Vec2(13, 11)), str(int(CDf)), Color.WHITE
                )
            game.draw_image(
                "spellslot",
                Vec2(x + 124, y + i + 33),
                Vec2(x + 124, y + i + 33).add(Vec2(35, 35)),
                Color.WHITE,
            )
            # game.draw_circle_filled(Vec2(x + 56, y + i + 26), 9.5, 360, Color.DARK_RED)
            cd = champ.R.get_current_cooldown(game.time)
            color = get_color_for_cooldown(cd) if champ.R.level > 0 else Color.GRAY
            if champ.R.level > 0 and cd > 0:
                color = Color.RED
            game.draw_image(
                Icon,
                Vec2(x + 46, y + i + 16),
                Vec2(x + 20, y + i - 8).add(Vec2(45, 45)),
                color,
                360.0,
            )

            game.draw_text(hpbarcoord.add(Vec2(46, 2.7)), hpword, Color.GRAY)

            # game.draw_rect_filled(Vec4(x, y + i + 32, x + width, y + i + 45), Color.GREEN)
            i += 110


        
def vision(game):
    i = 0
    x = ((GetSystemMetrics(0) / 2) * 2) - 1300
    y = GetSystemMetrics(1) / 2 - 500

    xSpell = ((GetSystemMetrics(0) / 2) * 2) - 950
    ySpell = GetSystemMetrics(1) / 2 - 500

    

    for champ in game.champs:
        if champ.is_enemy_to(game.player):
            Rcd=game.time - champ.R.ready_at
            if IsReady(game,champ.R):
                if Rcd<=3:
                    game.draw_image(
                                champ.name.lower() + "_square",
                                Vec2(x + 124, y + i + 33),
                                Vec2(x + 124, y + i + 33).add(Vec2(70, 70)),
                                Color.WHITE,100,)

                    game.draw_image(
                                "hud2",
                                Vec2(x + 124, y + i + 30),
                                Vec2(x + 124, y + i + 33).add(Vec2(73, 73)),
                                Color.WHITE,100,)
                    

                    game.draw_image(
                                champ.R.icon,
                                Vec2(xSpell + 124, ySpell + i + 33),
                                Vec2(xSpell + 124, ySpell + i + 33).add(Vec2(70, 70)),
                                Color.WHITE,100,)

                    game.draw_image(
                                "hud2",
                                Vec2(xSpell + 120, ySpell + i + 30),
                                Vec2(xSpell + 124, ySpell + i + 33).add(Vec2(73, 73)),
                                Color.WHITE,100,)

                    game.draw_image(
                                "ready",
                                Vec2(xSpell -120, ySpell + i + 20),
                                Vec2(xSpell -0, ySpell + i + 25).add(Vec2(110, 110)),
                                Color.WHITE,100,)

                    
                    i+=110 


def winstealer_update(game, ui):
    global show_allies, show_enemies, show_local_champ, show_info
    # if show_hud:
    #     draw_right_hud(game)
    # show_ready_spells(game)
    if show_info:
        vision(game)
    for champ in game.champs:
        if champ.name=="kogmaw" or champ.name=="karthus":
            if not champ.health>0:
                continue
        if (
            # not champ.health>0
            not champ.is_alive
            or not champ.is_visible
            or champ.has_tags(UnitTag.Unit_Champion_Clone)
            or champ.has_tags(UnitTag.Unit_Special)
            or champ.has_tags(UnitTag.Unit_Special_Peaceful)
        ):
            continue

        if champ == game.player and show_local_champ:
            draw_overlay_on_champ2(game, champ)
            # draw_overlay_on_champ(game, champ)
        elif champ != game.player:
            if champ.is_ally_to(game.player) and show_allies:
                draw_overlay_on_champ2(game, champ)
                # draw_overlay_on_champ(game, champ)
            elif champ.is_enemy_to(game.player) and show_enemies:
                draw_overlay_on_champ2(game, champ)
                # draw_overlay_on_champ(game, champ)

        if show_hud_right:
            draw_right_hud(game)
        if show_hud_left:
            draw_left_hud(game)
            # draw_Head(game)