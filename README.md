# Scythe

> Give Claude full control of your REAPER DAW.

Scythe is an MCP server with 82 tools across 16 domains — play, record, mix, edit MIDI, automate, render, and more. Works with Claude Desktop and Claude Code on Windows, macOS, and Linux.

---

## What can you do with it?

Ask Claude things like:

- *"Add a new track called Bass and set it to -6 dB"*
- *"List all the FX on track 1 and show me their parameter values"*
- *"Create a 4-bar MIDI pattern with a C minor chord progression"*
- *"Add a marker at 30 seconds called Chorus"*
- *"Set track 3 automation to write mode and add volume envelope points"*
- *"Mute tracks 4 through 6 and solo track 1"*
- *"Render the project with the current settings"*

### All 82 tools

| Domain | Tools | What you can do |
|--------|:-----:|-----------------|
| **Project & Transport** | 8 | Get project info, play/stop/pause/record, move cursor, save |
| **Tracks** | 10 | List/add/delete tracks, volume, pan, mute, solo, arm, color |
| **Track FX** | 9 | Add/remove FX, tweak parameters, browse presets, copy FX chains |
| **Take FX** | 5 | Same as track FX but for individual item takes |
| **Sends & Receives** | 6 | Create routing, adjust send levels, mute sends |
| **Markers & Regions** | 6 | Drop markers, create regions, navigate by marker |
| **Tempo** | 4 | Read/write tempo markers, change time signatures |
| **Media Items** | 7 | Add/delete/move/split items on the timeline |
| **MIDI** | 8 | Create MIDI items, add/edit/delete notes and CC events |
| **Envelopes** | 6 | Add automation points, set modes (read/write/touch/latch) |
| **Time Selection** | 3 | Set time selection, toggle loop on/off |
| **Actions** | 3 | Run *any* REAPER action by ID or name (escape hatch) |
| **Extended State** | 3 | Persistent key-value storage between sessions |
| **Devices** | 2 | List audio and MIDI hardware |
| **Render** | 2 | Insert media files, render/bounce the project |

The **Actions** tools are an escape hatch — they can run *any* REAPER command by its ID, even ones not covered by the other 79 tools.

---

## Setup Guide

Scythe talks to REAPER through [reapy](https://github.com/RomeoDespwortes/reapy), a Python bridge. You need to set this up once before installing Scythe.

### Step 1 — Install Python 3.12

> **Use Python 3.12 specifically.** Some users have had issues with 3.13. If you already have 3.12 installed, skip this step.

**Windows:** Download from [python.org/downloads](https://www.python.org/downloads/release/python-3120/) and install. Make sure to check "Add Python to PATH".

**macOS:** `brew install python@3.12`

**Linux:** `sudo apt install python3.12` (or your distro's equivalent)

### Step 2 — Configure Python in REAPER

1. Open REAPER
2. Go to **Options → Preferences → Plug-Ins → ReaScript**
3. Check **"Enable Python for use with ReaScript"**
4. Set the **Python DLL path** to where Python 3.12 is installed:
   - Windows: `C:\Users\<you>\AppData\Local\Programs\Python\Python312\` with DLL `python312.dll`
   - macOS: `/usr/local/Cellar/python@3.12/.../Frameworks/.../libpython3.12.dylib`
   - Linux: `/usr/lib/python3.12/config-3.12-.../libpython3.12.so`
5. Click **OK** and restart REAPER

### Step 3 — Install reapy and enable the bridge

```bash
pip install python-reapy
python -c "import reapy; reapy.configure_reaper()"
```

> You may see a `DisabledDistAPIWarning` — that's expected. It means the bridge isn't active in REAPER yet.

Now enable it from inside REAPER:

1. Open REAPER
2. Press **`?`** to open the **Actions** list
3. Click **New action...** (bottom right) → **New ReaScript...**
4. Name it `enable_bridge.py` and click Save
5. Paste this code in the editor:
   ```python
   import reapy
   reapy.config.enable_dist_api()
   reapy.print("Bridge Enabled! Restart REAPER now.")
   ```
6. Press **Ctrl+S** to save and run it
7. Check the REAPER console — you should see **"Bridge Enabled!"**
8. **Close REAPER completely and reopen it**

### Step 4 — Set reapy to start automatically

After restarting REAPER:

1. Press **`?`** to open the **Actions** list
2. Search for **`reapy`**
3. You should see **"reapy: Activate reapy server"**
4. Run it — this starts the bridge so Claude can connect

> **Tip:** To avoid running this manually every time, right-click the action and choose **"Set as startup action"** so it runs automatically when REAPER opens.

### Step 5 — Verify it works

With REAPER open and the reapy server active, run this in your terminal:

```bash
python -c "import reapy; print(reapy.Project().name)"
```

You should see your project name (or an empty string for an untitled project). If you see an error, make sure:
- REAPER is running
- The "Activate reapy server" action has been run
- Python 3.12 is the version being used

---

## Install Scythe

Pick whichever method matches your setup:

### Claude Desktop (one-click)

Download `scythe.mcpb` from [Releases](https://github.com/notpaddy2k/reaper-mcp/releases) and double-click it. Done.

Python dependencies are handled automatically via [uv](https://docs.astral.sh/uv/).

### Claude Code (plugin)

```
/plugin marketplace add notpaddy2k/reaper-mcp
/plugin install scythe
```

The MCP server and any available skills register automatically.

### Manual

```bash
git clone https://github.com/notpaddy2k/reaper-mcp.git
cd reaper-mcp
pip install -e .
```

Add to your Claude Desktop config at `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "scythe": {
      "command": "python",
      "args": ["-m", "scythe"]
    }
  }
}
```

---

## Troubleshooting

### `DisabledDistAPIWarning` when running reapy from terminal
REAPER's bridge isn't active. Open REAPER, press `?`, search for "reapy", and run "Activate reapy server".

### `AttributeError: module 'reapy.reascript_api' has no attribute 'ShowConsoleMsg'`
Same issue — reapy falls back to "dummy mode" when it can't reach REAPER. Enable the bridge (see Step 3 above).

### Python 3.13 issues
Some users have reported problems with Python 3.13 and reapy. Use Python 3.12 for a known-good setup.

### REAPER doesn't show "reapy: Activate reapy server" in Actions
Run `python -c "import reapy; reapy.configure_reaper()"` again, then follow Step 3 to manually create the bridge script inside REAPER.

### Connection works in terminal but not from Claude
Make sure Claude is using the same Python version where reapy is installed. Check your Claude Desktop config or plugin settings point to Python 3.12.

---

## How it works

Scythe uses [FastMCP 3.x](https://gofastmcp.com/) with a modular architecture — 16 domain modules composed into one server via `mount()`:

```
scythe/
├── server.py            # Mounts all 16 domain sub-servers
├── helpers.py           # Connection, dB conversion, validation
└── tools/
    ├── project.py       # Project info & transport
    ├── tracks.py        # Track management
    ├── track_fx.py      # Track FX chain
    ├── take_fx.py       # Take FX chain
    ├── sends.py         # Routing (sends & receives)
    ├── markers.py       # Markers & regions
    ├── tempo.py         # Tempo & time signatures
    ├── items.py         # Media items
    ├── midi.py          # MIDI notes & CC
    ├── envelopes.py     # Automation envelopes
    ├── time_selection.py# Time selection & loop
    ├── actions.py       # Action escape hatch
    ├── ext_state.py     # Key-value storage
    ├── devices.py       # Audio & MIDI devices
    └── render.py        # Rendering & media import
```

Built with [reapy](https://github.com/RomeoDespwortes/reapy) for REAPER communication and [FastMCP](https://gofastmcp.com/) for the MCP protocol.

---

## Contributing

PRs welcome! Two ways to contribute:

- **Tools** — Python files in `scythe/tools/`. Add new tools or improve existing ones.
- **Skills** — Markdown files in `skills/`. Add guided workflows for common production tasks.

If you find a bug or have a feature request, [open an issue](https://github.com/notpaddy2k/reaper-mcp/issues).

---

## License

MIT
