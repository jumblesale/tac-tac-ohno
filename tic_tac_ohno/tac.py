from typing import List

import pytest


def is_the_game_complete(state: str) -> bool:
    unique_characters = set(''.join(state.split('\n')))
    unique_characters.discard('*')
    return len(unique_characters) < 2


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
