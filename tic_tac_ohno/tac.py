from typing import List

import pytest


def is_the_game_complete(state: str) -> bool:
    return True


def a_state_with_rows(rows: List[str]) -> str:
    return '\n'.join(rows)


complete_games = [a_state_with_rows(x) for x in [
    ['***', '*&*', '***'],
    ['&&&', '&&&', '&&&'],
]]

incomplete_games = [a_state_with_rows(x) for x in [
    ['***', '***', '*0q'],
    ['***', '***', '***'],
    ['ppp', 'ppp', 'ppy'],
]]


@pytest.mark.parametrize("state", complete_games)
def test_it_returns_true_when_only_one_icon_is_present(state):
    # arrange
    expected_result = True

    # act
    result = is_the_game_complete(state)

    # assert
    assert result == expected_result
