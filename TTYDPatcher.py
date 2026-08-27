import io
import os
import shutil
import sys
import tempfile
import zipfile

from typing import Dict, List, Optional
from settings import get_settings
from .Data import Rels


def _find_apworld_path() -> Optional[str]:
    """Walk up from this file to the containing .apworld, if there is one."""
    if ".apworld" not in __file__:
        return None
    path = __file__
    while not path.lower().endswith(".apworld"):
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent
    return path


def _extraction_valid(target_dir: str, required_files: List[str]) -> bool:
    return all(os.path.isfile(os.path.join(target_dir, rel)) for rel in required_files)


def _cleanup_stale_extractions(cache_root: str, keep_dir: str) -> None:
    try:
        entries = os.listdir(cache_root)
    except OSError:
        return
    keep = os.path.basename(keep_dir)
    for entry in entries:
        if entry != keep:
            shutil.rmtree(os.path.join(cache_root, entry), ignore_errors=True)
    # Cache locations used before per-build directories existed.
    for legacy in ("ttyd_temp_dme", "ttyd_temp_gclib"):
        shutil.rmtree(os.path.join(tempfile.gettempdir(), legacy), ignore_errors=True)


def _extract_from_apworld(zip_file_path: str, member_filter: str, cache_name: str,
                          required_files: List[str]) -> str:
    stat = os.stat(zip_file_path)
    stamp = f"{int(stat.st_mtime)}_{stat.st_size}"
    cache_root = os.path.join(tempfile.gettempdir(), cache_name)
    final_dir = os.path.join(cache_root, stamp)

    if not _extraction_valid(final_dir, required_files):
        os.makedirs(cache_root, exist_ok=True)
        work_dir = tempfile.mkdtemp(dir=cache_root, prefix=stamp + ".tmp")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                if member_filter in member:
                    zip_ref.extract(member, work_dir)
        if not _extraction_valid(work_dir, required_files):
            shutil.rmtree(work_dir, ignore_errors=True)
            raise FileNotFoundError(
                f"{zip_file_path} does not contain the expected {member_filter} files; "
                f"please re-install the apworld")
        shutil.rmtree(final_dir, ignore_errors=True)
        try:
            os.rename(work_dir, final_dir)
        except OSError:
            if _extraction_valid(final_dir, required_files):
                shutil.rmtree(work_dir, ignore_errors=True)
            else:
                final_dir = work_dir

    _cleanup_stale_extractions(cache_root, final_dir)
    return final_dir


def setup_gclib_path():
    """Makes the bundled gclib package importable; returns its directory."""
    apworld_path = _find_apworld_path()
    if apworld_path is not None:
        target = _extract_from_apworld(apworld_path, "gclib", "ttyd_cache_gclib",
                                       [os.path.join("ttyd", "lib", "gclib", "__init__.py")])
        lib_parent = os.path.join(target, "ttyd", "lib")
    else:
        lib_parent = os.path.join(os.path.dirname(__file__), "lib")

    if lib_parent not in sys.path:
        sys.path.insert(0, lib_parent)
    return os.path.join(lib_parent, "gclib")


def _select_native_binary(pkg_dir: str) -> None:
    import platform
    system = platform.system()
    if system == "Linux":
        src = "_abi3_linux_x86_64.so"
    elif system == "Darwin":
        machine = platform.machine().lower()
        src = "_abi3_macos_arm64.so" if machine in ("arm64", "aarch64") else "_abi3_macos_x86_64.so"
    else:
        return
    src_path = os.path.join(pkg_dir, src)
    dest_path = os.path.join(pkg_dir, "_dolphin_memory_engine.abi3.so")
    if os.path.exists(src_path) and not os.path.exists(dest_path):
        shutil.copyfile(src_path, dest_path)


def _dme_required_files() -> List[str]:
    import platform
    pkg = os.path.join("ttyd", "lib", "dolphin_memory_engine_ttyd")
    system = platform.system()
    if system == "Linux":
        native = "_abi3_linux_x86_64.so"
    elif system == "Darwin":
        machine = platform.machine().lower()
        native = "_abi3_macos_arm64.so" if machine in ("arm64", "aarch64") else "_abi3_macos_x86_64.so"
    else:
        native = "_dolphin_memory_engine.pyd"
    return [os.path.join(pkg, "__init__.py"), os.path.join(pkg, native)]


def setup_dme_path():
    """Makes the bundled dolphin_memory_engine_ttyd package importable."""
    apworld_path = _find_apworld_path()
    if apworld_path is not None:
        target = _extract_from_apworld(apworld_path, "dolphin_memory_engine", "ttyd_cache_dme",
                                       _dme_required_files())
        lib_parent = os.path.join(target, "ttyd", "lib")
    else:
        lib_parent = os.path.join(os.path.dirname(__file__), "lib")

    pkg_dir = os.path.join(lib_parent, "dolphin_memory_engine_ttyd")
    _select_native_binary(pkg_dir)

    if lib_parent not in sys.path:
        sys.path.insert(0, lib_parent)

    if hasattr(os, "add_dll_directory") and os.path.isdir(pkg_dir):
        try:
            os.add_dll_directory(pkg_dir)
        except OSError:
            pass

    return lib_parent


dolphin = None


class TTYDPatcher:
    rels: Dict[Rels, io.BytesIO] = {}

    def __init__(self):
        setup_gclib_path()
        from gclib.gcm import GCM
        from gclib.dol import DOL

        self.iso = GCM(get_settings().ttyd_options.rom_file)
        self.iso.read_entire_disc()
        self.dol = DOL()
        self.dol.read(self.iso.read_file_data("sys/main.dol"))
        for rel in Rels:
            if rel == Rels.dol:
                continue
            path = get_rel_path(rel)
            self.rels[rel] = self.iso.read_file_data(path)


def get_rel_path(rel: Rels):
    return f'files/rel/{rel.value}.rel'