import functools
from typing import List, Literal, Callable, NamedTuple, Generator

ColumnOrRow = Literal['c', 'r']
Move = Callable[[str, ColumnOrRow, str, str, int], str]
ValidMoveCheck = Callable[[str, ColumnOrRow, int], bool]


class TacTurn(NamedTuple):
    current_state:     str
    player_icon:       str
    other_player_icon: str
    column_or_row:     ColumnOrRow
    index:             int


def valid_move(state: str, column_or_row: ColumnOrRow, icon: str, index: int):
    matrix = [list(x) for x in state.split('\n')]
    if column_or_row == 'c':
        return matrix[0][index] == icon
    return matrix[index][0] == icon


def default_tac(
        _starting_grid: str
) -> Generator[str, TacTurn, str]:
    return tac(is_the_game_complete, move, _starting_grid)


def tac(
        _is_the_game_complete: Callable[[str], bool],
        _move:                 Move,
        _valid_move:           Callable[[ColumnOrRow, int], bool],
        _starting_grid:        str,
) -> Generator[str, TacTurn, str]:
    turn: TacTurn = yield _starting_grid
    while True:
        new_state = _move(
            turn.current_state,
            turn.column_or_row,
            turn.player_icon,
            turn.other_player_icon,
            turn.index
        )
        if _is_the_game_complete(new_state):
            return new_state
        turn = yield new_state


def is_the_game_complete(state: str) -> bool:
    unique_characters = set(''.join(state.split('\n')))
    unique_characters.discard('*')
    return len(unique_characters) < 2


def move(state:             str,
         column_or_row:     ColumnOrRow,
         player_icon:       str,
         other_player_icon: str,
         index:             int, ) -> str:
    matrix = state.split('\n')
    partial_transform_row = functools.partial(transform_row, player_icon, other_player_icon, index)
    if column_or_row is 'c':
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
