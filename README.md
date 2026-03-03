# g9SourceSwitch

A lightweight CLI tool to switch a monitor's active input source via DDC/CI (Display Data Channel / Command Interface). Works on Windows and macOS.

## Requirements

- Python 3.8 or higher
- `monitorcontrol` package

## Installation

1. Install the required package:
   ```bash
   pip install monitorcontrol
   ```

2. Clone or download this repository:
   ```bash
   git clone https://github.com/joseluislucio/g9SourceSwitch.git
   cd g9SourceSwitch
   ```

## Usage

Switch your monitor's input source by running:

```bash
python switch.py hdmi1
python switch.py DisplayPort1
python switch.py DisplayPort2
```

Arguments are case-insensitive. The tool will automatically switch all DDC-capable monitors connected to your system.

### Supported Inputs

| Input | VCP Code |
|-------|----------|
| `hdmi1` | 0x11 (17) |
| `DisplayPort1` | 0x0f (15) |
| `DisplayPort2` | 0x10 (16) |

## How It Works

g9SourceSwitch uses the DDC/CI protocol to communicate with your monitor over the video cable. It writes to VCP feature code `0x60` (INPUT_SELECT) as defined in the MCCS (Monitor Control Command Set) standard. The tool:

1. Enumerates all DDC-capable monitors connected to your system
2. Sends the input source selection command to each monitor
3. Exits with status 0 if at least one monitor switches successfully; status 1 otherwise

DDC/CI support is handled by the [`monitorcontrol`](https://github.com/newAM/monitorcontrol) library, which uses WinAPI on Windows and IOKit on macOS.

## Credits

The DDC/CI switching mechanism was derived from [display-switch](https://github.com/haimgel/display-switch) by haimgel.
