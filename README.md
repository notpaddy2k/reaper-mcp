# Scythe

### Make Claude your REAPER assistant.

Scythe connects Claude to [REAPER](https://www.reaper.fm/) through **89 MCP tools** across 17 domains. Control playback, manage tracks, tweak FX parameters, write MIDI, automate envelopes, run scripts, render — all from natural language.

One prompt replaces dozens of clicks.

```
"Add a track called Synth Pad, load Serum, set the cutoff to 60% and reverb mix to 40%"
```

```
"Create an 8-bar MIDI pattern — C minor chord progression, quarter notes, velocity 100"
```

```
"Automate the compressor ratio from 4:1 to 8:1 over 4 bars with a linear ramp"
```

```
"Solo the drum bus, mute everything else, and render to WAV"
```

Works with **Claude Desktop** and **Claude Code** on Windows, macOS, and Linux.

---

## What can it do?

**Anything you'd do with a mouse — but described in words.**

- Set up a session from scratch: tracks, FX chains, routing, templates
- Write MIDI: chord progressions, drum patterns, melodies, CC automation
- Mix: adjust levels, pan, EQ, compression, bus routing across any number of tracks
- Automate: create FX parameter envelopes, set automation modes, add ramps and curves
- Script: run Lua or EEL code directly inside REAPER when you need the full ReaScript API
- Manage: markers, regions, tempo changes, time selections, renders

Claude sees your project state, understands context, and chains multiple operations together. Ask for something complex and it figures out the steps.

---

## What's inside

| Domain | Tools | What you can do |
|--------|:-----:|-----------------|
| **Project & Transport** | 8 | Play, stop, pause, record, move cursor, get project info, save |
| **Tracks** | 10 | Add/delete tracks, set volume, pan, mute, solo, arm, color |
| **Track FX** | 10 | Add/remove FX, tweak parameters, browse presets, copy chains, probe display values |
| **Take FX** | 5 | Same as track FX but scoped to individual item takes |
| **Sends & Receives** | 6 | Create routing, adjust send levels, mute sends |
| **Markers & Regions** | 6 | Drop markers, create regions, jump to any marker |
| **Tempo** | 4 | Read/write tempo markers, change time signatures |
| **Media Items** | 7 | Add/delete/move/split items on the timeline |
| **MIDI** | 8 | Create MIDI items, add/edit/delete notes and CC events |
| **Envelopes** | 10 | Create FX envelopes, add points, set automation modes, bulk insert |
| **Time Selection** | 3 | Set time selection, toggle loop on/off |
| **Actions** | 3 | Run *any* REAPER action by command ID or name |
| **Scripting** | 2 | Execute Lua or EEL2 scripts with optional result return via IPC |
| **Extended State** | 3 | Persistent key-value storage across sessions |
| **Devices** | 2 | List audio and MIDI hardware |
| **Render** | 2 | Insert media files, render/bounce the project |

The **Scripting** and **Actions** tools are escape hatches — if REAPER can do it, Scythe can do it. Lua scripts have full access to the ReaScript API and can return data back to Claude through an ExtState IPC channel.

---

## Skills (Claude Code)

Skills are pre-built workflows that combine multiple tools into guided, multi-step operations. They run as slash commands in Claude Code.

Skills are where Scythe gets powerful — instead of individual tool calls, a skill can orchestrate an entire mixing session, automate FX parameters across multiple tracks, or generate complex MIDI arrangements from a single prompt.

You can write your own skills as markdown files and contribute them back to the community.

---

## Prerequisites

Scythe talks to REAPER through [reapy](https://github.com/RomeoDespwortes/reapy), a Python bridge. Three steps to set up — you only do this once.

### 1. Install Python 3.12

> **Python 3.12 is recommended.** Versions 3.13+ have known issues with reapy. Your Python architecture (32/64-bit) must match your REAPER installation — most users run 64-bit.

| Platform | Download | Notes |
|----------|----------|-------|
| **Windows** | [Python 3.12.12 (64-bit)](https://www.python.org/ftp/python/3.12.12/python-3.12.12-amd64.exe) | Check **"Add Python to PATH"** during install |
| **Windows (32-bit)** | [Python 3.12.12 (32-bit)](https://www.python.org/ftp/python/3.12.12/python-3.12.12.exe) | Only if you run 32-bit REAPER |
| **macOS** | [Python 3.12.12 (universal)](https://www.python.org/ftp/python/3.12.12/python-3.12.12-macos11.pkg) | Or `brew install python@3.12` |
| **Linux** | `sudo apt install python3.12` | Or your distro's package manager |

All downloads at [python.org/downloads](https://www.python.org/downloads/release/python-31212/).

### 2. Enable Python in REAPER

1. Open REAPER > **Options > Preferences > Plug-Ins > ReaScript**
2. Check **"Enable Python for use with ReaScript"**
3. Set the **Python DLL path** to the folder containing the shared library:

| Platform | Path | File |
|----------|------|------|
| **Windows** | `C:\Users\<you>\AppData\Local\Programs\Python\Python312\` | `python312.dll` |
| **macOS (brew)** | `/usr/local/Cellar/python@3.12/.../Frameworks/.../` | `libpython3.12.dylib` |
| **macOS (pkg)** | `/Library/Frameworks/Python.framework/Versions/3.12/lib/` | `libpython3.12.dylib` |
| **Linux** | `/usr/lib/python3.12/config-3.12-.../` | `libpython3.12.so` |

4. Click **OK** and **restart REAPER**

### 3. Connect reapy

Install reapy and configure the bridge:

```bash
pip install python-reapy
python -c "import reapy; reapy.configure_reaper()"
```

Now enable the bridge from inside REAPER:

1. Press **`?`** > **New action...** > **New ReaScript...** > name it `enable_bridge.py`
2. Paste and save (**Ctrl+S** / **Cmd+S**):
   ```python
   import reapy
   reapy.config.enable_dist_api()
   reapy.print("Bridge Enabled! Restart REAPER now.")
   ```
3. You should see **"Bridge Enabled!"** in the console — **restart REAPER**
4. After restart, press **`?`**, search for **`reapy`**, and run **"Activate reapy server"**

> **Tip:** Right-click that action and choose **"Set as startup action"** so it runs automatically every time REAPER opens.

**Verify it works** — with REAPER open, run:

```bash
python -c "import reapy; print(reapy.Project().name)"
```

You should see your project name (or an empty string for untitled projects). If not, check that REAPER is running and the reapy server is active.

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

**`DisabledDistAPIWarning` when running reapy from terminal**
REAPER's bridge isn't active. Open REAPER, press `?`, search for "reapy", and run "Activate reapy server".

**`AttributeError: module 'reapy.reascript_api' has no attribute 'ShowConsoleMsg'`**
Same root cause — reapy falls back to "dummy mode" when it can't reach REAPER. Make sure the bridge is enabled (see step 3 above).

**Python 3.13+ not working**
reapy has known issues with Python 3.13 and newer. Stick with [Python 3.12](https://www.python.org/downloads/release/python-31212/) for a reliable setup.

**REAPER doesn't show "reapy: Activate reapy server" in Actions**
Run `python -c "import reapy; reapy.configure_reaper()"` again, then manually create the bridge script inside REAPER (step 3).

**32-bit vs 64-bit mismatch**
If REAPER can't find your Python DLL, make sure you installed the same architecture. 64-bit REAPER needs 64-bit Python; 32-bit REAPER needs 32-bit Python.

**Connection works in terminal but not from Claude**
Make sure Claude is using the same Python where reapy is installed. Check your Claude Desktop config or plugin settings point to Python 3.12.

**MCP stops working after restarting REAPER**
Scythe v0.2.0+ auto-reconnects when it detects a stale connection. If you're on an older version, restart the MCP server after restarting REAPER.

---

## How it works

Scythe uses [FastMCP 3.x](https://gofastmcp.com/) with a modular architecture — 17 domain modules composed into one server via `mount()`:

```
scythe/
├── server.py            # Mounts all 17 domain sub-servers
├── helpers.py           # Connection, dB conversion, validation
└── tools/
    ├── project.py       # Project info & transport
    ├── tracks.py        # Track management
    ├── track_fx.py      # Track FX chain & parameter probing
    ├── take_fx.py       # Take FX chain
    ├── sends.py         # Routing (sends & receives)
    ├── markers.py       # Markers & regions
    ├── tempo.py         # Tempo & time signatures
    ├── items.py         # Media items
    ├── midi.py          # MIDI notes & CC
    ├── envelopes.py     # Automation envelopes & FX automation
    ├── time_selection.py# Time selection & loop
    ├── actions.py       # Action escape hatch
    ├── scripting.py     # Lua & EEL script execution
    ├── ext_state.py     # Key-value storage
    ├── devices.py       # Audio & MIDI devices
    └── render.py        # Rendering & media import
```

Built with [reapy](https://github.com/RomeoDespwortes/reapy) for REAPER communication and [FastMCP](https://gofastmcp.com/) for the MCP protocol.

---

## Roadmap

### Skills
Pre-built workflows you can trigger from Claude Code:
- `/scythe:mix` — guided mixing workflow (gain staging, EQ, compression, bus routing)
- `/scythe:session` — set up a session from scratch (create tracks, load templates, configure I/O)
- `/scythe:bounce` — export stems, master bus, or individual tracks with naming conventions
- `/scythe:midi` — generate MIDI patterns from descriptions (chord progressions, drum patterns, arpeggios)
- `/scythe:cleanup` — remove empty tracks, unused items, and organize markers

### Lightweight mode
Reduce overhead for lower-spec machines:
- Lazy tool loading — only mount domains you actually use
- Configurable tool subsets via environment variables
- Minimal memory footprint when idle

### Hooks
Automated actions triggered by events:
- Auto-save REAPER project on git commit
- Sync markers with project timeline notes
- Auto-backup before destructive operations

### Expanded tool coverage
- **Video** — timeline sync, video track management
- **SWS extensions** — access to the SWS/S&M action set
- **ReaPack** — install and manage REAPER packages from Claude
- **Custom actions** — create and chain REAPER actions programmatically

### Community
- Shared skill library — contribute and discover workflows
- Template packs — session templates for genres (EDM, orchestral, podcast, etc.)
- Integration examples — combining Scythe with other MCP servers

Have an idea? [Open an issue](https://github.com/notpaddy2k/reaper-mcp/issues) or submit a PR.

---

## Contributing

PRs welcome! Two ways to contribute:

- **Tools** — Python files in `scythe/tools/`. Add new tools or improve existing ones.
- **Skills** — Markdown files in `skills/`. Add guided workflows for common production tasks.

If you find a bug or have a feature request, [open an issue](https://github.com/notpaddy2k/reaper-mcp/issues).

---

## License

MIT
