from typing import Callable, NamedTuple, Literal, Tuple

Players = Literal['⍺', 'Ω']


class Player(NamedTuple):
    player: Players
    icon:   str


class GameState(NamedTuple):
    state:          str
    current_player: Player
    other_player:   Player


def get_player_icon(player: str) -> str:
    icon = input(f'Player {player}, choose an icon: ')
    if len(icon) > 1:
        print(f'"{icon}" is too long, please choose a single character')
        return get_player_icon(player)
    return icon


def create_players() -> Tuple[Player, Player]:
    return tuple([Player(x, get_player_icon(x)) for x in ('α', 'Ω')])


def get_dimension():
    _max = 9
    _min = 2
    dimension = int(input('How big should the grid be? '))
    if dimension > _max:
        print(f'Maximum dimension is {_max}')
        return get_dimension()
    if dimension < _min:
        print(f'Minimum dimension is {_min}')
        return get_dimension()
    return dimension


def player_prompt(what_are_they_inputting: str) -> Callable[[Player], str]:
    def _player_prompt(player: Player):
        return f'{player.player}({player.icon}) {what_are_they_inputting}: '
    return _player_prompt


def get_bounded_player_input(maximum: int) -> Callable[[str], int]:
    def _out_of_bounds(_input: int):
        print(f'{_input} is out of bounds')

    def _get_player_x_y(prompt: str):
        nonlocal maximum
        _input = input(prompt)
        try:
            _input = int(_input)
        except ValueError:
            print(f"I'm sorry I don't think that {_input} is a number")
            return _get_player_x_y(prompt)
        if _input > maximum:
            _out_of_bounds(_input)
            return _get_player_x_y(prompt)
        return _input
    return _get_player_x_y
