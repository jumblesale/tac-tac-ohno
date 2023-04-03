import itertools
from typing import Generator, Tuple

from game_lib import Player, GameState, create_players, get_dimension
from tic_game import tic, default_tic
from tac_game import tac, default_tac

INFO_BOX_WIDTH = 36


def draw_state(screen_width: int, _state: str):
    rows = _state.splitlines()
    width = len(rows[0])
    return [x.center(screen_width, ' ') for x in [
        f'   | {"".join([str(x) for x in range(0, width)])}',
        f'---+-{"-" * width}',
        *[f'{str(row_counter).ljust(3, " ")}| {row}' for row_counter, row in enumerate(rows)]
    ]]


def draw_final_state(state: str):
    print('GAME OVER')
    print('Final state:')
    [print(x) for x in draw_state(INFO_BOX_WIDTH, state)]


def draw(title: str, state: str, current_player: Player, next_player: Player, turn_count: int):
    title = f'| {title} |'
    new_line = '\n'

    def _draw_players(_current_player: Player, _next_player: Player):
        return f"""
| ✅ {current_player.player}({current_player.icon}){' ' * 20}🛑 {next_player.player}({next_player.icon}) |""".lstrip()

    def _draw_turn_counter(_turn_count: int):
        turn = ' Turn: '
        width = len(title) - len(turn)
        return f"""
+-------<{turn}{str(_turn_count).ljust(width, ' ')}>--------+""".lstrip()

    return f"""
{new_line.join(list(draw_state(INFO_BOX_WIDTH, state)))}

 {("=" * len(title)).center(INFO_BOX_WIDTH, ' ')}
+{title.center(INFO_BOX_WIDTH, '-')}+
|{("=" * len(title)).center(INFO_BOX_WIDTH, ' ')}|
{_draw_players(current_player, next_player)}
{_draw_turn_counter(turn_count)}
"""


def turn_count_generator():
    yield from itertools.count(0)


def player_generator_from_icons(alpha_icon: str, omega_icon: str):
    alpha, omega = Player('ɑ', alpha_icon), Player('Ω', omega_icon)
    return itertools.cycle(
        [(alpha, omega), (omega, alpha)])


def player_generator():
    alpha, omega = create_players()
    return itertools.cycle(
        [(alpha, omega), (omega, alpha)])


def consume_generator(generator):
    while True:
        try:
            _next = next(generator)
            print(_next)
        except StopIteration as ex:
            return ex.value


def game(
    title: str,
    _player_generator,
    state_generator,
    turn_generator,
    _turn_count_generator,
) -> Generator[str, None, Tuple[str, str]]:
    state = next(state_generator)
    next(turn_generator)
    turn_count = next(_turn_count_generator)
    current_player, next_player = next(_player_generator)
    yield draw(title, state, current_player, next_player, turn_count)
    while True:
        game_state = GameState(state, current_player, next_player)
        turn = turn_generator.send(game_state)
        try:
            state = state_generator.send(turn)
        except StopIteration as ex:
            yield draw(title, ex.value, current_player, next_player, turn_count)
            # discard the next player
            next(_player_generator)
            return ex.value
        turn_count = next(_turn_count_generator)
        current_player, next_player = next(_player_generator)
        yield draw(title, state, current_player, next_player, turn_count)


def _play_tac(
    tac_creator,
    _player_generator=None,
    _turn_count_generator=None,
):
    if _turn_count_generator is None:
        _turn_count_generator = turn_count_generator()
    if _player_generator is None:
        _player_generator = player_generator()

    _tac_state_generator, _tac_turn_generator = tac_creator
    tac_game = game(
        title='tic, TAC, oh no!',
        state_generator=_tac_state_generator,
        _player_generator=_player_generator,
        turn_generator=_tac_turn_generator,
        _turn_count_generator=_turn_count_generator,
    )

    final_state = consume_generator(tac_game)
    draw_final_state(final_state)
    return final_state, player_generator, _turn_count_generator


def play_tac(
    tic_result,
    _is_the_game_complete,
    _move,
    _tac_turn_checker,
):
    final_tic_state, _player_generator, _turn_count_generator = tic_result
    return _play_tac(tic_result, tac(
            _is_the_game_complete=_is_the_game_complete,
            _move=_move,
            _tac_turn_checker=_tac_turn_checker,
            _starting_grid=final_tic_state,
    ))


def _play_tic(tic_creator):
    _turn_count_generator = turn_count_generator()
    _player_generator = player_generator()
    _tic_state_generator, _tic_turn_generator = tic_creator
    tic_game = game(
        title='TIC, tac, oh no!',
        state_generator=_tic_state_generator,
        _player_generator=_player_generator,
        turn_generator=_tic_turn_generator,
        _turn_count_generator=_turn_count_generator,
    )

    final_state = consume_generator(tic_game)
    draw_final_state(final_state)
    return final_state, _player_generator, _turn_count_generator


def play_tic(
    _grid_generator,
    _is_the_game_complete_horizontally,
    _is_the_game_complete_vertically,
    _move
):
    return _play_tic(tic(
        _grid_generator=_grid_generator,
        _is_the_game_complete_horizontally=_is_the_game_complete_horizontally,
        _is_the_game_complete_vertically=_is_the_game_complete_vertically,
        _move=_move,
        _dimension=get_dimension()))


def welcome():
    print(r"""
 __    __     _                            _
/ / /\ \ \___| | ___ ___  _ __ ___   ___  | |_ ___                  
\ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \                 
 \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |                
  \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/                 
                                                                    
 _____ _          _____                 ___ _           __        _ 
/__   (_) ___    /__   \__ _  ___      /___\ |__     /\ \ \___   / \
  / /\/ |/ __|     / /\/ _` |/ __|    //  // '_ \   /  \/ / _ \ /  /
 / /  | | (__ _   / / | (_| | (__ _  / \_//| | | | / /\  / (_) /\_/ 
 \/   |_|\___( )  \/   \__,_|\___( ) \___/ |_| |_| \_\ \/ \___/\/   
             |/                  |/                                 
""")


def main():
    tic_tac_ohno = 'tac'
    if tic_tac_ohno == 'tic':
        tic_result = _play_tic(default_tic(get_dimension()))
    else:
        tic_result = '0*\n01', player_generator_from_icons('0', '1'), turn_count_generator()
    tac_result = _play_tac(default_tac(tic_result[0]), tic_result[1], tic_result[2])


if __name__ == '__main__':
    main()
