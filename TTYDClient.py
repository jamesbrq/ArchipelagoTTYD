import asyncio
import subprocess
import traceback
import settings

import Patch
import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
import dolphin_memory_engine as dolphin

from NetUtils import NetworkItem, ClientStatus
from worlds.ttyd.Data import location_gsw_info
from worlds.ttyd.Items import items_by_id, item_type_dict

RECEIVED_INDEX = 0x803DB860
RECEIVED_ITEM = 0x803DB864
NAME_LENGTH = 0x800031FF
PLAYER_NAME = 0x80003200
SEED = 0x80003210
GP_BASE = 0x803DAC18
GSWF_BASE = 0x178
GSW0 = 0x174
GSW_BASE = 0x578
ROOM = 0x803DF728
SHOP_POINTER = 0x8041EB60
SHOP_ITEM_OFFSET = 0x2F
SHOP_ITEM_PURCHASED = 0xD7

def read_string(address: int, length: int):
    return dolphin.read_bytes(address, length).decode().strip("\0")

def get_rom_item_id(item: NetworkItem):
    item = item_type_dict[items_by_id[item.item].itemName]
    return item

def _get_bit_address(bit_number: int) -> tuple:
    word_index = bit_number >> 5
    bit_position = bit_number & 0x1F
    word_address = GP_BASE + (word_index * 4) + GSWF_BASE
    byte_within_word = 3 - (bit_position >> 3)
    byte_address = word_address + byte_within_word
    bit = bit_position & 0x7
    return byte_address, bit

def gswf_set(bit_number: int):
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    new_byte = current_byte | bit_mask
    dolphin.write_byte(byte_address, new_byte)
    return result

def gswf_check(bit_number: int) -> bool:
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    return bool(current_byte & bit_mask)

def gsw_set(index, value):
    dolphin.write_word(GP_BASE + GSW0, value) if index == 0 else dolphin.write_byte(GP_BASE + index + GSW_BASE, value)

def gsw_check(index):
    return dolphin.read_word(GP_BASE + GSW0) if index == 0 else dolphin.read_byte(GP_BASE + index + GSW_BASE)


class TTYDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_set_gswf(self, bit_number: int):
        byte_address, bit = gswf_set(int(bit_number))
        logger.info(f"Bit {bit} written at {byte_address}")

    def _cmd_check_gswf(self, bit_number: int):
        result = gswf_check(int(bit_number))
        logger.info(f"GSWF Check: 0x{format(result, 'x')}")

    def _cmd_set_gsw(self, gsw: int, value: int):
        gsw_set(int(gsw), int(value))

    def _cmd_check_gsw(self, gsw: int):
        result = gsw_check(int(gsw))
        logger.info(f"GSWF Check: {result}")


class TTYDContext(CommonContext):
    command_processor = TTYDCommandProcessor
    game = "Paper Mario The Thousand Year Door"
    items_handling = 0b101
    dolphin_connected: bool = False
    seed_verified: bool = False
    slot_data: dict | None = {}
    checked_locations = set()
    previous_room = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TTYDContext, self).server_auth(password_requested)
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.slot = args["slot"]
            self.team = args["team"]
            self.slot_data = args["slot_data"]
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to TTYDClient: {args}")
                return
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect()
        self.slot = None
        self.team = None
        self.slot_data = None
        self.checked_locations = set()
        self.seed_name = None
        self.seed_verified = False

    def run_gui(self):
        from kvui import GameManager

        class TTYDManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago TTYD Client"

        self.ui = TTYDManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def receive_items(self):
        index = dolphin.read_word(RECEIVED_INDEX)
        for i in range(index, len(self.items_received)):
            dolphin.write_word(RECEIVED_ITEM, get_rom_item_id(self.items_received[i]))
            await asyncio.sleep(0.2)
            dolphin.write_word(RECEIVED_INDEX, i + 1)

    async def check_ttyd_locations(self):
        locations_to_send = set()
        try:
            for location, gsw_info in location_gsw_info.items():
                gsw_type, offset, value = gsw_info
                if offset == 0:
                    continue
                if gsw_type.value == 0:
                    if gsw_check(offset) >= value:
                        locations_to_send.add(location)
                elif gsw_type.value == 1:
                    if gswf_check(offset):
                        locations_to_send.add(location)
            if len(locations_to_send) > 0:
                self.checked_locations &= locations_to_send
                await self.send_msgs([{"cmd": 'LocationChecks', "locations": locations_to_send}])
        except Exception as e:
            logger.error(traceback.format_exc())

    def save_loaded(self) -> bool:
        value = dolphin.read_byte(0x80003228)
        return value > 0
    
async def _run_game(rom: str):
    import os
    auto_start = settings.get_settings().ttyd_options.rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings().ttyd_options.dolphin_path
        subprocess.Popen(
            [
                dolphin_path,
                f"--exec={os.path.realpath(rom)}",
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    Utils.async_start(_run_game(output_file))
    return metadata


# Sends player items from server
# Checks for player status to see if they are in/loading a level
# Checks location status inside of levels
async def ttyd_sync_task(ctx: TTYDContext):
    logger.info("Starting Dolphin connector...")
    while not ctx.exit_event.is_set():
        if dolphin.is_hooked() and ctx.dolphin_connected:
            if ctx.slot:
                try:
                    if not ctx.seed_verified:
                        logger.info("Checking ROM seed...")
                        seed = read_string(SEED, 0x10)
                        logger.info(ctx.seed_name)
                        if seed not in ctx.seed_name:
                            await ctx.disconnect()
                            logger.info("ROM Seed does not match Room seed. Please make sure you are using the correct patch.")
                            dolphin.un_hook()
                            await asyncio.sleep(3)
                            continue
                        ctx.seed_verified = True
                    if not ctx.save_loaded():
                        await asyncio.sleep(1)
                        continue
                    current_room = read_string(ROOM, 6)
                    if ctx.previous_room != current_room:
                        ctx.previous_room = current_room
                        await ctx.send_msgs([{
                                "cmd": "Set",
                                "key": f"ttyd_room_{ctx.team}_{ctx.slot}",
                                "default": 0,
                                "want_reply": False,
                                "operations":[{"operation": "replace","value": current_room}]
                            }])
                    await ctx.receive_items()
                    await ctx.check_ttyd_locations()
                    if not ctx.finished_game and gsw_check(1708) >= 18:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    await asyncio.sleep(0.1)
                except Exception as e:
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
            else:
                try:
                    if not ctx.auth:
                        name_length = dolphin.read_byte(NAME_LENGTH)
                        if name_length == 0:
                            ctx.auth = read_string(PLAYER_NAME, 0x10)
                        else:
                            ctx.auth = dolphin.read_bytes(PLAYER_NAME, name_length).decode()
                        if not ctx.auth:
                            logger.info(f"Name Read: {dolphin.read_bytes(PLAYER_NAME, name_length).decode()}")
                            ctx.auth = None
                            logger.info("No slot name was detected. Please load the correct ROM.")
                            ctx.dolphin_connected = False
                            dolphin.un_hook()
                            await asyncio.sleep(3)
                            continue
                    await asyncio.sleep(0.1)
                except Exception as e:
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
        else:
            try:
                logger.info("Attempting to connect to Dolphin...")
                dolphin.hook()
                if not dolphin.is_hooked():
                    logger.info("Connection to Dolphin failed... Attempting again")
                    ctx.dolphin_connected = False
                    await ctx.disconnect()
                    await asyncio.sleep(3)
                    continue

                logger.info("Dolphin connected")
                ctx.dolphin_connected = True
            except Exception as e:
                dolphin.un_hook()
                logger.info("Connection to Dolphin failed... Attempting again")
                logger.error(traceback.format_exc())
                ctx.dolphin_connected = False
                await ctx.disconnect()
                await asyncio.sleep(3)
                continue


def launch(*args):
    async def main(args):
        if args.patch_file:
            await asyncio.create_task(_patch_and_run_game(args.patch_file))
        ctx = TTYDContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.gl_sync_task = asyncio.create_task(ttyd_sync_task(ctx), name="Gauntlet Legends Sync Task")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APTTYD file")
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
