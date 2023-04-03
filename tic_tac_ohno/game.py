import itertools
from typing import Generator, Tuple

from tic_tac_ohno.game_lib import Player, GameState, create_players, get_dimension
from tic_tac_ohno.tic_game import tic


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
    yield from itertools.count(0)


def player_generator():
    alpha, omega = create_players()
    return itertools.cycle(
        [(alpha, omega), (omega, alpha)])


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
) -> Generator[str, None, Tuple[str, str]]:
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


def play_tic(
    _grid_generator,
    _is_the_game_complete_horizontally,
    _is_the_game_complete_vertically,
    _move
):
    def _play(tic_creator):
        _tic_state_generator, _tic_turn_generator = tic_creator
        tic_game = game(
            title='TIC, tac, oh no!',
            state_generator=_tic_state_generator,
            player_generator=player_generator(),
            turn_generator=_tic_turn_generator,
            _turn_count_generator=turn_count_generator(),
        )

        return consume_generator(tic_game)

    return _play(
        tic(
            _grid_generator=_grid_generator,
            _is_the_game_complete_horizontally=_is_the_game_complete_horizontally,
            _is_the_game_complete_vertically=_is_the_game_complete_vertically,
            _move=_move,
            _dimension=get_dimension(),
        )
    )


def main():
    pass


if __name__ == '__main__':
    main()
