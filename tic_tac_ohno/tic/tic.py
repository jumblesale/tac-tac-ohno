from typing import Optional, Callable, NamedTuple

GridGenerator = Callable[[int], str]
GameCompleteCheck = Callable[[str], bool]
Move = Callable[[str, str, int, int], str]


def move(icon: str, state: str, x: int, y: int) -> str:
    matrix = [list(x) for x in state.split('\n')]
    matrix[y][x] = icon
    return '\n'.join([''.join(x) for x in matrix])


def grid_generator(dimension: int) -> str:
    return '\n'.join([('*' * dimension)] * dimension)


def is_the_game_complete_horizontally(state: str) -> bool:
    for index, row in enumerate(state.split('\n')):
        first_character = row[0]
        if first_character == '*':
            continue
        if all([x == first_character for x in row]):
            return True
    return False


def is_the_game_complete_vertically(state: str) -> bool:
    if len(state) == 1:
        return False if state == '*' else True
    matrix = [list(x) for x in state.split('\n')]
    first_row = matrix[0]
    for column_index, _ in enumerate(matrix):
        if (first_character := first_row[column_index]) == '*':
            continue
        if all([x[column_index] == first_character for x in matrix]):
            return True
    return False
