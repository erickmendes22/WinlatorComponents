#!/usr/bin/env python3
"""Convert a VKD3D Gamesir DLL ZIP into a Winlator WCP (tar.xz)."""
import argparse
import io
import json
import tarfile
import zipfile
from pathlib import Path

REQUIRED = (
    "system32/d3d12.dll",
    "system32/d3d12core.dll",
    "syswow64/d3d12.dll",
    "syswow64/d3d12core.dll",
)
DXGI = "system32/dxgi.dll"

def find_dlls(zip_path):
    found = {}
    with zipfile.ZipFile(zip_path) as src:
        for entry in src.infolist():
            if entry.is_dir():
                continue
            name = entry.filename.replace("\\", "/").lower().strip("/")
            for target in (*REQUIRED, DXGI):
                if name == target or name.endswith("/" + target):
                    if target in found:
                        raise ValueError("Duplicated DLL: " + target)
                    found[target] = src.read(entry)
    missing = set(REQUIRED) - set(found)
    if missing:
        raise ValueError("Missing DLLs: " + ", ".join(sorted(missing)))
    return found

def add_data(tar, name, content):
    info = tarfile.TarInfo(name)
    info.size = len(content)
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(content))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output_wcp", type=Path)
    parser.add_argument("--with-dxgi", action="store_true")
    args = parser.parse_args()
    files = find_dlls(args.source_zip)
    chosen = list(REQUIRED)
    if args.with_dxgi:
        if DXGI not in files:
            raise ValueError("DXGI not included in source ZIP")
        chosen.append(DXGI)
    profile = {
        "type": "VKD3D",
        "versionName": "3.1.0 Gamesir" + (" + DXGI" if args.with_dxgi else ""),
        "versionCode": 1,
        "description": "VKD3D Gamesir x64/x86" + (" with DXGI" if args.with_dxgi else ", without DXGI"),
        "files": [
            {
                "source": path,
                "target": "${" + path.split("/")[0] + "}/" + path.split("/")[1],
            } for path in chosen
        ],
    }
    args.output_wcp.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(args.output_wcp, "w:xz") as tar:
        add_data(tar, "profile.json", json.dumps(profile, indent=2).encode())
        for folder in ("system32/", "syswow64/"):
            entry = tarfile.TarInfo(folder)
            entry.type = tarfile.DIRTYPE
            entry.mode = 0o755
            tar.addfile(entry)
        for name in chosen:
            add_data(tar, name, files[name])
    with tarfile.open(args.output_wcp, "r:xz") as tar:
        parsed = json.loads(tar.extractfile("profile.json").read())
        assert parsed["files"] == profile["files"]
        for name in chosen:
            assert tar.extractfile(name).read() == files[name]
    print("Validated WCP:", args.output_wcp)

if __name__ == "__main__":
    main()
