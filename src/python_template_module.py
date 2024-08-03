"""
REST-based node that interfaces with WEI and provides an Arduino interface
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi.datastructures import UploadFile
from starlette.datastructures import State
from typing_extensions import Annotated
from wei.modules.rest_module import RESTModule
from wei.types.module_types import ModuleState
from wei.types.step_types import (
    ActionRequest,
    StepFileResponse,
    StepResponse,
    StepStatus,
)
from wei.utils import extract_version

import python_template_driver as driver

rest_module = RESTModule(
    name="python_template_module",
    version=extract_version(Path(__file__).parent.parent / "pyproject.toml"),
    description="TODO: Provide a description of your module here.",
    model="TODO: specify the device model this module controls",
)

#############
# Lifecycle #
#############


@rest_module.startup_handler()
def custom_startup_handler(state: State):
    """
    Custom startup handler that is called whenever the module is started.

    If this isn't provided, the default startup handler will be used, which will do nothing.
    """

    # driver.initialize()  # *Initialize the device, if needed


@rest_module.shutdown()
def custom_shutdown_handler(state: State):
    """
    Custom shutdown handler that is called whenever the module is shutdown.

    If this isn't provided, the default shutdown handler will be used, which will do nothing.
    """

    # driver.shutdown()  # *Shutdown the device or close connection, if needed


@rest_module.state_handler()
def custom_state_handler(state: State) -> ModuleState:
    """
    Custom state handler that is called whenever the modules state is requested via the REST API.

    If this isn't provided, the default state handler will be used, which will return the following:

    ModuleState(status=state.status, error=state.error)
    """

    # driver.update_state(state)  # *Query the state of the device, if supported

    return ModuleState(
        status=state.status,  # *Required
        error=state.error,
        # *Custom state fields
        sum=state.sum,
        difference=state.difference,
    )


###########
# Actions #
###########

# TODO: Define functions to handle each action the device should be able to perform


@rest_module.action(
    name="add", description="An example action that adds two numbers together."
)
def add(
    a: Annotated[float, "First number to add"],
    b: Annotated[float, "Second number to add"],
    state: State,  # *This is an optional argument that can be used to access the current state of the module
) -> StepResponse:
    """
    Add two numbers together

    Example workflow step yaml:

    - name: Add on python_template
      module: python_template
      action: add
      args:
        a: 5
        b: 7
    """

    state.sum = a + b

    return StepResponse.succeeded(state.sum)


# * If you don't specify a name or description, the function name and docstring will be used
@rest_module.action()
def subtract(
    a: Annotated[float, "First number to subtract from"],
    b: Annotated[float, "Second number to subtract"],
    action: ActionRequest,  # *This is an optional argument that can be used to access the entire action request
    state: State,  # *This is an optional argument that can be used to access the current state of the module
) -> StepResponse:
    """
    Subtract two numbers

    Example workflow step yaml:

    - name: Subtract on python_template
      module: python_template
      action: subtract
      args:
        a: 12
        b: 10
    """

    # state.difference = a - b
    state.difference = (
        action.args["a"] - action.args["b"]
    )  # *This is equivalent to the above

    return StepResponse.succeeded(state.difference)


@rest_module.action(name="run_protocol", description="Run a protocol file")
def run_protocol(
    protocol: Annotated[UploadFile, "Protocol file to run"],
) -> StepFileResponse:
    """
    Run a protocol file

    Example workflow step yaml:

    - name: Run protocol on python_template
      module: python_template
      action: run_protocol
      files:
        protocol: path/to/protocol/file
    """
    # *Save the protocol file to a temporary location
    with NamedTemporaryFile() as f:
        f.write(protocol.file.read())
        f.seek(0)

        # *Run protocol file
        driver.run_protocol(Path(f.name))

    output_file = Path("path/to/output/file")

    return StepFileResponse(
        status=StepStatus.SUCCEEDED,
        path=output_file,
    )


if __name__ == "__main__":
    rest_module.start()
