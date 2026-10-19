# Deluge Plugins Collection

This workspace contains two Deluge plugins packaged as `.egg` files:

1. **`TrackerStatus`**: Adds a dedicated **Tracker Status** column to the main torrent table.
2. **`TorrentFilter`**: Adds an instant **Name Filter Search Box** with clear button and match counter to the Deluge toolbar.

---

## 1. TorrentFilter Plugin (`TorrentFilter`)

Adds an instant search/filter input box to the Deluge interface (Web UI & GTK UI):
- **Live Filtering:** Filters the torrent table immediately as you type.
- **Multi-Word Search:** Supports multiple terms (e.g., typing `ubuntu 24` matches torrents containing both `ubuntu` and `24`).
- **Clear Button & Esc Key:** Click the `✕` button or press `Escape` to instantly reset the filter.
- **Match Counter:** Displays a badge showing `(matches / total)` torrents.
- **Live Update Compatible:** Preserves your active search query during the automatic 2-second background refresh.

### Pre-Built Eggs for TorrentFilter:
Download pre-built `.egg` files from the [GitHub Releases](https://github.com/zapturk/Deluge-Plugins/releases) page, or build locally into `dist/`:
- **Python 3.13:** `TorrentFilter-0.1-py3.13.egg` *(Recommended for Deluge on Python 3.13)*
- **Python 3.12:** `TorrentFilter-0.1-py3.12.egg`
- **Python 3.11:** `TorrentFilter-0.1-py3.11.egg`
- **Python 3.10:** `TorrentFilter-0.1-py3.10.egg`
- **Python 3.9:**  `TorrentFilter-0.1-py3.9.egg`
- **Python 3.8:**  `TorrentFilter-0.1-py3.8.egg`
- **Python 2.7:**  `TorrentFilter-0.1-py2.7.egg`

---

## 2. TrackerStatus Plugin (`TrackerStatus`)

Adds a dedicated **Tracker Status** column to the main torrent table:
- **Direct Visibility:** Displays announce messages (`Announce OK`, `Announce Sent`, `Error: ...`).
- **Sortable & Toggleable:** Sort torrents by status or right-click to show/hide.

### Pre-Built Eggs for TrackerStatus:
Download pre-built `.egg` files from the [GitHub Releases](https://github.com/zapturk/Deluge-Plugins/releases) page, or build locally into `dist/`:
- **Python 3.13:** `TrackerStatus-0.1-py3.13.egg` *(Recommended for Deluge on Python 3.13)*
- **Python 3.12:** `TrackerStatus-0.1-py3.12.egg`
- **Python 3.11:** `TrackerStatus-0.1-py3.11.egg`
- **Python 3.10:** `TrackerStatus-0.1-py3.10.egg`
- **Python 3.9:**  `TrackerStatus-0.1-py3.9.egg`
- **Python 3.8:**  `TrackerStatus-0.1-py3.8.egg`
- **Python 2.7:**  `TrackerStatus-0.1-py2.7.egg`

---

## Installation Instructions

> **Note on WebUI `[object FileList]` Bug:**  
> The Deluge WebUI "Install Plugin" button has a known ExtJS bug in modern browsers. The reliable way to install plugins is to drop the `.egg` files directly into Deluge's `plugins/` directory.

### Step 1: Copy Eggs to Deluge Plugins Directory
Copy the `.egg` file(s) into your Deluge `plugins` folder:
- **Linux / macOS:** `~/.config/deluge/plugins/`
- **Docker:** The directory mapped to `/config/plugins/`
- **Windows:** `%APPDATA%\deluge\plugins\`

For Python 3.13.5:
```bash
# Example for local / Linux / macOS
cp dist/TorrentFilter-0.1-py3.13.egg ~/.config/deluge/plugins/
cp dist/TrackerStatus-0.1-py3.13.egg ~/.config/deluge/plugins/
```

### Step 2: Restart Deluge
Restart `deluged` / `deluge-web` (or your Docker container).

### Step 3: Enable in Preferences
1. Refresh the Deluge WebUI.
2. Go to **Preferences** -> **Plugins**.
3. Check the box for **TorrentFilter** (and/or **TrackerStatus**) and click **Apply** / **OK**.
4. The search input box will appear on your top toolbar!

---

## Building from Source

To compile all `.egg` packages locally across Python 2.7 and Python 3.8 – 3.13:

```bash
# Install packaging tools
python3 -m pip install "setuptools<71" wheel

# Run the build script
python3 build_all.py
```

All 14 `.egg` files will be placed into the `dist/` directory.

---

## Release Automation (GitHub Actions)

This repository includes automated GitHub Actions workflows:

- **CI Build (`build.yml`)**: Automatically runs on every push and pull request to `main` to compile and validate all eggs.
- **Release (`release.yml`)**: Triggers when a git tag starting with `v` is pushed (e.g. `git tag v0.1 && git push origin v0.1`) or run manually via **Actions -> Release -> Run workflow**. It builds all eggs, attaches them directly to the GitHub Release, and automatically generates release notes.

