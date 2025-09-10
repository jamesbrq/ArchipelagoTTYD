import logging
import os

from Fill import fill_restrictive
from typing import List, Dict, ClassVar, Any
from settings import UserFilePath, Group
from BaseClasses import Tutorial, ItemClassification, CollectionState, Item
from worlds.AutoWorld import WebWorld, World
from .Data import starting_partners, limit_eight, stars, chapter_items, limited_location_ids, limit_pit, \
    pit_exclusive_tattle_stars_required
from .Locations import all_locations, location_table, pit, location_id_to_name, TTYDLocation, locationName_to_data, \
    palace, riddle_tower, tattlesanity_region
from .Options import TTYDOptions, YoshiColor, StartingPartner, PitItems, LimitChapterEight, Goal
from .Items import TTYDItem, itemList, item_frequencies, item_table, ItemData
from .Regions import create_regions, connect_regions, get_regions_dict, register_indirect_connections
from .Rom import TTYDProcedurePatch, write_files
from .Rules import set_rules, get_tattle_rules_dict, set_tattle_rules
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess


def launch_client(*args):
    from .TTYDClient import launch
    launch_subprocess(launch, name="TTYDClient", args=args)


components.append(
    Component(
        "TTYDClient",
        func=launch_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apttyd"),
    ),
)


class TTYDWebWorld(WebWorld):
    theme = 'partyTime'
    bug_report_page = "https://github.com/jamesbrq/ArchipelagoTTYD/issues"
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to setting up Paper Mario; The Thousand Year Door for Archipelago.',
            language='English',
            file_name='setup_en.md',
            link='setup/en',
            authors=['jamesbrq']
        )
    ]


class TTYDSettings(Group):
    class DolphinPath(UserFilePath):
        """
        The location of the Dolphin you want to auto launch patched ROMs with
        """
        is_exe = True
        description = "Dolphin Executable"

    class RomFile(UserFilePath):
        """File name of the TTYD US iso"""
        copy_to = "Paper Mario - The Thousand Year Door.iso"
        description = "US TTYD .iso File"

    dolphin_path: DolphinPath = DolphinPath(None)
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class TTYDWorld(World):
    """
    TTYD
    """
    game = "Paper Mario The Thousand Year Door"
    web = TTYDWebWorld()

    options_dataclass = TTYDOptions
    options: TTYDOptions
    settings: ClassVar[TTYDSettings]
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    required_client_version = (0, 6, 0)
    disabled_locations: set
    excluded_regions: set
    items: List[TTYDItem]
    required_chapters: List[int]
    limited_chapters: List[int]
    limited_chapter_locations: set
    limited_item_names: set
    limited_items: List[TTYDItem]
    limited_state: CollectionState = None

    def generate_early(self) -> None:
        self.disabled_locations = set()
        self.excluded_regions = set()
        self.items = []
        self.required_chapters = []
        self.limited_chapters = []
        self.limited_chapter_locations = set()
        self.limited_item_names = set()
        self.limited_items = []
        if self.options.limit_chapter_eight and self.options.palace_skip:
            logging.warning(f"{self.player_name}'s has enabled both Palace Skip and Limit Chapter 8. "
                            f"Disabling the Limit Chapter 8 option due to incompatibility.")
            self.options.limit_chapter_eight.value = LimitChapterEight.option_false
        if self.options.goal == Goal.option_bonetail and self.options.goal_stars < 5:
            logging.warning(f"{self.player_name}'s has Bonetail as the goal with less than 5 stars required. "
                            f"Increasing number of goal stars to 5 for accessibility.")
            self.options.goal_stars.value = 5
        if self.options.goal != Goal.option_shadow_queen and self.options.palace_stars > self.options.goal_stars:
            logging.warning(f"{self.player_name}'s has more palace stars required than goal stars. "
                            f"Reducing number of stars required to enter the palace of shadow for accessibility.")
            self.options.palace_stars.value = self.options.goal_stars.value
        chapters = [i for i in range(1, 8)]
        for i in range((self.options.palace_stars.value if self.options.goal == Goal.option_shadow_queen else self.options.goal_stars.value)):
            self.required_chapters.append(chapters.pop(self.multiworld.random.randint(0, len(chapters) - 1)))
        if self.options.limit_chapter_logic:
            self.limited_chapters += chapters
        if self.options.limit_chapter_eight:
            self.limited_chapters += [8]
        elif self.options.pit_items == PitItems.option_filler:
            self.options.exclude_locations.value.update(location.name for location in pit if "Pit of 100 Trials" in location.name)
        if self.options.palace_skip:
            self.excluded_regions.update(["Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"])
        if not self.options.tattlesanity:
            self.excluded_regions.update(["Tattlesanity"])
        if self.options.goal != Goal.option_shadow_queen:
            self.excluded_regions.update(["Shadow Queen"])
            if self.options.tattlesanity:
                self.disabled_locations.update(["Tattle: Shadow Queen"])
        if self.options.tattlesanity and self.options.disable_intermissions:
            self.disabled_locations.update(["Tattle: Lord Crump"])
        if self.options.starting_partner == StartingPartner.option_random_partner:
            self.options.starting_partner.value = self.random.randint(1, 7)
        if self.options.yoshi_color == YoshiColor.option_random_color:
            self.options.yoshi_color.value = self.random.randint(0, 6)
        if self.options.tattlesanity:
            extra_disabled = [location.name for name, locations in get_regions_dict().items()
                if name in self.excluded_regions for location in locations]
            for location_name, locations in get_tattle_rules_dict().items():
                if len(locations) == 0:
                    if "Palace of Shadow (Post-Riddle Tower)" in self.excluded_regions:
                        self.disabled_locations.update([location_name])
                else:
                    if all([location_id_to_name[location] in self.disabled_locations or location_id_to_name[location] in extra_disabled for location in locations]):
                        self.disabled_locations.update([location_name])

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        register_indirect_connections(self)
        for chapter in self.limited_chapters:
            self.limited_chapter_locations.update([self.get_location(location_id_to_name[location]) for location in limited_location_ids[chapter - 1]])
        if self.options.tattlesanity:
            self.limit_tattle_locations()
        self.lock_item("Rogueport Center: Goombella", starting_partners[self.options.starting_partner.value - 1])
        self.lock_item("Hooktail's Castle Hooktail's Room: Diamond Star", "Diamond Star")
        self.lock_item("Great Tree Entrance: Emerald Star", "Emerald Star")
        self.lock_item("Glitzville Arena: Gold Star", "Gold Star")
        self.lock_item("Creepy Steeple Upper Room: Ruby Star", "Ruby Star")
        self.lock_item("Pirate's Grotto Cortez' Hoard: Sapphire Star", "Sapphire Star")
        self.lock_item("Poshley Heights Sanctum Altar: Garnet Star", "Garnet Star")
        self.lock_item("X-Naut Fortress Boss Room: Crystal Star", "Crystal Star")
        if self.options.goal == Goal.option_shadow_queen:
            self.lock_item("Shadow Queen", "Victory")
        if self.options.limit_chapter_eight:
            for location in [location for location in palace + riddle_tower if "Palace Key" in location.name]:
                if "Palace Key (Riddle Tower)" in location.name:
                    self.lock_item(location.name, "Palace Key (Riddle Tower)")
                elif "Palace Key" in location.name:
                    self.lock_item(location.name, "Palace Key")
            self.lock_item("Palace of Shadow Gloomtail Room: Star Key", "Star Key")
        if self.options.pit_items == PitItems.option_vanilla:
            self.lock_item("Pit of 100 Trials Floor 10: Sleepy Stomp", "Sleepy Stomp")
            self.lock_item("Pit of 100 Trials Floor 20: Fire Drive", "Fire Drive")
            self.lock_item("Pit of 100 Trials Floor 30: Zap Tap", "Zap Tap")
            self.lock_item("Pit of 100 Trials Floor 40: Pity Flower", "Pity Flower")
            self.lock_item("Pit of 100 Trials Floor 50: Strange Sack", "Strange Sack")
            self.lock_item("Pit of 100 Trials Floor 60: Double Dip", "Double Dip")
            self.lock_item("Pit of 100 Trials Floor 70: Double Dip P", "Double Dip P")
            self.lock_item("Pit of 100 Trials Floor 80: Bump Attack", "Bump Attack")
            self.lock_item("Pit of 100 Trials Floor 90: Lucky Day", "Lucky Day")
            self.lock_item("Pit of 100 Trials Floor 100: Return Postage", "Return Postage")


    def limit_tattle_locations(self):
        for stars_required, locations in pit_exclusive_tattle_stars_required.items():
            if stars_required > len(self.required_chapters):
                self.limited_chapter_locations.update([self.get_location(location) for location in locations if location not in self.disabled_locations])
        for location_name, locations in get_tattle_rules_dict().items():
            if location_name in self.disabled_locations:
                continue
            if self.options.limit_chapter_eight and len(locations) == 0:
                self.limited_chapter_locations.add(self.get_location(location_name))
                continue
            enabled_locations = [location for location in locations if location_id_to_name[location] not in self.disabled_locations]
            if len(enabled_locations) == 0:
                continue
            if self.options.pit_items != PitItems.option_all:
                if all(location in limit_pit for location in enabled_locations):
                    self.limited_chapter_locations.add(self.get_location(location_name))
            if self.options.limit_chapter_logic:
                if len(locations) == 1 and locations[0] == 78780511:
                    if 5 in self.limited_chapters:
                        self.limited_chapter_locations.add(self.get_location(location_name))
                if all(self.get_location(location_id_to_name[location]) in self.limited_chapter_locations for location in enabled_locations):
                    self.limited_chapter_locations.add(self.get_location(location_name))

    def create_items(self) -> None:
        # First add in all progression items
        self.items = []
        self.limited_items = []
        self.limited_state = CollectionState(self.multiworld)
        required_items = []
        precollected = [item for item in itemList if item in self.multiworld.precollected_items[self.player]]
        added_items = 0
        for chapter in self.limited_chapters:
            self.limited_item_names.update(chapter_items[chapter])
        for item in [item for item in itemList if item.progression == ItemClassification.progression]:
            if item not in precollected and item.itemName != starting_partners[self.options.starting_partner.value - 1]:
                freq = item_frequencies.get(item.itemName, 1)
                required_items += [item.itemName for _ in range(freq)]
        for itemName in required_items:
            if itemName in ["Star Key", "Palace Key", "Palace Key (Riddle Tower)"] and self.options.palace_skip:
                continue
            item = self.create_item(itemName)
            if itemName in self.limited_item_names:
                if itemName not in ["Star Key", "Palace Key", "Palace Key (Riddle Tower)"]:
                    self.limited_items.append(item)
                    added_items += 1
            else:
                self.limited_state.collect(item, prevent_sweep=True)
                self.multiworld.itempool.append(item)
                added_items += 1

        useful_items = []
        for item in [item for item in itemList if item.progression == ItemClassification.useful]:
            if item.itemName != starting_partners[self.options.starting_partner.value - 1]:
                freq = item_frequencies.get(item.itemName, 1)
                useful_items += [item.itemName for _ in range(freq)]
        for itemName in useful_items:
            self.items.append(self.create_item(itemName))
            added_items += 1


        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        for item in itemList:
            if item.progression == ItemClassification.filler:
                freq = item_frequencies.get(item.itemName)
                if freq is None:
                    freq = 1
                if self.options.tattlesanity:
                    freq += 2
                filler_items += [item.itemName for _ in range(freq)]

        remaining = len(self.multiworld.get_unfilled_locations(self.player)) - added_items
        for i in range(remaining):
            filler_item_name = self.multiworld.random.choice(filler_items)
            item = self.create_item(filler_item_name)
            self.items.append(item)
            filler_items.remove(filler_item_name)

        if len(self.limited_chapter_locations) > 0:
            self.multiworld.random.shuffle(self.items)
            for _ in range(len(self.limited_chapter_locations) - len(self.limited_items)):
                self.limited_items.append(self.items.pop())

        for item in self.items:
            self.multiworld.itempool.append(item)

    def pre_fill(self) -> None:
        _ = [self.limited_state.collect(location.item, prevent_sweep=True) for location in self.get_locations() if
             location.item is not None and location.item.name not in stars]
        self.multiworld.random.shuffle(self.limited_items)
        self.multiworld.random.shuffle(list(self.limited_chapter_locations))
        fill_restrictive(self.multiworld, self.limited_state, list(self.limited_chapter_locations), self.limited_items, single_player_placement=True, swap=True)

    def set_rules(self) -> None:
        set_rules(self)
        set_tattle_rules(self)
        if self.options.goal == Goal.option_shadow_queen:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        elif self.options.goal == Goal.option_crystal_stars:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("stars", self.player, self.options.goal_stars.value)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Pit of 100 Trials Floor 100: Return Postage", "Location", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "goal_stars": self.options.goal_stars.value,
            "chapter_clears": self.options.palace_stars.value, # TODO: Update name to palace_stars once ready to deprecate
            "pit_items": self.options.pit_items.value,
            "limit_chapter_logic": self.options.limit_chapter_logic.value,
            "limit_chapter_eight": self.options.limit_chapter_eight.value,
            "palace_skip": self.options.palace_skip.value,
            "yoshi_color": self.options.yoshi_color.value,
            "westside": self.options.open_westside.value,
            "tattlesanity": self.options.tattlesanity.value,
            "disable_intermissions": self.options.disable_intermissions.value,
            "cutscene_skip": self.options.cutscene_skip.value,
            "death_link": self.options.death_link.value,
        }

    def create_item(self, name: str) -> TTYDItem:
        item = item_table.get(name, ItemData(None, name, ItemClassification.progression))
        progression = (ItemClassification.useful if item.itemName == "Goombella" and not self.options.tattlesanity else item.progression)
        return TTYDItem(item.itemName, progression, item.code, self.player)

    def lock_item(self, location: str, item_name: str):
        item = self.create_item(item_name)
        self.get_location(location).place_locked_item(item)

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filter(lambda item: item.progression == ItemClassification.filler, itemList))).itemName

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change:
            if item.name in stars:
                state.prog_items[item.player]["stars"] += 1
            for star in self.required_chapters:
                if item.name == stars[star - 1]:
                    state.prog_items[item.player]["required_stars"] += 1
                    break
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change:
            if item.name in stars:
                state.prog_items[item.player]["stars"] -= 1
            for star in self.required_chapters:
                if item.name == stars[star - 1]:
                    state.prog_items[item.player]["required_stars"] -= 1
                    break
        return change

    def generate_output(self, output_directory: str) -> None:
        patch = TTYDProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_files(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
