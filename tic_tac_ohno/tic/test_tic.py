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
    assert is_the_game_complete_horizontally(state) is False


@pytest.mark.parametrize('state', non_complete_states + non_complete_columns)
def test_the_game_is_not_finished_when_there_are_incomplete_columns(state):
    assert is_the_game_complete_vertically(state) is False


complete_states_rows = [
    a_state_with_rows(['p']),
    a_state_with_rows(['**',
                       '55', ]),
    a_state_with_rows(['qq',
                       '*q', ]),
    a_state_with_rows(['zzzz*',
                       ';;*;;',
                       'zzzz*',
                       ';;;;;',
                       '*****', ]), ]


@pytest.mark.parametrize('state', complete_states_rows)
def test_the_game_is_finished_when_there_is_a_row_of_the_same_icon(state):
    assert is_the_game_complete_horizontally(state) is True


complete_states_columns = [
    a_state_with_rows(['¥']),
    a_state_with_rows(['.,',
                       '.*', ]),
    a_state_with_rows(['.q',
                       '*q', ]),
    a_state_with_rows(['S%',
                       '*%', ]),
    a_state_with_rows(['***#*',
                       '^**#*',
                       '*^*#*',
                       '**^#*',
                       '***#*', ]), ]


@pytest.mark.parametrize('state', complete_states_columns)
def test_the_game_is_finished_when_there_is_a_column_of_the_same_icon(state):
    assert is_the_game_complete_vertically(state) is True


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
