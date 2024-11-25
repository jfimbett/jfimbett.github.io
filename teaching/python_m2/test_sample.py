# content of test_sample.py
def inc(x):
    return x + 1


import pytest

@pytest.mark.parametrize(
        "input, expected", [
            (1,2),
            (2,3),
            (3,4),
            (4,5),
            (5, 6)
        ]
)
def test_answer(input, expected):
    assert inc(input) == expected