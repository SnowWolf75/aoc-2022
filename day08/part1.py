from __future__ import annotations

import argparse
import os.path
from io import StringIO

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
max_x = 0
max_y = 0


def vmax(x: int, y: int, g: np.ndarray) -> bool:
    if x == 0 or x == max_x-1:
        return True
    elif y == 0 or y == max_y-1:
        return True

    cell = g['n'][x, y]
    if cell > max(g['n'][0:x, y]):
        return True
    elif cell > max(g['n'][x+1:max_x, y]):
        return True
    elif cell > max(g['n'][x, 0:y]):
        return True
    elif cell > max(g['n'][x, y+1:max_y]):
        return True

    return False


def compute(s: str) -> int:
    lines = s.splitlines()
    global max_x
    max_x = len(lines[0])
    global max_y
    max_y = len(lines)
    regex = r'([0-9])'
    grid = StringIO(''.join(lines))
    g = np.fromregex(grid, regex, dtype=[('n', int)]).reshape([max_x, max_y])
    v = np.zeros([max_x, max_y], dtype=bool)

    for i in range(0, max_x):
        for j in range(0, max_y):
            v[i, j] = vmax(i, j, g)

    print(g)
    print(v)

    num_vis = np.count_nonzero(v)

    return num_vis


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
