from typing import Callable, NamedTuple, Literal

Players = Literal['⍺', 'Ω']


class Player(NamedTuple):
    player: Players
    icon:   str


class GameState(NamedTuple):
    state:          str
    current_player: Player
    other_player:   Player


def get_bounded_player_input(maximum: int) -> Callable[[str], int]:
    def _out_of_bounds(_input: int):
        nonlocal maximum
        print(f'{_input} is out of bounds')
        return _get_player_x_y(maximum)

    def _get_player_x_y(prompt: str):
        nonlocal maximum
        _input = input(prompt)
        try:
            _input = int(_input)
        except ValueError:
            print(f"I'm sorry I don't think that {_input} is a number")
        if _input > maximum:
            return _out_of_bounds(_input)
        return _input
    return _get_player_x_y
