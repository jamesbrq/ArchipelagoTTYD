import json
import pkgutil
import typing

from rule_builder.rules import Rule, False_, Has, CanReachLocation, CanReachRegion, CanReachEntrance
from . import StateLogic
from .Options import Goal, PitItems
from .Data import stars, pit_exclusive_tattle_stars_required
from .Locations import get_location_ids, get_locations_by_tags, location_id_to_name
from .Options import PalaceSkip
from worlds.generic.Rules import forbid_items_for_player

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def set_rules(world: "TTYDWorld"):
    for location, rule in create_lambda_from_json(pkgutil.get_data(__name__, "json/rules.json").decode(), world).items():
        if location not in world.disabled_locations:
            world.set_rule(world.get_location(location), rule)

    for location in ["Palace of Shadow Final Staircase: Ultra Shroom", "Palace of Shadow Final Staircase: Jammin' Jelly"]:
        if location not in world.disabled_locations:
            world.set_rule(world.multiworld.get_location(location, world.player), Has("stars", world.options.goal_stars.value))

    for location in get_locations_by_tags("shop"):
        if location.name in world.disabled_locations:
            continue
        forbid_items_for_player(world.get_location(location.name), set([item for item in stars.values()]), world.player)

    for location in get_locations_by_tags("dazzle"):
        if location.name in world.disabled_locations:
            continue
        forbid_items_for_player(world.get_location(location.name), {"Star Piece"}, world.player)

def set_tattle_rules(world: "TTYDWorld"):
    for location in get_locations_by_tags("tattle"):
        if location.name in world.disabled_locations:
            continue
        world.set_rule(world.get_location(location.name), Has("Goombella"))

    for location_name, locations in get_tattle_rules_dict().items():
        if location_name in world.disabled_locations:
            continue

        if len(locations) == 0:
            # Require access to the end of the game
            if world.options.palace_skip == PalaceSkip.option_true and world.options.goal != Goal.option_shadow_queen:
                extra_condition = Has("stars", count=world.options.palace_stars)
            elif world.options.goal == Goal.option_shadow_queen:
                extra_condition = CanReachLocation("Shadow Queen")
            else:
                extra_condition = CanReachLocation("Palace of Shadow Final Staircase: Ultra Shroom")
        else:
            # Filter out pit locations if pit items aren't fully randomized
            if world.options.pit_items != PitItems.option_all and location_name not in pit_exclusive_tattle_stars_required:
                pit_ids = set(get_location_ids(get_locations_by_tags("pit_floor")))
                locations = [loc for loc in locations if loc not in pit_ids]
                if len(locations) == 0:
                    continue

            valid_locations = [
                location_id_to_name[loc]
                for loc in locations
                if loc in location_id_to_name and location_id_to_name[loc] not in world.disabled_locations
            ]
            if len(valid_locations) == 0:
                continue

            extra_condition = CanReachLocation(valid_locations[0])
            for loc in valid_locations[1:]:
                extra_condition = extra_condition | CanReachLocation(loc)

        world.set_rule(
            world.get_location(location_name),
            Has("Goombella") & extra_condition
        )


def create_lambda_from_json(json_string: str, world: "TTYDWorld") -> typing.Dict[str, typing.Callable]:
    lambda_functions = {}
    for location, requirements in json.loads(json_string).items():
        lambda_functions[location] = _build_single_rule(requirements, world)
    return lambda_functions


def _build_single_rule(req: typing.Dict, world: "TTYDWorld") -> Rule:
    def build_rule(r) -> Rule:
        if "or" in r:
            children = [build_rule(c) for c in r["or"]]
            if not children:
                return False_()
            rule = children[0]
            for child in children[1:]:
                rule = rule | child
            return rule

        elif "and" in r:
            children = [build_rule(c) for c in r["and"]]
            if not children:
                return False_()
            rule = children[0]
            for child in children[1:]:
                rule = rule & child
            return rule

        elif "has" in r:
            has_value = r["has"]

            if isinstance(has_value, str):
                item = has_value
                count = r.get("count", 1)
            elif isinstance(has_value, dict):
                item = has_value.get("item", "")
                count = has_value.get("count", 1)
            else:
                item = str(has_value)
                count = r.get("count", 1)

            return Has(item, count=count)

        elif "function" in r:
            function_data = r["function"]

            if isinstance(function_data, dict):
                name = function_data.get("name", "")
                count = function_data.get("count", 0)
            else:
                name = function_data
                count = None

            logic_obj = getattr(StateLogic, name)

            # Case 1: Rule class (ChapterCompletions, PalaceAccess)
            if isinstance(logic_obj, type) and issubclass(logic_obj, Rule):
                if count is not None:
                    return logic_obj(count)
                return logic_obj()

            # Case 2: helper returning a Rule (fahr_outpost, westside, etc.)
            if callable(logic_obj):
                if count is not None:
                    return logic_obj(count)
                return logic_obj()

            raise Exception(f"Invalid logic function: {name}")

        elif "can_reach" in r:
            return CanReachLocation(r["can_reach"])

        elif "can_reach_region" in r:
            return CanReachRegion(r["can_reach_region"])

        elif "can_reach_entrance" in r:
            return CanReachEntrance(r["can_reach_entrance"])
        else:
            return False_()

    return build_rule(req)



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
        "Tattle: X-Naut": [78780231, 78780595],
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
