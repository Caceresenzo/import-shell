import typing

from .imports import load as load_imports


def run_inline(
    code: str,
    package_names: typing.List[typing.Union[str, typing.Tuple[str, str]]],
    no_common=False,
    strict=False,
) -> None:
    locals, _ = load_imports(package_names, no_common, strict)

    exec(code, locals)
