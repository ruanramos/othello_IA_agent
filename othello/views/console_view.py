# Internal
import typing as T

# External
from othello.enums import Color

# Project
from ..adapters import BoardAdapter
from ..protocol import ViewProtocol, ColoredPlayerProtocol
from ..misc.runtime_importer import import_player, available_players


class ConsoleView(ViewProtocol):
    def __init__(
        self, player_paths: T.Optional[T.Sequence[str]] = None, automatic: bool = False
    ) -> None:
        self.automatic = automatic
        self.player_paths = player_paths or tuple()

    @staticmethod
    def print_view_data(adapter: BoardAdapter) -> None:
        print("┌─────────────────────┐")
        print("│     a b c d e f g h │")
        print("├───┬─────────────────┤")

        for i, column in enumerate(adapter.view_data):
            print(f"│ {i} │ " + " ".join(v.value for v in column) + " │")

        print("└───┴─────────────────┘")

    def loop(self) -> None:
        print(
            """\
   _|_|      _|      _|                  _|  _|
 _|    _|  _|_|_|_|  _|_|_|      _|_|    _|  _|    _|_|
 _|    _|    _|      _|    _|  _|_|_|_|  _|  _|  _|    _|
 _|    _|    _|      _|    _|  _|        _|  _|  _|    _|
   _|_|        _|_|  _|    _|    _|_|_|  _|  _|    _|_|"""
        )

        colors = {Color.BLACK: "preto", Color.WHITE: "branco"}
        players: T.List[ColoredPlayerProtocol] = []
        all_players = available_players()
        for i, (color, name) in enumerate(colors.items()):
            print(f"Selecione um dos players abaixo para ser o jogador {name}")

            for idx, player_info in enumerate(all_players):
                print(f"{idx} - {player_info.name}")

            player_cls: T.Type[ColoredPlayerProtocol] = import_player(  # type: ignore
                all_players[int(input("Digite o numero do player que voce deseja: "))]
            )

            player = player_cls(color)
            assert hasattr(player, "color")

            players.append(player)

        adapter = BoardAdapter(*players)
        self.print_view_data(adapter)
        while not adapter.finished:
            if not self.automatic:
                input()

            color = adapter.current_color
            if not adapter.update(self):
                print(f"Sem movimentos para o jogador {colors[color]}")
                continue

            print(f"Jogador: {colors[color]}")
            print(
                (
                    "Score: "
                    + " ".join(
                        f"{colors[color]} = {score}" for color, score in adapter.score.items()
                    )
                )
            )
            self.print_view_data(adapter)

        scores = adapter.score
        if scores[Color.WHITE] == scores[Color.BLACK]:
            print("Empate")
        else:
            print(
                f"Jogador {colors[Color.BLACK] if scores[Color.BLACK] > scores[Color.WHITE] else colors[Color.WHITE]} Ganhou"
            )

    def alert(self, msg: str) -> None:
        print(msg)

    def input(self, msg: str) -> str:
        return input(f"{msg}: ")


__all__ = ("ConsoleView",)
