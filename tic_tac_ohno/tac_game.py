from typing import Generator, Literal, Callable, Tuple, cast, NamedTuple

from game_lib import GameState, Player, get_bounded_player_input
from tac.tac import Move, is_the_game_complete, valid_move, move, ValidMoveCheck, GameCompleteCheck

ColumnOrRow = Literal['c', 'r']
RowColumnInput = Callable[[str], Tuple[ColumnOrRow, int]]
ColumnRow = Tuple[ColumnOrRow, int]
ColumnRowInput = Callable[[str], ColumnRow]


class TacTurn(NamedTuple):
    current_state:     str
    icon:              str
    other_player_icon: str
    column_or_row:     ColumnOrRow
    index:             int


TacTurnGenerator = Generator[TacTurn, GameState, None]
TacStateGenerator = Generator[str, TacTurn, None]
TacTurnChecker = Callable[[GameState, ColumnOrRow, int], bool]


def get_column_or_row_index(
        maximum: int
) -> ColumnRowInput:
    _input = get_bounded_player_input(maximum)

    def _input_to_column_row_literal(cr: str) -> ColumnOrRow:
        return {'c': 'c', 'r': 'r'}[cr]

    def _get_column_or_row(_current_player_icon: str) -> ColumnRow:
        _column_or_row = input(f'{_current_player_icon} column or row? [cr]')
        if len(_column_or_row) != 1 or _column_or_row[0].lower() not in 'cr':
            print(f"I don't understand {_column_or_row} - please choose from [cr]")
            return _get_column_or_row(_current_player_icon)
        _prompt = 'column' if _column_or_row == 'c' else 'row'
        _index = _input(f'Which {_prompt}? ')
        return _input_to_column_row_literal(_column_or_row), _index
    return _get_column_or_row


def tac_turn_generator(
    _column_row_input: ColumnRowInput,
    _valid_move_check: TacTurnChecker
) -> TacTurnGenerator:
    game_state: GameState = yield
    while True:
        column_or_row, index = _column_row_input(game_state.current_player.icon)
        if not _valid_move_check(game_state, column_or_row, index):
            print(f'{"Column" if column_or_row == "c" else "Row"} {index} does not start with',
                  f'{game_state.current_player.icon}, please choose a different move.')
            continue
        game_state = yield TacTurn(
            game_state.state,
            game_state.current_player.icon,
            game_state.other_player.icon,
            column_or_row,
            index
        )


def lift_valid_move(_valid_move: ValidMoveCheck) -> Callable[[GameState, ColumnOrRow, int], bool]:
    def _lift_valid_move(game_state: GameState, column_or_row: ColumnOrRow, index: int) -> bool:
        return _valid_move(game_state.state, column_or_row, game_state.current_player.icon, index)

    return _lift_valid_move


def tac_state_generator(
    _is_the_game_complete: GameCompleteCheck,
    _move:                 Move,
    _starting_grid:        str,
) -> Callable[[], TacStateGenerator]:
    turn = yield _starting_grid
    while True:
        new_state = _move(
            turn.current_state,
            turn.column_or_row,
            turn.icon,
            turn.other_player_icon,
            turn.index
        )
        if _is_the_game_complete(new_state, turn.icon):
            return new_state
        turn = yield new_state


def tac(
        _is_the_game_complete: Callable[[str], bool],
        _move:                 Move,
        _tac_turn_checker:     TacTurnChecker,
        _starting_grid:        str,
) -> Tuple[TacStateGenerator, TacTurnGenerator]:
    dimension = len(_starting_grid.split('\n')[0])
    return tac_state_generator(
        _is_the_game_complete,
        _move,
        _starting_grid,
    ), tac_turn_generator(
        get_column_or_row_index(dimension),
        _tac_turn_checker
    )


def default_tac(
    starting_grid:    str,
) -> Tuple[TacStateGenerator, TacTurnGenerator]:
    return tac(
        is_the_game_complete,
        move,
        lift_valid_move(valid_move),
        starting_grid,
    )
