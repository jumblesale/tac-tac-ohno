from typing import Optional, Tuple, Literal, Callable

GridGenerator = Callable[[int], str]
GameComplete = Optional[Tuple[int, str]]
GameCompleteCheck = Callable[[str], GameComplete]
Tic = Callable[[
    GridGenerator,
    GameCompleteCheck,
    GameCompleteCheck,
    Callable[[str], str]
], str]


def tic(
    _grid_generator:                    GridGenerator,
    _is_the_game_complete_horizontally: GameCompleteCheck,
    _is_the_game_complete_vertically:   GameCompleteCheck,
    _tic_to_tac:                        Callable[[str], str],
) -> str:
    ...


def grid_generator():
    pass


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
