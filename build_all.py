#!/usr/bin/env python3
"""
Build script to compile both Deluge plugin eggs:
- TrackerStatus
- TorrentFilter
"""

import os
import subprocess
import sys


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    plugins = [
        ("TrackerStatus", os.path.join(root_dir, "TrackerStatus")),
        ("TorrentFilter", os.path.join(root_dir, "TorrentFilter")),
    ]

    for name, path in plugins:
        print(f"\n{'='*20} Building {name} {'='*20}")
        script = os.path.join(path, "build_eggs.py")
        subprocess.check_call([sys.executable, script], cwd=path)

    print(f"\n{'='*20} Build Complete {'='*20}")
    dist_dir = os.path.join(root_dir, "dist")
    print(f"All eggs ready in: {dist_dir}\n")
    for f in sorted(os.listdir(dist_dir)):
        if f.endswith(".egg"):
            print(f"  - {f}")


if __name__ == "__main__":
    main()
