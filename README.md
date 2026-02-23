# reaper-mcp

MCP server for controlling [REAPER](https://www.reaper.fm/) DAW from Claude Desktop or Claude Code. Built with [FastMCP 3.x](https://gofastmcp.com/) and [reapy](https://github.com/RomeoDespwortes/reapy).

## Features

82 tools across 16 domains giving full control over REAPER:

| Domain | Tools | Examples |
|--------|-------|---------|
| Project & Transport | 8 | Get project info, play/stop/record, set cursor position, save |
| Tracks | 10 | List/add/delete tracks, set volume/pan/mute/solo/arm/color |
| Track FX | 9 | Add/remove FX, get/set parameters, presets, copy FX between tracks |
| Take FX | 5 | List/add/remove take FX, get/set parameters |
| Sends & Receives | 6 | List/create/remove sends, set volume/pan/mute |
| Markers & Regions | 6 | List/add/delete markers and regions, navigate to markers |
| Tempo & Time Sig | 4 | Get tempo info, add/edit/delete tempo markers |
| Media Items | 7 | List/add/delete items, set position/length, split items |
| MIDI | 8 | Create MIDI items, add/edit/delete notes and CC events |
| Envelopes | 6 | List envelopes, add/delete points, automation items, set mode |
| Time Selection | 3 | Get/set time selection, toggle loop |
| Actions | 3 | Execute any REAPER action by ID or name (escape hatch) |
| Extended State | 3 | Read/write/delete persistent key-value storage |
| Devices | 2 | List audio and MIDI devices |
| Render | 2 | Insert media files, render project |

## Prerequisites

- **REAPER** installed and running
- **Python 3.12+**
- **reapy** installed and its ReaScript extension enabled inside REAPER

### Setting up reapy in REAPER

1. Install reapy: `pip install python-reapy`
2. Run `python -c "import reapy; reapy.configure_reaper()"` — this installs the ReaScript helper into REAPER
3. Restart REAPER
4. Verify the connection: `python -c "import reapy; print(reapy.Project().name)"`

## Installation

### Claude Desktop — One-Click (.mcpb)

Download the latest `reaper-mcp.mcpb` from [Releases](https://github.com/notpaddy2k/reaper-mcp/releases) and double-click it. Claude Desktop will install the extension automatically.

Dependencies are handled via [uv](https://docs.astral.sh/uv/) — no manual Python setup needed.

### Claude Code — Plugin Install

```bash
/plugin marketplace add notpaddy2k/reaper-mcp
/plugin install reaper-mcp
```

This registers the MCP server and any available skills automatically.

### Manual Install

```bash
git clone https://github.com/notpaddy2k/reaper-mcp.git
cd reaper-mcp
pip install -e .
```

Then add to your Claude Desktop config at `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "reaper_mcp": {
      "command": "python",
      "args": ["-m", "reaper_mcp"]
    }
  }
}
```

> If `python` doesn't resolve to Python 3.12+, use the full path instead, e.g. `C:\\Users\\you\\AppData\\Local\\Programs\\Python\\Python312\\python.exe`

### Standalone

```bash
python -m reaper_mcp
```

This starts the server on stdio, which any MCP client can connect to.

## Project Structure

```
reaper-mcp/
├── manifest.json            # .mcpb packaging manifest (Claude Desktop)
├── .claude-plugin/          # Claude Code plugin registration
│   ├── plugin.json
│   └── marketplace.json
├── .mcp.json                # Auto-registers MCP server for plugin users
├── pyproject.toml
└── reaper_mcp/
    ├── __init__.py          # Package version
    ├── __main__.py          # Entry point (python -m reaper_mcp)
    ├── server.py            # Composes all domain sub-servers via mount()
    ├── helpers.py           # Shared utilities (connection, dB conversion, validation)
    └── tools/
        ├── project.py       # Project info & transport controls
        ├── tracks.py        # Track management
        ├── track_fx.py      # Track FX chain
        ├── take_fx.py       # Take/item FX chain
        ├── sends.py         # Sends & receives routing
        ├── markers.py       # Markers & regions
        ├── tempo.py         # Tempo & time signature markers
        ├── items.py         # Media items
        ├── midi.py          # MIDI notes & CC events
        ├── envelopes.py     # Envelopes & automation
        ├── time_selection.py# Time selection & loop
        ├── actions.py       # Action execution (escape hatch)
        ├── ext_state.py     # Extended state key-value storage
        ├── devices.py       # Audio & MIDI device info
        └── render.py        # Rendering & media import
```

## Contributing

PRs welcome! Skills are markdown files, tools are Python — both are easy to contribute to.

## License

MIT
