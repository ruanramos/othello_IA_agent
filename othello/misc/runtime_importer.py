# Internal
import typing as T
from pkgutil import ModuleInfo, iter_modules
from importlib.util import module_from_spec

# Project
from ..protocol import PlayerProtocol

PLAYER_MODULE = "models/players"


def available_players(path: T.Optional[T.Sequence[str]] = None) -> T.Sequence[ModuleInfo]:
    return tuple(iter_modules(path=path or (PLAYER_MODULE,)))


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
