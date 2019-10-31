# Internal
import typing as T
from os import path
from pkgutil import ModuleInfo, walk_packages
from importlib.util import module_from_spec

# Project
from ..abc import PlayerProtocol


def available_players(player_paths: T.Optional[T.Sequence[str]] = None) -> T.Sequence[ModuleInfo]:
    import othello

    module_path = othello.__path__  # type: ignore  # mypy issue #1422

    return (
        *walk_packages(
            (path.join(p, "models", "players") for p in module_path), onerror=lambda _: None,
        ),
        *(walk_packages(player_paths, onerror=lambda _: None) if player_paths else tuple()),
    )


def import_player(player_importer: ModuleInfo) -> T.Type[PlayerProtocol]:
    importer, module_name, *_ = player_importer

    module_spec = importer.find_spec(module_name)
    module = module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    module_all = getattr(module, "__all__", None)
    symbols = tuple(symbol for symbol in dir(module) if symbol[0] != "_")

    if module_all:
        symbols = tuple(symbol for symbol in symbols if symbol in module_all)

    objects = tuple(getattr(module, symbol) for symbol in symbols)

    try:
        player_cls: T.Type[PlayerProtocol] = next(
            cls for cls in objects if issubclass(cls, PlayerProtocol)
        )
    except StopIteration:
        raise ImportError(f"Failed to import player class from module: {module_name}") from None

    return player_cls


__all__ = (
    "import_player",
    "available_players",
)
