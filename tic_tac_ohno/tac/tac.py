import functools
from typing import List, Literal, Callable

ColumnOrRow = Literal['c', 'r']
Move = Callable[[str, ColumnOrRow, str, str, int], str]
GameCompleteCheck = Callable[[str, str], bool]
ValidMoveCheck = Callable[[str, ColumnOrRow, str, int], bool]


def state_to_list_of_lists(state: str) -> List[List[str]]:
    return [list(x) for x in state.split('\n')]


def valid_move(state: str, column_or_row: ColumnOrRow, icon: str, index: int) -> bool:
    matrix = state_to_list_of_lists(state)
    if column_or_row == 'c':
        return matrix[0][index] == icon
    return matrix[index][0] == icon


def is_the_game_complete(state: str, current_player_icon: str) -> bool:
    matrix = state_to_list_of_lists(state)
    if all([x != current_player_icon for x in matrix[0]] +
           [y[0] != current_player_icon for y in matrix]):
        return True
    unique_characters = set(''.join(state.split('\n')))
    unique_characters.discard('*')
    return len(unique_characters) < 2


def move(
        state:             str,
        column_or_row:     ColumnOrRow,
        player_icon:       str,
        other_player_icon: str,
        index:             int, ) -> str:
    matrix = state.split('\n')
    partial_transform_row = functools.partial(transform_row, player_icon, other_player_icon, index)
    if column_or_row == 'c':
        updated_matrix = transpose(partial_transform_row(transpose(matrix)))
    else:
        updated_matrix = partial_transform_row(matrix)
    return '\n'.join(updated_matrix)


def transform_row(
        player_icon:       str,
        other_player_icon: str,
        index:             int,
        matrix:            List[str], ) -> List[str]:
    return replace(index, matrix, transform_line(player_icon, other_player_icon, matrix[index]))


def transpose(matrix: List[str]) -> List[str]:
    return [''.join([matrix[j][i] for j in range(len(matrix))])
            for i in range(len(matrix[0]))]


def transform_line(player_icon: str, other_player_icon: str, line: str) -> str:
    new_line = ''
    transform_map = {
        player_icon:       '*',
        '*':               other_player_icon,
        other_player_icon: player_icon,
    }
    for character in line:
        new_line += transform_map[character]
        if character == other_player_icon:
            break
    return new_line + line[len(new_line):]


def replace(index: int, matrix: List[str], replacement: str) -> List[str]:
    matrix[index] = replacement
    return matrix
