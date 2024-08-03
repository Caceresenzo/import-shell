import click
import typing

from .interactive import start_session

@click.command()
@click.argument("package_names", nargs=-1, type=str)
def cli(
    package_names: typing.List[str]
):
    start_session(
        package_names=list(package_names)
    )
