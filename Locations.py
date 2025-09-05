import typing

from BaseClasses import Location
from .Data import Rels


class LocationData:
    name: str = ""
    id: int | None = 0x0
    rel: Rels = None
    offset: typing.List[int] = []

    def __init__(self, name: str, id_: int | None, rel: Rels, offset: typing.List[int]=None):
        self.name = name
        self.id = id_
        self.rel = rel
        self.offset = [] if offset is None else offset


class TTYDLocation(Location):
    game: str = "Paper Mario The Thousand Year Door"


rogueport: typing.List[LocationData] = [
    LocationData("Rogueport Docks: HP Drain", 78780000, Rels.gor, [0x2C624]),
    LocationData("Rogueport Docks: Star Piece", 78780001, Rels.gor, [0x2F460]),
    LocationData("Rogueport Docks: Star Piece 2", 78780706, Rels.gor, [0x2F49C]),
    LocationData("Rogueport Center: Goombella", 78780002, Rels.gor, [0x37F88]),
    #LocationData("Rogueport Center: Contact Lens", 78780808, Rels.gor, [0x36C8C]),
    LocationData("Rogueport Center: Old Letter", 78780004, Rels.gor, [0x3222C]),
    #LocationData("Rogueport Center: Attack FX G", 78780005, Rels.gor),
    #LocationData("Rogueport Center: Attack FX P", 78780006, Rels.gor),
    #LocationData("Rogueport Center: Boo's Sheet", 78780007, Rels.gor),
    #LocationData("Rogueport Center: Close Call", 78780008, Rels.gor),
    #LocationData("Rogueport Center: Close Call P", 78780009, Rels.gor),
    #LocationData("Rogueport Center: Damage Dodge", 78780010, Rels.gor),
    #LocationData("Rogueport Center: Damage Dodge P", 78780011, Rels.gor),
    #LocationData("Rogueport Center: Double Pain", 78780012, Rels.gor),
    #LocationData("Rogueport Center: Dried Shroom", 78780013, Rels.gor),
    #LocationData("Rogueport Center: Earthquake", 78780014, Rels.gor),
    #LocationData("Rogueport Center: Fire Drive", 78780015, Rels.gor),
    LocationData("Rogueport Center: Fire Flower", 78780003, Rels.gor, [0x36C74, 0x36CA4]),
    #LocationData("Rogueport Center: First Attack", 78780017, Rels.gor),
    #LocationData("Rogueport Center: FP Drain", 78780018, Rels.gor),
    LocationData("Rogueport Center: Fright Mask", 78780019, Rels.gor, [0x36C84, 0x36CB4]),
    #LocationData("Rogueport Center: Hammerman", 78780020, Rels.gor),
    #LocationData("Rogueport Center: Happy Flower", 78780021, Rels.gor),
    #LocationData("Rogueport Center: Head Rattle", 78780022, Rels.gor),
    LocationData("Rogueport Center: Honey Syrup", 78780023, Rels.gor, [0x36C64, 0x36C94]),
    #LocationData("Rogueport Center: Ice Smash", 78780024, Rels.gor),
    #LocationData("Rogueport Center: Jammin' Jelly", 78780025, Rels.gor),
    #LocationData("Rogueport Center: Jumpman", 78780026, Rels.gor),
    #LocationData("Rogueport Center: Last Stand", 78780027, Rels.gor),
    #LocationData("Rogueport Center: Last Stand P", 78780028, Rels.gor),
    #LocationData("Rogueport Center: Mega Rush", 78780029, Rels.gor),
    LocationData("Rogueport Center: Mushroom", 78780030, Rels.gor, [0x36C5C, 0x36C8C]),
    #LocationData("Rogueport Center: Piercing Blow", 78780031, Rels.gor),
    #LocationData("Rogueport Center: Power Jump", 78780032, Rels.gor),
    #LocationData("Rogueport Center: Power Rush", 78780033, Rels.gor),
    #LocationData("Rogueport Center: Power Rush P", 78780034, Rels.gor),
    #LocationData("Rogueport Center: Pretty Lucky P", 78780035, Rels.gor),
    #LocationData("Rogueport Center: Repel Cape", 78780036, Rels.gor),
    #LocationData("Rogueport Center: Shooting Star", 78780037, Rels.gor),
    #LocationData("Rogueport Center: Shrink Stomp", 78780038, Rels.gor),
    #LocationData("Rogueport Center: Simplifier", 78780039, Rels.gor),
    #LocationData("Rogueport Center: Simplifier (6 Chapters Cleared)", 78780040, Rels.gor),
    LocationData("Rogueport Center: Sleepy Sheep", 78780041, Rels.gor, [0x36C7C, 0x36CAC]),
    #LocationData("Rogueport Center: Sleepy Stomp", 78780042, Rels.gor),
    #LocationData("Rogueport Center: Slow Go", 78780043, Rels.gor),
    #LocationData("Rogueport Center: Soft Stomp", 78780044, Rels.gor),
    LocationData("Rogueport Center: Star Piece 1", 78780045, Rels.gor, [0x3C554]),
    LocationData("Rogueport Center: Star Piece 2", 78780046, Rels.gor, [0x3C578]),
    LocationData("Rogueport Center: Star Piece 3", 78780047, Rels.gor, [0x3C58C]),
    LocationData("Rogueport Center: Star Piece 4", 78780048, Rels.gor, [0x3C5B4]),
    LocationData("Rogueport Center: Star Piece 5", 78780049, Rels.gor, [0x3C5DC]),
    #LocationData("Rogueport Center: Stopwatch", 78780050, Rels.gor),
    #LocationData("Rogueport Center: Super Appeal", 78780051, Rels.gor),
    #LocationData("Rogueport Center: Super Appeal P", 78780052, Rels.gor),
    LocationData("Rogueport Center: Tasty Tonic", 78780053, Rels.gor, [0x36C6C, 0x36C9C]),
    #LocationData("Rogueport Center: Timing Tutor", 78780054, Rels.gor),
    LocationData("Rogueport Center: Ultra Hammer", 78780055, Rels.gor, [0x39344]),
    #LocationData("Rogueport Center: Ultra Shroom", 78780056, Rels.gor),
    #LocationData("Rogueport Center: Unsimplifier", 78780057, Rels.gor),
    #LocationData("Rogueport Center: Unsimplifier (6 Chapters Cleared)", 78780058, Rels.gor),
    #LocationData("Rogueport Center: W Emblem", 78780059, Rels.gor),
    LocationData("Rogueport Eastside: Power Smash", 78780060, Rels.gor, [0x49BF0]),
    LocationData("Rogueport Eastside: Double Dip", 78780061, Rels.gor, [0x4CE58]),
    LocationData("Rogueport Eastside: Shine Sprite 1", 78780062, Rels.gor, [0x4D76C]),
    LocationData("Rogueport Eastside: Shine Sprite 2", 78780708, Rels.gor, [0x4D7B4]),
    LocationData("Rogueport Eastside: Shine Sprite 3", 78780707, Rels.gor, [0x4D790]),
    LocationData("Rogueport Eastside: Star Piece 1", 78780064, Rels.gor, [0x4D7CC]),
    LocationData("Rogueport Eastside: Star Piece 2", 78780065, Rels.gor, [0x4D700]),
    LocationData("Rogueport Eastside: Star Piece 3", 78780066, Rels.gor, [0x4D7F4]),
    LocationData("Rogueport Eastside: Star Piece 4", 78780067, Rels.gor, [0x4D81C]),
    LocationData("Rogueport Eastside: Star Piece 5", 78780068, Rels.gor, [0x4D724]),
]

rogueport_westside: typing.List[LocationData] = [
    LocationData("Rogueport Westside: Blimp Ticket", 78780069, Rels.gor, [0x4E0E4]),
    LocationData("Rogueport Westside: Train Ticket", 78780070, Rels.gor, [0x506C4]),
    #LocationData("Rogueport Westside: Cake Mix", 78780071, Rels.dol, [0x3C7278]),
    LocationData("Rogueport Westside: Dizzy Dial", 78780072, Rels.gor, [0x57B90]),
    LocationData("Rogueport Westside: Dried Shroom", 78780073, Rels.gor, [0x57B80]),
    #LocationData("Rogueport Westside: FP Plus", 78780074, Rels.dol, [0x3C7294]),
    #LocationData("Rogueport Westside: Gold Bar x3", 78780075, Rels.dol, [0x3C729C]),
    #LocationData("Rogueport Westside: Hammer Throw", 78780076, Rels.dol, [0x3C72B0]),
    #LocationData("Rogueport Westside: HP Plus", 78780077, Rels.dol, [0x3C7290]),
    #LocationData("Rogueport Westside: HP Plus P", 78780078, Rels.dol, [0x3C72A4]),
    #LocationData("Rogueport Westside: Jammin' Jelly", 78780079, Rels.dol, [0x3C72D0]),
    LocationData("Rogueport Westside: Life Shroom", 78780080, Rels.gor, [0x57B88]),
    #LocationData("Rogueport Westside: Maple Syrup", 78780701, Rels.dol, [0x3C7288]),
    #LocationData("Rogueport Westside: Money Money", 78780081, Rels.dol, [0x3C72C8]),
    #LocationData("Rogueport Westside: Multibounce", 78780700, Rels.dol, [0x3C72A8]),
    LocationData("Rogueport Westside: Lottery", 78780082, Rels.gor, [0x59E18]),
    #LocationData("Rogueport Westside: Power Jump", 78780083, Rels.dol, [0x3C728C]),
    #LocationData("Rogueport Westside: Power Rush", 78780084, Rels.dol, [0x3C72B4]),
    #LocationData("Rogueport Westside: Power Rush P", 78780085, Rels.dol, [0x3C72BC]),
    #LocationData("Rogueport Westside: Power Smash", 78780086, Rels.dol, [0x3C72A0]),
    #LocationData("Rogueport Westside: Quake Hammer", 78780087, Rels.dol, [0x3C72C4]),
    #LocationData("Rogueport Westside: Refund", 78780088, Rels.dol, [0x3C7280]),
    LocationData("Rogueport Westside: Shine Sprite 1", 78780089, Rels.gor, [0x5A68C]),
    LocationData("Rogueport Westside: Shine Sprite 2", 78780090, Rels.gor, [0x5A668]),
    LocationData("Rogueport Westside: Star Piece 1", 78780091, Rels.gor, [0x5A5C0]),
    LocationData("Rogueport Westside: Star Piece 2", 78780092, Rels.gor, [0x5A5E8]),
    LocationData("Rogueport Westside: Star Piece 3", 78780093, Rels.gor, [0x5A610]),
    LocationData("Rogueport Westside: Star Piece 4", 78780094, Rels.gor, [0x5A648]),
    #LocationData("Rogueport Westside: Super Appeal", 78780095, Rels.dol, [0x3C727C]),
    LocationData("Rogueport Westside: Super Shroom 1", 78780096, Rels.gor, [0x57B70]),
    #LocationData("Rogueport Westside: Super Shroom 2", 78780097, Rels.dol, [0x3C7274]),
    LocationData("Rogueport Westside: Thunder Bolt", 78780098, Rels.gor, [0x57B98]),
    #LocationData("Rogueport Westside: Tornado Jump", 78780099, Rels.dol, [0x3C72B8]),
    #LocationData("Rogueport Westside: Ultra Shroom", 78780100, Rels.dol, [0x3C72CC]),
    LocationData("Rogueport Westside: Volt Shroom", 78780102, Rels.gor, [0x57B78]),
    LocationData("Rogueport Blimp Room: Star Piece 1", 78780103, Rels.gor, [0x60480]),
    LocationData("Rogueport Blimp Room: Star Piece 2", 78780104, Rels.gor, [0x6046C])
]

sewers: typing.List[LocationData] = [
    #LocationData("Rogueport Sewers Town: Attack FX Y", 78780105, Rels.dol, [0x3AA038]),
    #LocationData("Rogueport Sewers Town: Chill Out", 78780106, Rels.dol, [0x3AA03C]),
    #LocationData("Rogueport Sewers Town: Flower Finder", 78780107, Rels.dol, [0x3AA058]),
    #LocationData("Rogueport Sewers Town: Flower Saver", 78780108, Rels.dol, [0x3AA064]),
    #LocationData("Rogueport Sewers Town: Flower Saver P", 78780109, Rels.dol, [0x3AA068]),
    #LocationData("Rogueport Sewers Town: Happy Flower", 78780113, Rels.dol, [0x3AA044]),
    #LocationData("Rogueport Sewers Town: Happy Heart", 78780114, Rels.dol, [0x3AA048]),
    #LocationData("Rogueport Sewers Town: Happy Heart P", 78780115, Rels.dol, [0x3AA04C]),
    #LocationData("Rogueport Sewers Town: Heart Finder", 78780116, Rels.dol, [0x3AA054]),
    #LocationData("Rogueport Sewers Town: Item Hog", 78780117, Rels.dol, [0x3AA050]),
    #LocationData("Rogueport Sewers Town: Peekaboo", 78780119, Rels.dol, [0x3AA05C]),
    #LocationData("Rogueport Sewers Town: Power Plus", 78780120, Rels.dol, [0x3AA06C]),
    #LocationData("Rogueport Sewers Town: Power Plus P", 78780121, Rels.dol, [0x3AA070]),
    #LocationData("Rogueport Sewers Town: Pretty Lucky", 78780122, Rels.dol, [0x3AA040]),
    #LocationData("Rogueport Sewers Town: Quick Change", 78780123, Rels.dol, [0x3AA060]),
    LocationData("Rogueport Sewers Town: Star Piece 1", 78780127, Rels.tik, [0x13570]),
    LocationData("Rogueport Sewers East Entrance: Star Piece", 78780132, Rels.tik, [0x14CC8]),
    LocationData("Rogueport Sewers East Entrance: Defend Plus P", 78780705, Rels.tik, [0x14A40]),
    LocationData("Rogueport Sewers Petal Meadows Pipe: Shine Sprite", 78780133, Rels.tik, [0x16674]),
    LocationData("Rogueport Sewers Boggly Woods Pipe: Damage Dodge", 78780134, Rels.tik, [0x17DC8]),
    LocationData("Rogueport Sewers Boggly Woods Pipe: Star Piece", 78780135, Rels.tik, [0x17E00]),
    LocationData("Rogueport Sewers Black Key Room: Black Key", 78780136, Rels.tik, [0x18AA8]),
    LocationData("Rogueport Sewers Black Key Room: Happy Heart P", 78780137, Rels.tik, [0x18830]),
    LocationData("Rogueport Sewers Black Key Room: Pretty Lucky", 78780138, Rels.tik, [0x18B74]),
    LocationData("Rogueport Sewers Black Key Room: Star Piece", 78780139, Rels.tik, [0x18B90]),
    LocationData("Rogueport Sewers Thousand Year Door: Shine Sprite", 78780140, Rels.tik, [0x1F01C]),
    LocationData("Rogueport Sewers Thousand Year Door: Star Piece", 78780141, Rels.tik, [0x1F0B4]),
    LocationData("Rogueport Sewers Star Piece House: Star Piece", 78780704, Rels.tik, [0x212AC]),
    LocationData("Rogueport Sewers East Enemy Hall: Fire Flower", 78780147, Rels.tik, [0x2BAC8]),
    LocationData("Rogueport Sewers East Enemy Hall: Mushroom", 78780148, Rels.tik, [0x2BAF0]),
    LocationData("Rogueport Sewers East Pipe Room: Shine Sprite", 78780149, Rels.tik, [0x2C22C]),
    LocationData("Rogueport Sewers West Pipe Room: FP Plus", 78780150, Rels.tik, [0x2C7DC]),
    LocationData("Rogueport Sewers Black Chest Room: Plane Curse", 78780153, Rels.tik, [0x2D65C]),
    LocationData("Rogueport Sewers Black Chest Room: Star Piece", 78780154, Rels.tik, [0x2DAC8]),
    LocationData("Rogueport Sewers Spike Room: Spike Shield", 78780159, Rels.tik, [0x2B5F4])
]

sewers_westside: typing.List[LocationData] = [
    LocationData("Rogueport Sewers Town: Gold Bar", 78780110, Rels.tik, [0xDDB8]),
    LocationData("Rogueport Sewers Town: Gold Bar x3", 78780111, Rels.tik, [0xDDC0]),
    LocationData("Rogueport Sewers Town: Gradual Syrup", 78780112, Rels.tik, [0xDDA0]),
    LocationData("Rogueport Sewers Town: Jammin' Jelly", 78780118, Rels.tik, [0xDDB0]),
    LocationData("Rogueport Sewers Town: Shine Sprite", 78780124, Rels.tik, [0x134E4]),
    LocationData("Rogueport Sewers Town: Slow Shroom", 78780125, Rels.tik, [0xDD98]),
    LocationData("Rogueport Sewers Town: Soft Stomp", 78780126, Rels.tik, [0x132A0]),
    LocationData("Rogueport Sewers Town: Star Piece 2", 78780128, Rels.tik, [0x13598]),
    LocationData("Rogueport Sewers Town: Star Piece 3", 78780129, Rels.tik, [0x13534]),
    LocationData("Rogueport Sewers Town: Star Piece 4", 78780130, Rels.tik, [0x13548]),
    LocationData("Rogueport Sewers Town: Ultra Mushroom", 78780131, Rels.tik, [0xDDA8]),
    LocationData("Rogueport Sewers West Entrance: Shine Sprite", 78780144, Rels.tik, [0x20474]),
    LocationData("Rogueport Sewers West Entrance: Star Piece 2", 78780146, Rels.tik, [0x2048C])
]

sewers_westside_ground: typing.List[LocationData] = [
    LocationData("Rogueport Sewers West Enemy Hall: Gradual Syrup", 78780151, Rels.tik, [0x2CDA8]),
    LocationData("Rogueport Sewers West Enemy Hall: Slow Shroom", 78780152, Rels.tik, [0x2CDD0]),
    LocationData("Rogueport Sewers Spania Room: Defend Plus", 78780155, Rels.tik, [0x2DD20]),
    LocationData("Rogueport Sewers Spania Room: Shine Sprite 1", 78780156, Rels.tik, [0x2DD54]),
    LocationData("Rogueport Sewers Spania Room: Shine Sprite 2", 78780157, Rels.tik, [0x2DD78]),
    LocationData("Rogueport Sewers Spania Room: Shine Sprite 3", 78780158, Rels.tik, [0x2DD9C]),
    LocationData("Rogueport Sewers West Entrance: Flower Saver P", 78780143, Rels.tik, [0x20320]),
    LocationData("Rogueport Sewers West Entrance: Star Piece 1", 78780145, Rels.tik, [0x204C4])
]

petal_right: typing.List[LocationData] = [
    LocationData("Petal Meadows Bridge Room: Fire Flower", 78780161, Rels.hei, [0xEE68]),
    LocationData("Petal Meadows Bridge Room: Mystery", 78780162, Rels.hei, [0xCC98]),
    LocationData("Petal Meadows Bridge Room: Koops", 78780185, Rels.hei, [0xD2E4]),
    LocationData("Petal Meadows First Fort Exterior: Coin", 78780163, Rels.hei, [0xF184]),
    LocationData("Petal Meadows First Fort Exterior: Star Piece", 78780164, Rels.hei, [0xF294]),
    LocationData("Petal Meadows First Fort Exterior: POW Block", 78780165, Rels.hei, [0xF468]),
    LocationData("Petal Meadows Second Fort Exterior: Coin 1", 78780166, Rels.hei, [0x1012C]),
    LocationData("Petal Meadows Second Fort Exterior: Coin 2", 78780167, Rels.hei, [0x101DC]),
    LocationData("Petal Meadows Second Fort Exterior: POW Block", 78780800, Rels.hei, [0x1022C]),
    LocationData("Petal Meadows Third Fort Exterior: Coin", 78780801, Rels.hei, [0x10F14]),
    LocationData("Petal Meadows Third Fort Exterior: Fire Flower", 78780802, Rels.hei, [0x11098]),
    LocationData("Petal Meadows Third Fort Exterior: Inn Coupon", 78780803, Rels.hei, [0x110B4]),
    LocationData("Petal Meadows Sewers West Key Room: Moon Stone", 78780169, Rels.hei, [0x134FC]),
    LocationData("Petal Meadows Sewers: Multibounce", 78780170, Rels.hei, [0x13FD4]),
    LocationData("Petal Meadows Sewers East Key Room: Sun Stone", 78780171, Rels.hei, [0x14660]),
    LocationData("Petalburg Westside: Courage Shell", 78780172, Rels.nok, [0x3C24]),
    LocationData("Petalburg Westside: Fire Flower", 78780173, Rels.nok, [0x3C14]),
    LocationData("Petalburg Westside: Honey Syrup", 78780174, Rels.nok, [0x3C34]),
    LocationData("Petalburg Westside: Mr. Softener", 78780175, Rels.nok, [0x3C2C]),
    LocationData("Petalburg Westside: Mushroom", 78780176, Rels.nok, [0x3C3C]),
    LocationData("Petalburg Westside: POW Block", 78780177, Rels.nok, [0x3C1C]),
    LocationData("Petalburg Westside: Star Piece", 78780178, Rels.nok, [0x58C0]),
    LocationData("Petalburg Eastside: Mega Rush P", 78780179, Rels.nok, [0x9758]),
    LocationData("Petalburg Eastside: Star Piece", 78780180, Rels.nok, [0x9744]),
    LocationData("Petalburg Eastside: Turtley Leaf", 78780181, Rels.nok, [0x93B8, 0x941C, 0x9480, 0x978C])
]

petal_left: typing.List[LocationData] = [
    LocationData("Petal Meadows Entrance: Mushroom 1", 78780182, Rels.hei, [0xC980]),
    LocationData("Petal Meadows Entrance: Mushroom 2", 78780183, Rels.hei, [0xBE8C]),
    LocationData("Petal Meadows Entrance: Star Piece", 78780184, Rels.hei, [0xBE3C]),
    LocationData("Petal Meadows Bridge Room: Coin 1", 78780186, Rels.hei, [0xCCE8]),
    LocationData("Petal Meadows Bridge Room: Coin 2", 78780160, Rels.hei, [0xCC48]),
    LocationData("Petal Meadows Bridge Room: Star Piece", 78780187, Rels.hei, [0xEE84]),
    LocationData("Petal Meadows Field: 10 Coins", 78780188, Rels.hei, [0x14A94]),
    LocationData("Petal Meadows Field: Close Call", 78780189, Rels.hei, [0x149D0]),
    LocationData("Petal Meadows Field: Happy Heart", 78780190, Rels.hei, [0x14A5C]),
    LocationData("Petal Meadows Field: Horsetail", 78780191, Rels.hei, [0x148D4, 0x1492C])
]

hooktails_castle: typing.List[LocationData] = [
    LocationData("Hooktail's Castle Drawbridge: HP Plus", 78780192, Rels.gon, [0x8850]),
    LocationData("Hooktail's Castle Entrance: Power Bounce", 78780193, Rels.gon, [0x8F40]),
    LocationData("Hooktail's Castle Red Bones Room: Castle Key", 78780194, Rels.gon, [0xA158]),
    LocationData("Hooktail's Castle Red Bones Room: Star Piece", 78780195, Rels.gon, [0xA468]),
    LocationData("Hooktail's Castle Stair Switch Room: Castle Key", 78780196, Rels.gon, [0xCC8C]),
    LocationData("Hooktail's Castle Stair Switch Room: Shine Sprite", 78780197, Rels.gon, [0xCDFC]),
    LocationData("Hooktail's Castle Stair Switch Room: Star Piece 1", 78780198, Rels.gon, [0xCCB8]),
    LocationData("Hooktail's Castle Stair Switch Room: Star Piece 2", 78780199, Rels.gon, [0xCCE0]),
    LocationData("Hooktail's Castle Stair Central Staircase: Castle Key", 78780200, Rels.gon, [0xE718]),
    LocationData("Hooktail's Castle Stair Central Staircase: Last Stand P", 78780201, Rels.gon, [0xE76C]),
    LocationData("Hooktail's Castle Stair Central Staircase: Shine Sprite", 78780202, Rels.gon, [0xE860]),
    LocationData("Hooktail's Castle Stair Central Staircase: Star Piece", 78780203, Rels.gon, [0xE744]),
    LocationData("Hooktail's Castle Prison Entrance: Paper Curse", 78780204, Rels.gon, [0xF504]),
    LocationData("Hooktail's Castle Prison Entrance: Attack FX R", 78780205, Rels.gon, [0xFD5C]),
    LocationData("Hooktail's Castle Spikes Room: Black Key (Paper Curse)", 78780206, Rels.gon, [0x1026C]),
    LocationData("Hooktail's Castle Life Shroom Room: Life Shroom", 78780207, Rels.gon, [0x11C00]),
    LocationData("Hooktail's Castle Plane Rafters Room: Star Piece", 78780208, Rels.gon, [0x129AC]),
    LocationData("Hooktail's Castle Hooktail's Room: Diamond Star", 78780209, Rels.gon, []),
    LocationData("Hooktail's Castle Storeroom: Castle Key", 78780210, Rels.gon, [0x157D8]),
    LocationData("Hooktail's Castle Storeroom: Honey Syrup", 78780211, Rels.gon, [0x158F4]),
    LocationData("Hooktail's Castle Storeroom: Mushroom", 78780212, Rels.gon, [0x1586C]),
    LocationData("Hooktail's Castle Storeroom: Shine Sprite", 78780213, Rels.gon, [0x15A98]),
    LocationData("Hooktail's Castle Up Arrow Room: Up Arrow", 78780214, Rels.gon, [0x261D8])
]

boggly_woods: typing.List[LocationData] = [
    LocationData("Boggly Woods Shadow Sirens Room: Necklace", 78780215, Rels.win, [0x6D04, 0x8C0C, 0x98A0]),
    LocationData("Boggly Woods Shadow Sirens Room: Honey Syrup", 78780216, Rels.win, [0x98CC]),
    LocationData("Boggly Woods Shadow Sirens Room: Sleepy Sheep", 78780217, Rels.win, [0x9318]),
    LocationData("Boggly Woods Tree View: Coin", 78780218, Rels.win, [0xA518]),
    LocationData("Boggly Woods Tree View: Inn Coupon", 78780219, Rels.win, [0xA64C]),
    LocationData("Boggly Woods Plane Panel Room: P-Down D-Up P", 78780220, Rels.win, [0xAD64]),
    LocationData("Boggly Woods Plane Panel Room: Quake Hammer", 78780221, Rels.win, [0xAD8C]),
    LocationData("Boggly Woods Plane Panel Room: Shine Sprite", 78780222, Rels.win, [0xAD40]),
    LocationData("Boggly Woods Plane Panel Room: Star Piece", 78780223, Rels.win, [0xADA8]),
    LocationData("Boggly Woods Outside Flurrie's House: Star Piece 1", 78780224, Rels.win, [0xB5E0]),
    LocationData("Boggly Woods Outside Flurrie's House: Star Piece 2", 78780225, Rels.win, [0xB768]),
    LocationData("Boggly Woods Outside Flurrie's House: Volt Shroom", 78780226, Rels.win, [0xB740]),
    LocationData("Boggly Woods Flurrie's House: Flurrie", 78780227, Rels.win, [0xDFC4]),
    LocationData("Boggly Woods Flurrie's House Backroom: Star Piece", 78780228, Rels.win, [0x10128]),
    LocationData("Boggly Woods Flurrie's House Backroom: Super Appeal P", 78780229, Rels.win, [0xFE78]),
    LocationData("Boggly Woods Outside Great Tree: FP Plus", 78780230, Rels.mri, [0x2CBA0])
]

great_tree: typing.List[LocationData] = [
    LocationData("Great Tree Entrance: Coin", 78780231, Rels.mri, [0x36668]),
    LocationData("Great Tree Entrance: Emerald Star", 78780232, Rels.mri, []),
    LocationData("Great Tree Entrance: Mystic Egg", 78780233, Rels.mri, [0x2E474]),
    LocationData("Great Tree Entrance: Puni Orb", 78780234, Rels.mri, [0x326BC]),
    LocationData("Great Tree 10-Puni Pedestal: Star Piece", 78780235, Rels.mri, [0x38998]),
    LocationData("Great Tree Red/Blue Cages: Star Piece", 78780236, Rels.mri, [0x3C840]),
    LocationData("Great Tree Red Key Room: Coin", 78780237, Rels.mri, [0x3DFF0]),
    LocationData("Great Tree Red Key Room: Mushroom", 78780238, Rels.mri, [0x3CC58]),
    LocationData("Great Tree Red Key Room: Red Key", 78780239, Rels.mri, [0x3E378, 0x3DA14]),
    LocationData("Great Tree Red Key Room: Ultra Shroom", 78780240, Rels.mri, [0x3E098]),
    LocationData("Great Tree Bubble Room: Shine Sprite", 78780241, Rels.mri, [0x3F890]),
    LocationData("Great Tree Bubble Room: Thunder Rage", 78780242, Rels.mri, [0x3E954]),
    LocationData("Great Tree Zigzag Room: Coin", 78780243, Rels.mri, [0x40E84]),
    LocationData("Great Tree Zigzag Room: Damage Dodge P", 78780244, Rels.mri, [0x40E5C]),
    LocationData("Great Tree Zigzag Room: Star Piece", 78780245, Rels.mri, [0x40360]),
    LocationData("Great Tree Shop: Honey Syrup", 78780246, Rels.mri, [0x40FC8]),
    LocationData("Great Tree Shop: HP Drain", 78780247, Rels.mri, [0x40FA8]),
    LocationData("Great Tree Shop: Ice Storm", 78780248, Rels.mri, [0x40FB0]),
    LocationData("Great Tree Shop: Mini Mr.Mini", 78780249, Rels.mri, [0x40FC0]),
    LocationData("Great Tree Shop: Mushroom", 78780250, Rels.mri, [0x40FD0]),
    LocationData("Great Tree Shop: Mystery", 78780251, Rels.mri, [0x40FB8]),
    LocationData("Great Tree Blue Key Room: Blue Key", 78780252, Rels.mri, [0x44258]),
    LocationData("Great Tree Blue Key Room: Charge", 78780253, Rels.mri, [0x44788]),
    LocationData("Great Tree Blue Key Room: Shine Sprite", 78780254, Rels.mri, [0x447BC]),
    LocationData("Great Tree Super Boots Room: Super Boots", 78780255, Rels.mri, [0x44928]),
    LocationData("Great Tree 100-Puni Pedestal: Coin", 78780256, Rels.mri, [0x4674C]),
    LocationData("Great Tree 100-Puni Pedestal: Star Piece", 78780257, Rels.mri, [0x46A50]),
    LocationData("Great Tree Elevator Pedestal: Mushroom", 78780258, Rels.mri, [0x47AB4]),
    LocationData("Great Tree Escape Ambush Room: Star Piece", 78780259, Rels.mri, [0x4A83C]),
    LocationData("Great Tree Pool Room: Dizzy Dial", 78780260, Rels.mri, [0x4B9BC]),
    LocationData("Great Tree Pool Room: Shine Sprite", 78780261, Rels.mri, [0x4BA18]),
    LocationData("Great Tree Pool Room: Shrink Stomp", 78780262, Rels.mri, [0x4B56C]),
    LocationData("Great Tree Fake Pedestal: Star Piece", 78780263, Rels.mri, [0x5DF0C]),
    LocationData("Great Tree Lower Duplex: Coin", 78780264, Rels.mri, [0x5E614]),
    LocationData("Great Tree Middle Duplex: Shine Sprite", 78780265, Rels.mri, [0x5EC00]),
    LocationData("Great Tree Upper Duplex: Power Punch", 78780266, Rels.mri, [0x5E1E8])
]

glitzville: typing.List[LocationData] = [
    LocationData("Glitzville Main Square: Coin", 78780267, Rels.tou, [0x219F8]),
    LocationData("Glitzville Main Square: Earth Quake", 78780268, Rels.tou, [0x1AED4]),
    LocationData("Glitzville Main Square: Hot Dog", 78780269, Rels.tou, [0x1B0D8]),
    LocationData("Glitzville Main Square: Inn Coupon", 78780270, Rels.tou, [0x21B00]),
    LocationData("Glitzville Main Square: Point Swap", 78780271, Rels.tou, [0x1AEF4]),
    LocationData("Glitzville Main Square: Power Plus P", 78780272, Rels.tou, [0x21928]),
    LocationData("Glitzville Main Square: Power Punch", 78780273, Rels.tou, [0x1AEE4]),
    LocationData("Glitzville Main Square: Repel Cape", 78780274, Rels.tou, [0x1AEEC]),
    LocationData("Glitzville Main Square: Shine Sprite", 78780275, Rels.tou, [0x219D4]),
    LocationData("Glitzville Main Square: Star Piece 1", 78780276, Rels.tou, [0x21A60]),
    LocationData("Glitzville Main Square: Star Piece 2", 78780277, Rels.tou, [0x21A88]),
    LocationData("Glitzville Main Square: Star Piece 3", 78780278, Rels.tou, [0x21AB0]),
    LocationData("Glitzville Main Square: Star Piece 4", 78780279, Rels.tou, [0x21A4C]),
    LocationData("Glitzville Main Square: Star Piece 5", 78780280, Rels.tou, [0x21AD8]),
    LocationData("Glitzville Main Square: Storage Key 1", 78780281, Rels.tou, [0x21CE0]),
    LocationData("Glitzville Main Square: Super Hammer", 78780282, Rels.tou, [0x1B5E0]),
    LocationData("Glitzville Main Square: Super Shroom", 78780283, Rels.tou, [0x1AEFC]),
    LocationData("Glitzville Main Square: Thunder Bolt", 78780284, Rels.tou, [0x1AEDC]),
    LocationData("Glitzville Lobby: Star Piece", 78780285, Rels.tou, [0x26F38]),
    LocationData("Glitzville Lobby: Storage Key 2", 78780286, Rels.tou, [0x27C20, 0x26A88]),
    LocationData("Glitzville Arena: Gold Star", 78780287, Rels.tou2, []),
    LocationData("Glitzville Hall: Last Stand", 78780288, Rels.tou, [0x2C8B8]),
    LocationData("Glitzville Promoter's Office: Star Piece 1", 78780289, Rels.tou, [0x3104C]),
    LocationData("Glitzville Promoter's Office: Star Piece 2", 78780290, Rels.tou, [0x2DF0C]),
    LocationData("Glitzville Storage Room: Charge P", 78780291, Rels.tou, [0x33010]),
    LocationData("Glitzville Storage Room: HP Plus P", 78780292, Rels.tou, [0x32FE8]),
    LocationData("Glitzville Storage Room: Shine Sprite", 78780293, Rels.tou, [0x32F94]),
    LocationData("Glitzville Storage Room: Star Piece", 78780294, Rels.tou, [0x32FBC]),
    LocationData("Glitzville Major-League Room: Champ's Belt", 78780295, Rels.tou, [0x34328, 0x378D8]),
    LocationData("Glitzville Major-League Room: Ice Storm", 78780296, Rels.tou, [0x3857C]),
    LocationData("Glitzville Minor-League Room: Dubious Paper", 78780297, Rels.tou, [0x3DCB0]),
    LocationData("Glitzville Minor-League Room: Yoshi", 78780298, Rels.tou, [0x3BE30]),
    LocationData("Glitzville Storage Back Room: Star Piece", 78780299, Rels.tou, [0x3F3DC])
]

twilight_town_region: typing.List[LocationData] = [
    LocationData("Twilight Town Leftside: Coin", 78780300, Rels.usu, [0xBC7C]),
    LocationData("Twilight Town Leftside: Peachy Peach", 78780301, Rels.usu, [0xAEF8]),
    LocationData("Twilight Town Leftside: Star Piece 1", 78780302, Rels.usu, [0xBC18]),
    LocationData("Twilight Town Leftside: Star Piece 2", 78780303, Rels.usu, [0xF8A8]),
    LocationData("Twilight Town Leftside: Superbombomb", 78780304, Rels.usu, [0xBEC0]),
    LocationData("Twilight Town Leftside: Vivian", 78780305, Rels.usu, [0xA16C]),
    LocationData("Twilight Town Rightside: Boo's Sheet", 78780306, Rels.usu, [0x16D88]),
    LocationData("Twilight Town Rightside: Defend Plus", 78780307, Rels.usu, [0x1690C]),
    LocationData("Twilight Town Rightside: Inn Coupon", 78780308, Rels.usu, [0x16DD8]),
    LocationData("Twilight Town Rightside: Jammin' Jelly", 78780309, Rels.usu, [0x16DB0]),
    LocationData("Twilight Town Rightside: Life Shroom 1", 78780310, Rels.usu, [0x15C10]),
    LocationData("Twilight Town Rightside: Life Shroom 2", 78780311, Rels.usu, [0x16D60]),
    LocationData("Twilight Town Rightside: Maple Syrup", 78780312, Rels.usu, [0x15C00]),
    LocationData("Twilight Town Rightside: Spite Pouch", 78780313, Rels.usu, [0x15BF0]),
    LocationData("Twilight Town Rightside: Star Piece", 78780314, Rels.usu, [0x16D38]),
    LocationData("Twilight Town Rightside: Stopwatch", 78780315, Rels.usu, [0x15BF8]),
    LocationData("Twilight Town Rightside: Super Shroom", 78780316, Rels.usu, [0x15C08]),
    LocationData("Twilight Town Rightside: Thunder Rage", 78780317, Rels.usu, [0x15BE8]),
    LocationData("Twilight Town Rightside: Tube Curse", 78780318, Rels.usu, [0x162E8]),
    LocationData("Twilight Trail Entrance: 10 Coins", 78780319, Rels.gra, [0x4A38]),
    LocationData("Twilight Trail Entrance: Black Key (Tube Curse)", 78780320, Rels.gra, [0x4A60]),
    LocationData("Twilight Trail Hyper Goomba Room: 10 Coins", 78780321, Rels.gra, [0x4EB4]),
    LocationData("Twilight Trail Hyper Goomba Room: Coin", 78780322, Rels.gra, [0x4DEC]),
    LocationData("Twilight Trail Hyper Goomba Room: Super Shroom", 78780323, Rels.gra, [0x4E8C]),
    LocationData("Twilight Trail Fallen Tree: Shop Key", 78780324, Rels.gra, [0x53C8]),
]

twilight_trail: typing.List[LocationData] = [
    LocationData("Twilight Trail Fallen Tree: Star Piece 1", 78780325, Rels.gra, [0x5358]),
    LocationData("Twilight Trail Fallen Tree: Star Piece 2", 78780326, Rels.gra, [0x5380]),
    LocationData("Twilight Trail Dark Woods First Room: 10 Coins", 78780327, Rels.gra, [0x559C]),
    LocationData("Twilight Trail Dark Woods First Room: Earthquake", 78780328, Rels.gra, [0x55C4]),
    LocationData("Twilight Trail Dark Woods Second Room: Hammer Throw", 78780329, Rels.gra, [0x5D2C]),
    LocationData("Twilight Trail Dark Woods Third Room: 10 Coins", 78780330, Rels.gra, [0x6C74]),
    LocationData("Twilight Trail Dark Woods Third Room: Shine Sprite", 78780331, Rels.gra, [0x6C9C]),
    LocationData("Twilight Trail Steeple Exterior: Coin", 78780332, Rels.gra, [0x7D80]),
    LocationData("Twilight Trail Steeple Exterior: Star Piece", 78780333, Rels.gra, [0x7C7C])
]

creepy_steeple: typing.List[LocationData] = [
    LocationData("Creepy Steeple Main Hall: Lucky Start", 78780434, Rels.jin, [0xD7A8]),
    LocationData("Creepy Steeple Main Hall: Steeple Key", 78780435, Rels.jin, [0xD938]),
    LocationData("Creepy Steeple North Hall: Golden Leaf", 78780436, Rels.jin, [0xE104]),
    LocationData("Creepy Steeple Upper Room: Ruby Star", 78780437, Rels.jin, []),
    LocationData("Creepy Steeple Back Stairs: Star Piece", 78780805, Rels.jin, [0xEC80]),
    LocationData("Creepy Steeple Cookbook Room: Cookbook", 78780438, Rels.jin, [0x11C88]),
    LocationData("Creepy Steeple Cookbook Room: Ice Smash", 78780439, Rels.jin, [0x11D10]),
    LocationData("Creepy Steeple Cookbook Room: Shine Sprite", 78780440, Rels.jin, [0x11DD8]),
    LocationData("Creepy Steeple Cookbook Room: Star Piece", 78780441, Rels.jin, [0x11E40]),
    LocationData("Creepy Steeple Under Statue: Flower Saver", 78780442, Rels.jin, [0x120A8]),
    LocationData("Creepy Steeple Boo Chest Room: Star Piece", 78780443, Rels.jin, [0x131B4]),
    LocationData("Creepy Steeple Boo Chest Room: Ultra Mushroom", 78780444, Rels.jin, [0x12F6C, 0x12F90, 0x12FB4]),
    LocationData("Creepy Steeple Parrot Room: Mr. Softener", 78780445, Rels.jin, [0x13E38]),
    LocationData("Creepy Steeple Parrot Room: Power Plus", 78780446, Rels.jin, [0x13DB0]),
    LocationData("Creepy Steeple Parrot Room: Star Piece", 78780447, Rels.jin, [0x14050]),
    LocationData("Creepy Steeple Parrot Room: Steeple Key 2", 78780448, Rels.jin, [0x13798]),
    LocationData("Creepy Steeple Parrot Room: The Letter \"p\"", 78780449, Rels.jin, [0x13674]),
    LocationData("Creepy Steeple Well Entrance: Shine Sprite", 78780450, Rels.jin, [0x14244]),
    LocationData("Creepy Steeple Buzzy Room: Tornado Jump", 78780451, Rels.jin, [0x14DB8]),
    LocationData("Creepy Steeple Underground Tube Passage: Shine Sprite", 78780452, Rels.jin, [0x15060])
]

keelhaul_key: typing.List[LocationData] = [
    LocationData("Keelhaul Key Landing Site: Star Piece", 78780453, Rels.muj, [0x1E758]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 1", 78780454, Rels.muj, [0x160B0]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 2", 78780455, Rels.muj, [0x160C4]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 3", 78780456, Rels.muj, [0x160D8]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 4", 78780457, Rels.muj, [0x160EC]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 5", 78780458, Rels.muj, [0x16104]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 6", 78780459, Rels.muj, [0x16118]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 7", 78780460, Rels.muj, [0x1612C]),
    LocationData("Keelhaul Key Landing Site: Whacka Bump 8", 78780806, Rels.muj, [0x16144]),
    LocationData("Keelhaul Key Town: Chuckola Cola", 78780461, Rels.muj, [0x1FA7C]),
    LocationData("Keelhaul Key Town: Fire Flower", 78780462, Rels.muj, [0x21C20]),
    LocationData("Keelhaul Key Town: Fright Mask", 78780463, Rels.muj, [0x21C30]),
    LocationData("Keelhaul Key Town: Honey Syrup", 78780464, Rels.muj, [0x21C38]),
    LocationData("Keelhaul Key Town: Ice Storm", 78780465, Rels.muj, [0x21C18]),
    LocationData("Keelhaul Key Town: Sleepy Sheep", 78780466, Rels.muj, [0x21C28]),
    LocationData("Keelhaul Key Town: Star Piece 1", 78780467, Rels.muj, [0x24210]),
    LocationData("Keelhaul Key Town: Star Piece 2", 78780468, Rels.muj, [0x24238]),
    LocationData("Keelhaul Key Town: Super Shroom", 78780469, Rels.muj, [0x21C40]),
    LocationData("Keelhaul Key Jungle Entrance: Coin", 78780470, Rels.muj, [0x256D4]),
    LocationData("Keelhaul Key Jungle Entrance: Courage Shell", 78780471, Rels.muj, [0x25A54]),
    LocationData("Keelhaul Key Jungle Entrance: Head Rattle", 78780472, Rels.muj, [0x25A2C]),
    LocationData("Keelhaul Key Jungle Entrance: Keel Mango", 78780473, Rels.muj, [0x25684]),
    LocationData("Keelhaul Key Jungle Entrance: Star Piece", 78780474, Rels.muj, [0x25724]),
    LocationData("Keelhaul Key Jungle Winding Climb: 10 Coins", 78780475, Rels.muj, [0x262B4]),
    LocationData("Keelhaul Key Jungle Winding Climb: Coin 1", 78780476, Rels.muj, [0x2628C]),
    LocationData("Keelhaul Key Jungle Winding Climb: Coin 2", 78780477, Rels.muj, [0x26108]),
    LocationData("Keelhaul Key Jungle Winding Climb: Jammin' Jelly", 78780478, Rels.muj, [0x26350]),
    LocationData("Keelhaul Key Jungle Winding Climb: Mini Mr.Mini", 78780479, Rels.muj, [0x260B8]),
    LocationData("Keelhaul Key Jungle Winding Climb: Shine Sprite", 78780480, Rels.muj, [0x26304]),
    LocationData("Keelhaul Key Jungle Winding Climb: Star Piece", 78780481, Rels.muj, [0x2636C]),
    LocationData("Keelhaul Key Jungle Winding Climb: Thunder Rage", 78780482, Rels.muj, [0x26328]),
    LocationData("Keelhaul Key Jungle Bridge: Coconut 1", 78780483, Rels.muj, [0x2756C]),
    LocationData("Keelhaul Key Jungle Bridge: Coconut 2", 78780484, Rels.muj, [0x27768]),
    LocationData("Keelhaul Key Jungle Bridge: Ice Power", 78780485, Rels.muj, [0x278E0]),
    LocationData("Keelhaul Key Jungle Bridge: Inn Coupon", 78780486, Rels.muj, [0x27908]),
    LocationData("Keelhaul Key Jungle Bridge: Shine Sprite", 78780487, Rels.muj, [0x2793C]),
    LocationData("Keelhaul Key Grotto Entrance: Bobbery", 78780488, Rels.muj, [0x27DFC]),
    LocationData("Keelhaul Key Grotto Entrance: Skull Gem", 78780489, Rels.muj, [0x284CC]),
    LocationData("Keelhaul Key Grotto Entrance: Spite Pouch", 78780490, Rels.muj, [0x2AEA0]),
    LocationData("Keelhaul Key Grotto Entrance: Star Piece", 78780491, Rels.muj, [0x2B1D4]),
    LocationData("Keelhaul Key Grotto Entrance: Wedding Ring", 78780492, Rels.muj, [0x2B144])
]

pirates_grotto: typing.List[LocationData] = [
    LocationData("Pirate's Grotto Entrance: Ruin Powder", 78780493, Rels.dou, [0x717C]),
    LocationData("Pirate's Grotto Gate Handle Room: Gate Handle", 78780494, Rels.dou, [0x7DC8]),
    LocationData("Pirate's Grotto Gate Handle Room: Shine Sprite", 78780495, Rels.dou, [0x7E24]),
    LocationData("Pirate's Grotto Gate Handle Room: Star Piece", 78780496, Rels.dou, [0x7DF0]),
    LocationData("Pirate's Grotto Sluice Gate: Star Piece", 78780497, Rels.dou, [0x8C84]),
    LocationData("Pirate's Grotto Storeroom: Grotto Key", 78780498, Rels.dou, [0xAA2C]),
    LocationData("Pirate's Grotto Storeroom: Shine Sprite", 78780499, Rels.dou, [0xAA9C]),
    LocationData("Pirate's Grotto Storeroom: Star Piece", 78780500, Rels.dou, [0xAA54]),
    LocationData("Pirate's Grotto Staircase: Coin", 78780501, Rels.dou, [0xB370]),
    LocationData("Pirate's Grotto Staircase: Defend Plus P", 78780502, Rels.dou, [0xB04C]),
    LocationData("Pirate's Grotto Staircase: Shine Sprite", 78780503, Rels.dou, [0xB34C]),
    LocationData("Pirate's Grotto Parabuzzy Room: Star Piece", 78780504, Rels.dou, [0xB598]),
    LocationData("Pirate's Grotto Chest Boat: Black Key (Boat Curse)", 78780505, Rels.dou, [0xC464, 0xB64C]),
    LocationData("Pirate's Grotto Chest Boat: Boat Curse", 78780506, Rels.dou, [0xBE8C]),
    LocationData("Pirate's Grotto Chest Boat: P-Down D-Up", 78780507, Rels.dou, [0xC408]),
    LocationData("Pirate's Grotto Barrel Room: 10 Coins", 78780508, Rels.dou, [0xD858]),
    LocationData("Pirate's Grotto Barrel Room: Shine Sprite", 78780509, Rels.dou, [0xD834]),
    LocationData("Pirate's Grotto Spike Wall Room: Shine Sprite", 78780510, Rels.dou, [0xEBCC]),
    LocationData("Pirate's Grotto Cortez' Hoard: Sapphire Star", 78780511, Rels.muj, [])
]

excess_express: typing.List[LocationData] = [
    LocationData("Excess Express Locomotive: Autograph", 78780512, Rels.rsh, [0x18E48]),
    LocationData("Excess Express Locomotive: Star Piece", 78780513, Rels.rsh, [0x19330, 0x19358]),
    LocationData("Excess Express Front Passenger Car: Vital Paper", 78780514, Rels.rsh, [0x1A848]),
    LocationData("Excess Express Front Passenger Car: 30 Coins", 78780515, Rels.rsh, [0x1A094, 0x6F84]),
    LocationData("Excess Express Middle Passenger Car: Blanket", 78780516, Rels.rsh, [0x1CA20]),
    LocationData("Excess Express Middle Passenger Car: Briefcase", 78780517, Rels.rsh, [0x1DE04]),
    LocationData("Excess Express Middle Passenger Car: Dried Shroom", 78780518, Rels.rsh, [0x1EAA4]),
    LocationData("Excess Express Middle Passenger Car: Galley Pot", 78780519, Rels.rsh, [0x1BD4C]),
    LocationData("Excess Express Middle Passenger Car: Gold Ring", 78780520, Rels.rsh, [0x1DE4C]),
    LocationData("Excess Express Middle Passenger Car: Shell Earrings", 78780521, Rels.rsh, [0x1DE94]),
    LocationData("Excess Express Middle Passenger Car: Shine Sprite", 78780522, Rels.rsh, [0x1ED80]),
    LocationData("Excess Express Middle Passenger Car: Star Piece", 78780523, Rels.rsh, [0x1ED60]),
    LocationData("Excess Express Dining Car: Boo's Sheet", 78780524, Rels.rsh, [0x23780]),
    LocationData("Excess Express Dining Car: Maple Syrup", 78780525, Rels.rsh, [0x23790]),
    LocationData("Excess Express Dining Car: Mystery", 78780526, Rels.rsh, [0x23778]),
    LocationData("Excess Express Dining Car: Star Piece 1", 78780527, Rels.rsh, [0x212C0]),
    LocationData("Excess Express Dining Car: Star Piece 2", 78780528, Rels.rsh, [0x21AA0]),
    LocationData("Excess Express Dining Car: Super Shroom", 78780529, Rels.rsh, [0x23798]),
    LocationData("Excess Express Dining Car: Tasty Tonic", 78780530, Rels.rsh, [0x23788]),
    LocationData("Excess Express Dining Car: Thunder Rage", 78780531, Rels.rsh, [0x23770]),
    LocationData("Excess Express Back Passenger Car: Mushroom", 78780532, Rels.rsh, [0x26B38]),
    LocationData("Excess Express Back Passenger Car: Shine Sprite", 78780533, Rels.rsh, [0x27AE4]),
    LocationData("Excess Express Back Passenger Car: Star Piece", 78780534, Rels.rsh, [0x283C0]),
    LocationData("Excess Express Storage Car: Ragged Diary", 78780535, Rels.rsh, [0x2ADAC])
]

riverside: typing.List[LocationData] = [
    LocationData("Riverside Station Drawbridge: Station Key 1", 78780536, Rels.hom, [0x14CC]),
    LocationData("Riverside Station Entrance: Close Call P", 78780537, Rels.eki, [0xCA40, 0xC894]),
    LocationData("Riverside Station Clockwork Room: Star Piece", 78780538, Rels.eki, [0xD6C8]),
    LocationData("Riverside Station Clockwork Room: Station Key 2", 78780539, Rels.eki, [0xD68C]),
    LocationData("Riverside Station Back Exterior: HP Plus", 78780540, Rels.eki, [0xDCA4]),
    LocationData("Riverside Station Back Exterior: Shine Sprite", 78780541, Rels.eki, [0xDCD8]),
    LocationData("Riverside Station Back Exterior: Thunder Rage", 78780542, Rels.eki, [0xDD20]),
    LocationData("Riverside Station Tube Mode Maze: Dried Shroom", 78780543, Rels.eki, [0xE628]),
    LocationData("Riverside Station Tube Mode Maze: P-Up D-Down", 78780544, Rels.eki, [0xE650]),
    LocationData("Riverside Station Ultra Boots Room: Elevator Key (Riverside)", 78780545, Rels.eki, [0xEB7C, 0xEA28]),
    LocationData("Riverside Station Ultra Boots Room: Ultra Boots", 78780546, Rels.eki, [0xE990]),
    LocationData("Riverside Station Goomba Room: Shine Sprite", 78780547, Rels.eki, [0xF5D4])
]

poshley_heights: typing.List[LocationData] = [
    LocationData("Poshley Heights Station: Goldbob Guide", 78780548, Rels.pik, [0x6538]),
    LocationData("Poshley Heights Station: HP Drain P", 78780549, Rels.pik, [0x7D88]),
    LocationData("Poshley Heights Station: Star Piece 1", 78780550, Rels.pik, [0x81D0]),
    LocationData("Poshley Heights Station: Star Piece 2", 78780551, Rels.pik, [0x81F8]),
    LocationData("Poshley Heights Station: Star Piece 3", 78780552, Rels.pik, [0x8194]),
    LocationData("Poshley Heights Sanctum Exterior: Shine Sprite", 78780553, Rels.pik, [0xB854]),
    LocationData("Poshley Heights Sanctum Altar: Garnet Star", 78780554, Rels.pik, []),
    LocationData("Poshley Heights Sanctum Altar: L Emblem", 78780555, Rels.pik, [0xEE6C]),
    LocationData("Poshley Heights Sanctum Altar: Shine Sprite", 78780556, Rels.pik, [0xEEA0]),
    LocationData("Poshley Heights Downtown: Fresh Pasta", 78780557, Rels.pik, [0x10CB4]),
    LocationData("Poshley Heights Downtown: Inn Coupon", 78780558, Rels.pik, [0x115D8]),
    LocationData("Poshley Heights Downtown: Omelette Meal", 78780559, Rels.pik, [0x10E50]),
    LocationData("Poshley Heights Downtown: Star Piece", 78780560, Rels.pik, [0x115B0])
]

fahr_outpost: typing.List[LocationData] = [
    LocationData("Fahr Outpost Entrance: Double Dip P", 78780561, Rels.bom, [0x8CB0]),
    LocationData("Fahr Outpost Entrance: Star Piece", 78780562, Rels.bom, [0x8CDC]),
    LocationData("Fahr Outpost Town Outskirts: Star Piece", 78780563, Rels.bom, [0xDCD0]),
    LocationData("Fahr Outpost Town: Ice Storm", 78780564, Rels.bom, [0x1117C]),
    LocationData("Fahr Outpost Town: Inn Coupon", 78780565, Rels.bom, [0x11F70]),
    LocationData("Fahr Outpost Town: Maple Syrup", 78780566, Rels.bom, [0x11194]),
    LocationData("Fahr Outpost Town: Ruin Powder", 78780567, Rels.bom, [0x11184]),
    LocationData("Fahr Outpost Town: Shine Sprite", 78780568, Rels.bom, [0x11F0C]),
    LocationData("Fahr Outpost Town: Shooting Star", 78780569, Rels.bom, [0x11174]),
    LocationData("Fahr Outpost Town: Space Food", 78780570, Rels.bom, [0x11CAC]),
    LocationData("Fahr Outpost Town: Star Piece 1", 78780571, Rels.bom, [0x11F34]),
    LocationData("Fahr Outpost Town: Star Piece 2", 78780572, Rels.bom, [0x11F48]),
    LocationData("Fahr Outpost Town: Stopwatch", 78780573, Rels.bom, [0x1118C]),
    LocationData("Fahr Outpost Town: Super Shroom", 78780574, Rels.bom, [0x1119C]),
    LocationData("Fahr Outpost West Enemy Room: Shine Sprite", 78780575, Rels.bom, [0x1264C]),
    LocationData("Fahr Outpost West Enemy Room: Star Piece", 78780576, Rels.bom, [0x12664]),
    LocationData("Fahr Outpost East Enemy Room: HP Plus P", 78780577, Rels.bom, [0x12434]),
    LocationData("Fahr Outpost East Enemy Room: Star Piece", 78780578, Rels.bom, [0x12400])
]

xnaut_fortress: typing.List[LocationData] = [
    LocationData("Moon Landing Site: Stopwatch", 78780579, Rels.moo, [0x52B8]),
    LocationData("Moon East Room 1: Volt Shroom", 78780807, Rels.moo, [0x55AC]),
    LocationData("Moon Fortress View: Power Punch", 78780580, Rels.moo, [0x5C68]),
    LocationData("Moon Fortress View: Star Piece", 78780581, Rels.moo, [0x5B14]),
    LocationData("Moon West Room 2: Ruin Powder", 78780582, Rels.moo, [0x979C]),
    LocationData("Moon West Room 1: Courage Shell", 78780583, Rels.moo, [0x99F0]),
    LocationData("X-Naut Fortress Elevator Key Room: Elevator Key 1", 78780584, Rels.aji, [0x1EC14]),
    LocationData("X-Naut Fortress Elevator Key Room: Super Shroom", 78780585, Rels.aji, [0x1F180]),
    LocationData("X-Naut Fortress Crane Room: Coin 1", 78780586, Rels.aji, [0x21DBC]),
    LocationData("X-Naut Fortress Crane Room: Coin 2", 78780587, Rels.aji, [0x21DE4]),
    LocationData("X-Naut Fortress Crane Room: Coin 3", 78780588, Rels.aji, [0x21E0C]),
    LocationData("X-Naut Fortress Crane Room: Coin 4", 78780589, Rels.aji, [0x21E34]),
    LocationData("X-Naut Fortress Crane Room: Coin 5", 78780590, Rels.aji, [0x21E94]),
    LocationData("X-Naut Fortress Crane Room: Coin 6", 78780591, Rels.aji, [0x21EF4]),
    LocationData("X-Naut Fortress Crane Room: Feeling Fine", 78780592, Rels.aji, [0x21E68]),
    LocationData("X-Naut Fortress Crane Room: Feeling Fine P", 78780593, Rels.aji, [0x21EC8]),
    LocationData("X-Naut Fortress Crane Room: Star Piece", 78780594, Rels.aji, [0x21F28]),
    LocationData("X-Naut Fortress Quiz Room: Elevator Key 2", 78780595, Rels.aji, [0x23DFC, 0x23BAC]),
    LocationData("X-Naut Fortress Card Key Room A: Card Key 1", 78780596, Rels.aji, [0x23FD8]),
    LocationData("X-Naut Fortress Card Key Room A: Sleepy Sheep", 78780597, Rels.aji, [0x24338]),
    LocationData("X-Naut Fortress Teleporter Room: Cog", 78780598, Rels.aji, [0x299D0]),
    LocationData("X-Naut Fortress Ceiling Grate Room: Star Piece", 78780599, Rels.aji, [0x29FAC]),
    LocationData("X-Naut Fortress Office: Card Key 2", 78780600, Rels.aji, [0x30D60]),
    LocationData("X-Naut Fortress Card Key Room B: Card Key 3", 78780601, Rels.aji, [0x31080]),
    LocationData("X-Naut Fortress Card Key Room B: HP Drain", 78780702, Rels.aji, [0x31370]),
    LocationData("X-Naut Fortress Factory: Card Key 4", 78780602, Rels.aji, [0x32D9C]),
    LocationData("X-Naut Fortress Factory: Ultra Shroom", 78780603, Rels.aji, [0x32F14]),
    LocationData("X-Naut Fortress Boss Room: Crystal Star", 78780604, Rels.aji, [])
]

palace: typing.List[LocationData] = [
    LocationData("Palace of Shadow Swoopula Staircase: Stopwatch", 78780605, Rels.las, [0x1BF04]),
    LocationData("Palace of Shadow Bullet Bill Hallway: Shooting Star", 78780606, Rels.las, [0x1C2A4]),
    LocationData("Palace of Shadow Spike Trap Room: All or Nothing", 78780607, Rels.las, [0x1C970]),
    LocationData("Palace of Shadow Fire Trap Room: Boo's Sheet", 78780608, Rels.las, [0x1D098]),
    LocationData("Palace of Shadow Dark Bones Room: Palace Key", 78780609, Rels.las, [0x1E45C, 0x1E8F8]),
    LocationData("Palace of Shadow Second Bullet Bill Hallway: Ultra Shroom", 78780610, Rels.las, [0x1ECF4]),
    LocationData("Palace of Shadow Large Open Room: Coin", 78780611, Rels.las, [0x1F270]),
    LocationData("Palace of Shadow Large Open Room: Jammin' Jelly", 78780612, Rels.las, [0x1F298]),
    LocationData("Palace of Shadow Large Open Room: P-Up D-Down P", 78780613, Rels.las, [0x1F2C0]),
    LocationData("Riddle Tower Floor 1 NW: Palace Key (Riddle Tower)", 78780614, Rels.las, [0x251E8]),
    LocationData("Riddle Tower Floor 1 NE: Palace Key (Riddle Tower)", 78780615, Rels.las, [0x25690]),
    LocationData("Riddle Tower Floor 1 SW: Palace Key (Riddle Tower)", 78780616, Rels.las, [0x25AC0]),
    LocationData("Riddle Tower Floor 1 SE: Palace Key (Riddle Tower)", 78780617, Rels.las, [0x26008]),
    LocationData("Riddle Tower Floor 2 NW: Palace Key (Riddle Tower)", 78780618, Rels.las, [0x26438]),
    LocationData("Riddle Tower Floor 2 NE: Palace Key (Riddle Tower)", 78780619, Rels.las, [0x268E0]),
    LocationData("Riddle Tower Floor 2 SW: Palace Key (Riddle Tower)", 78780620, Rels.las, [0x26F40]),
    LocationData("Riddle Tower Floor 2 SE: Palace Key (Riddle Tower)", 78780621, Rels.las, [0x27600]),
    LocationData("Palace of Shadow Gloomtail Room: Star Key", 78780634, Rels.las, [0x2D0BC])
]

riddle_tower: typing.List[LocationData] = [
    LocationData("Palace of Shadow Far Hallway 1: Thunder Rage", 78780622, Rels.las, [0x2870C]),
    LocationData("Palace of Shadow Far Backroom 1: Life Shroom", 78780623, Rels.las, [0x298D4]),
    LocationData("Palace of Shadow Far Backroom 1: Repel Cape", 78780624, Rels.las, [0x298AC]),
    LocationData("Palace of Shadow Far Backroom 2: Life Shroom", 78780625, Rels.las, [0x2B678]),
    LocationData("Palace of Shadow Far Backroom 2: Palace Key", 78780626, Rels.las, [0x2B6C0]),
    LocationData("Palace of Shadow Far Backroom 2: Shooting Star", 78780627, Rels.las, [0x2B488]),
    LocationData("Palace of Shadow Far Backroom 3: Coin", 78780628, Rels.las, [0x2C75C]),
    LocationData("Palace of Shadow Far Backroom 3: Palace Key", 78780629, Rels.las, [0x2C478]),
    LocationData("Palace of Shadow Far Backroom 3: Point Swap", 78780630, Rels.las, [0x2C784]),
    LocationData("Palace of Shadow Far Hallway 4: Life Shroom", 78780631, Rels.las, [0x2CE68]),
    LocationData("Palace of Shadow Far Hallway 4: Shooting Star", 78780632, Rels.las, [0x2CE90]),
    LocationData("Palace of Shadow Gloomtail Room: Jammin' Jelly", 78780633, Rels.las, [0x2E6B4]),
    LocationData("Palace of Shadow Gloomtail Room: Ultra Shroom", 78780635, Rels.las, [0x2E68C]),
    LocationData("Palace of Shadow Final Staircase: Jammin' Jelly", 78780636, Rels.las, [0x5CD4C]),
    LocationData("Palace of Shadow Final Staircase: Ultra Shroom", 78780637, Rels.las, [0x5CCC4])
]

pit: typing.List[LocationData] = [
    LocationData("Rogueport Sewers Pit Entrance: Star Piece", 78780142, Rels.tik, [0x1FB68]),
    LocationData("Pit of 100 Trials Floor 10: Sleepy Stomp", 78780638, Rels.jon, [0x11320]),
    LocationData("Pit of 100 Trials Floor 20: Fire Drive", 78780639, Rels.jon, [0x11324]),
    LocationData("Pit of 100 Trials Floor 30: Zap Tap", 78780640, Rels.jon, [0x11328]),
    LocationData("Pit of 100 Trials Floor 40: Pity Flower", 78780641, Rels.jon, [0x1132C]),
    LocationData("Pit of 100 Trials Floor 50: Strange Sack", 78780642, Rels.jon, [0x11330]),
    LocationData("Pit of 100 Trials Floor 60: Double Dip", 78780643, Rels.jon, [0x11334]),
    LocationData("Pit of 100 Trials Floor 70: Double Dip P", 78780644, Rels.jon, [0x11338]),
    LocationData("Pit of 100 Trials Floor 80: Bump Attack", 78780645, Rels.jon, [0x1133C]),
    LocationData("Pit of 100 Trials Floor 90: Lucky Day", 78780646, Rels.jon, [0x11340]),
    LocationData("Pit of 100 Trials Floor 100: Return Postage", 78780647, Rels.jon, [0x11344]),
    #LocationData("Pit of 100 Trials Charlieton: Fire Flower", 78780648, Rels.dol, [0x3C726C]),
    #LocationData("Pit of 100 Trials Charlieton: Honey Syrup", 78780649, Rels.dol, [0x3C7260]),
    #LocationData("Pit of 100 Trials Charlieton: Maple Syrup", 78780650, Rels.dol, [0x3C7264]),
    #LocationData("Pit of 100 Trials Charlieton: Mushroom", 78780651, Rels.dol, [0x3C7258]),
    #LocationData("Pit of 100 Trials Charlieton: Super Shroom", 78780652, Rels.dol, [0x3C725C]),
    #LocationData("Pit of 100 Trials Charlieton: Thunder Rage", 78780653, Rels.dol, [0x3C7270])
]

tattlesanity_region: typing.List[LocationData] = [
    LocationData("Tattle: Goomba", 78780850, Rels.dol, []),  # Tattle Log #1
    LocationData("Tattle: Paragoomba", 78780851, Rels.dol, []),  # Tattle Log #2
    LocationData("Tattle: Spiky Goomba", 78780852, Rels.dol, []),  # Tattle Log #3
    LocationData("Tattle: Hyper Goomba", 78780853, Rels.dol, []),  # Tattle Log #4
    LocationData("Tattle: Hyper Paragoomba", 78780854, Rels.dol, []),  # Tattle Log #5
    LocationData("Tattle: Hyper Spiky Goomba", 78780855, Rels.dol, []),  # Tattle Log #6
    LocationData("Tattle: Gloomba", 78780856, Rels.dol, []),  # Tattle Log #7
    LocationData("Tattle: Paragloomba", 78780857, Rels.dol, []),  # Tattle Log #8
    LocationData("Tattle: Spiky Gloomba", 78780858, Rels.dol, []),  # Tattle Log #9
    LocationData("Tattle: Koopa Troopa", 78780859, Rels.dol, []),  # Tattle Log #10
    LocationData("Tattle: Paratroopa", 78780860, Rels.dol, []),  # Tattle Log #11
    LocationData("Tattle: KP Koopa", 78780861, Rels.dol, []),  # Tattle Log #12
    LocationData("Tattle: KP Paratroopa", 78780862, Rels.dol, []),  # Tattle Log #13
    LocationData("Tattle: Shady Koopa", 78780863, Rels.dol, []),  # Tattle Log #14
    LocationData("Tattle: Shady Paratroopa", 78780864, Rels.dol, []),  # Tattle Log #15
    LocationData("Tattle: Dark Koopa", 78780865, Rels.dol, []),  # Tattle Log #16
    LocationData("Tattle: Dark Paratroopa", 78780866, Rels.dol, []),  # Tattle Log #17
    LocationData("Tattle: Koopatrol", 78780867, Rels.dol, []),  # Tattle Log #18
    LocationData("Tattle: Dark Koopatrol", 78780868, Rels.dol, []),  # Tattle Log #19
    LocationData("Tattle: Dull Bones", 78780869, Rels.dol, []),  # Tattle Log #20
    LocationData("Tattle: Red Bones", 78780870, Rels.dol, []),  # Tattle Log #21
    LocationData("Tattle: Dry Bones", 78780871, Rels.dol, []),  # Tattle Log #22
    LocationData("Tattle: Dark Bones", 78780872, Rels.dol, []),  # Tattle Log #23
    LocationData("Tattle: Hammer Bro", 78780873, Rels.dol, []),  # Tattle Log #24
    LocationData("Tattle: Boomerang Bro", 78780874, Rels.dol, []),  # Tattle Log #25
    LocationData("Tattle: Fire Bro", 78780875, Rels.dol, []),  # Tattle Log #26
    LocationData("Tattle: Lakitu", 78780876, Rels.dol, []),  # Tattle Log #27
    LocationData("Tattle: Dark Lakitu", 78780877, Rels.dol, []),  # Tattle Log #28
    LocationData("Tattle: Spiny", 78780878, Rels.dol, []),  # Tattle Log #29
    LocationData("Tattle: Sky-Blue Spiny", 78780879, Rels.dol, []),  # Tattle Log #30
    LocationData("Tattle: Buzzy Beetle", 78780880, Rels.dol, []),  # Tattle Log #31
    LocationData("Tattle: Spike Top", 78780881, Rels.dol, []),  # Tattle Log #32
    LocationData("Tattle: Parabuzzy", 78780882, Rels.dol, []),  # Tattle Log #33
    LocationData("Tattle: Spiky Parabuzzy", 78780883, Rels.dol, []),  # Tattle Log #34
    LocationData("Tattle: Red Spike Top", 78780884, Rels.dol, []),  # Tattle Log #35
    LocationData("Tattle: Magikoopa", 78780885, Rels.dol, []),  # Tattle Log #36
    LocationData("Tattle: Red Magikoopa", 78780886, Rels.dol, []),  # Tattle Log #37
    LocationData("Tattle: White Magikoopa", 78780887, Rels.dol, []),  # Tattle Log #38
    LocationData("Tattle: Green Magikoopa", 78780888, Rels.dol, []),  # Tattle Log #39
    LocationData("Tattle: Kammy Koopa", 78780889, Rels.dol, []),  # Tattle Log #40
    LocationData("Tattle: Bowser", 78780890, Rels.dol, []),  # Tattle Log #41
    LocationData("Tattle: Gus", 78780891, Rels.dol, []),  # Tattle Log #42
    LocationData("Tattle: Dark Craw", 78780892, Rels.dol, []),  # Tattle Log #43
    LocationData("Tattle: Bandit", 78780893, Rels.dol, []),  # Tattle Log #44
    LocationData("Tattle: Big Bandit", 78780894, Rels.dol, []),  # Tattle Log #45
    LocationData("Tattle: Badge Bandit", 78780895, Rels.dol, []),  # Tattle Log #46
    LocationData("Tattle: Spinia", 78780896, Rels.dol, []),  # Tattle Log #47
    LocationData("Tattle: Spania", 78780897, Rels.dol, []),  # Tattle Log #48
    LocationData("Tattle: Spunia", 78780898, Rels.dol, []),  # Tattle Log #49
    LocationData("Tattle: Fuzzy", 78780899, Rels.dol, []),  # Tattle Log #50
    LocationData("Tattle: Gold Fuzzy", 78780900, Rels.dol, []),  # Tattle Log #51
    LocationData("Tattle: Green Fuzzy", 78780901, Rels.dol, []),  # Tattle Log #52
    LocationData("Tattle: Flower Fuzzy", 78780902, Rels.dol, []),  # Tattle Log #53
    LocationData("Tattle: Pokey", 78780903, Rels.dol, []),  # Tattle Log #54
    LocationData("Tattle: Poison Pokey", 78780904, Rels.dol, []),  # Tattle Log #55
    LocationData("Tattle: Pale Piranha", 78780905, Rels.dol, []),  # Tattle Log #56
    LocationData("Tattle: Putrid Piranha", 78780906, Rels.dol, []),  # Tattle Log #57
    LocationData("Tattle: Frost Piranha", 78780907, Rels.dol, []),  # Tattle Log #58
    LocationData("Tattle: Piranha Plant", 78780908, Rels.dol, []),  # Tattle Log #59
    LocationData("Tattle: Crazee Dayzee", 78780909, Rels.dol, []),  # Tattle Log #60
    LocationData("Tattle: Amazy Dayzee", 78780910, Rels.dol, []),  # Tattle Log #61
    LocationData("Tattle: Pider", 78780911, Rels.dol, []),  # Tattle Log #62
    LocationData("Tattle: Arantula", 78780912, Rels.dol, []),  # Tattle Log #63
    LocationData("Tattle: Swooper", 78780913, Rels.dol, []),  # Tattle Log #64
    LocationData("Tattle: Swoopula", 78780914, Rels.dol, []),  # Tattle Log #65
    LocationData("Tattle: Swampire", 78780915, Rels.dol, []),  # Tattle Log #66
    LocationData("Tattle: Dark Puff", 78780916, Rels.dol, []),  # Tattle Log #67
    LocationData("Tattle: Ruff Puff", 78780917, Rels.dol, []),  # Tattle Log #68
    LocationData("Tattle: Ice Puff", 78780918, Rels.dol, []),  # Tattle Log #69
    LocationData("Tattle: Poison Puff", 78780919, Rels.dol, []),  # Tattle Log #70
    LocationData("Tattle: Boo", 78780920, Rels.dol, []),  # Tattle Log #71
    LocationData("Tattle: Atomic Boo", 78780921, Rels.dol, []),  # Tattle Log #72
    LocationData("Tattle: Dark Boo", 78780922, Rels.dol, []),  # Tattle Log #73
    LocationData("Tattle: Ember", 78780923, Rels.dol, []),  # Tattle Log #74
    LocationData("Tattle: Lava Bubble", 78780924, Rels.dol, []),  # Tattle Log #75
    LocationData("Tattle: Phantom Ember", 78780925, Rels.dol, []),  # Tattle Log #76
    LocationData("Tattle: Bald Cleft", 78780926, Rels.dol, []),  # Tattle Log #77
    LocationData("Tattle: Hyper Bald Cleft", 78780927, Rels.dol, []),  # Tattle Log #78
    LocationData("Tattle: Cleft", 78780928, Rels.dol, []),  # Tattle Log #79
    LocationData("Tattle: Iron Cleft", 78780929, Rels.dol, []),  # Tattle Log #80
    LocationData("Tattle: Hyper Cleft", 78780931, Rels.dol, []),  # Tattle Log #82
    LocationData("Tattle: Moon Cleft", 78780932, Rels.dol, []),  # Tattle Log #83
    LocationData("Tattle: Bristle", 78780933, Rels.dol, []),  # Tattle Log #84
    LocationData("Tattle: Dark Bristle", 78780934, Rels.dol, []),  # Tattle Log #85
    LocationData("Tattle: Bob-omb", 78780935, Rels.dol, []),  # Tattle Log #86
    LocationData("Tattle: Bulky Bob-omb", 78780936, Rels.dol, []),  # Tattle Log #87
    LocationData("Tattle: Bob-ulk", 78780937, Rels.dol, []),  # Tattle Log #88
    LocationData("Tattle: Chain-Chomp", 78780938, Rels.dol, []),  # Tattle Log #89
    LocationData("Tattle: Red Chomp", 78780939, Rels.dol, []),  # Tattle Log #90
    LocationData("Tattle: Bill Blaster", 78780940, Rels.dol, []),  # Tattle Log #91
    LocationData("Tattle: Bullet Bill", 78780941, Rels.dol, []),  # Tattle Log #92
    LocationData("Tattle: B. Bill Blaster", 78780942, Rels.dol, []),  # Tattle Log #93
    LocationData("Tattle: Bombshell Bill", 78780943, Rels.dol, []),  # Tattle Log #94
    LocationData("Tattle: Dark Wizzerd", 78780944, Rels.dol, []),  # Tattle Log #95
    LocationData("Tattle: Wizzerd", 78780945, Rels.dol, []),  # Tattle Log #96
    LocationData("Tattle: Elite Wizzerd", 78780946, Rels.dol, []),  # Tattle Log #97
    LocationData("Tattle: Blooper", 78780947, Rels.dol, []),  # Tattle Log #98
    LocationData("Tattle: Hooktail", 78780948, Rels.dol, []),  # Tattle Log #99
    LocationData("Tattle: Gloomtail", 78780949, Rels.dol, []),  # Tattle Log #100
    LocationData("Tattle: Bonetail", 78780950, Rels.dol, []),  # Tattle Log #101
    LocationData("Tattle: Rawk Hawk", 78780951, Rels.dol, []),  # Tattle Log #102
    LocationData("Tattle: Macho Grubba", 78780952, Rels.dol, []),  # Tattle Log #103
    LocationData("Tattle: Doopliss", 78780953, Rels.dol, []),  # Tattle Log #104
    LocationData("Tattle: Cortez", 78780954, Rels.dol, []),  # Tattle Log #105
    LocationData("Tattle: Smorg", 78780955, Rels.dol, []),  # Tattle Log #106
    LocationData("Tattle: X-Naut", 78780956, Rels.dol, []),  # Tattle Log #107
    LocationData("Tattle: X-Naut PhD", 78780957, Rels.dol, []),  # Tattle Log #108
    LocationData("Tattle: Elite X-Naut", 78780958, Rels.dol, []),  # Tattle Log #109
    LocationData("Tattle: Yux", 78780959, Rels.dol, []),  # Tattle Log #110
    LocationData("Tattle: Mini-Yux", 78780960, Rels.dol, []),  # Tattle Log #111
    LocationData("Tattle: Z-Yux", 78780961, Rels.dol, []),  # Tattle Log #112
    LocationData("Tattle: Mini-Z-Yux", 78780962, Rels.dol, []),  # Tattle Log #113
    LocationData("Tattle: X-Yux", 78780963, Rels.dol, []),  # Tattle Log #114
    LocationData("Tattle: Mini-X-Yux", 78780964, Rels.dol, []),  # Tattle Log #115
    LocationData("Tattle: Grodus X", 78780965, Rels.dol, []),  # Tattle Log #116
    LocationData("Tattle: Magnus von Grapple", 78780966, Rels.dol, []),  # Tattle Log #117
    LocationData("Tattle: Magnus von Grapple 2.0", 78780967, Rels.dol, []),  # Tattle Log #118
    LocationData("Tattle: Lord Crump", 78780968, Rels.dol, []),  # Tattle Log #119
    LocationData("Tattle: Sir Grodus", 78780969, Rels.dol, []),  # Tattle Log #120
    LocationData("Tattle: Beldam", 78780970, Rels.dol, []),  # Tattle Log #121
    LocationData("Tattle: Marilyn", 78780971, Rels.dol, []),  # Tattle Log #122
    LocationData("Tattle: Vivian", 78780972, Rels.dol, []),  # Tattle Log #123
    LocationData("Tattle: Shadow Queen", 78780973, Rels.dol, []),  # Tattle Log #124
]

shadow_queen: typing.List[LocationData] = [
    LocationData("Shadow Queen", None, Rels.las, [])
]

all_locations: typing.List[LocationData] = (rogueport + rogueport_westside + sewers + sewers_westside + sewers_westside_ground +
                                            petal_left + petal_right + hooktails_castle + boggly_woods +
                                            great_tree + glitzville + twilight_town_region + twilight_trail + creepy_steeple +
                                            keelhaul_key + pirates_grotto + excess_express + riverside + poshley_heights +
                                            fahr_outpost + xnaut_fortress + palace + riddle_tower + pit + shadow_queen + tattlesanity_region)

location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}

location_id_to_name: typing.Dict[int, str] = {locData.id: locData.name for locData in all_locations if locData.id is not None}

locationName_to_data: typing.Dict[str, LocationData] = {locData.name: locData for locData in all_locations}
