from typing import List
import pytest
from tic_tac_ohno.game import is_the_game_complete_horizontally,\
                              is_the_game_complete_vertically


def a_blank_state(dimension: int) -> str:
    return a_state_with_rows(['*'] * dimension)


def a_state_with_rows(rows: List[str]) -> str:
    return '\n'.join(rows)


non_complete_states = [
    a_blank_state(3),
    a_state_with_rows(['*']),
    a_state_with_rows(['**',
                       'X*']),
    a_state_with_rows(['*e*',
                       'e**',
                       '**&', ]),
    a_state_with_rows([''.join(['*'] * 99)] * 99), ]
non_complete_rows = [
    a_state_with_rows(['o**',
                       'o**',
                       'o**', ]),
    a_state_with_rows(['**o',
                       '*o*',
                       'o**', ]),
    a_state_with_rows(['o**',
                       '*o*',
                       '**o', ]),
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
    (a_state_with_rows(['p']),  (0, 'p')),
    (a_state_with_rows(['**',
                        '55']), (1, '5')),
    (a_state_with_rows(['qq',
                        '*q']), (0, 'q')),
    (a_state_with_rows(['zzzz*',
                        ';;*;;',
                        'zzzz*',
                        ';;;;;',
                        '*****', ]), (3, ';')), ]


@pytest.mark.parametrize('state, expected', complete_states_rows)
def test_the_game_is_finished_when_there_is_a_row_of_the_same_icon(state, expected):
    assert is_the_game_complete_horizontally(state) == expected


complete_states_columns = [
    (a_state_with_rows(['¥']),  (0, '¥')),
    (a_state_with_rows(['.,',
                        '..']), (0, '.')),
    (a_state_with_rows(['q%',
                        '*%']), (1, '%')),
    (a_state_with_rows(['***#*',
                        '^**#*',
                        '*^*#*',
                        '**^#*',
                        '***#*', ]), (3, '#')), ]


@pytest.mark.parametrize('state, expected', complete_states_columns)
def test_the_game_is_finished_when_there_is_a_column_of_the_same_icon(state, expected):
    assert is_the_game_complete_horizontally(state) == expected
