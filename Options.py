from Options import Range, StartInventoryPool, PerGameCommonOptions, Choice, FreeText, Toggle, DeathLink, \
    DefaultOnToggle
from dataclasses import dataclass


class Goal(Choice):
    """
    This determines the goal of the game.
    shadow_queen: Defeat the Shadow Queen.
    crystal_stars: Collect a specified amount of Crystal Stars.
    bonetail: Defeat Bonetail.
    """
    display_name = "Goal"
    option_shadow_queen = 0
    option_crystal_stars = 1
    option_bonetail = 2
    default = 0


class GoalStars(Range):
    """
    This determines how many crystal stars are required for the goal option crystal_stars.
    This is only used if the goal option is set to crystal_stars.
    """
    display_name = "Goal Crystal Stars"
    range_start = 1
    range_end = 7
    default = 7


class PalaceStars(Range):
    """
    This determines how many Crystal Stars are required to enter the Palace of Shadow.
    """
    display_name = "Palace Crystal Stars"
    range_start = 0
    range_end = 7
    default = 7


class PitItems(Choice):
    """
    This determines what type of items are in the Pit of 100 Trials.
    vanilla: The locations contain the same items as the original game, and the locations themselves will not be created.
    filler: The locations will be marked as excluded.
    all: The locations can contain any item.
    """
    display_name = "Pit Items"
    option_vanilla = 0
    option_filler = 1
    option_all = 2
    default = 1


class TattleSanityOption(Toggle):
    """
    Creates a location for every enemy being tattled.
    All key items can possibly be placed in these locations.
    """
    display_name = "Tattlesanity"


class Piecesanity(DefaultOnToggle):
    """
    Determines if Star Piece locations will be randomized.
    vanilla: Star Piece locations will remain in their original locations.
    nonpanel_only: Only Star Pieces that are not in panels will be randomized.
    all: All Star Pieces will be randomized.
    """
    display_name = "Star Piecesanity"
    option_vanilla = 0
    option_nonpanel_only = 1
    option_all = 2
    default = 2


class Shopsanity(DefaultOnToggle):
    """
    Shop items will be randomized.
    This includes only regular shops.
    """
    display_name = "Shopsanity"


class LimitChapterLogic(Toggle):
    """
    Progression items will only appear in required chapters, and in common areas. You will not need to
    check the chapters that are out of logic whatsoever. You can still visit them for local items (badges, consumables, etc) if you want or need to.
    """
    display_name = "Limit Chapter Logic"


class LimitChapterEight(Toggle):
    """
    All chapter 8 keys items will be placed in vanilla locations.
    All other locations will have local non-progression items.
    """
    display_name = "Limit Chapter 8"


class PalaceSkip(Toggle):
    """
    Entering the Thousand-Year door will take you straight to Grodus.
    """
    display_name = "Palace Skip"


class CutsceneSkip(Toggle):
    """
    Skips some of the longer cutscenes in the game,
    such as the Shadow Queen cutscene, Fahr Outpost Cannon etc.
    """
    display_name = "Skip Cutscenes"


class OpenWestside(Toggle):
    """
    Rogueport Westside is open from the start.
    """
    display_name = "Open West Side"


class PermanentPeekaboo(Toggle):
    """
    The Peekaboo badge is always active, even when not equipped.
    """
    display_name = "Permanent Peekaboo"


class FullRunBar(Toggle):
    """
    The run bar in battle always starts at 100 percent.
    """
    display_name = "Full Run Bar"


class DisableIntermissions(Toggle):
    """
    After obtaining a crystal star, mario will stay in the boss' room,
    and the sequence will be updated past the intermission.
    """
    display_name = "Disable Intermissions"


class FastTravel(Toggle):
    """
    Enable this to gain the ability to warp to any area you have visited from the map
    screen in the main menu. Press A on the destination to open the warp confirmation dialog.
    """
    display_name = "Fast Travel"


class AlwaysSucceedConditions(Toggle):
    """
    Enable this to make it so the battle condition in fights in the Glitz Pit
    will always be fulfilled, regardless of their actual fulfillment.
    """
    display_name = "Always Succeed Conditions"


class ZeroBPFirstAttack(Toggle):
    """
    The First Attack badge costs 0 BP, just like the remake.
    """
    display_name = "0 BP First Attack"


class MusicSettings(Choice):
    """
    Choose in-game music settings.
    normal: Music will not change.
    silent: No music will play at all.
    randomized: Music will be randomized.
    """
    display_name = "Music Settings"
    option_normal = 0
    option_silent = 1
    option_randomized = 2
    default = 0


class BlockVisibility(Choice):
    """
    Choose how visible item blocks are.
    normal: All blocks will keep their vanilla visibility.
    all_visible: All blocks will be visible.
    """
    display_name = "Block Visibility"
    option_normal = 0
    option_all_visible = 1
    default = 0


class ExperienceMultiplier(Range):
    """
    Multiplies the experience you gain from battles.
    """
    display_name = "Experience Multiplier"
    range_start = 0
    range_end = 10
    default = 1


class StartingHP(Range):
    """
    How much health you start with.
    """
    display_name = "Starting HP"
    range_start = 1
    range_end = 100
    default = 10


class StartingFP(Range):
    """
    How much flower points you start with.
    """
    display_name = "Starting FP"
    range_start = 0
    range_end = 100
    default = 5


class StartingBP(Range):
    """
    How many badge points you start with.
    """
    display_name = "Starting BP"
    range_start = 0
    range_end = 99
    default = 3


class StartingLevel(Range):
    """
    What level you start at.
    """
    display_name = "Starting Level"
    range_start = 1
    range_end = 99
    default = 1


class StartingCoins(Range):
    """
    How many coins you start with.
    """
    display_name = "Starting Coins"
    range_start = 0
    range_end = 999
    default = 100


class StartingPartner(Choice):
    """
    Choose the partner that you start with.
    """
    display_name = "Starting Partner"
    option_goombella = 1
    option_koops = 2
    option_bobbery = 3
    option_yoshi = 4
    option_flurrie = 5
    option_vivian = 6
    option_ms_mowz = 7
    option_random_partner = 8
    default = 1


class YoshiColor(Choice):
    """
    Select the color of your Yoshi partner.
    """
    display_name = "Yoshi Color"
    option_green = 0
    option_red = 1
    option_blue = 2
    option_orange = 3
    option_pink = 4
    option_black = 5
    option_white = 6
    option_random_color = 7
    default = 0


class YoshiName(FreeText):
    """
    Set the name of your Yoshi partner.
    This has a maximum length of 8 characters.
    """
    display_name = "Yoshi Name"
    default = "Yoshi"


@dataclass
class TTYDOptions(PerGameCommonOptions):
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    goal_stars: GoalStars
    palace_stars: PalaceStars
    tattlesanity: TattleSanityOption
    piecesanity: Piecesanity
    shopsanity: Shopsanity
    pit_items: PitItems
    limit_chapter_logic: LimitChapterLogic
    limit_chapter_eight: LimitChapterEight
    palace_skip: PalaceSkip
    cutscene_skip: CutsceneSkip
    disable_intermissions: DisableIntermissions
    fast_travel: FastTravel
    succeed_conditions: AlwaysSucceedConditions
    open_westside: OpenWestside
    permanent_peekaboo: PermanentPeekaboo
    full_run_bar: FullRunBar
    first_attack: ZeroBPFirstAttack
    music_settings: MusicSettings
    block_visibility: BlockVisibility
    experience_multiplier: ExperienceMultiplier
    starting_hp: StartingHP
    starting_fp: StartingFP
    starting_bp: StartingBP
    starting_coins: StartingCoins
    starting_level: StartingLevel
    starting_partner: StartingPartner
    yoshi_color: YoshiColor
    yoshi_name: YoshiName
