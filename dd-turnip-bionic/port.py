#!/usr/bin/env python3
"""Port source-level Linux-only DD-Turnip GPU patches to Android Bionic.

Pinned to Droid-Deck/Drivers at DD-Turnip-v0.9.1 (ac34abe140).
Preserves the Android gralloc patches and the original Mesa patch ordering.
Only GPU/IR3/Turnip patches cross the platform boundary. No Linux WSI or
DroidDeck-specific display-buffer protocol is enabled on Android.
"""
import json
import sys
from pathlib import Path

PORT = (
    "linux/0001-tu-mesh-shader-emulation.patch",
    "linux/0002-ir3-half-wave-subgroups.patch",
    "linux/0003-ir3-a8xx-cube-direction-sanitize.patch",
    "linux/0004-tu-a8xx-bindless-invalidate.patch",
    "linux/0005-tu-kgsl-a8xx-ib-virtual-alias.patch",
    "linux/0006-ir3-shuffle-broadcast.patch",
)
LINUX_SPECIFIC = {
    "scripts/linux_kgsl_wsi.py",
    "scripts/linux_gralloc_exports.py",
}

def port(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    paths = {entry["file"] for entry in data}
    missing = (set(PORT) | LINUX_SPECIFIC) - paths
    if missing:
        raise RuntimeError(f"DD release patch set changed: {sorted(missing)}")
    changed = []
    for entry in data:
        if entry["file"] in PORT:
            if entry["targets"] != ["linux"]:
                raise RuntimeError(f"Unexpected patch targets: {entry['file']}: {entry['targets']}")
            entry["targets"] = ["android", "linux"]
            changed.append(entry["file"])
        elif entry["file"] in LINUX_SPECIFIC and entry["targets"] != ["linux"]:
            raise RuntimeError(f"Linux WSI/display patch unexpectedly changed: {entry['file']}")
    if changed != list(PORT):
        raise RuntimeError(f"Unexpected port order: {changed!r}")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Ported {len(changed)} Linux GPU patches for Android Bionic:")
    for name in changed:
        print(f"  - {name}")
    print("Linux DRM/WSI and DroidDeck display-buffer socket remain Linux-only.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <drivers/patches/series.json>")
    port(Path(sys.argv[1]))
