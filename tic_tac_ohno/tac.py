def how_many_neighbours(state: str):
    return 0


def test_it_returns_0_for_a_state_with_no_neighbours():
    # arrange
    state = ['***', '*&*', '***']
    expected_neighbours = 0

    # act
    result = how_many_neighbours(state)

    # assert
    assert result == expected_neighbours
