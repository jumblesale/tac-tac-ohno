from typing import Callable, Generator, Tuple, NamedTuple

from game_lib import GameState, get_bounded_player_input, Player, player_prompt
from tic.tic import GridGenerator, GameCompleteCheck, Move, grid_generator, \
    is_the_game_complete_horizontally, is_the_game_complete_vertically, move

XYInput = Callable[[str], Tuple[int, int]]


class TicTurn(NamedTuple):
    current_state: str
    icon:          str
    x:             int
    y:             int


TicTurnGenerator = Generator[TicTurn, GameState, None]
TicStateGenerator = Generator[str, TicTurn, str]
Tic = Callable[[
    GridGenerator,
    GameCompleteCheck,
    GameCompleteCheck,
    Callable[[str], str]
], str]


def get_player_x_y(maximum: int) -> XYInput:
    _input = get_bounded_player_input(maximum)

    def _get_player_x_y(player: Player):
        return (_input(player_prompt(z)(player)) for z in ('x', 'y'))
    return _get_player_x_y


def tic_turn_generator(
    x_y_input: XYInput,
) -> TicTurnGenerator:
    game_state: GameState = yield
    while True:
        x, y = x_y_input(game_state.current_player)
        game_state = yield TicTurn(
            game_state.state, game_state.current_player.icon, x, y
        )


def tic_state_generator(
    _grid_generator:                    GridGenerator,
    _is_the_game_complete_horizontally: GameCompleteCheck,
    _is_the_game_complete_vertically:   GameCompleteCheck,
    _move:                              Move,
    dimension:                          int,
) -> TicStateGenerator:
    state = _grid_generator(dimension)
    turn = yield state

    while True:
        new_state = _move(turn.icon, turn.current_state, turn.x, turn.y)
        if _is_the_game_complete_horizontally(new_state) or \
                _is_the_game_complete_vertically(new_state):
            return new_state

        turn = yield new_state


def tic(
    _grid_generator:                    GridGenerator,
    _is_the_game_complete_horizontally: GameCompleteCheck,
    _is_the_game_complete_vertically:   GameCompleteCheck,
    _move:                              Move,
    _dimension:                         int,
) -> Tuple[TicStateGenerator, TicTurnGenerator]:
    return tic_state_generator(
        _grid_generator,
        _is_the_game_complete_horizontally,
        _is_the_game_complete_vertically,
        _move,
        _dimension
    ), tic_turn_generator(get_player_x_y(_dimension))


def default_tic(
        dimension: int
) -> Tuple[TicStateGenerator, TicTurnGenerator]:
    return tic(
        grid_generator,
        is_the_game_complete_horizontally,
        is_the_game_complete_vertically,
        move,
        dimension
    )
