import code
import importlib
import os
import rlcompleter
import sys
import typing

from .constants import DEFAULT_HISTORY_FILE_PATH


def _load(
    imports: typing.Dict[str, typing.Any],
    name: str,
    alias: typing.Optional[str] = None,
    only_aliases=False,
):
    key = alias or name.split(".", 2)[0]
    suffix = f"as {alias}" if alias is not None else ""

    try:
        globals_ = {}
        exec(f"\nimport {name} {suffix}\n", globals_)
        module = globals_[key]
    except (ModuleNotFoundError, NameError) as error:
        print(f"cannot load {name}: {error}", file=sys.stderr)
        module = None

    if not only_aliases:
        imports[key] = module

    if alias is not None:
        imports[alias] = module

    return module


def load_common_imports():
    imports = {
        "sys": sys,
        "os": os,
    }

    _load(imports, "json")
    _load(imports, "pandas", "pd")
    _load(imports, "numpy", "np")

    return imports


def load_imports(
    package_names: typing.List[typing.Union[str, typing.Tuple[str, str]]],
):
    imports = {}

    banner = "available imports:\n"
    for package_name in package_names:
        if isinstance(package_name, tuple):
            package_name, alias = package_name
            module = _load(imports, package_name, alias, only_aliases=True)

            display_name = f"{package_name} (as {alias})"
        else:
            module = _load(imports, package_name)

            display_name = package_name

        location = getattr(module, '__path__', module.__name__) if module is not None else None
        banner += f"{display_name}: {location}\n"

    return imports, banner


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
    history_file_path=DEFAULT_HISTORY_FILE_PATH
):
    common = {} if no_common else load_common_imports()
    user, banner = load_imports(package_names)

    locals = {
        **common,
        **user,
    }

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
