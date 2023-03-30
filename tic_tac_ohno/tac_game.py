from typing import Generator, Literal, Callable, Tuple

from tic_tac_ohno.game_lib import InputDisplay, Player, get_bounded_player_input
from tic_tac_ohno.tac.tac import TacTurn

ColumnOrRow = Literal['column', 'row']
RowColumnInput = Callable[[str], Tuple[ColumnOrRow, int]]
TacStateGenerator = Generator[str, TacTurn, None]
ColumnRowInput = Callable[[str], Tuple[ColumnOrRow, int]]
TacTurnGenerator = Generator[TacTurn, InputDisplay, None]
ValidMoveCheck = Callable[[str, str, ColumnOrRow, int], bool]


def get_column_or_row_index(
        maximum:     int,
        _valid_move: ValidMoveCheck,
) -> ColumnRowInput:
    _input = get_bounded_player_input(maximum)

    def _get_column_or_row(_current_player_icon: str):
        _column_or_row = input(f'{_current_player_icon} column or row? [cr]')
        if _column_or_row[0].lower() not in 'cr':
            print(f"I don't understand {_column_or_row} - please choose from [cr]")
            return _get_column_or_row(_current_player_icon)
        _prompt = 'column' if _column_or_row == 'c' else 'row'
        _index = _input(f'Which {_prompt}? ')
        return _column_or_row, _index
    return _get_column_or_row


def tac_turn_generator(
    column_row_input: ColumnRowInput
) -> Generator[TacTurn, InputDisplay, None]:
    input_display: InputDisplay = yield
    while True:
        column_or_row, index = column_row_input(input_display.current_player.icon)
        input_display = yield TacTurn(
            input_display.state, input_display.current_player.icon, column_or_row, index
        )


def tac_game(
    alpha_player:        Player,
    omega_player:        Player,
    tac_state_generator: TacStateGenerator,
    _tac_turn_generator: TacTurnGenerator,
):
    state = next(tac_state_generator)
    return 'hello'
