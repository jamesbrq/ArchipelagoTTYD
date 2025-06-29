def westside(state, player):
    return state.has("Contact Lens", player) or state.has("Bobbery", player) or tube_curse(state, player) or ultra_hammer(state, player)


def super_hammer(state, player):
    return state.has("Progressive Hammer", player, 1)


def ultra_hammer(state, player):
    return state.has("Progressive Hammer", player, 2)


def super_boots(state, player):
    return state.has("Progressive Boots", player, 1)


def ultra_boots(state, player):
    return state.has("Progressive Boots", player, 2)


def tube_curse(state, player):
    return state.has("Paper Curse", player) and state.has("Tube Curse", player)


def petal_left(state, player):
    return state.has("Plane Curse", player)


def petal_right(state, player):
    return super_hammer(state, player) and super_boots(state, player)


def hooktails_castle(state, player):
    return state.has("Sun Stone", player) and state.has("Moon Stone", player) and (state.has("Koops", player) or state.has("Bobbery", player))


def boggly_woods(state, player):
    return state.has("Paper Curse", player) or (super_hammer(state, player) and super_boots(state, player))


def great_tree(state, player):
    return state.has("Flurrie", player)


def glitzville(state, player):
    return state.has("Blimp Ticket", player)

def twilight_trail(state, player):
    return tube_curse(state, player)


def steeple(state, player):
    return state.has("Paper Curse", player) and state.has("Flurrie", player) and super_boots(state, player)


def keelhaul_key(state, player):
    return ((state.has("Yoshi", player) and tube_curse(state, player) and state.has("Old Letter", player))
            or (ultra_hammer(state, player) and super_boots(state, player)))


def pirates_grottos(state, player):
    return state.has("Yoshi", player) and state.has("Bobbery", player) and state.has("Skull Gem", player) and super_boots(state, player)


def excess_express(state, player):
    return state.has("Train Ticket", player)


def riverside(state, player):
    return state.has("Vivian", player) and state.has("Autograph", player) and state.has("Ragged Diary", player) and state.has("Blanket", player) and state.has("Vital Paper", player)


def poshley_heights(state, player):
    return state.has("Station Key 1", player) and state.has("Elevator Key (Riverside)", player) and super_hammer(state, player) and ultra_boots(state, player)


def fahr_outpost(state, player):
    return ultra_hammer(state, player) and ((state.can_reach("Rogueport Sewers Westside Ground", "Region", player) and ultra_boots(state, player)) or (state.can_reach("Rogueport Sewers Westside", "Region", player) and state.has("Yoshi", player)))


def moon(state, player):
    return state.has("Bobbery", player) and state.has("Goldbob Guide", player)


def ttyd(state, player):
    return (state.has("Plane Curse", player) or super_hammer(state, player)
            or (state.has("Flurrie", player) and (state.has("Bobbery", player) or tube_curse(state, player)
            or (state.has("Contact Lens", player) and state.has("Paper Curse", player)))))


def pit(state, player):
    return state.has("Paper Curse", player) and state.has("Plane Curse", player)


def pit_westside_ground(state, player):
    return state.has("Flurrie", player) and ((state.has("Contact Lens", player) and state.has("Paper Curse", player)) or state.has("Bobbery", player) or tube_curse(state, player) or ultra_hammer(state, player))


def palace(state, player, chapters: int):
    return ttyd(state, player) and state.has("required_stars", player, chapters)


def riddle_tower(state, player):
    return tube_curse(state, player) and state.has("Palace Key", player) and state.has("Bobbery", player) and state.has("Boat Curse", player) and state.has("Star Key", player) and state.has("Palace Key (Riddle Tower)", player, 8)


def sewer_westside(state, player):
    return tube_curse(state, player) or state.has("Bobbery", player) or (state.has("Paper Curse", player) and state.has("Contact Lens", player)) or (ultra_hammer(state, player) and (state.has("Paper Curse", player) or (ultra_boots(state, player) and state.has("Yoshi", player))))


def sewer_westside_ground(state, player):
    return (state.has("Contact Lens", player) and state.has("Paper Curse", player)) or state.has("Bobbery", player) or tube_curse(state, player) or ultra_hammer(state, player)

def key_any(state, player):
    return state.has("Red Key", player) or state.has("Blue Key", player)
