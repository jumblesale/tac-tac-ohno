import itertools

from tic_tac_ohno.game_lib import Player, GameState
from tic_tac_ohno.tac_game import tac_turn_generator, get_column_or_row_index, default_tac
from tic_tac_ohno.tic_game import tic_turn_generator, get_player_x_y, default_tic


def draw(title: str, state: str, current_player: Player, next_player: Player, turn_count: int):
    title = f'| {title} |'
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


def turn_count_generator():
    count = 0
    while True:
        yield count
        count += 1


def consume_generator(generator):
    while True:
        try:
            print(next(generator))
        except StopIteration as ex:
            return ex.value


def game(
    title: str,
    player_generator,
    state_generator,
    turn_generator,
    _turn_count_generator,
):
    state = next(state_generator)
    next(turn_generator)
    turn_count = next(_turn_count_generator)
    current_player, next_player = next(player_generator)
    yield draw(title, state, current_player, next_player, turn_count)
    while True:
        game_state = GameState(state, current_player, next_player)
        turn = turn_generator.send(game_state)
        try:
            state = state_generator.send(turn)
        except StopIteration as ex:
            yield draw(title, ex.value, current_player, next_player, turn_count)
            # discard the next player
            next(player_generator)
            return ex.value, next_player.icon
        turn_count = next(_turn_count_generator)
        current_player, next_player = next(player_generator)
        yield draw(title, state, current_player, next_player, turn_count)


def main():
    def _get_dimension():
        return 2
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
    player_generator = itertools.cycle(
        [(alpha, omega), (omega, alpha)])
    _turn_count_generator = turn_count_generator()

    _tic_state_generator, _tic_turn_generator = default_tic(dimension)
    tic_game = game(
        'TIC, tac, oh no!',
        player_generator,
        _tic_state_generator,
        _tic_turn_generator,
        _turn_count_generator,
    )
    final_state, next_player_icon = consume_generator(tic_game)

    _tac_turn_generator, _tac_state_generator = default_tac(final_state)
    tac_game = game(
        'tic, TAC, oh no!',
        player_generator,
        _tac_state_generator,
        _tac_turn_generator,
        _turn_count_generator,
    )
    final_state = consume_generator(tac_game)


if __name__ == '__main__':
    main()
