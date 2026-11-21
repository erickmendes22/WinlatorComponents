#!/usr/bin/env python3
"""Pack an actual Android Bionic libvulkan_freedreno.so as an Adrenotools ZIP."""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("drivers/out/android/libvulkan_freedreno.so")
OUT = Path("dist/DD-Turnip-v0.9.1-Bionic-LinuxGPU6.zip")
MESA = "0c418c5054a1223668c73614227c5f4cb67addaf"
RECIPE = "ac34abe1406645fe18e12db9fe3102ebd2c637d2"

def main():
    if not LIB.is_file() or LIB.stat().st_size < 1_000_000:
        raise SystemExit(f"Missing or suspicious Android Turnip ELF: {LIB}")
    hdr = subprocess.check_output(["readelf", "-h", str(LIB)], text=True)
    dynamic = subprocess.check_output(["readelf", "-d", str(LIB)], text=True)
    linked = set(re.findall(r"\(NEEDED\)\s+Shared library: \[(.+?)\]", dynamic))
    if "AArch64" not in hdr or "DYN" not in hdr or "libc.so" not in linked or "libc.so.6" in linked:
        raise SystemExit(f"Not an Android Bionic AArch64 driver (NEEDED={sorted(linked)})")
    driver = LIB.read_bytes()
    if b"Using IMapper v5 stable-C API via SP-HAL" not in driver:
        raise SystemExit("Android IMapper5 support missing from built driver")
    meta = {
        "schemaVersion": 1,
        "name": "DD Turnip v0.9.1 Bionic + Linux GPU patches",
        "description": "DD Turnip 0.9.1 (Mesa 27.0.0-devel), six IR3/Turnip Linux GPU patches ported to Android Bionic",
        "author": "DroidDeck; Android port recipe: erickmendes22",
        "packageVersion": "1",
        "vendor": "Mesa",
        "driverVersion": "DD-Turnip-v0.9.1-Bionic-LinuxGPU6",
        "minApi": 29,
        "libraryName": "libvulkan_freedreno.so"
    }
    notice = (
        "DD Turnip 0.9.1 Android Bionic + six Linux GPU/IR3 patches\n"
        f"Mesa: {MESA}\n"
        f"Recipe: https://github.com/Droid-Deck/Drivers/commit/{RECIPE}\n"
        "Upstream source archive: https://github.com/Droid-Deck/Drivers/releases/tag/DD-Turnip-v0.9.1\n"
        "Integration recipe: https://github.com/erickmendes22/WinlatorComponents/tree/dd-turnip-v0.9.1-bionic-port/dd-turnip-bionic\n"
        "Original DD driver patches under GPL-3.0; Mesa licensing preserved.\n"
        "Linux WSI/compositor socket patches are not applicable to Android WSI.\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("meta.json", json.dumps(meta, indent=2)+"\n")
        z.writestr("libvulkan_freedreno.so", driver)
        z.writestr("NOTICE", notice)
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        assert {"meta.json", "libvulkan_freedreno.so"} <= set(z.namelist())
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    OUT.with_name(OUT.name + ".sha256").write_text(f"{digest}  {OUT.name}\n")
    print(OUT, OUT.stat().st_size, digest)

if __name__ == "__main__":
    main()
