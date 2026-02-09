import typing

from BaseClasses import Region
from .Locations import (TTYDLocation, shadow_queen, LocationData)
from . import StateLogic, get_locations_by_tags
import json
import pkgutil
import random
from .Data import warp_table
from .Rules import _build_single_lambda
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
        ("Menu", "Rogueport Center"): None,
        ("Rogueport West Tall Pipe", "Rogueport West"): None,
        ("Rogueport Sewers East", "Rogueport Sewers East Bobbery Pipe"): 
        lambda state: state.has("Bobbery", world.player),
        ("Rogueport Sewers East Bobbery Pipe", "Rogueport Sewers East"): 
        lambda state: state.has("Bobbery", world.player),
        ("Rogueport Sewers East", "Rogueport Sewers East Fortune"):
        lambda state: state.has("Paper Mode", world.player),
        ("Rogueport Sewers East Fortune", "Rogueport Sewers East"): None,
        ("Rogueport Sewers East", "Rogueport Sewers East Plane Mode"):
        lambda state: state.has("Plane Mode", world.player),
        ("Rogueport Sewers East Plane Mode", "Rogueport Sewers East"): None,
        ("Rogueport Sewers East Top", "Rogueport Sewers East"): None,
        ("Rogueport Sewers East Top", "Rogueport Sewers East Fortune"):
        lambda state: state.has("Yoshi", world.player),
        ("Rogueport Sewers East Top", "Rogueport Sewers East Plane Mode"): None,
        ("Rogueport Sewers Blooper", "Rogueport Sewers Blooper Pipe"): None,
        ("Rogueport Sewers Town", "Rogueport Sewers Town Dazzle"):
        lambda state: StateLogic.fallen_pipe(state, world.player),
        ("Rogueport Sewers Town Dazzle", "Rogueport Sewers Town"):
        lambda state: StateLogic.fallen_pipe(state, world.player),
        ("Rogueport Sewers Town Teleporter", "Rogueport Sewers Town"): None,
        ("Rogueport Sewers Town", "Rogueport Sewers Town Teleporter"): None,
        ("Rogueport Sewers West", "Rogueport Sewers West West"):
        lambda state: state.has("Yoshi", world.player),
        ("Rogueport Sewers West West", "Rogueport Sewers West"):
        lambda state: state.has("Yoshi", world.player),
        ("Rogueport Sewers West", "Rogueport Sewers West Bottom"): None,
        ("Rogueport Sewers West West", "Rogueport Sewers West Bottom"): None,
        ("Rogueport Sewers West Bottom", "Rogueport Sewers West West"):
        lambda state: StateLogic.ultra_boots(state, world.player),
        ("Rogueport Sewers West West", "Rogueport Sewers West Fahr"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers West Fahr", "Rogueport Sewers West West"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers East Enemy Hall", "Rogueport Sewers East Enemy Hall Barred Door"):
        lambda state: state.has("Paper Mode", world.player),
        ("Rogueport Sewers East Enemy Hall Barred Door", "Rogueport Sewers East Enemy Hall"):
        lambda state: state.has("Paper Mode", world.player),
        ("Rogueport Sewers West Enemy Hall", "Rogueport Sewers West Enemy Hall Flurrie"):
        lambda state: state.has("Flurrie", world.player),
        ("Rogueport Sewers West Enemy Hall Flurrie", "Rogueport Sewers West Enemy Hall"):
        lambda state: state.has("Flurrie", world.player),
        ("Rogueport Sewers West Warp Room Left", "Rogueport Sewers West Warp Room Right"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers West Warp Room Right", "Rogueport Sewers West Warp Room Left"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers West Warp Room Left", "Rogueport Sewers West Warp Room Top"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers West Warp Room Top", "Rogueport Sewers West Warp Room Left"): None,
        ("Rogueport Sewers West Warp Room Right", "Rogueport Sewers West Warp Room Top"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers West Warp Room Top", "Rogueport Sewers West Warp Room Right"): None,
        ("Rogueport Sewers East Warp Room Left", "Rogueport Sewers East Warp Room Right"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers East Warp Room Right", "Rogueport Sewers East Warp Room Left"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers East Warp Room Left", "Rogueport Sewers East Warp Room Top"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers East Warp Room Top", "Rogueport Sewers East Warp Room Left"): None,
        ("Rogueport Sewers East Warp Room Right", "Rogueport Sewers East Warp Room Top"):
        lambda state: StateLogic.ultra_hammer(state, world.player),
        ("Rogueport Sewers East Warp Room Top", "Rogueport Sewers East Warp Room Right"): None,
        ("Rogueport Sewers Black Key Room", "Rogueport Sewers Black Key Room Puni Door"):
        lambda state: state.has("Paper Mode", world.player),
        ("Rogueport Sewers Black Key Room Puni Door", "Rogueport Sewers Black Key Room"):
        lambda state: state.has("Paper Mode", world.player),
        ("Rogueport Sewers Puni Room", "Rogueport Sewers Puni Room Exit"): None,
        ("Petal Meadows Bridge West", "Petal Meadows Bridge East"): None,
        ("Hooktail's Castle Drawbridge East Bottom", "Hooktail's Castle Drawbridge West Bottom"):
        lambda state: state.has("Yoshi", world.player),
        ("Hooktail's Castle Drawbridge West Bottom", "Hooktail's Castle Drawbridge East Bottom"): None,
        ("Hooktail's Castle Drawbridge East Top", "Hooktail's Castle Drawbridge East Bottom"): None,
        ("Hooktail's Castle Drawbridge East Top", "Hooktail's Castle Drawbridge West Bottom"): 
        lambda state: state.has("Plane Mode", world.player),
        ("Hooktail's Castle Drawbridge West Top", "Hooktail's Castle Drawbridge West Bottom"): None,
        ("Hooktail's Castle Stair Switch Room Upper Level", "Hooktail's Castle Stair Switch Room"): None,
        ("Hooktail's Life Shroom Room", "Hooktail's Life Shroom Room Upper Level"):
        lambda state: StateLogic.partner_press_switch(state, world.player),
        ("Hooktail's Life Shroom Room Upper Level", "Hooktail's Life Shroom Room"): None,
        ("Hooktail's Castle Central Staircase Upper Level", "Hooktail's Castle Central Staircase"): None,
        ("boggly_plane_panel", "boggly_plane_panel_upper"):
        lambda state: state.has("Plane Mode", world.player),
        ("boggly_plane_panel_upper", "boggly_plane_panel"): None,
        ("boggly_flurrie_outside", "boggly_flurrie_outside_grass"):
        lambda state: state.has("Paper Mode", world.player),
        ("boggly_flurrie_outside_grass", "boggly_flurrie_outside"):
        lambda state: state.has("Paper Mode", world.player),

        ("Rogueport Sewers Blooper Pipe", "Petal Meadows (Left)"): None,
        ("Petal Meadows (Left)", "Petal Meadows (Right)"): None,\
        ("Rogueport Sewers East Warp Room Top", "Petal Meadows (Right)"): None,
        ("Petal Meadows (Left)", "Hooktail's Castle"): 
        lambda state: StateLogic.hooktails_castle(state, world.player),
        ("Rogueport Sewers Puni Room Exit", "Boggly Woods"): None,
        ("Boggly Woods", "Great Tree"): None,
        ("Great Tree", "Boggly Woods"): None,
        ("Rogueport Sewers East Warp Room Top", "Great Tree"): None,
        ("Rogueport Blimp", "Glitzville"): 
        lambda state: state.has("Blimp Ticket", world.player),
        ("Rogueport Sewers Twilight", "Twilight Town"): None,
        ("Twilight Town", "Twilight Trail"): 
        lambda state: StateLogic.tube_curse(state, world.player),
        ("Twilight Trail", "Creepy Steeple"): 
        lambda state: StateLogic.steeple(state, world.player),
        ("Rogueport Docks", "Keelhaul Key"): 
        lambda state: StateLogic.keelhaul_key,
        ("Keelhaul Key", "Pirate's Grotto"): 
        lambda state: StateLogic.pirates_grotto,
        ("Rogueport Blimp", "Excess Express"): 
        lambda state: StateLogic.excess_express,
        ("Excess Express", "Riverside Station"): 
        lambda state: StateLogic.riverside,
        ("Riverside Station", "Poshley Heights"): 
        lambda state: StateLogic.poshley_heights,
        ("Rogueport Sewers West Fahr", "Fahr Outpost"): None,
        ("Fahr Outpost", "X-Naut Fortress"): 
        lambda state: StateLogic.moon,
        ("TTYD", "Palace of Shadow"): 
        lambda state: StateLogic.palace(state, world, world.options.palace_stars.value),
        ("Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"): 
        lambda state: StateLogic.riddle_tower(state, world.player),
        ("Rogueport Sewers Pit Room", "Pit of 100 Trials"): 
        lambda state: StateLogic.pit(state, world.player),
        ("Menu", "Tattlesanity"): None,
        ("TTYD", "Shadow Queen"):
        lambda state: StateLogic.palace(state, world, world.options.goal_stars.value)
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

    connections_dict = get_region_connections_dict(world)
    zones = get_zone_dict_from_json()
    names: typing.Dict[str, int] = {}
    reachable_regions = {"Menu", "Rogueport Center"}

    for (source, target), rule in connections_dict.items():
        # Skip connections where either the source or target is in excluded_regions
        if source in world.excluded_regions or target in world.excluded_regions:
            continue
        if source == "Rogueport" and target == "Shadow Queen" and not world.options.palace_skip:
            continue
        if source == "Menu" and target == "Rogueport (Westside)" and not world.options.open_westside:
            continue

        # Verify that both regions exist before trying to connect them
        try:
            world.multiworld.get_region(source, world.player)
            world.multiworld.get_region(target, world.player)
            connect(world, names, source, target, rule)
            add_edge(source, target)
        except Exception:
            continue


    tag_to_region = get_region_name_by_tag()

    for z in zones.values():
        if "is_vanilla" in z or not world.options.loading_zone:
            vanilla.append(z)
        elif z["target"] == "One Way":
            one_way.append(z)
        elif z["target"] == "":
            continue
        else:
            region = tag_to_region.get(z["region"])
            zones_by_region[region].append(z)

    all_regions = set(zones_by_region.keys())
    unreached_regions = all_regions - reachable_regions

    for src in vanilla:
        if not (src["target"] == "" or src["target"] == "One Way" or src["target"] == "filler"):
            dst = zones[src["target"]]

            src_region = tag_to_region[src["region"]]
            dst_region = tag_to_region[dst["region"]]
            rule = build_rule_lambda(src.get("rules"), world)

            connect(world, names, src_region, dst_region, rule)
            add_edge(src_region, dst_region)
        elif src["target"] == "One Way":
            source = src["src_region"]
            target = src["region"]
            rule = build_rule_lambda(src.get("rules"), world)
            try:
                world.multiworld.get_region(source, world.player)
                world.multiworld.get_region(target, world.player)
                connect(world, names, source, target, rule)
            except Exception:
                continue

    while unreached_regions:
        # pick a reachable region with unused zones
        src_region_contenders = [
            r for r in reachable_regions if unused_zones(r)
        ]

        src_region = random.choice(src_region_contenders)
        dst_region = random.choice(list(unreached_regions))

        src_zone_contenders = unused_zones(src_region)
        dst_zone_contenders = unused_zones(dst_region)
        if len(src_region_contenders) == 1 and len(src_zone_contenders) == 1 and len(dst_zone_contenders) == 1 and len(unreached_regions) != 1:
            continue
        
        src_zone = random.choice(src_zone_contenders)
        dst_zone = random.choice(dst_zone_contenders)
        src_target = zones[src_zone["target"]]
        dst_target = zones[dst_zone["target"]]
        src_rule = build_rule_lambda(src_zone.get("rules"), world)
        dst_rule = build_rule_lambda(dst_zone.get("rules"), world)

        # warp wiring
        warp_table[(src_target["map"], src_target["bero"])] = (dst_zone["map"], dst_zone["bero"])
        warp_table[(dst_target["map"], dst_target["bero"])] = (src_zone["map"], src_zone["bero"])

        connect(world, names, src_region, dst_region, src_rule)
        connect(world, names, dst_region, src_region, dst_rule)

        mark_used(src_zone, dst_zone)

        add_edge(src_region, dst_region)
        add_edge(dst_region, src_region)
        reachable_regions = compute_reachable("Menu")
        unreached_regions = all_regions - reachable_regions


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

        src_region = tag_to_region[src["region"]]
        dst_region = tag_to_region[dst["region"]]

        src_target = zones[src["target"]]
        dst_target = zones[dst["target"]]

        src_rule = build_rule_lambda(src.get("rules"), world)
        dst_rule = build_rule_lambda(dst.get("rules"), world)

        warp_table[(src_target["map"], src_target["bero"])] = (dst_zone["map"], dst_zone["bero"])
        warp_table[(dst_target["map"], dst_target["bero"])] = (src_zone["map"], src_zone["bero"])

        connect(world, names, src_region, dst_region, src_rule)
        connect(world, names, dst_region, src_region, dst_rule)
    
    random.shuffle(one_way)

    for i in range(len(one_way)):
        if i < len(one_way) - 1:
            a = one_way[i]
            b = one_way[i+ 1]
        else:
            a = one_way[i]
            b= one_way[0]
        warp_table[(a["map"], a["bero"])] = (b["map"], b["bero"])
        source = a["src_region"]
        target = b["region"]
        rule = build_rule_lambda(a.get("rules"), world)
        try:
            world.multiworld.get_region(source, world.player)
            world.multiworld.get_region(target, world.player)
            connect(world, names, source, target, rule)
        except Exception:
            continue


        
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
        return None
    return _build_single_lambda(rule_json, world)

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


def register_indirect_connections(world: "TTYDWorld"):
    print("something")


def create_region(world: "TTYDWorld", name: str, locations: list[LocationData]):
    """Create a region with the given name and locations."""
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, TTYDLocation)
    world.multiworld.regions.append(reg)


def connect(world: "TTYDWorld",
            used_names: typing.Dict[str, int],
            source: str,
            target: str,
            rule: typing.Optional[typing.Callable] = None):
    """Connect two regions with an optional access rule."""
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    source_region.connect(target_region, name, rule)
