import typing
from typing import Any
from worlds.generic.Rules import add_rule
from . import StateLogic, location_id_to_name, tattlesanity_region, Goal, PitItems, limit_pit, \
    pit_exclusive_tattle_stars_required
from .Options import PalaceSkip

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def set_rules(world: "TTYDWorld"):
    for location, rule in get_rules_dict(world).items():
        if location not in world.disabled_locations:
            add_rule(world.multiworld.get_location(location, world.player), rule)

def set_tattle_rules(world: "TTYDWorld"):
    for location in tattlesanity_region:
        if location.name in world.disabled_locations:
            continue
        add_rule(world.get_location(location.name), lambda state: state.has("Goombella", world.player))
    for location_name, locations in get_tattle_rules_dict().items():
        if location_name in world.disabled_locations:
            continue
        if len(locations) == 0:
            # Require access to Shadow Queen
            if world.options.palace_skip == PalaceSkip.option_true and world.options.goal != Goal.option_shadow_queen:
                extra_condition = lambda state: state.has("stars", world.player, world.options.palace_stars)
            elif world.options.goal == Goal.option_shadow_queen:
                extra_condition = lambda state: state.can_reach("Shadow Queen", "Location", world.player)
            else:
                extra_condition = lambda state: state.can_reach("Palace of Shadow Final Staircase: Ultra Shroom", "Location", world.player)
        else:
            # Require access to any of the listed locations
            if world.options.pit_items != PitItems.option_all and location_name not in pit_exclusive_tattle_stars_required:
                locations = [loc for loc in locations if loc not in limit_pit]
                if len(locations) == 0:
                    continue
            valid_locations = [
                location_id_to_name[loc] for loc in locations
                if location_id_to_name[loc] not in world.disabled_locations
            ]
            if len(valid_locations) == 0:
                continue
            extra_condition = lambda state, locs=valid_locations: any(
                state.can_reach(loc, "Location", world.player) for loc in locs
            )

        add_rule(world.get_location(location_name), extra_condition)

def get_rules_dict(world: "TTYDWorld") -> dict[str, Any]:
    return {
        "Boggly Woods Plane Panel Room: Shine Sprite":
            lambda state: state.has("Koops", world.player) or StateLogic.ultra_boots(state, world.player),
        "Boggly Woods Plane Panel Room: Quake Hammer":
            lambda state: state.has("Plane Curse", world.player),
        "Boggly Woods Outside Flurrie's House: Star Piece 1":
            lambda state: state.has("Plane Curse", world.player),
        "Boggly Woods Shadow Sirens Room: Necklace":
            lambda state: state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player),
        "Boggly Woods Outside Flurrie's House: Star Piece 2":
            lambda state: state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player),
        "Boggly Woods Outside Flurrie's House: Volt Shroom":
            lambda state: state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player),
        "Boggly Woods Flurrie's House: Flurrie":
            lambda state: state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player)
                          and state.has("Necklace", world.player),
        "Boggly Woods Flurrie's House Backroom: Super Appeal P":
            lambda state: state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player)
                          and state.has("Necklace", world.player),
        "Boggly Woods Flurrie's House Backroom: Star Piece":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player)
                           and state.has("Necklace", world.player) and StateLogic.super_boots(state, world.player)),
        "Boggly Woods Outside Great Tree: FP Plus":
            lambda state: StateLogic.super_boots(state, world.player),
        "Great Tree Entrance: Mystic Egg":
            lambda state: state.can_reach("Great Tree Entrance: Emerald Star", "Location", world.player),
        "Great Tree Red Key Room: Mushroom":
            lambda state: state.can_reach("Great Tree Entrance: Emerald Star", "Location", world.player),
        "Keelhaul Key Grotto Entrance: Wedding Ring":
            lambda state: state.has("Yoshi", world.player),
        "Creepy Steeple Main Hall: Steeple Key":
            lambda state: state.has("Koops", world.player) or state.has("Yoshi", world.player),
        "Creepy Steeple Main Hall: Lucky Start":
            lambda state: StateLogic.super_hammer(state, world.player),
        "Creepy Steeple Upper Room: Ruby Star":
            lambda state: state.has("Steeple Key", world.player) and state.has("The Letter \"p\"", world.player),
        "Creepy Steeple Underground Tube Passage: Shine Sprite":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Boo Chest Room: Star Piece":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Parrot Room: Mr. Softener":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Parrot Room: Power Plus":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Parrot Room: Star Piece":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Parrot Room: Steeple Key 2":
            lambda state: state.has("Vivian", world.player),
        "Creepy Steeple Parrot Room: The Letter \"p\"":
            lambda state: state.has("Vivian", world.player),
        "Excess Express Middle Passenger Car: Blanket":
            lambda state: state.has("Autograph", world.player) and state.has("Vivian", world.player)
                          and state.has("Ragged Diary", world.player),
        "Excess Express Back Passenger Car: Shine Sprite":
            lambda state: state.has("Autograph", world.player),
        "Excess Express Back Passenger Car: Mushroom":
            lambda state: state.has("Autograph", world.player) and state.has("Blanket", world.player)
                          and state.has("Ragged Diary", world.player) and state.has("Vivian", world.player),
        "Excess Express Storage Car: Ragged Diary":
            lambda state: state.has("Paper Curse", world.player) or StateLogic.ultra_boots(state, world.player),
        "Excess Express Front Passenger Car: Vital Paper":
            lambda state: (state.has("Autograph", world.player) and state.has("Vivian", world.player)
                           and state.has("Ragged Diary", world.player) and state.has("Blanket", world.player)),
        "Excess Express Middle Passenger Car: Briefcase":
            lambda state: (state.has("Autograph", world.player) and state.has("Vivian", world.player)
                           and state.has("Ragged Diary", world.player) and state.has("Blanket", world.player)
                           and state.has("Vital Paper", world.player)),
        "Excess Express Middle Passenger Car: Gold Ring":
            lambda state: (state.has("Autograph", world.player) and state.has("Vivian", world.player)
                           and state.has("Ragged Diary", world.player) and state.has("Blanket", world.player)
                           and state.has("Vital Paper", world.player)),
        "Excess Express Middle Passenger Car: Shell Earrings":
            lambda state: (state.has("Autograph", world.player) and state.has("Vivian", world.player)
                           and state.has("Ragged Diary", world.player) and state.has("Blanket", world.player)
                           and state.has("Vital Paper", world.player)),
        "Excess Express Dining Car: Star Piece 1":
            lambda state: state.has("Galley Pot", world.player),
        "Excess Express Dining Car: Star Piece 2":
            lambda state: state.has("Shell Earrings", world.player),
        "Excess Express Front Passenger Car: 30 Coins":
            lambda state: state.has("Gold Ring", world.player),
        "Excess Express Locomotive: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Excess Express Middle Passenger Car: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Fahr Outpost Entrance: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Fahr Outpost Town: Star Piece 1":
            lambda state: StateLogic.super_boots(state, world.player),
        "Glitzville Lobby: Storage Key 2":
            lambda state: state.has("Flurrie", world.player),
        "Glitzville Lobby: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Glitzville Storage Back Room: Star Piece":
            lambda state: (state.has("Flurrie", world.player) and state.has("Storage Key 1", world.player)
                           and state.has("Storage Key 2", world.player) and state.has("Yoshi", world.player)
                           and StateLogic.super_hammer(state, world.player)),
        "Glitzville Storage Room: Charge P":
            lambda state: state.has("Flurrie", world.player) and state.has("Storage Key 1", world.player),
        "Glitzville Storage Room: Shine Sprite":
            lambda state: state.has("Flurrie", world.player) and state.has("Storage Key 1", world.player),
        "Glitzville Storage Room: HP Plus P":
            lambda state: state.has("Flurrie", world.player) and state.has("Storage Key 1", world.player)
                          and state.has("Yoshi", world.player),
        "Glitzville Storage Room: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player) and state.has("Storage Key 1", world.player),
        "Glitzville Main Square: Power Plus P":
            lambda state: StateLogic.super_boots(state, world.player),
        "Glitzville Main Square: Star Piece 4":
            lambda state: StateLogic.super_boots(state, world.player),
        "Glitzville Main Square: Star Piece 5":
            lambda state: StateLogic.super_boots(state, world.player) and (
                        state.has("Koops", world.player) or StateLogic.tube_curse(state, world.player)),
        "Glitzville Minor-League Room: Yoshi":
            lambda state: StateLogic.super_boots(state, world.player) and state.has("Plane Curse", world.player),
        "Glitzville Minor-League Room: Dubious Paper":
            lambda state: StateLogic.super_hammer(state, world.player) and state.has("Yoshi", world.player),
        "Glitzville Major-League Room: Champ's Belt":
            lambda state: state.has("Flurrie", world.player) and state.has("Yoshi", world.player),
        "Glitzville Major-League Room: Ice Storm":
            lambda state: state.has("Yoshi", world.player),
        "Glitzville Arena: Gold Star":
            lambda state: state.has("Yoshi", world.player) and state.has("Flurrie", world.player)
                          and StateLogic.super_hammer(state, world.player),
        "Great Tree Red/Blue Cages: Star Piece":
            lambda state: (state.has("Blue Key", world.player) or state.has("Paper Curse", world.player)) and StateLogic.super_boots(state, world.player),
        "Great Tree Entrance: Puni Orb":
            lambda state: state.has("Red Key", world.player),
        "Great Tree Bubble Room: Shine Sprite":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree Bubble Room: Thunder Rage":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree Zigzag Room: Coin":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree Zigzag Room: Damage Dodge P":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree Zigzag Room: Star Piece":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree Shop: Honey Syrup":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Shop: HP Drain":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Shop: Ice Storm":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Shop: Mini Mr. Mini":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Shop: Mushroom":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Shop: Mystery":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Blue Key Room: Blue Key":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and state.has("Flurrie", world.player),
        "Great Tree Super Boots Room: Super Boots":
            lambda state: StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player),
        "Great Tree 100-Puni Pedestal: Coin":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and StateLogic.super_boots(state, world.player)),
        "Great Tree 100-Puni Pedestal: Star Piece":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and StateLogic.super_boots(state, world.player)),
        "Great Tree Fake Pedestal: Star Piece":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)),
        "Great Tree Entrance: Emerald Star":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Elevator Pedestal: Mushroom":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Escape Ambush Room: Star Piece":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Pool Room: Dizzy Dial":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Pool Room: Shine Sprite":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Pool Room: Shrink Stomp":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and state.has("Koops", world.player) and StateLogic.super_boots(state, world.player)),
        "Great Tree Lower Duplex: Coin":
            lambda state: (state.has("Red Key", world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Blue Key", world.player)
                           and StateLogic.super_boots(state, world.player)),
        "Great Tree Middle Duplex: Shine Sprite":
            lambda state: (StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                           and state.has("Flurrie", world.player) and state.has("Plane Curse", world.player)),
        "Great Tree Blue Key Room: Charge":
            lambda state: (StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                           and StateLogic.super_boots(state, world.player)
                           and (state.has("Yoshi", world.player) or state.has("Koops", world.player))),
        "Great Tree Blue Key Room: Shine Sprite":
            lambda state: (StateLogic.key_any(state, world.player) and state.has("Puni Orb", world.player)
                          and StateLogic.super_boots(state, world.player)),
        "Great Tree 10-Puni Pedestal: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Hooktail's Castle Drawbridge: HP Plus":
            lambda state: state.has("Yoshi", world.player) or state.has("Koops", world.player),
        "Hooktail's Castle Entrance: Power Bounce":
            lambda state: state.has("Yoshi", world.player) or state.has("Plane Curse", world.player),
        "Hooktail's Castle Red Bones Room: Castle Key":
            lambda state: (state.has("Yoshi", world.player) or state.has("Plane Curse", world.player)) and state.has("Paper Curse", world.player),
        "Hooktail's Castle Red Bones Room: Star Piece":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Paper Curse", world.player) and StateLogic.super_boots(state, world.player)),
        "Hooktail's Castle Stair Switch Room: Castle Key":
            lambda state: (state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player),
        "Hooktail's Castle Stair Switch Room: Shine Sprite":
            lambda state: (state.has("Yoshi", world.player) or state.has("Plane Curse", world.player)),
        "Hooktail's Castle Stair Switch Room: Star Piece 1":
            lambda state: (state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player),
        "Hooktail's Castle Stair Switch Room: Star Piece 2":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Stair Central Staircase: Castle Key":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Koops", world.player)
                           and state.has("Castle Key", world.player, 3) and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Stair Central Staircase: Last Stand P":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Koops", world.player)
                           and state.has("Castle Key", world.player, 3) and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Stair Central Staircase: Shine Sprite":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Koops", world.player)
                           and state.has("Castle Key", world.player, 3) and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Stair Central Staircase: Star Piece":
            lambda state: (state.has("Yoshi", world.player) or state.has("Plane Curse", world.player)) and state.has("Koops", world.player),
        "Hooktail's Castle Prison Entrance: Paper Curse":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 1)
                           and state.has("Black Key (Paper Curse)", world.player)),
        "Hooktail's Castle Prison Entrance: Attack FX R":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 1)
                           and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Spikes Room: Black Key (Paper Curse)":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 1)
                           and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Life Shroom Room: Life Shroom":
            lambda state: ((state.has("Yoshi", world.player)
                           or (state.has("Plane Curse", world.player) and state.has("Paper Curse", world.player)))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Plane Rafters Room: Star Piece":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Koops", world.player)
                           and state.has("Castle Key", world.player, 3) and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Hooktail's Room: Diamond Star":
            lambda state: (state.has("Plane Curse", world.player) and state.has("Koops", world.player)
                           and state.has("Castle Key", world.player, 4) and state.has("Paper Curse", world.player)),
        "Hooktail's Castle Storeroom: Castle Key":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Storeroom: Honey Syrup":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Storeroom: Mushroom":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Storeroom: Shine Sprite":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 2)),
        "Hooktail's Castle Up Arrow Room: Up Arrow":
            lambda state: ((state.has("Yoshi", world.player) or state.has("Plane Curse", world.player))
                           and state.has("Koops", world.player) and state.has("Castle Key", world.player, 1)
                           and state.has("Bobbery", world.player)),
        "Keelhaul Key Landing Site: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Keelhaul Key Jungle Winding Climb: Coin 2":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Winding Climb: Thunder Rage":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Bridge: Coconut 1":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Bridge: Coconut 2":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Bridge: Inn Coupon":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Bridge: Shine Sprite":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Grotto Entrance: Spite Pouch":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Grotto Entrance: Star Piece":
            lambda state: state.has("Yoshi", world.player),
        "Keelhaul Key Jungle Bridge: Ice Power":
            lambda state: state.has("Yoshi", world.player) and state.has("Paper Curse", world.player),
        "Keelhaul Key Jungle Winding Climb: Jammin' Jelly":
            lambda state: state.has("Yoshi", world.player) and (StateLogic.ultra_boots(state, world.player)
                          or StateLogic.super_hammer(state, world.player) or state.has("Bobbery", world.player)),
        "Keelhaul Key Jungle Winding Climb: Shine Sprite":
            lambda state: state.has("Yoshi", world.player) or StateLogic.ultra_boots(state, world.player),
        "Keelhaul Key Grotto Entrance: Bobbery":
            lambda state: state.has("Yoshi", world.player) and state.has("Chuckola Cola", world.player),
        "Keelhaul Key Grotto Entrance: Skull Gem":
            lambda state: state.has("Yoshi", world.player) and state.has("Coconut", world.player),
        "Keelhaul Key Town: Chuckola Cola":
            lambda state: state.has("Yoshi", world.player) and state.has("Coconut", world.player),
        "Palace of Shadow Dark Bones Room: Palace Key":
            lambda state: StateLogic.tube_curse(state, world.player),
        "Palace of Shadow Second Bullet Bill Hallway: Ultra Shroom":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player),
        "Palace of Shadow Large Open Room: Coin":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player),
        "Palace of Shadow Large Open Room: Jammin' Jelly":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player),
        "Palace of Shadow Large Open Room: P-Up D-Down P":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player),
        "Palace of Shadow Gloomtail Room: Star Key":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player),
        "Palace of Shadow Gloomtail Room: Jammin' Jelly":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                          and state.has("Bobbery", world.player),
        "Palace of Shadow Gloomtail Room: Ultra Shroom":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                          and state.has("Bobbery", world.player),
        "Riddle Tower Floor 1 NW: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)
                           and StateLogic.ultra_hammer(state, world.player)),
        "Riddle Tower Floor 1 NE: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)),
        "Riddle Tower Floor 1 SW: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)),
        "Riddle Tower Floor 1 SE: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)
                           and state.has("Flurrie", world.player)),
        "Riddle Tower Floor 2 NW: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)
                           and StateLogic.ultra_hammer(state, world.player)),
        "Riddle Tower Floor 2 NE: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)),
        "Riddle Tower Floor 2 SW: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)),
        "Riddle Tower Floor 2 SE: Palace Key (Riddle Tower)":
            lambda state: (StateLogic.tube_curse(state, world.player) and state.has("Palace Key", world.player)
                           and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player)
                           and state.has("Vivian", world.player)),
        "Petal Meadows Field: Happy Heart":
            lambda state: state.has("Koops", world.player) or state.has("Yoshi", world.player)
                          or StateLogic.ultra_boots(state, world.player),
        "Petalburg Eastside: Mega Rush P":
            lambda state: state.has("Paper Curse", world.player),
        "Petalburg Eastside: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Petalburg Westside: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Pirate's Grotto Staircase: Coin":
            lambda state: state.has("Yoshi", world.player),
        "Pirate's Grotto Staircase: Shine Sprite":
            lambda state: state.has("Yoshi", world.player),
        "Pirate's Grotto Storeroom: Grotto Key":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player),
        "Pirate's Grotto Storeroom: Shine Sprite":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player),
        "Pirate's Grotto Storeroom: Star Piece":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player),
        "Pirate's Grotto Gate Handle Room: Gate Handle":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player),
        "Pirate's Grotto Staircase: Defend Plus P":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player) and state.has("Boat Curse", world.player),
        "Pirate's Grotto Cortez' Hoard: Sapphire Star":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and state.has("Boat Curse", world.player) and state.has("Gate Handle", world.player)
                           and state.has("Plane Curse", world.player),
        "Pirate's Grotto Sluice Gate: Star Piece":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                          and StateLogic.super_boots(state, world.player),
        "Pirate's Grotto Spike Wall Room: Shine Sprite":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and state.has("Koops", world.player),
        "Pirate's Grotto Parabuzzy Room: Star Piece":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and StateLogic.super_boots(state, world.player),
        "Pirate's Grotto Chest Boat: Black Key (Boat Curse)":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and StateLogic.tube_curse(state, world.player),
        "Pirate's Grotto Chest Boat: P-Down D-Up":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and StateLogic.tube_curse(state, world.player),
        "Pirate's Grotto Barrel Room: 10 Coins":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and StateLogic.tube_curse(state, world.player),
        "Pirate's Grotto Barrel Room: Shine Sprite":
            lambda state: state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                          and StateLogic.tube_curse(state, world.player),
        "Pirate's Grotto Chest Boat: Boat Curse":
            lambda state: (state.has("Yoshi", world.player) and state.has("Grotto Key", world.player)
                           and StateLogic.tube_curse(state, world.player)
                           and state.has("Black Key (Boat Curse)", world.player)),
        "Poshley Heights Station: Goldbob Guide":
            lambda state: StateLogic.fahr_outpost(state, world.player) and state.has("Bobbery", world.player),
        "Poshley Heights Station: Star Piece 3":
            lambda state: StateLogic.super_boots(state, world.player),
        "Poshley Heights Sanctum Exterior: Shine Sprite":
            lambda state: StateLogic.ultra_boots(state, world.player),
        "Poshley Heights Station: HP Drain P":
            lambda state: state.has("Paper Curse", world.player),
        "Palace of Shadow Far Hallway 1: Thunder Rage":
            lambda state: StateLogic.ultra_boots(state, world.player)
                          or (state.has("Yoshi", world.player) and state.has("Koops", world.player)),
        "Palace of Shadow Far Backroom 1: Repel Cape":
            lambda state: state.has("Yoshi", world.player)
                          and (state.has("Bobbery", world.player) or state.has("Koops", world.player)),
        "Palace of Shadow Far Backroom 2: Palace Key":
            lambda state: state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                          and StateLogic.ultra_boots(state, world.player),
        "Palace of Shadow Far Backroom 1: Life Shroom":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)),
        "Palace of Shadow Far Backroom 2: Life Shroom":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player)),
        "Palace of Shadow Far Backroom 3: Coin":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player)),
        "Palace of Shadow Far Backroom 3: Point Swap":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player)),
        "Palace of Shadow Far Backroom 3: Palace Key":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player) and state.has("Plane Curse", world.player)),
        "Palace of Shadow Far Hallway 4: Life Shroom":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player) and state.has("Plane Curse", world.player)),
        "Palace of Shadow Far Hallway 4: Shooting Star":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 2)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player) and state.has("Plane Curse", world.player)),
        "Palace of Shadow Final Staircase: Jammin' Jelly":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 3)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player) and state.has("Plane Curse", world.player)),
        "Palace of Shadow Final Staircase: Ultra Shroom":
            lambda state: (state.has("Yoshi", world.player) and state.has("Bobbery", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Palace Key", world.player, 3)
                           and state.has("Paper Curse", world.player) and state.has("Flurrie", world.player)
                           and StateLogic.ultra_hammer(state, world.player) and state.has("Plane Curse", world.player)),
        "Riverside Station Tube Mode Maze: Dried Shroom":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player)
                          and StateLogic.tube_curse(state, world.player) and state.has("Flurrie", world.player),
        "Riverside Station Tube Mode Maze: P-Up D-Down":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player)
                          and StateLogic.tube_curse(state, world.player) and state.has("Flurrie", world.player),
        "Riverside Station Back Exterior: HP Plus":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2",world.player)
                          and StateLogic.tube_curse(state, world.player),
        "Riverside Station Back Exterior: Shine Sprite":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player),
        "Riverside Station Back Exterior: Thunder Rage":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player),
        "Riverside Station Ultra Boots Room: Ultra Boots":
            lambda state: state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player)
                          and StateLogic.tube_curse(state, world.player) and state.has("Flurrie", world.player),
        "Riverside Station Goomba Room: Shine Sprite":
            lambda state: (state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player)
                           and StateLogic.tube_curse(state, world.player)
                           and (StateLogic.ultra_boots(state, world.player) or state.has("Koops", world.player))
                           and state.has("Flurrie", world.player)),
        "Riverside Station Ultra Boots Room: Elevator Key (Riverside)":
            lambda state: (state.has("Station Key 1", world.player) and state.has("Station Key 2", world.player)
                           and StateLogic.tube_curse(state, world.player) and StateLogic.ultra_boots(state, world.player)
                           and state.has("Flurrie", world.player) and state.has("Yoshi", world.player)),
        "Riverside Station Clockwork Room: Star Piece":
            lambda state: state.has("Station Key 1", world.player) and StateLogic.tube_curse(state, world.player),
        "Riverside Station Clockwork Room: Station Key 2":
            lambda state: (state.has("Station Key 1", world.player) and StateLogic.tube_curse(state, world.player)
                           and (state.has("Yoshi", world.player) or state.has("Koops", world.player))),
        "Riverside Station Entrance: Close Call P":
            lambda state: state.has("Station Key 1", world.player) and StateLogic.ultra_boots(state, world.player),
        "Poshley Heights Sanctum Altar: Garnet Star":
            lambda state: (StateLogic.riverside(state, world.player) and state.has("Station Key 1", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Elevator Key (Riverside)", world.player)
                           and state.has("Plane Curse", world.player) and StateLogic.super_hammer(state, world.player)),
        "Poshley Heights Sanctum Altar: L Emblem":
            lambda state: (StateLogic.riverside(state, world.player) and state.has("Station Key 1", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Elevator Key (Riverside)", world.player)
                           and state.has("Plane Curse", world.player) and StateLogic.super_hammer(state, world.player)),
        "Poshley Heights Sanctum Altar: Shine Sprite":
            lambda state: (StateLogic.riverside(state, world.player) and state.has("Station Key 1", world.player)
                           and StateLogic.ultra_boots(state, world.player) and state.has("Elevator Key (Riverside)", world.player)
                           and state.has("Plane Curse", world.player) and StateLogic.super_hammer(state, world.player)),
        "Rogueport Sewers Boggly Woods Pipe: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player) and (state.has("Paper Curse", world.player) or StateLogic.super_hammer(state, world.player)),
        "Rogueport Sewers Boggly Woods Pipe: Damage Dodge":
            lambda state: state.has("Paper Curse", world.player),
        "Rogueport Sewers Town: Shine Sprite":
            lambda state: StateLogic.ultra_boots(state, world.player),
        "Rogueport Sewers Town: Star Piece 3":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Sewers West Entrance: Flower Saver P":
            lambda state: StateLogic.ultra_boots(state, world.player),
        "Rogueport Sewers West Entrance: Shine Sprite":
            lambda state: StateLogic.ultra_boots(state, world.player) or state.has("Yoshi", world.player),
        "Rogueport Sewers West Entrance: Star Piece 2":
            lambda state: StateLogic.ultra_boots(state, world.player) or state.has("Yoshi", world.player),
        "Rogueport Sewers Spania Room: Defend Plus":
            lambda state: state.has("Flurrie", world.player) and state.has("Boat Curse", world.player)
                          and (state.has("Yoshi", world.player) or (state.has("Koops", world.player) and StateLogic.ultra_boots(state, world.player))),
        "Rogueport Sewers Spania Room: Shine Sprite 1":
            lambda state: state.has("Flurrie", world.player) and state.has("Boat Curse", world.player),
        "Rogueport Sewers Spania Room: Shine Sprite 2":
            lambda state: state.has("Flurrie", world.player) and state.has("Boat Curse", world.player)
                          and StateLogic.ultra_boots(state, world.player),
        "Rogueport Sewers Spania Room: Shine Sprite 3":
            lambda state: state.has("Flurrie", world.player) and state.has("Boat Curse", world.player),
        "Rogueport Blimp Room: Star Piece 1":
            lambda state: state.has("Blimp Ticket", world.player),
        "Rogueport Westside: Star Piece 4":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Blimp Room: Star Piece 2":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Sewers Thousand Year Door: Shine Sprite":
            lambda state: ((StateLogic.ttyd(state, world.player) and state.has("Paper Curse", world.player)
                            and state.has("Plane Curse", world.player)) or
                           (StateLogic.pit(state, world.player) and state.has("Paper Curse", world.player))),
        "Rogueport Sewers Thousand Year Door: Star Piece":
            lambda state: StateLogic.ttyd(state, world.player) and StateLogic.super_boots(state, world.player),
        "Twilight Town Leftside: Vivian":
            lambda state: state.has("Superbombomb", world.player),
        "Twilight Town Rightside: Boo's Sheet":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Defend Plus":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Jammin' Jelly":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Life Shroom 1":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Life Shroom 2":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Maple Syrup":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Spite Pouch":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Stop Watch":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Super Shroom":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Thunder Rage":
            lambda state: state.has("Shop Key", world.player),
        "Twilight Town Rightside: Tube Curse":
            lambda state: state.has("Shop Key", world.player) and state.has("Black Key (Tube Curse)", world.player),
        "Twilight Trail Fallen Tree: Shop Key":
            lambda state: state.has("Koops", world.player) or StateLogic.tube_curse(state, world.player),
        "Twilight Trail Fallen Tree: Star Piece 2":
            lambda state: state.has("Flurrie", world.player),
        "Twilight Trail Dark Woods First Room: 10 Coins":
            lambda state: state.has("Flurrie", world.player),
        "Twilight Trail Dark Woods First Room: Earth Quake":
            lambda state: state.has("Flurrie", world.player),
        "Twilight Trail Dark Woods Second Room: Hammer Throw":
            lambda state: state.has("Flurrie", world.player),
        "Twilight Trail Dark Woods Third Room: 10 Coins":
            lambda state: state.has("Flurrie", world.player),
        "Twilight Trail Dark Woods Third Room: Shine Sprite":
            lambda state: state.has("Flurrie", world.player) and StateLogic.super_boots(state, world.player),
        "Twilight Trail Steeple Exterior: Coin":
            lambda state: state.has("Flurrie", world.player) and StateLogic.super_boots(state, world.player),
        "Twilight Trail Steeple Exterior: Star Piece":
            lambda state: state.has("Flurrie", world.player) and StateLogic.super_boots(state, world.player),
        "X-Naut Fortress Crane Room: Coin 1":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Coin 2":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Coin 3":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Coin 4":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Coin 5":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Coin 6":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Feeling Fine":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Feeling Fine P":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Crane Room: Star Piece":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Cog", world.player),
        "X-Naut Fortress Ceiling Grate Room: Star Piece":
            lambda state: state.has("Elevator Key 1", world.player) and StateLogic.ultra_boots(state, world.player),
        "X-Naut Fortress Teleporter Room: Cog":
            lambda state: (state.has("Elevator Key 1", world.player) and StateLogic.ultra_boots(state, world.player)
                           and state.has("Paper Curse", world.player)),
        "X-Naut Fortress Quiz Room: Elevator Key 2":
            lambda state: state.has("Elevator Key 1", world.player),
        "X-Naut Fortress Card Key Room A: Card Key 1":
            lambda state: state.has("Elevator Key 1", world.player),
        "X-Naut Fortress Card Key Room A: Sleepy Sheep":
            lambda state: state.has("Elevator Key 1", world.player),
        "X-Naut Fortress Office: Card Key 2":
            lambda state: state.has("Elevator Key 1", world.player),
        "X-Naut Fortress Card Key Room B: Card Key 3":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Elevator Key 2", world.player),
        "X-Naut Fortress Card Key Room B: HP Drain":
            lambda state: state.has("Elevator Key 1", world.player) and state.has("Elevator Key 2", world.player),
        "X-Naut Fortress Factory: Ultra Shroom":
            lambda state: (state.has("Elevator Key 1", world.player) and state.has("Elevator Key 2", world.player)
                           and state.has("Card Key 1", world.player) and state.has("Card Key 2", world.player)
                           and state.has("Card Key 3", world.player) and state.has("Paper Curse", world.player)
                           and state.has("Vivian", world.player)),
        "X-Naut Fortress Factory: Card Key 4":
            lambda state: (state.has("Elevator Key 1", world.player) and state.has("Elevator Key 2", world.player)
                           and state.has("Card Key 1", world.player) and state.has("Card Key 2", world.player)
                           and state.has("Card Key 3", world.player) and state.has("Paper Curse", world.player)
                           and state.has("Vivian", world.player) and state.has("Plane Curse", world.player)),
        "X-Naut Fortress Boss Room: Crystal Star":
            lambda state: (state.has("Elevator Key 1", world.player) and state.has("Elevator Key 2", world.player)
                           and state.has("Card Key 1", world.player) and state.has("Card Key 2", world.player)
                           and state.has("Card Key 3", world.player) and state.has("Card Key 4", world.player)
                           and state.has("Paper Curse", world.player) and state.has("Vivian", world.player)),
        "Rogueport Sewers Black Chest Room: Plane Curse":
            lambda state: state.has("Black Key (Plane Curse)", world.player),
        "Rogueport Docks: HP Drain":
            lambda state: state.has("Boat Curse", world.player),
        "Rogueport Docks: Star Piece 2":
            lambda state: state.has("Boat Curse", world.player),
        "Rogueport Westside: Shine Sprite 1":
            lambda state: state.has("Bobbery", world.player),
        "Rogueport Westside: Shine Sprite 2":
            lambda state: StateLogic.tube_curse(state, world.player),
        "Rogueport Westside: Train Ticket":
            lambda state: StateLogic.keelhaul_key(state, world.player) and state.has("Wedding Ring", world.player)
                          and state.has("Yoshi", world.player),
        "Rogueport Sewers Black Key Room: Happy Heart P":
            lambda state: state.has("Flurrie", world.player),
        "Rogueport Sewers Spike Room: Spike Shield":
            lambda state: state.has("Paper Curse", world.player) and state.has("Vivian", world.player),
        "Rogueport Sewers Petal Meadows Pipe: Shine Sprite":
            lambda state: state.has("Plane Curse", world.player) and state.has("Boat Curse", world.player),
        "Rogueport Sewers Star Piece House: Star Piece":
            lambda state: state.has("Plane Curse", world.player) and StateLogic.ultra_boots(state, world.player),
        "Rogueport Sewers East Entrance: Defend Plus P":
            lambda state: (state.has("Plane Curse", world.player) and StateLogic.ultra_boots(state, world.player)
                           and state.has("Bobbery", world.player)),
        "Rogueport Docks: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Sewers Black Chest Room: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Sewers East Entrance: Star Piece":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Center: Star Piece 1":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Center: Star Piece 2":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Eastside: Star Piece 2":
            lambda state: StateLogic.super_boots(state, world.player),
        "Rogueport Sewers East Pipe Room: Shine Sprite":
            lambda state: StateLogic.super_hammer(state, world.player),
        "Rogueport Sewers West Pipe Room: FP Plus":
            lambda state: StateLogic.ultra_hammer(state, world.player),
        "Rogueport Center: Ultra Hammer":
            lambda state: StateLogic.ultra_boots(state, world.player),
        "Rogueport Eastside: Double Dip":
            lambda state: state.has("Boat Curse", world.player) and (
                        state.has("Paper Curse", world.player) or state.has("Yoshi", world.player)),
        "Rogueport Eastside: Shine Sprite 1":
            lambda state: state.has("Yoshi", world.player),
        "Rogueport Eastside: Shine Sprite 2":
            lambda state: state.has("Yoshi", world.player),
        "Rogueport Eastside: Shine Sprite 3":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Yoshi", world.player),
        "Rogueport Center: Old Letter":
            lambda state: StateLogic.tube_curse(state, world.player) and state.has("Yoshi", world.player),
        "Rogueport Eastside: Star Piece 3":
            lambda state: state.has("Yoshi", world.player),
        "Rogueport Eastside: Star Piece 4":
            lambda state: state.has("Paper Curse", world.player) or state.has("Yoshi", world.player),
        "Rogueport Eastside: Star Piece 5":
            lambda state: StateLogic.super_boots(state, world.player) and state.has("Yoshi", world.player),
        "Pit of 100 Trials Floor 10: Sleepy Stomp":
            lambda state: state.has("stars", world.player, 1),
        "Pit of 100 Trials Floor 20: Fire Drive":
            lambda state: state.has("stars", world.player, 1),
        "Pit of 100 Trials Floor 30: Zap Tap":
            lambda state: state.has("stars", world.player, 2),
        "Pit of 100 Trials Floor 40: Pity Flower":
            lambda state: state.has("stars", world.player, 2),
        "Pit of 100 Trials Floor 50: Strange Sack":
            lambda state: state.has("stars", world.player, 3),
        "Pit of 100 Trials Floor 60: Double Dip":
            lambda state: state.has("stars", world.player, 3),
        "Pit of 100 Trials Floor 70: Double Dip P":
            lambda state: state.has("stars", world.player, 4),
        "Pit of 100 Trials Floor 80: Bump Attack":
            lambda state: state.has("stars", world.player, 4),
        "Pit of 100 Trials Floor 90: Lucky Day":
            lambda state: state.has("stars", world.player, 5),
        "Pit of 100 Trials Floor 100: Return Postage":
            lambda state: state.has("stars", world.player, 5)
    }


def get_tattle_rules_dict() -> dict[str, typing.List[int]]:
    return {
        "Tattle: Spania": [78780145, 78780267, 78780638],
        "Tattle: Fuzzy": [78780170, 78780296, 78780638],
        "Tattle: Koopa Troopa": [78780193, 78780170],
        "Tattle: Blooper": [78780184],
        "Tattle: Lord Crump": [78780511],
        "Tattle: Cleft": [78780216, 78780639],
        "Tattle: Bald Cleft": [78780165],
        "Tattle: Bristle": [78780800, 78780296],
        "Tattle: Gold Fuzzy": [78780170],
        "Tattle: Paratroopa": [78780193],
        "Tattle: Dull Bones": [78780193, 78780267, 78780615, 78780638],
        "Tattle: Red Bones": [78780193, 78780615],
        "Tattle: Hooktail": [78780209],
        "Tattle: Pale Piranha": [78780216, 78780267],
        "Tattle: Dark Puff": [78780216, 78780267, 78780639],
        "Tattle: Vivian": [78780215],
        "Tattle: Marilyn": [78780215, 78780622],
        "Tattle: Beldam": [78780215, 78780622],
        "Tattle: X-Naut": [78780231, 78780584],
        "Tattle: Yux": [78780231],
        "Tattle: Mini-Yux": [78780231],
        "Tattle: Pider": [78780241, 78780267, 78780639],
        "Tattle: Magnus von Grapple": [78780232],
        "Tattle: KP Koopa": [78780267],
        "Tattle: KP Paratroopa": [78780267],
        "Tattle: Pokey": [78780267, 78780639],
        "Tattle: Spiny": [78780267, 78780640],
        "Tattle: Lakitu": [78780267, 78780640],
        "Tattle: Bandit": [78780267, 78780640],
        "Tattle: Big Bandit": [78780267],
        "Tattle: Hyper Bald Cleft": [78780267],
        "Tattle: Bob-omb": [78780267, 78780640],
        "Tattle: Swooper": [78780287, 78780436],
        "Tattle: Iron Cleft": [78780267],
        "Tattle: Red Spike Top": [78780296],
        "Tattle: Shady Koopa": [78780296, 78780641],
        "Tattle: Shady Paratroopa": [78780296],
        "Tattle: Green Fuzzy": [78780296, 78780470],
        "Tattle: Flower Fuzzy": [78780296, 78780470],
        "Tattle: Magikoopa": [78780511],
        "Tattle: Red Magikoopa": [78780296],
        "Tattle: White Magikoopa": [78780296],
        "Tattle: Green Magikoopa": [78780296],
        "Tattle: Hammer Bro": [78780296, 78780511],
        "Tattle: Boomerang Bro": [78780296],
        "Tattle: Fire Bro": [78780296],
        "Tattle: Dark Craw": [78780296, 78780644],
        "Tattle: Red Chomp": [78780296, 78780643],
        "Tattle: Koopatrol": [78780511],
        "Tattle: Dark Koopatrol": [78780296, 78780645],
        "Tattle: Rawk Hawk": [78780295],
        "Tattle: Macho Grubba": [78780287],
        "Tattle: Hyper Goomba": [78780319],
        "Tattle: Hyper Paragoomba": [78780319],
        "Tattle: Crazee Dayzee": [78780327],
        "Tattle: Hyper Spiky Goomba": [78780319],
        "Tattle: Amazy Dayzee": [78780327],
        "Tattle: Hyper Cleft": [78780329, 78780641],
        "Tattle: Buzzy Beetle": [78780450],
        "Tattle: Spike Top": [78780450],
        "Tattle: Atomic Boo": [78780434],
        "Tattle: Boo": [78780434],
        "Tattle: Doopliss": [78780437, 78780622],
        "Tattle: Ember": [78780503],
        "Tattle: Putrid Piranha": [78780470],
        "Tattle: Lava Bubble": [78780495, 78780642],
        "Tattle: Bullet Bill": [78780497],
        "Tattle: Bill Blaster": [78780497],
        "Tattle: Bulky Bob-omb": [78780497, 78780642],
        "Tattle: Parabuzzy": [78780503],
        "Tattle: Cortez": [78780511],
        "Tattle: Smorg": [78780554],
        "Tattle: Ruff Puff": [78780538],
        "Tattle: Poison Pokey": [78780541, 78780642],
        "Tattle: Spiky Parabuzzy": [78780543, 78780642],
        "Tattle: Ice Puff": [78780562, 78780643],
        "Tattle: Frost Piranha": [78780562, 78780644],
        "Tattle: Moon Cleft": [78780579, 78780643],
        "Tattle: Z-Yux": [78780579],
        "Tattle: Mini-Z-Yux": [78780579],
        "Tattle: Elite X-Naut": [78780584],
        "Tattle: X-Yux": [78780595],
        "Tattle: Mini-X-Yux": [78780595],
        "Tattle: X-Naut PhD": [78780595],
        "Tattle: Magnus von Grapple 2.0": [78780604],
        "Tattle: Spunia": [78780646, 78780156],
        "Tattle: Swoopula": [78780605, 78780645],
        "Tattle: Dry Bones": [78780605, 78780644],
        "Tattle: Bombshell Bill": [78780605, 78780609],
        "Tattle: B. Bill Blaster": [78780605, 78780609],
        "Tattle: Phantom Ember": [78780634, 78780645],
        "Tattle: Dark Bones": [78780609],
        "Tattle: Chain-Chomp": [78780634, 78780645],
        "Tattle: Dark Wizzerd": [78780634, 78780644],
        "Tattle: Gloomtail": [78780634],
        "Tattle: Sir Grodus": [],
        "Tattle: Grodus X": [],
        "Tattle: Kammy Koopa": [],
        "Tattle: Bowser": [],
        "Tattle: Shadow Queen": [],
        "Tattle: Gloomba": [78780638],
        "Tattle: Paragloomba": [78780639],
        "Tattle: Spiky Gloomba": [78780640],
        "Tattle: Dark Koopa": [78780641],
        "Tattle: Dark Paratroopa": [78780642],
        "Tattle: Badge Bandit": [78780643],
        "Tattle: Dark Boo": [78780643],
        "Tattle: Dark Lakitu": [78780644],
        "Tattle: Sky-Blue Spiny": [78780644],
        "Tattle: Wizzerd": [78780645],
        "Tattle: Piranha Plant": [78780646],
        "Tattle: Dark Bristle": [78780646],
        "Tattle: Arantula": [78780646],
        "Tattle: Elite Wizzerd": [78780647],
        "Tattle: Swampire": [78780647],
        "Tattle: Poison Puff": [78780647],
        "Tattle: Bob-ulk": [78780647],
        "Tattle: Bonetail": [78780647]
    }
