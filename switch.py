# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗  ██╗███████╗  ║
# ║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝████╗ ██║██╔════╝ ║
# ║  ██║     ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ██║ ╚████╔╝ ██╔██╗██║█████╗    ║
# ║  ██║      ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║  ██║  ╚██╔╝  ██║╚████║██╔══╝    ║
# ║  ╚██████╗  ██║   ██████╔╝███████╗██║  ██║██████╔╝   ██║   ██║ ╚███║███████╗  ║
# ║   ╚═════╝  ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝   ╚═╝  ╚══╝╚══════╝  ║
# ║                                                   · S Y S T E M S ·          ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  Script  : switch.py                  Version : 1.0.1   Date : 2026-03-03    ║
# ║  Author  : Cyberdyne Systems           Status  : Production                  ║
# ║  Purpose : Switch monitor input source via DDC/CI VCP 0x60                   ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  CHANGELOG                                                                   ║
# ║  v1.0.1 · 2026-03-03 · Fix: use set_input_source(); fix generator to list    ║
# ║  v1.0.0 · 2026-03-03 · Initial release                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

import argparse
import logging
import sys

try:
    from monitorcontrol import get_monitors
except ImportError:
    print("ERROR: 'monitorcontrol' is not installed. Run: pip install monitorcontrol", file=sys.stderr)
    sys.exit(1)

INPUT_MAP = {
    "hdmi1":        0x11,
    "displayport1": 0x0f,
    "displayport2": 0x10,
}

VALID_INPUTS = ["hdmi1", "DisplayPort1", "DisplayPort2"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Switch monitor input source via DDC/CI (VCP 0x60)."
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        help="Input source to activate. Valid values: " + ", ".join(VALID_INPUTS),
    )
    args = parser.parse_args()

    key = args.input.lower()
    if key not in INPUT_MAP:
        parser.error(
            f"Invalid input '{args.input}'. Valid values are: {', '.join(VALID_INPUTS)}"
        )

    return args.input, INPUT_MAP[key]


def switch_monitors(input_name: str, vcp_value: int) -> int:
    logging.info("Starting input switch — target: %s (VCP 0x60 = 0x%02x)", input_name, vcp_value)

    try:
        monitors = list(get_monitors())
    except Exception as exc:
        logging.error("Failed to enumerate monitors: %s", exc)
        return 1

    if not monitors:
        logging.error("No DDC/CI monitors found.")
        return 1

    logging.info("Discovered %d monitor(s).", len(monitors))

    success_count = 0
    failure_count = 0

    for index, monitor in enumerate(monitors):
        label = f"Monitor[{index}]"
        logging.info("%s — attempting to set input to %s...", label, input_name)
        try:
            with monitor:
                monitor.set_input_source(vcp_value)
            logging.info("%s — input switched successfully.", label)
            success_count += 1
        except Exception as exc:
            logging.warning("%s — failed to switch input: %s", label, exc)
            failure_count += 1

    if success_count == 0:
        logging.error("All monitors failed to switch. success=%d failure=%d", success_count, failure_count)
        return 1

    logging.info(
        "Switch complete. success=%d failure=%d", success_count, failure_count
    )
    return 0


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    input_name, vcp_value = parse_args()
    exit_code = switch_monitors(input_name, vcp_value)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
