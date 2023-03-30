from typing import List, Literal

import pytest

ColumnOrRow = Literal['c', 'r']


def is_the_game_complete(state: str) -> bool:
    unique_characters = set(''.join(state.split('\n')))
    unique_characters.discard('*')
    return len(unique_characters) < 2


def move(
        state:             str,
        column_or_row:     ColumnOrRow,
        player_icon:       str,
        other_player_icon: str,
        index:             int, ) -> str:
    if column_or_row is not 'c':
        raise Exception
    transposed = transpose(state.split('\n'))
    new_line = transform_line(transposed[index], player_icon, other_player_icon)
    transposed[index] = new_line
    return '\n'.join(transpose(transposed))
    # return '\n'.join(['**%*', '%&*%', '&&&*', '*%%&', ])


def transpose(matrix: List[str]) -> List[str]:
    return [''.join([matrix[j][i] for j in range(len(matrix))])
            for i in range(len(matrix[0]))]


def transform_line(
        line:              str,
        player_icon:       str,
        other_player_icon: str, ) -> str:
    new_line = ''
    transform_map = {
        player_icon:       '*',
        '*':               other_player_icon,
        other_player_icon: player_icon,
    }
    for character in line:
        new_line += transform_map[character]
        if character == other_player_icon:
            break
    return new_line + line[len(new_line):]


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
    assert transform_line(initial_state, icon_1, icon_2) == expected_state


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
        '***^', '^^@*', '*@^@', '*%%&', ])

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
