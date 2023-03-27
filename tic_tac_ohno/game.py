from typing import Optional, Tuple, Literal

GameComplete = Optional[Tuple[int, str]]
InvalidGrid = Literal['characters', 'horizontal', 'vertically', 'diagonally']


def is_the_game_complete_horizontally(state: str) -> GameComplete:
    for index, row in enumerate(state.split('\n')):
        first_character = row[0]
        if first_character == '*':
            continue
        if all([x == first_character for x in row]):
            return index, first_character
    return None


def is_the_game_complete_vertically(state: str) -> GameComplete:
    pass
