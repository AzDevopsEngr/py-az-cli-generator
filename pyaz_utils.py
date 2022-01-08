"""Utility functions for the pyaz generated code to use."""

import json
import logging
import shutil
import subprocess
from typing import Dict


def _call_az(command: str, parameters: Dict) -> object:
    """
    Call an az command (supplied as a string, and parameters as dictionary).

    Calls az cli via a subprocess
    Returns the az cli json converted to python object

    Example:
    `
    _call_az("az group create", locals())
    `
    """
    # format the parameters into a list
    params = _get_params(parameters)

    # split commands into a list
    commands = command.split()

    # add the params to the commands
    commands.extend(params)

    full_command = " ".join(commands)
    logging.info("Executing command: %s", full_command)

    # strip off az and replace it with full path to az to accomodate Windows
    commands.pop(0)
    commands.insert(0, shutil.which("az"))

    output = subprocess.run(
        commands,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    stdout = output.stdout.decode("utf-8")
    stderr = output.stderr.decode("utf-8")
    if stdout:
        try:
            return json.loads(stdout)
        except: # pylint: disable=bare-except
            return stdout
    elif stderr:
        raise Exception(stderr)


def _get_cli_param_name(name: str) -> str:
    """
    Convert parameter name back to cli format from pythonic version.

    - Strips trailing underscore from keywords
    - Converts remaining underscores to dashes
    - Adds leading dashes
    """
    if name[-1] == "_":
        name = name[0:-1]
    name = name.replace("_", "-")
    name = f"--{name}"
    return name


def _get_params(params: Dict) -> str:
    """
    Given the built-in locals dictionary returns a formatted string of parameters.

    The parameter string contains the az cli formatted parameter names and values
    in a comma-separated list.
    """
    # return params
    output = []

    # loop through locals and append list of parameters and their values
    # as long as the parameter has a value
    for param in params:
        if params[param]:

            # if value is a boolean then don't append value, just param, used for flags
            if isinstance(params[param], bool):
                output.append(_get_cli_param_name(param))
            else:
                output.append(_get_cli_param_name(param))
                output.append(params[param])

    return output
