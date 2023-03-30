import itertools
from typing import Callable, Generator, Tuple

from tic_tac_ohno.game_lib import Player, InputDisplay, get_bounded_player_input
from tic_tac_ohno.tic.tic import TicTurn, MoveResult, GridGenerator, GameCompleteCheck, Move, CompletedGame, \
    grid_generator, is_the_game_complete_horizontally, is_the_game_complete_vertically, move

XYInput = Callable[[str], Tuple[int, int]]
TicTurnGenerator = Generator[TicTurn, InputDisplay, None]
TicStateGenerator = Generator[str, TicTurn, MoveResult]


def get_player_x_y(maximum: int) -> XYInput:
    _input = get_bounded_player_input(maximum)

    def _get_player_x_y(player_icon: str):
        x = _input(f'{player_icon} x: ')
        y = _input(f'{player_icon} y: ')
        return x, y
    return _get_player_x_y


def tic_turn_generator(
    x_y_input: XYInput,
) -> Generator[TicTurn, InputDisplay, None]:
    input_display: InputDisplay = yield
    while True:
        x, y = x_y_input(input_display.current_player.icon)
        input_display = yield TicTurn(
            input_display.state, input_display.current_player.icon, x, y
        )


def tic(
        _grid_generator:                    GridGenerator,
        _is_the_game_complete_horizontally: GameCompleteCheck,
        _is_the_game_complete_vertically:   GameCompleteCheck,
        _move:                              Move,
        _dimension:                         int,
) -> TicStateGenerator:
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


def main():
    def _get_dimension():
        return 4
        _max = 9
        _min = 2
        _dimension = int(input('How big should the grid be? '))
        if _dimension > _max:
            print(f'Maximum dimension is {_max}')
            return _get_dimension()
        if _dimension < _min:
            print(f'Minimum dimension is {_min}')
            return _get_dimension()
        return _dimension
    dimension = _get_dimension()
    # alpha_icon = input('Player ⍺, choose an icon: ')
    # omega_icon = input('Player Ω, choose an icon: ')
    alpha_icon = '@'
    omega_icon = 'O'
    alpha = Player('⍺', alpha_icon)
    omega = Player('Ω', omega_icon)
    tic_state_generator = tic_game(
        alpha,
        omega,
        default_tic(dimension),
        tic_turn_generator(get_player_x_y(dimension))
    )
    tac_state_generator = tac_game(
        alpha,
        omega,
        default_tac,
        tac_turn_generator(get_column_or_row_index(dimension))
    )
    for screen in tac_state_generator:
        print(screen)


def default_tic(
        dimension: int
) -> TicStateGenerator:
    return tic(
        grid_generator,
        is_the_game_complete_horizontally,
        is_the_game_complete_vertically,
        move,
        dimension
    )
