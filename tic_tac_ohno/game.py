import itertools
from typing import Literal

from tic_tac_ohno.tic import *

Players = Literal['⍺', 'Ω']
XY = Callable[[str], Tuple[int, int]]


class Player(NamedTuple):
    player: Players
    icon:   str


def draw(state, current_player: Player, next_player: Player, turn_count: int):
    title = '| TIC, TAC, OH NO |'
    info_box_width = 36
    new_line = '\n'

    def _draw_players(_current_player: Player, _next_player: Player):
        return f"""
| ✅ {current_player.player}({current_player.icon}){' ' * 20}🛑 {next_player.player}({next_player.icon}) |""".lstrip()

    def _draw_turn_counter(_turn_count: int):
        turn = ' Turn: '
        width = len(title) - len(turn)
        return f"""
+-------<{turn}{str(_turn_count).ljust(width, ' ')}>--------+""".lstrip()

    def _draw_state(_state: str):
        rows = _state.splitlines()
        width = len(rows[0])
        return [x.center(info_box_width, ' ') for x in [
            f'   | {"".join([str(x) for x in range(0, width)])}',
            f'---+-{"-" * width}',
            *[f'{str(row_counter).ljust(3, " ")}| {row}' for row_counter, row in enumerate(rows)]
        ]]

    return f"""
{new_line.join(list(_draw_state(state)))}

 {("=" * len(title)).center(info_box_width, ' ')}
+{title.center(info_box_width, '-')}+
|{("=" * len(title)).center(info_box_width, ' ')}|
{_draw_players(current_player, next_player)}
{_draw_turn_counter(turn_count)}
"""


def get_player_x_y(maximum: int) -> XY:

    def _out_of_bounds(x_or_y: int):
        nonlocal maximum
        print(f'{x_or_y} is out of bounds')
        yield from get_player_x_y(maximum)

    def _get_x_y(_current_player_icon: str):
        nonlocal maximum
        x = int(input(f'{_current_player_icon} x: '))
        if x > maximum:
            return _out_of_bounds(x)
        y = int(input(f'{_current_player_icon} y: '))
        if y > maximum:
            return _out_of_bounds(y)
        return x, y

    return _get_x_y


def game(
    alpha_player:    Player,
    omega_player:    Player,
    state_generator: StateGenerator,
    x_y:             XY,
):
    player_generator = itertools.cycle(
        [(omega_player, alpha_player), (alpha_player, omega_player)])
    state = next(state_generator)
    current_player, next_player = alpha_player, omega_player
    turn_count = 0
    yield draw(state, alpha_player, omega_player, turn_count)
    while True:
        x, y = x_y(current_player.player)
        turn = Turn(state, current_player.icon, x, y)
        try:
            state = state_generator.send(turn)
        except StopIteration as ex:
            print(draw(ex.value.state, current_player, next_player, turn_count))
            return ex.value
        turn_count += 1
        current_player, next_player = next(player_generator)
        yield draw(state, current_player, next_player, turn_count)


def main():
    def _get_dimension():
        _max = 10
        _dimension = int(input('How big should the grid be? '))
        if _dimension > _max:
            print(f'Maximum dimension is {_max}')
            return _get_dimension()
        return _dimension
    dimension = _get_dimension()
    alpha_icon = input('Player ⍺, choose an icon: ')
    omega_icon = input('Player Ω, choose an icon: ')
    alpha = Player('⍺', alpha_icon)
    omega = Player('Ω', omega_icon)
    players = {
        alpha_icon: Player('⍺', alpha_icon),
        omega_icon: Player('Ω', omega_icon),
    }
    screen_generator = game(
        alpha,
        omega,
        default_tic(dimension),
        get_player_x_y(dimension),
    )
    for screen in screen_generator:
        print(screen)


if __name__ == '__main__':
    main()
