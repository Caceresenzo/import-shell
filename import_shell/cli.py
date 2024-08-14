import re
import typing

import click

from .constants import DEFAULT_HISTORY_FILE_PATH
from .interactive import start_session


def _parse(line: str):
    package_names = []

    for part in line.split(","):
        part = part.strip()
        if not part:
            continue

        match = re.match(r"^(\w+)\s+as\s+(\w+)$", part)
        if match:
            package_names.append(tuple(match.groups()))
        else:
            package_names.append(part)

    return package_names


@click.command()
@click.option("--history-file", default=DEFAULT_HISTORY_FILE_PATH)
@click.option("--no-common", is_flag=True)
@click.argument("package_names", nargs=-1, type=str)
def cli(
    history_file: str,
    no_common: bool,
    package_names: typing.List[str]
):
    if any("," in x for x in package_names):
        line = " ".join(package_names)
        package_names = _parse(line)

    start_session(
        package_names=list(package_names),
        no_common=no_common,
        history_file_path=history_file,
    )
