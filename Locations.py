import typing

from BaseClasses import Location
from .Data import Rels


class LocationData:
    name: str = ""
    id: int | None = 0x0
    rel: Rels = None
    offset: typing.List[int] = []
    vanilla_item: int = 0x0
    tags: typing.List[str] = []

    def __init__(self, name: str, id: int | None, rel: Rels, offsets: typing.List[str]=None, vanilla_item: int=0x0, tags=None):
        if tags is None:
            tags = []
        self.name = name
        self.id = id
        self.rel = Rels(rel)
        self.offset = [int(offset, 16) for offset in offsets]
        self.vanilla_item = vanilla_item
        self.tags = tags



class TTYDLocation(Location):
    game: str = "Paper Mario: The Thousand-Year Door"

def import_locations() -> typing.List[LocationData]:
    import json
    import pkgutil

    return (json.loads(pkgutil.get_data(__name__, "json/locations.json").decode("utf-8"), object_hook=lambda d: LocationData(**d)) +
              json.loads(pkgutil.get_data(__name__, "json/tattles.json").decode("utf-8"), object_hook=lambda d: LocationData(**d)))



def get_locations_by_tags(tags: str | typing.List[str]) -> typing.List[LocationData]:
    if isinstance(tags, str):
        tags = [tags]
    return [loc for loc in all_locations if any(tag in loc.tags for tag in tags)]


def get_locations_by_all_tags(tags: typing.List[str]) -> typing.List[LocationData]:
    if isinstance(tags, str):
        tags = [tags]
    return [loc for loc in all_locations if all(tag in loc.tags for tag in tags)]


def get_location_ids(locations: typing.List[LocationData]) -> typing.List[int]:
    return [loc.id for loc in locations if loc.id]


def get_location_names(locations: typing.List[LocationData]) -> typing.List[str]:
    return [loc.name for loc in locations if loc.name]


def get_vanilla_item_names(locations: typing.List[LocationData]) -> typing.List[str]:
    from .Items import items_by_id
    return [items_by_id.get(loc.vanilla_item, "Unknown").item_name for loc in locations]


shadow_queen: typing.List[LocationData] = [
    LocationData("Shadow Queen", None, Rels.las, [])
]

all_locations: typing.List[LocationData] = import_locations() + shadow_queen

location_table: typing.Dict[str, int] = {locData.name: locData.id for locData in all_locations}

location_id_to_name: typing.Dict[int, str] = {locData.id: locData.name for locData in all_locations if locData.id is not None}

locationName_to_data: typing.Dict[str, LocationData] = {locData.name: locData for locData in all_locations}
