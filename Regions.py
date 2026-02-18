import typing

from BaseClasses import Region
from .Locations import (TTYDLocation, shadow_queen, LocationData)
from . import StateLogic, get_locations_by_tags
import json
import pkgutil
import random
from .Data import warp_table
from .Rules import _build_single_rule
from rule_builder.rules import Has, True_, CanReachRegion, CanReachLocation
from collections import defaultdict, deque

if typing.TYPE_CHECKING:
    from . import TTYDWorld


class RegionState:
    """Holds all the state needed for region connection logic."""

    def __init__(self):
        self.zones_by_region: dict[str, list[dict]] = defaultdict(list)
        self.region_graph: dict[str, set[str]] = defaultdict(set)
        self.used_zones: set[str] = set()
        self.edge_dependencies: dict[tuple[str, str], set[str]] = {}
        self.unneeded_regions: set[str] = set()


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
    connections = {
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
        ("Hooktail's Castle Life Shroom Room", "Hooktail's Castle Life Shroom Room Upper Level"):
            StateLogic.partner_press_switch(),
        ("Hooktail's Castle Life Shroom Room Upper Level", "Hooktail's Castle Life Shroom Room Upper Level"): True_(),
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
        ("Excess Express Storage Car", "Excess Express Storage Car West"):
            CanReachRegion("Riverside Station Entrance") & Has("Elevator Key (Station)")
            & CanReachRegion("Excess Express Middle Passenger Car") & CanReachLocation(
                "Excess Express Middle Passenger Car: Briefcase") & CanReachRegion("Excess Express Locomotive")
            & CanReachRegion("Excess Express Back Passenger Car") & CanReachRegion("Excess Express Front Passenger Car"),
        ("Excess Express Storage Car West", "Excess Express Storage Car"): True_(),
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
    # Create fresh state for this generation
    state = RegionState()
    chapters = ["Prologue", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
    one_way = []
    vanilla = []
    delayed_connections: dict[str, list] = defaultdict(list)


    connections_dict = get_region_connections_dict(world)
    zones = get_zone_dict_from_json()
    reachable_regions = {"Menu", "Rogueport Center"}

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
        if source == "Excess Express Storage Car" and target == "Excess Express Storage Car West":
            add_edge(state, source, target, ["Riverside Station Entrance", "Excess Express Middle Passenger Car", "Excess Express Locomotive", "Excess Express Back Passenger Car", "Excess Express Front Passenger Car"])
        add_edge(state, source, target)

    tag_to_region = get_region_name_by_tag()

    # Mark chapter regions not in limited_chapters as unneeded
    region_defs = get_region_defs_from_json()
    for region in region_defs:
        chapter = region.get("chapter")
        if chapter and chapter in chapters and chapters.index(chapter) in world.limited_chapters:
            state.unneeded_regions.add(region["name"])

    # Always unneeded
    state.unneeded_regions.update(
        {"Tattlesanity", "Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)", "Shadow Queen"})

    for z in zones.values():
        if "vanilla" in z["tags"] or not world.options.loading_zone_shuffle or any(chapters.index(tag) in world.limited_chapters for tag in z["tags"]):
            print(z["name"])
            vanilla.append(z)
        elif z["target"] == "One Way":
            one_way.append(z)
        elif z["target"] == "":
            continue
        else:
            region = tag_to_region.get(z["region"])
            state.zones_by_region[region].append(z)

    all_regions = set(tag_to_region.values())
    unreached_regions = all_regions - reachable_regions - state.unneeded_regions

    for src in vanilla:
        if not (src["target"] == "" or src["target"] == "One Way" or src["target"] == "filler"):
            dst = zones[src["target"]]

            src_region = tag_to_region[src["region"]]
            dst_region = tag_to_region[dst["region"]]
            rule_dict = src.get("rules")
            rule = build_rule_lambda(rule_dict, world)
            source_region = world.multiworld.get_region(src_region, world.player)
            target_region = world.multiworld.get_region(dst_region, world.player)
            region_dependents = has_region_dependency(rule_dict)
            if region_dependents != [] and world.options.loading_zone_shuffle:
                for region in region_dependents:
                    delayed_connections[region].append([region_dependents, src, dst])
                continue
            print("Vanilla Entrance: ", dst["name"])
            world.create_entrance(source_region, target_region, rule, dst["name"])
            add_edge(state, src_region, dst_region, has_region_dependency(rule_dict))
            mark_used(state, src, dst)
        elif src["target"] == "One Way":
            source = tag_to_region.get(src["src_region"])
            target = tag_to_region.get(src["region"])
            rule = build_rule_lambda(src.get("rules"), world)
            source_region = world.multiworld.get_region(source, world.player)
            target_region = world.multiworld.get_region(target, world.player)
            add_edge(state, source, target)
            world.create_entrance(source_region, target_region, rule, src["name"])

    max_attempts = 1000
    for attempt in range(max_attempts):
        random.shuffle(one_way)
        if is_valid_one_way_arrangement(one_way):
            break
    else:
        raise RuntimeError(f"Could not find valid one_way arrangement after {max_attempts} attempts")

    print(one_way)
    for i in range(len(one_way)):
        a = one_way[i]
        b = one_way[(i + 1) % len(one_way)]

        warp_table[(a["map"], a["bero"])] = (b["map"], b["bero"])
        source = tag_to_region.get(a["src_region"])
        target = tag_to_region.get(b["region"])
        rule_dict = a.get("rules")
        rule = build_rule_lambda(rule_dict, world)


        source_region = world.multiworld.get_region(source, world.player)
        target_region = world.multiworld.get_region(target, world.player)
        region_dependents = has_region_dependency(rule_dict)
        if region_dependents != []:
            for region in region_dependents:
                delayed_connections[region].append([region_dependents, a, b])
            continue

        print("One Way Entrance: ", b["name"])
        add_edge(state, source, target, has_region_dependency(rule_dict))
        world.create_entrance(source_region, target_region, rule, b["name"])

    consecutive_failures = 0
    max_consecutive_failures = 50
    reachable_regions = compute_reachable(state, "Menu")
    unreached_regions = all_regions - reachable_regions - state.unneeded_regions
    dst_zone_contenders = [
        z
        for r in unreached_regions
        for z in state.zones_by_region[r]
        if z["name"] not in state.used_zones and not any(
            dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
    ]
    src_zone_contenders = [
        z
        for r in reachable_regions
        for z in state.zones_by_region[r]
        if z["name"] not in state.used_zones and not any(
            dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
    ]
    print(unreached_regions)
    while unreached_regions:
        if src_zone_contenders == []:
            print(dst_zone_contenders)
            print(unreached_regions)
        src_zone = random.choice(src_zone_contenders)
        if dst_zone_contenders == []:
            print(unreached_regions)
        dst_zone = random.choice(dst_zone_contenders)
        src_region = tag_to_region[src_zone.get("region")]
        dst_region = tag_to_region[dst_zone.get("region")]

        src_target = zones[src_zone["target"]]
        dst_target = zones[dst_zone["target"]]
        src_rule_dict = src_zone.get("rules")
        dst_rule_dict = dst_zone.get("rules")
        src_rule = build_rule_lambda(src_rule_dict, world)
        dst_rule = build_rule_lambda(dst_rule_dict, world)

        warp_table[(src_target["map"], src_target["bero"])] = (dst_zone["map"], dst_zone["bero"])
        warp_table[(dst_target["map"], dst_target["bero"])] = (src_zone["map"], src_zone["bero"])

        source_region = world.multiworld.get_region(src_region, world.player)
        target_region = world.multiworld.get_region(dst_region, world.player)

        mark_used(state, src_zone, dst_zone)
        add_edge(state, src_region, dst_region, has_region_dependency(src_rule_dict))
        add_edge(state, dst_region, src_region, has_region_dependency(dst_rule_dict))
        reachable_regions = compute_reachable(state, "Menu")
        unreached_regions = all_regions - reachable_regions - state.unneeded_regions

        dst_zone_contenders = [
            z
            for r in unreached_regions
            for z in state.zones_by_region[r]
            if z["name"] not in state.used_zones and not any(
                dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
        ]
        src_zone_contenders = [
            z
            for r in reachable_regions
            for z in state.zones_by_region[r]
            if z["name"] not in state.used_zones and not any(
                dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
        ]

        if len(dst_zone_contenders) != 0 and len(src_zone_contenders) == 0:
            warp_table.pop((src_target["map"], src_target["bero"]), None)
            warp_table.pop((dst_target["map"], dst_target["bero"]), None)
            mark_unused(state, src_zone, dst_zone)
            remove_edge(state, src_region, dst_region)
            remove_edge(state, dst_region, src_region)
            reachable_regions = compute_reachable(state, "Menu")
            unreached_regions = all_regions - reachable_regions - state.unneeded_regions
            dst_zone_contenders = [
                z
                for r in unreached_regions
                for z in state.zones_by_region[r]
                if z["name"] not in state.used_zones and not any(
                    dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
            ]
            src_zone_contenders = [
                z
                for r in reachable_regions
                for z in state.zones_by_region[r]
                if z["name"] not in state.used_zones and not any(
                    dep in unreached_regions for dep in has_region_dependency(z.get("rules")))
            ]
            consecutive_failures += 1
            if consecutive_failures > max_consecutive_failures:
                print("YOU LOSE GOOD DAY SIR")
                break
            continue

        if dst_region in delayed_connections.keys():
            connections = delayed_connections.get(dst_region)
            del delayed_connections[dst_region]
            for connection in connections:
                connection[0].remove(dst_region)
                region_dependents = connection[0]
                dep_src = connection[1]
                dep_dst = connection[2]
                if region_dependents == []:
                    if dep_src["target"] == "One Way":
                        print("One Way For The Win")
                        dep_src_region_name = tag_to_region[dep_src["src_region"]]
                        dep_dst_region_name = tag_to_region[dep_dst["region"]]
                        dep_src_region = world.multiworld.get_region(dep_src_region_name, world.player)
                        dep_dst_region = world.multiworld.get_region(dep_dst_region_name, world.player)
                        dep_rule_dict = dep_src["rules"]
                        dep_rule = build_rule_lambda(dep_rule_dict, world)
                        add_edge(state, dep_src_region_name, dep_dst_region_name)
                        print("Delayed One Way Entrance: ", dep_dst["name"])
                        world.create_entrance(dep_src_region, dep_dst_region, dep_rule, dep_dst["name"])
                    else:
                        dep_src_region_name = tag_to_region[dep_src["region"]]
                        dep_dst_region_name = tag_to_region[dep_dst["region"]]
                        dep_src_region = world.multiworld.get_region(dep_src_region_name, world.player)
                        dep_dst_region = world.multiworld.get_region(dep_dst_region_name, world.player)
                        dep_src_rule_dict = dep_src["rules"]
                        dep_src_rule = build_rule_lambda(dep_src_rule_dict, world)
                        add_edge(state, dep_src_region_name, dep_dst_region_name)
                        print("Delayed Entrance: ", dep_dst["name"])
                        world.create_entrance(dep_src_region, dep_dst_region, dep_src_rule, dep_dst["name"])
            reachable_regions = compute_reachable(state, "Menu")
            unreached_regions = all_regions - reachable_regions - state.unneeded_regions


        print("Unreached Entrance: ", dst_zone["name"])
        world.create_entrance(source_region, target_region, src_rule, dst_zone["name"])
        print("Unreached Entrance: ", src_zone["name"])
        world.create_entrance(target_region, source_region, dst_rule, src_zone["name"])

    # Process any remaining delayed connections whose dependencies are now all resolved
    processed = set()
    for key in list(delayed_connections.keys()):
        connections = delayed_connections.get(key, [])
        for connection in connections:
            # Use id() to identify the connection list itself across multiple entries
            conn_id = id(connection)
            if conn_id in processed:
                continue

            connection[0].discard(key) if hasattr(connection[0], 'discard') else (
                connection[0].remove(key) if key in connection[0] else None)
            region_dependents = connection[0]
            dep_src = connection[1]
            dep_dst = connection[2]

            if region_dependents == []:
                processed.add(conn_id)
                if dep_src["target"] == "One Way":
                    dep_src_region_name = tag_to_region[dep_src["src_region"]]
                    dep_dst_region_name = tag_to_region[dep_dst["region"]]
                    dep_src_region = world.multiworld.get_region(dep_src_region_name, world.player)
                    dep_dst_region = world.multiworld.get_region(dep_dst_region_name, world.player)
                    dep_rule = build_rule_lambda(dep_src["rules"], world)
                    add_edge(state, dep_src_region_name, dep_dst_region_name)
                    print("Delayed One Way Entrance: ", dep_dst["name"])
                    world.create_entrance(dep_src_region, dep_dst_region, dep_rule, dep_dst["name"])
                else:
                    dep_src_region_name = tag_to_region[dep_src["region"]]
                    dep_dst_region_name = tag_to_region[dep_dst["region"]]
                    dep_src_region = world.multiworld.get_region(dep_src_region_name, world.player)
                    dep_dst_region = world.multiworld.get_region(dep_dst_region_name, world.player)
                    dep_src_rule = build_rule_lambda(dep_src["rules"], world)
                    add_edge(state, dep_src_region_name, dep_dst_region_name)
                    print("Delayed Entrance: ", dep_dst["name"])
                    world.create_entrance(dep_src_region, dep_dst_region, dep_src_rule, dep_dst["name"])

    delayed_connections.clear()
    reachable_regions = compute_reachable(state, "Menu")
    unreached_regions = all_regions - reachable_regions - state.unneeded_regions

    # Process remaining zones
    remaining_zones = [
        z for region in state.zones_by_region
        for z in state.zones_by_region[region]
        if z["name"] not in state.used_zones
    ]

    random.shuffle(remaining_zones)
    assert len(remaining_zones) % 2 == 0

    for i in range(0, len(remaining_zones), 2):
        src = remaining_zones[i]
        dst = remaining_zones[i + 1]

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

        print("Remaining Entrance: ", dst["name"])
        world.create_entrance(source_region, target_region, src_rule, dst["name"])
        print("Remaining Entrance: ", src["name"])
        world.create_entrance(target_region, source_region, dst_rule, src["name"])

    print(warp_table)


def has_region_dependency(rule_dict):
    """
    Extract all region dependencies from a rule dictionary.
    Returns a flat list of region names that this rule depends on.
    """
    dependency_list = []

    if not rule_dict:
        return dependency_list

    if isinstance(rule_dict, dict):
        # Check for direct region dependency
        if "can_reach_region" in rule_dict:
            dependency_list.append(rule_dict["can_reach_region"])

        # Recursively check nested rules (and, or conditions)
        for key, value in rule_dict.items():
            if key in ["and", "or"]:
                if isinstance(value, list):
                    for sub_rule in value:
                        # Use extend to flatten the list
                        dependency_list.extend(has_region_dependency(sub_rule))
                else:
                    # Use extend to flatten the list
                    dependency_list.extend(has_region_dependency(value))

    return dependency_list


def is_valid_one_way_arrangement(one_way):
    """Check if the one_way arrangement has no forbidden connections."""
    forbidden_one_ways = ["steeple_boo_background", "glitzville_attic"]
    allowed = 0
    for i in range(len(one_way)):
        a = one_way[i]
        b = one_way[(i + 1) % len(one_way)]  # Wrap around to first element

        # Check if this connection is forbidden
        if a["src_region"] == b["region"] or b["src_region"] == a["region"]:
            return False
        if a["src_region"] in forbidden_one_ways and b["region"] in forbidden_one_ways:
            allowed += 1
            if allowed == 2:
                return False
    return True


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

def unused_zones(state: RegionState, region):
    return [z for z in state.zones_by_region[region] if z["name"] not in state.used_zones]

def mark_used(state: RegionState, *zones):
    for z in zones:
        state.used_zones.add(z["name"])

def mark_unused(state: RegionState, *zones):
    for z in zones:
        state.used_zones.discard(z["name"])


def add_edge(state: RegionState,a: str, b: str, dependencies: list[str] = None):
    state.region_graph[a].add(b)
    if dependencies:
        state.edge_dependencies[(a, b)] = set(dependencies)

def remove_edge(state: RegionState, a: str, b: str):
    state.region_graph[a].discard(b)
    state.edge_dependencies.pop((a, b), None)


def compute_reachable(state: RegionState, start: str, excluding_region: str = None) -> set[str]:
    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        # Get neighbors, filtering out edges dependent on excluded region
        neighbors = set()
        for neighbor in state.region_graph[current]:
            edge = (current, neighbor)
            # Check if this edge has dependencies
            if excluding_region and edge in state.edge_dependencies:
                # Skip this edge if it depends on the excluded region
                if excluding_region in state.edge_dependencies[edge]:
                    continue
            neighbors.add(neighbor)

        queue.extend(neighbors - visited)

    return visited


def get_reachable_regions_excluding_dependencies(state: RegionState, start: str, excluded_region: str) -> set[str]:
    return compute_reachable(state, start, excluding_region=excluded_region)


def create_region(world: "TTYDWorld", name: str, locations: list[LocationData]):
    """Create a region with the given name and locations."""
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, TTYDLocation)
    world.multiworld.regions.append(reg)