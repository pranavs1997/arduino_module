"""
REST-based node that interfaces with WEI and provides a USB camera interface
"""

from pathlib import Path
import subprocess
import serial.tools.list_ports
from fastapi.datastructures import State
from typing_extensions import Annotated
from wei.modules.rest_module import RESTModule
from wei.types.step_types import (
    ActionRequest,
    StepFileResponse,
    StepResponse,
    StepStatus,
)
from wei.utils import extract_version

rest_module = RESTModule(
    name="arduino_node",
    version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
    description="An example REST arduino  implementation",
    model="arduino",
)
rest_module.arg_parser.add_argument(
    "--arduino_address", type=str, help="the arduino address", default="/dev/ttyACM0"
)


@rest_module.action(
    name="flash", description="An action that flashes a sketch onto the arduino"
)
def flash(
    state: State,
    action: ActionRequest,
    # file_name: Annotated[str, "Name of the file to flash"] = "src.ino",
) -> StepResponse:
    """Function to flash arduino"""
    # sketch_name = file_name
    # sketch_path = Path("~/.wei/temp").expanduser() / sketch_name
    # sketch_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        command1 = ['arduino-cli', 'compile', '--fqbn', 'arduino:avr:uno', 'src.ino']
        command2 = ['arduino-cli', 'upload', '-p', '/dev/ttyACM0', '--fqbn', 'arduino:avr:uno', 'src.ino']
        subprocess.run(command1, capture_output=True, text=True, check=True)
        subprocess.run(command2, capture_output=True, text=True, check=True)

    except Exception:
        print("Arduino unavailable, returning empty image")

    return StepFileResponse(
        action_response=StepStatus.SUCCEEDED,
        path="",
        action_log="",
    )


if __name__ == "__main__":
    rest_module.start()
