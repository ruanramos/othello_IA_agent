# Internal
import typing as T
from argparse import ArgumentParser

# External
from othello.abc import AbstractView
from othello.views import ConsoleView

view_whitelist: T.Dict[str, T.Type[AbstractView]] = {"console": ConsoleView}


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


def main(
    view: str = "console",
    automatic: bool = False,
    player_paths: T.Optional[T.Sequence[str]] = None,
) -> None:
    view_whitelist[view](automatic=automatic, player_paths=player_paths).loop()


if __name__ == "__main__":
    try:
        main(**vars(arg_parser.parse_args()))
    except KeyboardInterrupt:
        print()
        pass
