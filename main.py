import pytest


def is_the_game_finished(state: str) -> bool:
    pass


class TestTickTacOhno:
    def test_the_game_is_finished_when_there_is_a_row_of_the_same_icon(self):
        state = """
***
XXX
***
"""
        assert is_the_game_finished(state) is True
