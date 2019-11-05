# Internal
import random
import math
import typing as T
# Project
if T.TYPE_CHECKING:
    from ...enums import Color
    from ...models import Board, Position

BASE_DEPTH = 3

def minimax(
        max_depth: int,
        board: "Board", depth: int, color: "Color", maximizing: bool,
        alpha: float, beta: float,
        turn: int,
        heuristic: T.Callable[["Board", "Color", int], float]) -> (float, "Position"):

    pos_to_play = (-1, -1)

    if depth >= max_depth:
        res = heuristic(board, color, turn)
        return res, pos_to_play

    if maximizing:
        max_evaluation = -math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(max_depth, child_board, depth + 1, color.opposite(),
                                 not maximizing, alpha, beta, turn + 1, heuristic)

            if max_evaluation < evaluation:
                max_evaluation = evaluation
                pos_to_play = pos
            alpha = max(alpha, evaluation)
            if (beta <= alpha):
                break
        return max_evaluation, pos_to_play

    else:
        min_evaluation = math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(max_depth, child_board, depth + 1, color.opposite(), 
            not maximizing, alpha, beta, turn + 1, heuristic)

            if min_evaluation > evaluation:
                min_evaluation = evaluation
                pos_to_play = pos
            beta = min(beta, evaluation)
            if (beta <= alpha):
                break
        return min_evaluation, pos_to_play


def children_boards(board: "Board", color: "Color") -> T.Sequence[T.Tuple["Board", "Position"]]:
    res = []
    valid_moves = list(board.valid_moves(color))
    for move in valid_moves:
        b = board.get_clone()
        b.play(move, color)
        res.append((b, move))

    return res


def get_a_child_board(board: "Board", color: "Color", valid_moves):
    b = board.get_clone()
    b.play(valid_moves.pop(0), color)
    return b


class MiniMaxAB:
    POSITION_VALUES = {}
    POSITION_VALUES_INITIALIZED = False

    def give_values_to_positions(self, b: "Board") -> T.Dict[T.Tuple[int, int], int]:
        values = {}
        for x, y in b.positions():
            if (3 <= x <= 6) and (3 <= y <= 6):
                values[(x, y)] = -1
            elif ((3 <= x <= 6) and (y == 2 or y == 7)) or ((3 <= y <= 6) and (x == 2 or x == 7)):
                values[(x, y)] = -2
            elif ((x == 3 or x == 6) and (y == 1 or y == 8)) or ((y == 3 or y == 6) and (x == 1 or x == 8)):
                values[(x, y)] = 10
            elif ((x == 4 or x == 5) and (y == 1 or y == 8)) or ((y == 4 or y == 5) and (x == 1 or x == 8)):
                values[(x, y)] = 5
            elif ((x == 2 or x == 7) and (y == 1 or y == 8)) or ((y == 2 or y == 7) and (x == 1 or x == 8)):
                values[(x, y)] = -20
            elif ((x == 2 or x == 7) and (y == 2 or y == 7)) or ((y == 2 or y == 7) and (x == 2 or x == 7)):
                values[(x, y)] = -50
            elif ((x == 1 or x == 8) and (y == 1 or y == 8)) or ((y == 1 or y == 8) and (x == 1 or x == 8)):
                values[(x, y)] = 100
            # values[(x, y)] = x
            # print('{} : {}'.format((x, y), values[(x, y)]))
            # input()
        return values

    def coin_parity(self, board: "Board", color: "Color", turn: int) -> float:
        actual_score = board.score()
        return 100 * (max(actual_score) - min(actual_score)) / (max(actual_score) - min(actual_score))

    def stupid(self, board: "Board", color: "Color", turn: int) -> float:
        if self.color == '@':
            s = board.score()
            return s[1]
            # return board.score()[1]
        s = board.score()
        return s[0]

    def simple_mobility(self, board: "Board", color: "Color", turn: int) -> float:
        return len(board.valid_moves(color)) - len(board.valid_moves(color.opposite()))

    def frontier_control(self, board: "Board", color: "Color", turn: int) -> float:
        def frontier(board: "Board") -> T.List[T.Tuple]:
            def adjacent(px: int, py: int) -> T.List[T.Tuple]:
                adj = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        x = px + i
                        y = py + j
                        if x > 0 and x < 9 and y > 0 and y < 9:
                            adj.append((x, y))
                # print("adj = ", adj)
                # input()
                return adj
            
            r = []
            for x, y in board.positions():
                if board.get_square_color(x, y) == ".":
                    continue
                print((x, y))
                # if (x == 1 or y == 1 or x == 8 or y == 8):
                #     continue
                for ax, ay in adjacent(x, y):
                    print((ax, ay))
                    if board.get_square_color(ax, ay) == ".":
                        r.append((ax, ay))
                        break
            # print("r = ", r)
            # input()    
            return r

        score = 0
        for px, py in frontier(board):
            # print((px, py))
            pcolor = board.get_square_color(px, py)
            if pcolor == color:
                score -= 1
            elif pcolor == color.opposite:
                score += 1

        return score

    def positional_heuristic(self, board: "Board", color: "Color", turn: int) -> float:
        multiplier = 0
        sum = 0

        for x, y in board.positions():
            pcolor = board.get_square_color(x, y)
            if pcolor == color:
                multiplier = 1
            elif pcolor == color.opposite():
                multiplier = -1
            elif pcolor == color.EMPTY:
                multiplier = 0
            sum += multiplier * self.POSITION_VALUES[(x,y)]
        return sum

    def can_take_corner(self, board: "Board", color: "Color") -> T.Tuple[bool, T.Tuple[int, int]]:
        corners = {(1,1), (1, 8),(8, 1),(8, 8)}
        moves = board.valid_moves(color)
        for c in corners:
            if c in moves:
                # print("da pra pegar esse canto", c)
                # input()
                return (True, c)
        return (False, None)        

    def uber_heuristic(self, board: "Board", color: "Color", turn: int) -> float:
        #End
        if (turn > 55):
            return self.coin_parity(board, color, turn)
        #Beginning
        elif (turn < 20):
            return self.positional_heuristic(board, color, turn)
        #Middle
        else:
            return self.positional_heuristic(board, color, turn)



    def __init__(self, color: "Color") -> None:
        self.color = color
    
    turn = 0
    def play(self, board: "Board") -> "Position":
        if (not self.POSITION_VALUES_INITIALIZED):
            self.POSITION_VALUES = self.give_values_to_positions(board)
            self.POSITION_VALUES_INITIALIZED = True
        
        take_corner = self.can_take_corner(board, self.color)
        if(take_corner[0]):
            return take_corner[1]
        depth = BASE_DEPTH
        if(self.turn < 3):
            depth = 4
        elif (self.turn > 55):
            depth = 62 - self.turn
        elif (self.turn > 50):
            depth = 62 - self.turn - 6
        elif (self.turn > 45):
            depth += math.floor((self.turn-40) / 5)

        print("Turn: ",self.turn, "Depth: ", depth)
        res = minimax(depth, board, 0, self.color, True, -math.inf, math.inf, self.turn, self.uber_heuristic)
        self.turn += 2
        return res[1]


__all__ = ("MiniMaxAB",)
