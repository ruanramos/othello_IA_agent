# Internal
import typing as T

# External
from othello.views import ConsoleView
from othello.protocol import ViewProtocol

view_whitelist: T.Dict[str, T.Type[ViewProtocol]] = {"console": ConsoleView}


def main(
    view: str = "console",
    automatic: bool = False,
    player_paths: T.Optional[T.Sequence[str]] = None,
) -> None:
    view_whitelist[view](automatic=automatic, player_paths=player_paths).loop()


if __name__ == "__main__":
    main()
