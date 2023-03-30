import itertools

from tic_tac_ohno.game_lib import Player, InputDisplay
from tic_tac_ohno.tic_game import TicTurnGenerator, tic_turn_generator, get_player_x_y, TicStateGenerator, default_tic


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


def game(
    alpha_player:        Player,
    omega_player:        Player,
    tic_state_generator: TicStateGenerator,
    _tic_turn_generator: TicTurnGenerator,
):
    player_generator = itertools.cycle(
        [(omega_player, alpha_player), (alpha_player, omega_player)])
    state = next(tic_state_generator)
    next(_tic_turn_generator)
    current_player, next_player = alpha_player, omega_player
    turn_count = 0
    yield draw(state, alpha_player, omega_player, turn_count)
    while True:
        turn = _tic_turn_generator.send(InputDisplay(state, current_player))
        try:
            state = tic_state_generator.send(turn)
        except StopIteration as ex:
            yield draw(ex.value.state, current_player, next_player, turn_count)
            return ex.value
        turn_count += 1
        current_player, next_player = next(player_generator)
        yield draw(state, current_player, next_player, turn_count)


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
    tic_state_generator = game(
        alpha,
        omega,
        default_tic(dimension),
        tic_turn_generator(get_player_x_y(dimension))
    )
    for screen in tic_state_generator:
        print(screen)


if __name__ == '__main__':
    main()
