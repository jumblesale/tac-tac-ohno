from tic_tac_ohno.tic import *



if __name__ == '__main__':
    alpha = '🐊'
    omega = '🦥'
    tic_game = tic(
        is_the_game_complete_horizontally,
        is_the_game_complete_vertically,
        lambda x: x
    )
