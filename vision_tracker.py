from winstealer import *
import json

winstealer_script_info = {
    "script": "Vision Tracker",
    "author": "SA1",
    "description": "Tracks enemy invisible objects and clones",
}

show_clones, show_wards, show_traps, ward_awareness = None, None, None, None

blue_to_side_brush = {
    "clickPosition": Vec3(2380.09, -71.24, 11004.69),
    "wardPosition": Vec3(2826.47, -71.02, 11221.34),
    "movePosition": Vec3(1774, 52.84, 10856),
}

mid_to_wolves_blue_side = {
    "clickPosition": Vec3(5174.83, 50.57, 7119.81),
    "wardPosition": Vec3(4909.10, 50.65, 7110.90),
    "movePosition": Vec3(5749.25, 51.65, 7282.75),
}

tower_to_wolves_blue_side = {
    "clickPosition": Vec3(5239.21, 50.67, 6944.90),
    "wardPosition": Vec3(4919.83, 50.64, 7023.80),
    "movePosition": Vec3(5574, 51.74, 6458),
}

red_blue_side = {
    "clickPosition": Vec3(8463.64, 50.60, 4658.71),
    "wardPosition": Vec3(8512.29, 51.30, 4745.90),
    "movePosition": Vec3(8022, 53.72, 4258),
}

dragon_got_bush = {
    "clickPosition": Vec3(10301.03, 49.03, 3333.20),
    "wardPosition": Vec3(10322.94, 49.03, 3244.38),
    "movePosition": Vec3(10072, -71.24, 3908),
}
dragon_2_bush={
    "clickPosition": Vec3(8689.00, 54.86, 4526.00),
    "wardPosition": Vec3(8680.00, 52.86, 4516.00),
    "movePosition": Vec3(9310.00, -71.24, 4516.0),
}

baron_top_bush = {
    "clickPosition": Vec3(4633.83, 50.51, 11354.40),
    "wardPosition": Vec3(4524.69, 53.25, 11515.21),
    "movePosition": Vec3(4824, -71.24, 10906),
}

red_red_side = {
    "clickPosition": Vec3(6360.12, 52.61, 10362.71),
    "wardPosition": Vec3(6269.35, 53.72, 10306.69),
    "movePosition": Vec3(6824, 56, 10656),
}

tower_to_wolves = {
    "clickPosition": Vec3(9586.57, 59.62, 8020.29),
    "wardPosition": Vec3(9871.77, 51.47, 8014.44),
    "movePosition": Vec3(9122, 53.74, 8356),
}

mid_to_wolves = {
    "clickPosition": Vec3(9647.62, 51.31, 7889.96),
    "wardPosition": Vec3(9874.42, 51.50, 7969.29),
    "movePosition": Vec3(9122, 52.60, 7606),
}

red_bot_side_bush = {
    "clickPosition": Vec3(12427.00, -35.46, 3984.26),
    "wardPosition": Vec3(11975.34, 66.37, 3927.68),
    "movePosition": Vec3(13022, 51.37, 3808),
}

traps = {
    # Name -> (radius, show_radius_circle, show_radius_circle_minimap, icon)
    "caitlyntrap": [50, True, False, "caitlyn_yordlesnaptrap"],
    "jhintrap": [140, True, False, "jhin_e"],
    "jinxmine": [50, True, False, "jinx_e"],
    "maokaisproutling": [50, False, False, "maokai_e"],
    "nidaleespear": [50, True, False, "nidalee_w1"],
    "shacobox": [300, True, False, "jester_deathward"],
    "teemomushroom": [75, True, True, "teemo_r"],
}

wards = {
    "bluetrinket": [900, True, True, "bluetrinket"],
    "jammerdevice": [900, True, True, "pinkward"],
    "perkszombieward": [900, True, True, "bluetrinket"],
    "sightward": [900, True, True, "sightward"],
    "visionward": [900, True, True, "sightward"],
    "yellowtrinket": [900, True, True, "yellowtrinket"],
    "yellowtrinketupgrade": [900, True, True, "yellowtrinket"],
    "ward": [900, True, True, "sightward"],
}

clones = {
    "shaco": [0, False, False, "shaco_square"],
    "leblanc": [0, False, False, "leblanc_square"],
    "monkeyking": [0, False, False, "monkeyking_square"],
    "neeko": [0, False, False, "neeko_square"],
    "fiddlesticks": [0, False, False, "fiddlesticks_square"],
}


def winstealer_load_cfg(cfg):
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards

    ward_awareness = cfg.get_bool("ward_awareness", True)

    show_clones = cfg.get_bool("show_clones", True)
    show_wards = cfg.get_bool("show_wards", True)
    show_traps = cfg.get_bool("show_traps", True)

    traps = json.loads(cfg.get_str("traps", json.dumps(traps)))
    wards = json.loads(cfg.get_str("wards", json.dumps(wards)))


def winstealer_save_cfg(cfg):
    global show_clones, show_wards, show_traps, ward_awareness, traps, wards

    cfg.set_bool("ward_awareness", ward_awareness)

    cfg.set_bool("show_clones", show_clones)
    cfg.set_bool("show_wards", show_wards)
    cfg.set_bool("show_traps", show_traps)

    cfg.set_str("traps", json.dumps(traps))
    cfg.set_str("wards", json.dumps(wards))


def winstealer_draw_settings(game, ui):
    global traps, wards
    global show_clones, show_wards, show_traps, ward_awareness

    ward_awareness = ui.checkbox("Ward awareness", ward_awareness)
    show_clones = ui.checkbox("Show clones", show_clones)
    show_wards = ui.checkbox("Show wards", show_wards)
    show_traps = ui.checkbox("Show clones", show_traps)

    ui.text("Traps")
    for x in traps.keys():
        if ui.treenode(x):
            traps[x][1] = ui.checkbox("Show range circles", traps[x][1])
            traps[x][2] = ui.checkbox("Show on minimap", traps[x][2])

            ui.treepop()

    ui.text("Wards")
    for x in wards.keys():
        if ui.treenode(x):
            wards[x][1] = ui.checkbox("Show range circles", wards[x][1])
            wards[x][2] = ui.checkbox("Show on minimap", wards[x][2])

            ui.treepop()


def draw(game, obj, radius, show_circle_world, show_circle_map, icon):

    sp = game.world_to_screen(obj.pos)

    if game.is_point_on_screen(sp):
        duration = obj.duration + obj.last_visible_at - game.time
        # if duration > 0:
        #     game.draw_text(sp, f"{duration:.0f}", Color.WHITE)
        game.draw_image(icon, sp, sp.add(Vec2(30, 30)), Color.WHITE)

        if show_circle_world:
            game.draw_circle_world(obj.pos, radius, 100, 3, Color.YELLOW)

    # if show_circle_map:
    #     game.draw_circle(
    #         game.world_to_minimap(obj.pos),
    #         game.distance_to_minimap(radius),
    #         100,
    #         2,
    #         Color.YELLOW,
    #     )


def drawAwareness(game, wardSpot):
    spotDist = wardSpot["movePosition"].distance(game.player.pos)
    if (spotDist < 400) and (spotDist > 70):
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.YELLOW)
    elif spotDist < 70:
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.GREEN)
    clickDist = game.get_cursor().distance(
        game.world_to_screen(wardSpot["clickPosition"])
    )
    if clickDist > 10:
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, Color.YELLOW)
    else:
        # game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.GREEN)
        game.draw_circle_world(wardSpot["clickPosition"], 30, 100, 1, Color.GREEN)
        game.draw_circle_world(wardSpot["movePosition"], 100, 100, 1, Color.WHITE)


def wardAwareness(game):
    global tower_to_wolves, tower_to_wolves_blue_side
    global dragon_got_bush
    global mid_to_wolves, mid_to_wolves_blue_side
    global blue_to_side_brush
    global red_blue_side, red_bot_side_bush, red_red_side
    global baron_top_bush
    if game.map.type == MapType.SummonersRift:
        drawAwareness(game, tower_to_wolves)
        drawAwareness(game, tower_to_wolves_blue_side)
        drawAwareness(game, dragon_got_bush)
        drawAwareness(game, mid_to_wolves)
        drawAwareness(game, mid_to_wolves_blue_side)
        drawAwareness(game, blue_to_side_brush)
        drawAwareness(game, red_blue_side)
        drawAwareness(game, red_bot_side_bush)
        drawAwareness(game, red_red_side)
        drawAwareness(game, baron_top_bush)
        drawAwareness(game, dragon_2_bush)

def winstealer_update(game, ui):

    global show_clones, show_wards, show_traps
    global traps, wards, clones
    
    if ward_awareness:
        wardAwareness(game)

    for obj in game.others:
        if obj.is_ally_to(game.player) or not obj.is_alive:
            continue

        if show_wards and obj.has_tags(UnitTag.Unit_Ward) and obj.name in wards:
            draw(game, obj, *(wards[obj.name]))
        elif (
            show_traps and obj.has_tags(UnitTag.Unit_Special_Trap) and obj.name in traps
        ):
            draw(game, obj, *(traps[obj.name]))

    if show_clones:
        for champ in game.champs:
            if champ.is_ally_to(game.player) or not champ.is_alive:
                continue
            if champ.name in clones and champ.R.name == champ.D.name:
                draw(game, champ, *(clones[champ.name]))
                game.draw_text(game.world_to_screen(champ.pos).add(Vec2(-5,35)),"Clone",Color.GREEN)