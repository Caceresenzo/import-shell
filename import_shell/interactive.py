import code
import os
import rlcompleter
import typing

from .constants import DEFAULT_HISTORY_FILE_PATH
from .imports import load as load_imports


def _get_readline():
    if os.name == 'nt':
        import pyreadline3
        return pyreadline3.Readline()
    else:
        import readline
        return readline


def start_session(
    package_names: typing.List[typing.Union[str, typing.Tuple[str, str]]],
    no_common=False,
    strict=False,
    history_file_path=DEFAULT_HISTORY_FILE_PATH
):
    locals, banner = load_imports(package_names, no_common, strict)

    readline = _get_readline()
    readline.set_completer(rlcompleter.Completer(locals).complete)
    readline.parse_and_bind("tab: complete")

    history_file_path = os.path.expanduser(history_file_path)
    if os.path.exists(history_file_path):
        readline.read_history_file(history_file_path)

    console = code.InteractiveConsole(locals)
    console.interact(
        banner=banner,
        exitmsg=""
    )

    readline.write_history_file(history_file_path)
