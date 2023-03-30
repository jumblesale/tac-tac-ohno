from typing import List
import pytest

from tic_tac_ohno.tac.tac import ColumnOrRow, transpose, move, transform_line, is_the_game_complete, valid_move, replace


def a_state_with_rows(rows: List[str]) -> str:
    return '\n'.join(rows)


complete_games = [a_state_with_rows(x) for x in [
    ['***', '*&*', '***'],
    ['***', '***', '***'],
    ['&&&', '&&&', '&&&'], ]]

incomplete_games = [a_state_with_rows(x) for x in [
    ['***', '***', '*0q'],
    ['ppp', 'ppp', 'ppy'], ]]


@pytest.mark.parametrize("state", complete_games)
def test_it_returns_true_when_only_one_icon_is_present(state):
    assert is_the_game_complete(state) is True


@pytest.mark.parametrize("state", incomplete_games)
def test_it_returns_true_when_only_one_icon_is_present(state):
    assert is_the_game_complete(state) is False


line_transformations = [
    ('$**$', '*@@*', '$', '@'),
    ('$@@@', '*$@@', '$', '@'),
    ('$@@@', '*$@@', '$', '@'),
    ('Q*P*', '*PQ*', 'Q', 'P'),
    ('Q***', '*PPP', 'Q', 'P'),
]


@pytest.mark.parametrize("initial_state, expected_state, icon_1, icon_2", line_transformations)
def test_it_converts_lines(initial_state: str, expected_state: str, icon_1: str, icon_2: str):
    assert transform_line(icon_1, icon_2, initial_state) == expected_state


def test_it_fills_in_columns():
    # arrange
    initial_state = a_state_with_rows([
        '**%&',
        '%&**',
        '&&&&',
        '*%%%', ])
    expected_state = '\n'.join([
        '**%*',
        '%&*%',
        '&&&*',
        '*%%&', ])

    # act
    result = move(initial_state, 'c', '&', '%', 3)

    # assert
    assert result == expected_state


def test_it_fills_in_rows():
    # arrange
    initial_state = a_state_with_rows([
        '***^', '^^@*', '^*@@', '**^@', ])
    expected_state = '\n'.join([
        '***^', '^^@*', '*@^@', '**^@', ])

    # act
    result = move(initial_state, 'r', '^', '@', 2)

    # assert
    assert result == expected_state


def test_it_transposes():
    # arrange
    matrix = ['123', '456']
    expected = ['14', '25', '36']

    # act
    result = transpose(matrix)

    # assert
    assert result == expected


def test_it_replaces_lines():
    # arrange
    matrix = ['12345', '67890', '22345', '27890', ]
    expected = ['12345', '67890', '*****', '27890', ]

    # act
    result = replace(2, matrix, '*****')

    # assert
    assert result == expected


invalid_moves = [
    (a_state_with_rows(['***', '***', '***']), 'c', 'Z', 0),
    (a_state_with_rows(['*i*', '***', '***']), 'c', 'Z', 1),
    (a_state_with_rows(['***', '***', '***']), 'r', 'F', 0),
    (a_state_with_rows(['***', '*p*', '***']), 'r', 'F', 1),
]


@pytest.mark.parametrize("state, column_or_row, icon, index", invalid_moves)
def test_it_rejects_invalid_moves(state: str, column_or_row: ColumnOrRow, icon: str, index: int):
    assert valid_move(state, column_or_row, icon, index) is False


valid_moves = [
    (a_state_with_rows(['*Z*', '***', '***']), 'c', 'Z', 1),
    (a_state_with_rows(['O**', '***', '***']), 'c', 'O', 0),
    (a_state_with_rows(['O**', '***', '***']), 'r', 'O', 0),
    (a_state_with_rows(['***', '***', 'P**']), 'r', 'P', 2), ]


@pytest.mark.parametrize("state, column_or_row, icon, index", valid_moves)
def test_it_rejects_invalid_moves(state: str, column_or_row: ColumnOrRow, icon: str, index: int):
    assert valid_move(state, column_or_row, icon, index) is True
