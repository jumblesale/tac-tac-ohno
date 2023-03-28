from typing import NamedTuple

from tic_tac_ohno.tic import *


class GameState(NamedTuple):
    alpha_icon: str
    omega_icon: str
    state:      str


def game(
    alpha_icon: str,
    omega_icon: str,
    tic:        Tic,
):
    state = GameState(alpha_icon, omega_icon, )


if __name__ == '__main__':
    alpha = '🐊'
    omega = '🦥'
    tic_game = tic(
        grid_generator,
        is_the_game_complete_horizontally,
        is_the_game_complete_vertically,
        lambda x: x
    )
