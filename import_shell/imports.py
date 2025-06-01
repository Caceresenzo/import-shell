import os
import sys
import typing


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


def load_commons():
    imports = {
        "sys": sys,
        "os": os,
    }

    _load(imports, "json")
    _load(imports, "pandas", "pd")
    _load(imports, "numpy", "np")

    return imports


def load_users(
    package_names: typing.List[typing.Union[str, typing.Tuple[str, str]]],
    strict=False,
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
    
    if strict and None in imports.values():
        print("some packages failed to load, exiting...", file=sys.stderr)
        exit(1)

    return imports, banner


def load(
    package_names: typing.List[typing.Union[str, typing.Tuple[str, str]]],
    no_common=False,
    strict=False,
) -> typing.Dict[str, typing.Any]:
    common = {} if no_common else load_commons()
    user, banner = load_users(package_names, strict)

    locals = {
        **common,
        **user,
    }

    return locals, banner
