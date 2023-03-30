from typing import Optional, Tuple, Callable, NamedTuple, List, Generator

GridGenerator = Callable[[int], str]
GameComplete = Optional[Tuple[int, str]]
GameCompleteCheck = Callable[[str], GameComplete]
Tic = Callable[[
    GridGenerator,
    GameCompleteCheck,
    GameCompleteCheck,
    Callable[[str], str]
], str]
Move = Callable[[str, str, int, int], str]


class TicTurn(NamedTuple):
    current_state: str
    icon:          str
    x:             int
    y:             int


class CompletedGame(NamedTuple):
    rows:    GameComplete
    columns: GameComplete


class MoveResult(NamedTuple):
    state:     str
    completed: Optional[CompletedGame]


StateGenerator = Generator[str, TicTurn, MoveResult]


def default_tic(
        dimension: int
) -> StateGenerator:
    return tic(
        grid_generator,
        is_the_game_complete_horizontally,
        is_the_game_complete_vertically,
        move,
        dimension
    )


def tic(
        _grid_generator:                    GridGenerator,
        _is_the_game_complete_horizontally: GameCompleteCheck,
        _is_the_game_complete_vertically:   GameCompleteCheck,
        _move:                              Move,
        _dimension:                         int,
) -> StateGenerator:
    def _lift_move(turn: TicTurn) -> MoveResult:
        new_state = _move(turn.icon, turn.current_state, turn.x, turn.y)
        if (h := _is_the_game_complete_horizontally(new_state)) is not None:
            return MoveResult(new_state, CompletedGame(h, None))
        if (v := _is_the_game_complete_vertically(new_state)) is not None:
            return MoveResult(new_state, CompletedGame(None, v))
        return MoveResult(new_state, None)

    def _play():
        state = _grid_generator(_dimension)
        turn = yield state
        while True:
            result = _lift_move(turn)
            if result.completed is not None:
                return result
            turn = yield result.state

    return _play()


def move(icon: str, state: str, x: int, y: int) -> str:
    matrix = [list(x) for x in state.split('\n')]
    matrix[y][x] = icon
    return '\n'.join([''.join(x) for x in matrix])


def grid_generator(dimension: int) -> str:
    return '\n'.join([('*' * dimension)] * dimension)


def is_the_game_complete_horizontally(state: str) -> GameComplete:
    for index, row in enumerate(state.split('\n')):
        first_character = row[0]
        if first_character == '*':
            continue
        if all([x == first_character for x in row]):
            return index, first_character
    return None


def is_the_game_complete_vertically(state: str) -> GameComplete:
    if len(state) == 1:
        return None if state == '*' else 0, state
    matrix = [list(x) for x in state.split('\n')]
    first_row = matrix[0]
    for column_index, _ in enumerate(matrix):
        if (first_character := first_row[column_index]) == '*':
            continue
        if all([x[column_index] == first_character for x in matrix]):
            return column_index, first_character
    return None
