from typing import List
import pytest
from tic_tac_ohno.tic.tic import is_the_game_complete_horizontally,\
                                 is_the_game_complete_vertically,\
                                 grid_generator,\
                                 move


def a_blank_state(dimension: int) -> str:
    return a_state_with_rows(['*' * dimension] * dimension)


def a_state_with_rows(rows: List[str]) -> str:
    return '\n'.join(rows)


blank_grids = [
    ('*',                             1),
    ('**\n**',                        2),
    ('***\n***\n***',                 3),
    ('****\n****\n****\n****',        4),
    (((('*' * 32) + '\n') * 32)[:-1], 32), ]


@pytest.mark.parametrize('expected, dimension', blank_grids)
def test_it_generates_blank_grids(expected, dimension):
    assert grid_generator(dimension) == expected


non_complete_states = [
    a_blank_state(1),
    a_blank_state(3),
    a_state_with_rows(['**o',
                       '*o*',
                       'o**', ]),
    a_state_with_rows(['o**',
                       '*o*',
                       '**o', ]),
    a_state_with_rows(['**',
                       'X*']),
    a_state_with_rows(['*e*',
                       'e**',
                       '**&', ]),
    a_state_with_rows(['*' * 99]) * 99, ]
non_complete_rows = [
    a_state_with_rows(['o**',
                       'o**',
                       'o**', ]),
    a_state_with_rows(['oo*',
                       '*oo',
                       '*o*', ]), ]
non_complete_columns = [
    a_state_with_rows(['o**',
                       '*o*',
                       '**o', ]),
    a_state_with_rows(['**o',
                       '*o*',
                       'o**', ]),
    a_state_with_rows(['ooo',
                       '***',
                       '***', ]), ]


@pytest.mark.parametrize('state', non_complete_states + non_complete_rows)
def test_the_game_is_not_finished_when_there_are_incomplete_rows(state):
    assert is_the_game_complete_horizontally(state) is None


@pytest.mark.parametrize('state', non_complete_states + non_complete_columns)
def test_the_game_is_not_finished_when_there_are_incomplete_columns(state):
    assert is_the_game_complete_vertically(state) is None


complete_states_rows = [
    (a_state_with_rows(['p']),    (0, 'p')),
    (a_state_with_rows(['**',
                        '55', ]), (1, '5')),
    (a_state_with_rows(['qq',
                        '*q', ]), (0, 'q')),
    (a_state_with_rows(['zzzz*',
                        ';;*;;',
                        'zzzz*',
                        ';;;;;',
                        '*****', ]), (3, ';')), ]


@pytest.mark.parametrize('state, expected', complete_states_rows)
def test_the_game_is_finished_when_there_is_a_row_of_the_same_icon(state, expected):
    assert is_the_game_complete_horizontally(state) == expected


complete_states_columns = [
    (a_state_with_rows(['¥']),    (0, '¥')),
    (a_state_with_rows(['.,',
                        '.*', ]), (0, '.')),
    (a_state_with_rows(['.q',
                        '*q', ]), (1, 'q')),
    (a_state_with_rows(['S%',
                        '*%', ]), (1, '%')),
    (a_state_with_rows(['***#*',
                        '^**#*',
                        '*^*#*',
                        '**^#*',
                        '***#*', ]), (3, '#')), ]


@pytest.mark.parametrize('state, expected', complete_states_columns)
def test_the_game_is_finished_when_there_is_a_column_of_the_same_icon(state, expected):
    assert is_the_game_complete_vertically(state) == expected


def test_moving_applies_an_icon_to_a_location():
    # arrange
    icon = '&'
    x = 1
    y = 2
    starting_state = a_state_with_rows(
        ['&*$', '*$*', '$*&'])
    expected_state = '\n'.join(
        ['&*$', '*$*', '$&&'])

    # act
    new_state = move(icon, starting_state, x, y)

    # assert
    assert new_state == expected_state
