#!/usr/bin/env python3
"""
Build script for TorrentFilter Deluge plugin.
Packages .egg files for multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 2.7)
so it can be installed on any Deluge instance.
"""

import os
import subprocess
import sys
import zipfile
import shutil

TARGET_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "2.7"]
PLUGIN_NAME = "TorrentFilter"


def get_version(base_dir):
    setup_file = os.path.join(base_dir, "setup.py")
    if os.path.exists(setup_file):
        with open(setup_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("__version__"):
                    return line.split("=")[1].strip().strip("'\"")
    return "0.1"


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    version = get_version(base_dir)

    print("=== Building base egg using current Python interpreter ===")
    dist_dir = os.path.join(base_dir, "dist")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    build_dir = os.path.join(base_dir, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    egg_info_dir = os.path.join(base_dir, f"{PLUGIN_NAME}.egg-info")
    if os.path.exists(egg_info_dir):
        shutil.rmtree(egg_info_dir)

    subprocess.check_call([sys.executable, "setup.py", "bdist_egg"])

    # Find the newly built egg
    eggs = [f for f in os.listdir(dist_dir) if f.endswith(".egg")]
    if not eggs:
        print("Error: No egg found in dist/")
        sys.exit(1)

    base_egg_path = os.path.join(dist_dir, eggs[0])
    print(f"Base egg built: {base_egg_path}")

    # Read base egg entries, stripping out precompiled pyc files so the code
    # is cleanly re-compiled by whatever Python version runs Deluge.
    clean_entries = {}
    with zipfile.ZipFile(base_egg_path, "r") as z_in:
        for info in z_in.infolist():
            if "__pycache__" not in info.filename and not info.filename.endswith(".pyc"):
                clean_entries[info] = z_in.read(info.filename)

    # Generate eggs for all target versions
    output_eggs = []
    for ver in TARGET_VERSIONS:
        egg_filename = f"{PLUGIN_NAME}-{version}-py{ver}.egg"
        egg_path = os.path.join(dist_dir, egg_filename)
        with zipfile.ZipFile(egg_path, "w", compression=zipfile.ZIP_DEFLATED) as z_out:
            for info, data in clean_entries.items():
                z_out.writestr(info, data)
        print(f"Created egg for Python {ver}: {egg_filename}")
        output_eggs.append(egg_path)

    # Also copy to workspace root dist/
    workspace_root = os.path.dirname(base_dir)
    workspace_dist = os.path.join(workspace_root, "dist")
    os.makedirs(workspace_dist, exist_ok=True)
    for egg_path in output_eggs:
        shutil.copy2(egg_path, workspace_dist)

    print(f"\nAll eggs successfully created in:\n  - {dist_dir}\n  - {workspace_dist}")


if __name__ == "__main__":
    main()
