"""Generate the SUMO road network from configs/network.json."""

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "network.json"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Generate the SUMO road network and verify its signal IDs."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=(
            "Network settings JSON. A relative path resolves from the current "
            "directory. Default: configs/network.json in the project root."
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Generate the network and verify its traffic-light IDs."""

    config_path = parse_arguments().config.resolve()

    # Load the selected network settings.
    print(f"Using config: {config_path}", flush=True)
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))

    arguments = config["netgenerate_args"]

    if not isinstance(arguments, list) or not all(
        isinstance(argument, str) for argument in arguments
    ):
        raise ValueError("netgenerate_args must be a list of strings.")

    # On Windows, pip installs the launcher beside the venv's Python.
    executable = Path(sys.executable).parent / "netgenerate.exe"

    if not executable.is_file():
        raise FileNotFoundError(
            f"Cannot find {executable}. "
            "Run this script using the project's Windows virtual environment."
        )

    # Resolve paths relative to the project, rather than the current terminal.
    output_path = PROJECT_ROOT / config["output_file"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("SUMO network generator version:", flush=True)

    subprocess.run(
        [str(executable), "--version"],
        check=True,
    )

    command = [
        str(executable),
        *arguments,
        "--output-file",
        str(output_path),
    ]

    print(f"Generating network: {output_path}", flush=True)

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
    )

    # Verify that the generated network has the expected signals.
    network = ET.parse(output_path).getroot()
    programs = network.findall("tlLogic")

    actual_ids = {program.attrib["id"] for program in programs}
    expected_ids = set(config["expected_signal_ids"])

    if actual_ids != expected_ids:
        raise RuntimeError(
            f"Expected signals {sorted(expected_ids)}, "
            f"but found {sorted(actual_ids)}."
        )

    print(f"Verified signals: {', '.join(sorted(actual_ids))}")

    for program in programs:
        phases = program.findall("phase")
        print(f"{program.attrib['id']}: {len(phases)} signal phases")

    print("Network generation complete.")


if __name__ == "__main__":
    main()