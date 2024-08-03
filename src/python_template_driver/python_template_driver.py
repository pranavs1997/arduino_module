"""Driver for interfacing with the python_template device/instrument/robot."""

from pathlib import Path

from starlette.datastructures import State


def run_protocol(path: Path):
    """Run a protocol file"""
    pass


def update_state(state: State):
    """Update the state by querying the device"""
    pass
