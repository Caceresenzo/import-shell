import re
import typing

import click

from .constants import DEFAULT_HISTORY_FILE_PATH
from .inline import run_inline
from .interactive import start_session


def _parse(line: str):
    package_names = []

    for part in line.split(","):
        part = part.strip()
        if not part:
            continue

        match = re.match(r"^([\w\.]+)\s+as\s+(\w+)$", part)
        if match:
            package_names.append(tuple(match.groups()))
        else:
            package_names.append(part)

    return package_names


@click.command()
@click.option("--history-file", default=DEFAULT_HISTORY_FILE_PATH)
@click.option("--no-common", is_flag=True)
@click.option("--strict", is_flag=True, help="Enable strict mode for package names.")
@click.option("-c", "code", nargs=1, type=str, help="Code to execute.")
@click.argument("package_names", nargs=-1, type=str)
def cli(
    history_file: str,
    no_common: bool,
    strict: bool,
    code: typing.Optional[str],
    package_names: typing.List[str],
):
    line = " ".join(package_names)
    package_names = _parse(line)

    if code is not None:
        run_inline(
            code=code,
            package_names=list(package_names),
            no_common=no_common,
            strict=strict,
        )
    else:
        start_session(
            package_names=list(package_names),
            no_common=no_common,
            strict=strict,
            history_file_path=history_file,
        )
