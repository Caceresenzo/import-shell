import click
import typing

from .constants import DEFAULT_HISTORY_FILE_PATH
from .interactive import start_session


@click.command()
@click.option("--history-file", default=DEFAULT_HISTORY_FILE_PATH)
@click.argument("package_names", nargs=-1, type=str)
def cli(
    history_file: str,
    package_names: typing.List[str]
):
    start_session(
        package_names=list(package_names),
        history_file_path=history_file,
    )
