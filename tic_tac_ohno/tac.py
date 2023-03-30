def is_the_game_complete(state: str) -> bool:
    return False


def test_it_returns_true_when_only_one_icon_is_present():
    # arrange
    state = ['***', '*&*', '***']
    expected_result = True

    # act
    result = is_the_game_complete(state)

    # assert
    assert result == expected_result
