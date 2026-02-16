from .Data import star_locations
from .Options import StarShuffle
from rule_builder.rules import Rule, Has, CanReachRegion
from BaseClasses import CollectionState
import dataclasses



def westside():
    return Has("Contact Lens") | Has("Bobbery") | tube_curse() | ultra_hammer()

def fallen_pipe():
    return Has("Bobbery") | tube_curse()


def super_hammer():
    return Has("Progressive Hammer", count=1)


def ultra_hammer():
    return Has("Progressive Hammer", count=2)


def super_boots():
    return Has("Progressive Boots", count=1)


def ultra_boots():
    return Has("Progressive Boots", count=2)



def tube_curse():
    return Has("Paper Mode") & Has("Tube Mode")


def petal_left():
    return Has("Plane Mode")


def hooktails_castle():
    return Has("Sun Stone") & Has("Moon Stone") & (Has("Koops") | Has("Bobbery"))


def boggly_woods():
    return Has("Paper Mode")


def great_tree():
    return Has("Flurrie")


def glitzville():
    return Has("Blimp Ticket")

def twilight_town():
    return (
        (sewer_westside() & Has("Yoshi"))
        | (sewer_westside_ground() & ultra_boots())
    )



def twilight_trail():
    return twilight_town() & tube_curse()


def steeple():
    return Has("Paper Mode") & Has("Flurrie") & super_boots()


def keelhaul_key():
    return Has("Yoshi") & tube_curse() & Has("Old Letter")


def pirates_grotto():
    return Has("Yoshi") & Has("Bobbery") & Has("Skull Gem") & super_boots()


def excess_express():
    return Has("Train Ticket")


def riverside():
    return (
        Has("Vivian")
        & Has("Autograph")
        & Has("Ragged Diary")
        & Has("Blanket")
        & Has("Vital Paper")
        & Has("Train Ticket")
    )


def poshley_heights():
    return (
        Has("Station Key 1")
        & Has("Elevator Key (Station)")
        & super_hammer()
        & ultra_boots()
    )


def fahr_outpost():
    return ultra_hammer() & twilight_town()


def moon():
    return Has("Bobbery") & Has("Goldbob Guide")


def ttyd():
    return (
        Has("Plane Mode")
        | super_hammer()
        | (
            Has("Flurrie")
            & (
                Has("Bobbery")
                | tube_curse()
                | (Has("Contact Lens") & Has("Paper Mode"))
            )
        )
    )


def pit():
    return Has("Paper Mode") & Has("Plane Mode")


def pit_westside_ground():
    return (
        Has("Flurrie")
        & (
            (Has("Contact Lens") & Has("Paper Mode"))
            | Has("Bobbery")
            | tube_curse()
            | ultra_hammer()
        )
    )



@dataclasses.dataclass()
class PalaceAccess(Rule["TTYDWorld"], game="Paper Mario TTYD"):
    chapters: int

    def _instantiate(self, world: "TTYDWorld") -> Rule.Resolved:
        return self.Resolved(
            base_rule=ttyd().resolve(world),
            chapters=self.chapters,
            star_shuffle=world.options.star_shuffle.value,
            player=world.player,
        )

    class Resolved(Rule.Resolved):
        base_rule: Rule.Resolved
        chapters: int
        star_shuffle: int
        player: int

        def _evaluate(self, state: CollectionState) -> bool:
            if not self.base_rule(state):
                return False

            if self.star_shuffle == StarShuffle.option_all:
                return state.has("stars", self.player, self.chapters)

            return state.has("required_stars", self.player, self.chapters)




def riddle_tower():
    return (
        tube_curse()
        & Has("Palace Key")
        & Has("Bobbery")
        & Has("Boat Mode")
        & Has("Star Key")
        & Has("Palace Key (Tower)", count=8)
    )


def sewer_westside():
    return (
        tube_curse()
        | Has("Bobbery")
        | (Has("Paper Mode") & Has("Contact Lens"))
        | (ultra_hammer() & (Has("Paper Mode") | (ultra_boots() & Has("Yoshi"))))
    )


def sewer_westside_ground():
    return (
        (Has("Contact Lens") & Has("Paper Mode"))
        | Has("Bobbery")
        | tube_curse()
        | ultra_hammer()
    )


def key_any():
    return (
        (Has("Red Key") | Has("Blue Key"))
    )


def key_both():
    return (
        Has("Red Key")
        & Has("Blue Key")
    )


@dataclasses.dataclass()
class ChapterCompletions(Rule["TTYDWorld"], game="Paper Mario TTYD"):
    count: int

    def _instantiate(self, world: "TTYDWorld") -> Rule.Resolved:
        return self.Resolved(
            count=self.count,
            player=world.player,
        )

    class Resolved(Rule.Resolved):
        count: int
        player: int

        def _evaluate(self, state: CollectionState) -> bool:
            return (
                len([l for l in star_locations if state.can_reach(l, "Location", self.player)])
                >= self.count
            )

def partner_press_switch():
    return Has("Koops") | Has("Bobbery")

def super_blue_pipes():
    return super_hammer() & super_boots()


def ultra_blue_pipes():
    return ultra_hammer() & super_boots()
