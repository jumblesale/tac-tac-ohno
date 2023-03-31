import itertools
from typing import Callable, Generator, Tuple, NamedTuple

from tic_tac_ohno.game_lib import GameState, get_bounded_player_input
from tic_tac_ohno.tic.tic import MoveResult, GridGenerator, GameCompleteCheck, Move, CompletedGame, grid_generator,\
    is_the_game_complete_horizontally, is_the_game_complete_vertically, move

XYInput = Callable[[str], Tuple[int, int]]


class TicTurn(NamedTuple):
    current_state: str
    icon:          str
    x:             int
    y:             int


TicTurnGenerator = Generator[TicTurn, GameState, None]
TicStateGenerator = Generator[str, TicTurn, MoveResult]
Tic = Callable[[
    GridGenerator,
    GameCompleteCheck,
    GameCompleteCheck,
    Callable[[str], str]
], str]


def get_player_x_y(maximum: int) -> XYInput:
    _input = get_bounded_player_input(maximum)

    def _get_player_x_y(player_icon: str):
        x = _input(f'{player_icon} x: ')
        y = _input(f'{player_icon} y: ')
        return x, y
    return _get_player_x_y


def tic_turn_generator(
    x_y_input: XYInput,
) -> TicTurnGenerator:
    input_display: GameState = yield
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
