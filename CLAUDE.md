# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

`g9SourceSwitch` is a lightweight CLI tool that switches a monitor's active input source via **DDC/CI** (Display Data Channel / Command Interface). It runs on macOS and accepts a single argument specifying the target input.

```
python switch.py hdmi1
python switch.py DisplayPort1
python switch.py DisplayPort2
```

## Core Technical Concept

Monitor input switching uses **VCP feature code `0x60` (INPUT_SELECT)** from the MCCS standard. The values for this project are:

| Argument     | VCP value (hex) | VCP value (dec) |
|---|---|---|
| `hdmi1`        | `0x11`          | 17              |
| `DisplayPort1` | `0x0f`          | 15              |
| `DisplayPort2` | `0x10`          | 16              |

This is the same mechanism used by [display-switch](https://github.com/haimgel/display-switch) (Rust), which was confirmed working with this specific monitor.

## Implementation

**Language:** Python 3.8+
**Key library:** [`monitorcontrol`](https://github.com/newAM/monitorcontrol) — cross-platform DDC/CI over IOKit (macOS), WinAPI (Windows), I2C (Linux).

Install dependencies:
```bash
pip install monitorcontrol
```

Run:
```bash
python switch.py <input>
```

where `<input>` is one of: `hdmi1`, `DisplayPort1`, `DisplayPort2` (case-insensitive).

## Platform Notes (macOS)

- DDC/CI on macOS works over HDMI and DisplayPort cables via the IOKit `IOAVService` framework.
- The `monitorcontrol` library uses `pyobjc` internally for macOS DDC access.
- If `monitorcontrol` does not enumerate the monitor, the fallback approach is to call `ddcctl` (https://github.com/kfix/ddcctl) as a subprocess: `ddcctl -m 1 -i 17` (where `-i` is the VCP `0x60` value).

## Standards

- TERMINUS header required on `switch.py` (template: `~/.claude/TERMINUS_HEADER.md`). All `║` lines must be exactly 82 chars.
- `argparse` for CLI, `logging` for output, `try/except` with specific exceptions.
- No hardcoded credentials. No `eval()`. No `shell=True`.
