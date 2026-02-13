import typing

from BaseClasses import Region
from .Locations import (TTYDLocation, shadow_queen, LocationData)
from . import StateLogic, get_locations_by_tags
import json
import pkgutil
import random
from .Data import warp_table
from .Rules import _build_single_rule
from rule_builder.rules import Rule, Has, True_
from collections import defaultdict, deque

if typing.TYPE_CHECKING:
    from . import TTYDWorld

zones_by_region: dict[str, list[dict]] = defaultdict(list)
region_graph: dict[str, set[str]] = defaultdict(set)
used_zones: set[str] = set()


def get_region_defs_from_json():
    raw = pkgutil.get_data(__name__, "json/regions.json")
    if raw is None:
        raise FileNotFoundError("json/regions.json not found in apworld")
    return json.loads(raw.decode("utf-8"))


def get_zone_dict_from_json():
    raw = pkgutil.get_data(__name__, "json/zones.json")
    if raw is None:
        raise FileNotFoundError("json/zones.json not found in apworld")

    zone_defs = json.loads(raw.decode("utf-8"))
    return {z["name"]: z for z in zone_defs}




def get_regions_dict() -> dict[str, list[LocationData]]:
    """
    Returns a dictionary mapping region names to their corresponding location data lists.
    """
    return {
        "Rogueport": get_locations_by_tags("rogueport"),
        "Rogueport (Westside)": get_locations_by_tags("rogueport_westside"),
        "Rogueport Sewers": get_locations_by_tags("sewers"),
        "Rogueport Sewers Westside": get_locations_by_tags("sewers_westside"),
        "Rogueport Sewers Westside Ground": get_locations_by_tags("sewers_westside_ground"),
        "Petal Meadows (Left)": get_locations_by_tags("petal_left"),
        "Petal Meadows (Right)": get_locations_by_tags("petal_right"),
        "Hooktail's Castle": get_locations_by_tags("hooktails_castle"),
        "Boggly Woods": get_locations_by_tags("boggly_woods"),
        "Great Tree": get_locations_by_tags("great_tree"),
        "Glitzville": get_locations_by_tags("glitzville"),
        "Twilight Town": get_locations_by_tags("twilight_town"),
        "Twilight Trail": get_locations_by_tags("twilight_trail"),
        "Creepy Steeple": get_locations_by_tags("creepy_steeple"),
        "Keelhaul Key": get_locations_by_tags("keelhaul_key"),
        "Pirate's Grotto": get_locations_by_tags("pirates_grotto"),
        "Excess Express": get_locations_by_tags("excess_express"),
        "Riverside Station": get_locations_by_tags("riverside"),
        "Poshley Heights": get_locations_by_tags("poshley_heights"),
        "Fahr Outpost": get_locations_by_tags("fahr_outpost"),
        "X-Naut Fortress": get_locations_by_tags("xnaut_fortress"),
        "Palace of Shadow": get_locations_by_tags("palace"),
        "Palace of Shadow (Post-Riddle Tower)": get_locations_by_tags("riddle_tower"),
        "Pit of 100 Trials": get_locations_by_tags("pit"),
        "Shadow Queen": shadow_queen,
        "Tattlesanity": get_locations_by_tags("tattle")
    }


def get_region_connections_dict(world: "TTYDWorld") -> dict[tuple[str, str], typing.Optional[typing.Callable]]:
    """
    Returns a dictionary mapping region connections (source, target) to their access rules.
    If a rule is None, the connection is always available.
    """
    return {
        ("Menu", "Rogueport Center"): True_(),
        ("Rogueport West Tall Pipe", "Rogueport West"): True_(),
        ("Rogueport Sewers East", "Rogueport Sewers East Bobbery Pipe"): 
        Has("Bobbery"),
        ("Rogueport Sewers East Bobbery Pipe", "Rogueport Sewers East"): 
        Has("Bobbery"),
        ("Rogueport Sewers East", "Rogueport Sewers East Fortune Pipe"):
        Has("Paper Mode"),
        ("Rogueport Sewers East Fortune Pipe", "Rogueport Sewers East"): True_(),
        ("Rogueport Sewers East", "Rogueport Sewers East Plane Mode"):
        Has("Plane Mode"),
        ("Rogueport Sewers East Plane Mode", "Rogueport Sewers East"): True_(),
        ("Rogueport Sewers East Top", "Rogueport Sewers East"): True_(),
        ("Rogueport Sewers East Top", "Rogueport Sewers East Fortune Pipe"):
        Has("Yoshi"),
        ("Rogueport Sewers East Top", "Rogueport Sewers East Plane Mode"): True_(),
        ("Rogueport Sewers Blooper", "Rogueport Sewers Blooper Pipe"): True_(),
        ("Rogueport Sewers Town", "Rogueport Sewers Town Dazzle"):
        StateLogic.fallen_pipe(),
        ("Rogueport Sewers Town Dazzle", "Rogueport Sewers Town"):
        StateLogic.fallen_pipe(),
        ("Rogueport Sewers Town Teleporter", "Rogueport Sewers Town"): True_(),
        ("Rogueport Sewers Town", "Rogueport Sewers Town Teleporter"): True_(),
        ("Rogueport Sewers West", "Rogueport Sewers West West"):
        Has("Yoshi"),
        ("Rogueport Sewers West West", "Rogueport Sewers West"):
        Has("Yoshi"),
        ("Rogueport Sewers West", "Rogueport Sewers West Bottom"): True_(),
        ("Rogueport Sewers West West", "Rogueport Sewers West Bottom"): True_(),
        ("Rogueport Sewers West Bottom", "Rogueport Sewers West West"):
        StateLogic.ultra_boots(),
        ("Rogueport Sewers West West", "Rogueport Sewers West Fahr"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers West Fahr", "Rogueport Sewers West West"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers East Enemy Hall", "Rogueport Sewers East Enemy Hall Barred Door"):
        Has("Paper Mode"),
        ("Rogueport Sewers East Enemy Hall Barred Door", "Rogueport Sewers East Enemy Hall"):
        Has("Paper Mode"),
        ("Rogueport Sewers West Enemy Hall", "Rogueport Sewers West Enemy Hall Flurrie"):
        Has("Flurrie"),
        ("Rogueport Sewers West Enemy Hall Flurrie", "Rogueport Sewers West Enemy Hall"):
        Has("Flurrie"),
        ("Rogueport Sewers West Warp Room Left", "Rogueport Sewers West Warp Room Right"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers West Warp Room Right", "Rogueport Sewers West Warp Room Left"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers West Warp Room Left", "Rogueport Sewers West Warp Room Top"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers West Warp Room Top", "Rogueport Sewers West Warp Room Left"): True_(),
        ("Rogueport Sewers West Warp Room Right", "Rogueport Sewers West Warp Room Top"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers West Warp Room Top", "Rogueport Sewers West Warp Room Right"): True_(),
        ("Rogueport Sewers East Warp Room Left", "Rogueport Sewers East Warp Room Right"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers East Warp Room Right", "Rogueport Sewers East Warp Room Left"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers East Warp Room Left", "Rogueport Sewers East Warp Room Top"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers East Warp Room Top", "Rogueport Sewers East Warp Room Left"): True_(),
        ("Rogueport Sewers East Warp Room Right", "Rogueport Sewers East Warp Room Top"):
        StateLogic.ultra_hammer(),
        ("Rogueport Sewers East Warp Room Top", "Rogueport Sewers East Warp Room Right"): True_(),
        ("Rogueport Sewers Black Key Room", "Rogueport Sewers Black Key Room Puni Door"):
        Has("Paper Mode"),
        ("Rogueport Sewers Black Key Room Puni Door", "Rogueport Sewers Black Key Room"):
        Has("Paper Mode"),
        ("Rogueport Sewers Puni Room", "Rogueport Sewers Puni Room Exit"): True_(),
        ("Petal Meadows Bridge West", "Petal Meadows Bridge East"): True_(),
        ("Hooktail's Castle Drawbridge East Bottom", "Hooktail's Castle Drawbridge West Bottom"):
        Has("Yoshi"),
        ("Hooktail's Castle Drawbridge West Bottom", "Hooktail's Castle Drawbridge East Bottom"): True_(),
        ("Hooktail's Castle Drawbridge East Top", "Hooktail's Castle Drawbridge East Bottom"): True_(),
        ("Hooktail's Castle Drawbridge East Top", "Hooktail's Castle Drawbridge West Bottom"):
        Has("Plane Mode"),
        ("Hooktail's Castle Drawbridge West Top", "Hooktail's Castle Drawbridge West Bottom"): True_(),
        ("Hooktail's Castle Stair Switch Room Upper Level", "Hooktail's Castle Stair Switch Room"): True_(),
        ("Hooktail's Life Shroom Room", "Hooktail's Life Shroom Room Upper Level"):
        StateLogic.partner_press_switch(),
        ("Hooktail's Life Shroom Room Upper Level", "Hooktail's Life Shroom Room"): True_(),
        ("Hooktail's Castle Central Staircase Upper Level", "Hooktail's Castle Central Staircase"): True_(),
        ("Boggly Woods Plane Panel Room", "Boggly Woods Plane Panel Room Upper"):
        Has("Plane Mode"),
        ("Boggly Woods Plane Panel Room Upper", "Boggly Woods Plane Panel Room"): True_(),
        ("Boggly Woods Outside Flurrie's House", "Boggly Woods Outside Flurrie's House Grass Area"):
        Has("Paper Mode"),
        ("Boggly Woods Outside Flurrie's House Grass Area", "Boggly Woods Outside Flurrie's House"):
        Has("Paper Mode"),
        ("Glitzville Promoter's Office Vent", "Glitzville Promoter's Office"): True_(),
        ("Creepy Steeple Main Hall Upper", "Creepy Steeple Main Hall"): True_(),
        ("Creepy Steeple Main Hall Upper South", "Creepy Steeple Main Hall"): True_(),
        ("Creepy Steeple Well Buzzy Room", "Creepy Steeple Well Buzzy Room Vivian"):
        Has("Vivian"),
        ("Pirate's Grotto Handle Room Canal", "Pirate's Grotto Handle Room"):
        Has("Boat Mode"),
        ("Pirate's Grotto Sluice Gate Upper", "Pirate's Grotto Sluice Gate Upper Canal"):
        Has("Boat Mode"),
        ("Pirate's Grotto Sluice Gate Upper Canal", "Pirate's Grotto Sluice Gate Upper"):
        Has("Boat Mode"),
        ("Pirate's Grotto Sluice Gate Upper Canal", "Pirate's Grotto Sluice Gate Canal"): True_(),
        ("Riverside Station Ultra Boots Room Upper", "Riverside Station Ultra Boots Room"): True_(),
        ("Pirate's Grotto Toad Boat Room", "Pirate's Grotto Toad Boat Room East"):
        Has("Boat Mode") & Has("Plane Mode"),
        ("X-Naut Fortress Hall Ground Floor", "X-Naut Fortress Hall Sublevel One"):
        Has("Elevator Key 1"),
        ("X-Naut Fortress Hall Sublevel One", "X-Naut Fortress Hall Ground Floor"):
        Has("Elevator Key 1"),
        ("X-Naut Fortress Hall Ground Floor", "X-Naut Fortress Hall Sublevel Two"):
        Has("Elevator Key 1"),
        ("X-Naut Fortress Hall Sublevel One", "X-Naut Fortress Hall Sublevel Two"):
        Has("Elevator Key 1"),
        ("X-Naut Fortress Hall Sublevel Two", "X-Naut Fortress Hall Sublevel One"):
        Has("Elevator Key 1"),
        ("X-Naut Fortress Hall Sublevel Two", "X-Naut Fortress Hall Sublevel Three"):
        Has("Elevator Key 2"),
        ("X-Naut Fortress Hall Sublevel Three", "X-Naut Fortress Hall Sublevel Two"):
        Has("Elevator Key 2"),
        ("X-Naut Fortress Hall Sublevel Two", "X-Naut Fortress Hall Sublevel Four"):
        Has("Elevator Key 2"),
        ("X-Naut Fortress Hall Sublevel Four", "X-Naut Fortress Hall Sublevel Two"):
        Has("Elevator Key 2"),
        ("X-Naut Fortress Hall Sublevel Three", "X-Naut Fortress Hall Sublevel Four"):
        Has("Elevator Key 2"),
        ("X-Naut Fortress Hall Sublevel Four", "X-Naut Fortress Hall Sublevel Three"):
        Has("Elevator Key 2"),
        ("TTYD", "Palace of Shadow"): 
        StateLogic.PalaceAccess(world.options.goal_stars.value),
        ("Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"): 
        StateLogic.riddle_tower(),
        ("Rogueport Sewers Pit Room", "Pit of 100 Trials"): 
        StateLogic.pit(),
        ("Menu", "Tattlesanity"): True_(),
        ("TTYD", "Shadow Queen"):
        StateLogic.PalaceAccess(world.options.goal_stars.value)
    }

    if world.options.blue_pipe_toggle:
        connections[("Rogueport Sewers", "Petal Meadows (Right)")] = lambda state: StateLogic.super_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Boggly Woods")] = lambda state: StateLogic.super_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Keelhaul Key")] = lambda state: StateLogic.ultra_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Poshley Heights")] = lambda state: StateLogic.ultra_blue_pipes(state, world.player)

    return connections



def create_regions(world: "TTYDWorld"):
    # Create menu region (always included)
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # Create other regions from raw region definitions
    region_defs = get_region_defs_from_json()

    for region in region_defs:
        name = region["name"]
        tag = region["tag"]

        locations = get_locations_by_tags(tag)

        if name not in world.excluded_regions:
            create_region(world, name, locations)
        else:
            world.disabled_locations.update(
                loc.name for loc in locations
                if loc.name not in world.disabled_locations
            )


def connect_regions(world: "TTYDWorld"):
    one_way = []
    vanilla = []
    deferred_connections = []
    unneeded_regions = {
        "Tattlesanity",
        "Palace of Shadow",
        "Palace of Shadow (Post-Riddle Tower)",
        "Shadow Queen"
    }

    connections_dict = get_region_connections_dict(world)
    zones = get_zone_dict_from_json()
    reachable_regions = {"Menu", "Rogueport Center"}

    def has_entrance_dependency(rule_dict):
        """Recursively check if rules contain can_reach_entrance"""
        if not rule_dict:
            return False

        if isinstance(rule_dict, dict):
            if "can_reach_entrance" in rule_dict:
                return True

            for key, value in rule_dict.items():
                if key in ["and", "or"]:
                    if isinstance(value, list):
                        for sub_rule in value:
                            if has_entrance_dependency(sub_rule):
                                return True
                    elif has_entrance_dependency(value):
                        return True

        return False

    # First pass: Create entrances without dependencies
    for (source, target), rule in connections_dict.items():
        if source in world.excluded_regions or target in world.excluded_regions:
            continue
        if source == "Rogueport" and target == "Shadow Queen" and not world.options.palace_skip:
            continue
        if source == "Menu" and target == "Rogueport (Westside)" and not world.options.open_westside:
            continue

        world.multiworld.get_region(source, world.player)
        world.multiworld.get_region(target, world.player)
        source_region = world.multiworld.get_region(source, world.player)
        target_region = world.multiworld.get_region(target, world.player)
        world.create_entrance(source_region, target_region, rule)
        add_edge(source, target)

    tag_to_region = get_region_name_by_tag()

    for z in zones.values():
        if "is_vanilla" in z:
            vanilla.append(z)
        elif z["target"] == "One Way":
            one_way.append(z)
        elif z["target"] == "":
            continue
        else:
            region = tag_to_region.get(z["region"])
            zones_by_region[region].append(z)

    all_regions = set(tag_to_region.values())
    unreached_regions = all_regions - reachable_regions - unneeded_regions

    # Process vanilla connections, deferring those with entrance dependencies
    vanilla_deferred = []
    for src in vanilla:
        if not (src["target"] == "" or src["target"] == "One Way" or src["target"] == "filler"):
            dst = zones[src["target"]]

            # Check if this connection has entrance dependencies
            if has_entrance_dependency(src.get("rules")):
                vanilla_deferred.append((src, dst))
                mark_used(src, dst)
                continue

            src_region = tag_to_region[src["region"]]
            dst_region = tag_to_region[dst["region"]]
            rule = build_rule_lambda(src.get("rules"), world)
            source_region = world.multiworld.get_region(src_region, world.player)
            target_region = world.multiworld.get_region(dst_region, world.player)
            world.create_entrance(source_region, target_region, rule)
            add_edge(src_region, dst_region)
            mark_used(src, dst)
        elif src["target"] == "One Way":
            source = src["src_region"]
            target = src["region"]
            rule = build_rule_lambda(src.get("rules"), world)
            world.multiworld.get_region(source, world.player)
            world.multiworld.get_region(target, world.player)
            world.create_entrance(source, target, rule)

    random.shuffle(one_way)

    for i in range(len(one_way)):
        if i < len(one_way) - 1:
            a = one_way[i]
            b = one_way[i + 1]
        else:
            a = one_way[i]
            b = one_way[0]
        warp_table[(a["map"], a["bero"])] = (b["map"], b["bero"])
        source = tag_to_region.get(a["src_region"])
        target = tag_to_region.get(b["region"])
        rule = build_rule_lambda(a.get("rules"), world)
        world.multiworld.get_region(source, world.player)
        world.multiworld.get_region(target, world.player)
        add_edge(source, target)

        source_region = world.multiworld.get_region(source, world.player)
        target_region = world.multiworld.get_region(target, world.player)
        print(b["name"])
        world.create_entrance(source_region, target_region, rule, b["name"])

    while unreached_regions:
        src_region_contenders = [
            r for r in reachable_regions if unused_zones(r)
        ]


        src_region = random.choice(src_region_contenders)
        dst_region = random.choice(list(unreached_regions))

        src_zone_contenders = unused_zones(src_region)
        dst_zone_contenders = unused_zones(dst_region)
        if len(src_region_contenders) == 1 and len(src_zone_contenders) == 1 and len(dst_zone_contenders) == 1 and len(
                unreached_regions) != 1:
            continue
        if len(src_zone_contenders) == 0 or len(dst_zone_contenders) == 0:
            print(unreached_regions)
            print(src_region)
            print(dst_region)
            continue


        src_zone = random.choice(src_zone_contenders)
        dst_zone = random.choice(dst_zone_contenders)

        # Check if either zone has entrance dependencies
        if has_entrance_dependency(src_zone.get("rules")) or has_entrance_dependency(dst_zone.get("rules")):
            # Store the actual zone objects, not just region names
            deferred_connections.append(("non_vanilla", src_region, dst_region, src_zone, dst_zone, zones))
            mark_used(src_zone, dst_zone)
            add_edge(src_region, dst_region)
            add_edge(dst_region, src_region)
            reachable_regions = compute_reachable("Menu")
            unreached_regions = all_regions - reachable_regions - unneeded_regions
            continue

        src_target = zones[src_zone["target"]]
        dst_target = zones[dst_zone["target"]]
        src_rule = build_rule_lambda(src_zone.get("rules"), world)
        dst_rule = build_rule_lambda(dst_zone.get("rules"), world)

        warp_table[(src_target["map"], src_target["bero"])] = (dst_zone["map"], dst_zone["bero"])
        warp_table[(dst_target["map"], dst_target["bero"])] = (src_zone["map"], src_zone["bero"])

        source_region = world.multiworld.get_region(src_region, world.player)
        target_region = world.multiworld.get_region(dst_region, world.player)

        world.create_entrance(source_region, target_region, src_rule, dst_zone["name"])
        world.create_entrance(target_region, source_region, dst_rule, src_zone["name"])

        mark_used(src_zone, dst_zone)
        add_edge(src_region, dst_region)
        add_edge(dst_region, src_region)
        reachable_regions = compute_reachable("Menu")
        unreached_regions = all_regions - reachable_regions - unneeded_regions

    # Process remaining zones
    remaining_zones = [
        z for region in zones_by_region
        for z in zones_by_region[region]
        if z["name"] not in used_zones
    ]

    random.shuffle(remaining_zones)
    assert len(remaining_zones) % 2 == 0

    for i in range(0, len(remaining_zones), 2):
        src = remaining_zones[i]
        dst = remaining_zones[i + 1]

        # Check if either has entrance dependencies
        if has_entrance_dependency(src.get("rules")) or has_entrance_dependency(dst.get("rules")):
            deferred_connections.append(("remaining", src, dst, zones))
            continue

        src_region = tag_to_region[src["region"]]
        dst_region = tag_to_region[dst["region"]]

        src_target = zones[src["target"]]
        dst_target = zones[dst["target"]]

        src_rule = build_rule_lambda(src.get("rules"), world)
        dst_rule = build_rule_lambda(dst.get("rules"), world)

        warp_table[(src_target["map"], src_target["bero"])] = (dst["map"], dst["bero"])
        warp_table[(dst_target["map"], dst_target["bero"])] = (src["map"], src["bero"])

        source_region = world.multiworld.get_region(src_region, world.player)
        target_region = world.multiworld.get_region(dst_region, world.player)
        world.create_entrance(source_region, target_region, src_rule, dst["name"])
        world.create_entrance(target_region, source_region, dst_rule, src["name"])

    # ==========================================
    # SECOND PASS: Create deferred connections
    # ==========================================
    print("\n=== Creating deferred connections with entrance dependencies ===")

    # Process deferred vanilla connections
    for src, dst in vanilla_deferred:
        src_region = tag_to_region[src["region"]]
        dst_region = tag_to_region[dst["region"]]
        rule = build_rule_lambda(src.get("rules"), world)
        print("Deferred Vanilla source:", src["name"])
        print("Deferred Vanilla target:", dst["name"])
        source_region = world.multiworld.get_region(src_region, world.player)
        target_region = world.multiworld.get_region(dst_region, world.player)
        world.create_entrance(source_region, target_region, rule)
        add_edge(src_region, dst_region)

    # Process other deferred connections
    for conn in deferred_connections:
        if conn[0] == "non_vanilla":
            _, src_region, dst_region, src_zone, dst_zone, zones_dict = conn
            src_target = zones_dict[src_zone["target"]]
            dst_target = zones_dict[dst_zone["target"]]
            src_rule = build_rule_lambda(src_zone.get("rules"), world)
            dst_rule = build_rule_lambda(dst_zone.get("rules"), world)

            warp_table[(src_target["map"], src_target["bero"])] = (dst_zone["map"], dst_zone["bero"])
            warp_table[(dst_target["map"], dst_target["bero"])] = (src_zone["map"], src_zone["bero"])

            print("Deferred Non-Vanilla source:", src_zone["name"])
            print("Deferred Non-Vanilla target:", dst_zone["name"])
            source_region = world.multiworld.get_region(src_region, world.player)
            target_region = world.multiworld.get_region(dst_region, world.player)

            # Create with proper entrance names
            world.create_entrance(source_region, target_region, src_rule, dst_zone["name"])
            world.create_entrance(target_region, source_region, dst_rule, src_zone["name"])

        elif conn[0] == "remaining":
            _, src, dst, zones_dict = conn
            src_region = tag_to_region[src["region"]]
            dst_region = tag_to_region[dst["region"]]

            src_target = zones_dict[src["target"]]
            dst_target = zones_dict[dst["target"]]

            src_rule = build_rule_lambda(src.get("rules"), world)
            dst_rule = build_rule_lambda(dst.get("rules"), world)

            warp_table[(src_target["map"], src_target["bero"])] = (dst["map"], dst["bero"])
            warp_table[(dst_target["map"], dst_target["bero"])] = (src["map"], src["bero"])

            print("Deferred Remaining source:", src["name"])
            print("Deferred Remaining target:", dst["name"])
            source_region = world.multiworld.get_region(src_region, world.player)
            target_region = world.multiworld.get_region(dst_region, world.player)

            # Create with proper entrance names
            world.create_entrance(source_region, target_region, src_rule, dst["name"])
            world.create_entrance(target_region, source_region, dst_rule, src["name"])
    print(warp_table)

# Helper function to check if a rule contains entrance dependencies
def has_entrance_dependency(rule_dict):
    """Recursively check if rules contain can_reach_entrance"""
    if not rule_dict:
        return False

    # Check if this is a can_reach_entrance rule
    if isinstance(rule_dict, dict):
        if "can_reach_entrance" in rule_dict:
            return True

        # Recursively check nested rules (and, or conditions)
        for key, value in rule_dict.items():
            if key in ["and", "or"]:
                if isinstance(value, list):
                    for sub_rule in value:
                        if has_entrance_dependency(sub_rule):
                            return True
                elif has_entrance_dependency(value):
                    return True

    return False

        
def write_rel_warp_table(warp_table, filename="json/warp_table.json"):
    rel_table = {}
    for (src_map, src_bero), (dst_map, dst_bero) in warp_table.items():
        key = f"{src_map}:{src_bero}"
        value = f"{dst_map}:{dst_bero}"
        rel_table[key] = value

    with open(filename, "w") as f:
        json.dump(rel_table, f, indent=4)

    print(f"Wrote {len(rel_table)} warp entries to {filename}")


def build_rule_lambda(rule_json: dict | None, world: "TTYDWorld"):
    if rule_json is None:
        return True_()
    return _build_single_rule(rule_json, world)

def get_region_name_by_tag():
    region_defs = get_region_defs_from_json()
    return {r["tag"]: r["name"] for r in region_defs}

def unused_zones(region):
    return [z for z in zones_by_region[region] if z["name"] not in used_zones]

def mark_used(*zones):
    for z in zones:
        used_zones.add(z["name"])

def compute_reachable(start: str) -> set[str]:
    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        queue.extend(region_graph[current] - visited)

    return visited


def add_edge(a: str, b: str):
    region_graph[a].add(b)



def create_region(world: "TTYDWorld", name: str, locations: list[LocationData]):
    """Create a region with the given name and locations."""
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, TTYDLocation)
    world.multiworld.regions.append(reg)


