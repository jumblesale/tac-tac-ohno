from typing import List
import pytest
from tic_tac_ohno.game import is_the_game_complete_horizontally, is_the_game_complete_vertically


def a_blank_state(dimension: int) -> str:
    return a_state_with_rows(['*'] * dimension)


def a_state_with_rows(rows: List[str]) -> str:
    return '\n'.join(rows)


non_complete_states = [
    a_blank_state(3),
    a_state_with_rows(['*']),
    a_state_with_rows(['**',
                       'X*']),
    a_state_with_rows(['op',
                       'po']),
    a_state_with_rows(['o*',
                       'o*']),
    a_state_with_rows(['*o',
                       'o*']),
    a_state_with_rows(['o*',
                       '*o']), ]


@pytest.mark.parametrize('state', non_complete_states)
def test_the_game_is_not_finished_when_there_are_incomplete_rows(state):
    assert is_the_game_complete_horizontally(state) is None


complete_row_states_horizontal = [
    (a_state_with_rows(['p']),  (0, 'p')),
    (a_state_with_rows(['**',
                        '55']), (1, '5')),
    (a_state_with_rows(['qq',
                        '*q']), (0, 'q')),
    (a_state_with_rows(['zzzz*',
                        ';;*;;',
                        'zzzz*',
                        ';;;;;',
                        '*****', ]), (3, ';'))]


@pytest.mark.parametrize('state, expected', complete_row_states_horizontal)
def test_the_game_is_finished_when_there_is_a_row_of_the_same_icon(state, expected):
    assert is_the_game_complete_horizontally(state) == expected
