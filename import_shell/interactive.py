import code
import importlib
import os
import rlcompleter
import sys
import typing


from .constants import DEFAULT_HISTORY_FILE_PATH


def _load(imports: typing.Dict[str, typing.Any], name: str, aliases=[]):
    try:
        module = importlib.import_module(name)
    except (ModuleNotFoundError, NameError) as error:
        print(f"cannot load {name}: {error}", file=sys.stderr)
        module = None

    imports[name] = module
    for alias in aliases:
        imports[alias] = module


def load_common_imports():
    imports = {
        "sys": sys,
        "os": os,
    }

    _load(imports, "json")
    _load(imports, "pandas", ["pd"])
    _load(imports, "numpy", ["np"])

    return imports


def load_imports(
    package_names: typing.List[str],
):
    imports = {}

    for package_name in package_names:
        _load(imports, package_name)

    return imports


def _get_readline():
    if os.name == 'nt':
        import pyreadline3
        return pyreadline3.Readline()
    else:
        import readline
        return readline


def start_session(
    package_names: typing.List[str],
    history_file_path=DEFAULT_HISTORY_FILE_PATH
):
    common = load_common_imports()
    user = load_imports(package_names)

    locals = {
        **common,
        **user,
    }

    banner = "available imports:\n"
    for name, module in user.items():
        location = getattr(module, '__path__', module.__name__) if module is not None else None
        banner += f"{name}: {location}\n"

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
