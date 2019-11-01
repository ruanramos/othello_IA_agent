# Internal
import sys
import typing as T
from os import environ
from argparse import ArgumentParser

# External
import typing_extensions as Te

# External
from othello.views import ConsoleView
from othello.abstract import AbstractView
from othello.misc.error_dialog import gui_error

view_list: T.Dict[str, T.Sequence[T.Type[AbstractView]]] = {
    "gui": tuple(),
    "console": (ConsoleView,),
}

arg_parser = ArgumentParser(description="Jogue Othello")
arg_parser.add_argument(
    "player_paths",
    type=str,
    help="Lista de caminhos para pastas com definições de jogadores em python",
    nargs="*",
    metavar="PATHS",
)
arg_parser.add_argument(
    "--automatic",
    dest="automatic",
    help="Passa para próxima jogada automaticamente",
    action="store_true",
)


def main(view_type: str) -> None:
    namespace = arg_parser.parse_args()

    try:
        view = next(view for view in view_list[view_type] if view.available())
    except StopIteration:
        raise RuntimeError("Unavailable view")

    try:
        view(**vars(namespace)).loop()
    except KeyboardInterrupt:
        print()
        pass


def error_msg(exc: BaseException) -> str:
    return f"Falha irrecuperável\nRazão: {exc}"


def main_gui() -> Te.NoReturn:
    try:
        main("gui")
    except BaseException as exc:
        gui_error(error_msg(exc))
        sys.exit(error_msg(exc))
    sys.exit(0)


def main_console() -> Te.NoReturn:
    try:
        main("console")
    except BaseException as exc:
        sys.exit(error_msg(exc))

    sys.exit(0)


if __name__ == "__main__":
    view_type = environ.get("OTHELLO_VIEW_TYPE", "console")

    try:
        main(view_type)
    except BaseException as exc:
        if view_type == "gui":
            gui_error(error_msg(exc))
        sys.exit(error_msg(exc))

    sys.exit(0)
