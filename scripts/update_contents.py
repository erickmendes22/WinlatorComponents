#!/usr/bin/env python3
"""Create a Winlator contents.json catalog for WCP files actually on disk."""
import json
import tarfile
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://raw.githubusercontent.com/erickmendes22/WinlatorComponents/components/"
entries = []
for file in sorted((ROOT / "packages" / "vkd3d").glob("*.wcp")):
    with tarfile.open(file, "r:xz") as tar:
        profile = json.loads(tar.extractfile("profile.json").read())
    if profile.get("type") != "VKD3D":
        raise ValueError("Unexpected WCP type: " + str(file))
    entries.append({
        "type": "VKD3D",
        "verName": profile["versionName"],
        "verCode": int(profile["versionCode"]),
        "remoteUrl": BASE_URL + quote(file.relative_to(ROOT).as_posix(), safe="/"),
    })
(ROOT / "contents.json").write_text(json.dumps(entries, indent=2) + "\n")
print("VKD3D entries:", len(entries))
