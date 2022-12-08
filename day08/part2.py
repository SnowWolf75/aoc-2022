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


def view(x: int, y: int, g: np.ndarray) -> int:
    if x == 0 or x == max_x-1:
        return 0
    elif y == 0 or y == max_y-1:
        return 0

    cell = g['n'][x, y]

    (d_up, d_lf, d_rt, d_dn) = (0, 0, 0, 0)

    # Up
    for a in range(y-1, 0, -1):
        v = g['n'][x, a]
        if cell > v:
            d_up += 1
            # print(f'u{v}', end='')
        elif cell <= v:
            d_up += 1
            # print(f'U{v}', end='')
            break

    # Down
    for a in range(y+1, max_y-1):
        v = g['n'][x, a]
        if cell > v:
            d_dn += 1
            # print(f'd{v}', end='')
        elif cell <= v:
            d_dn += 1
            # print(f'D{v}', end='')
            break

    # Left
    for a in range(x-1, 0, -1):
        if cell > g['n'][a, y]:
            d_lf += 1
            # print('l', end='')
        elif cell <= g['n'][a, y]:
            d_lf += 1
            # print('L', end='')
            break

    # Right
    for a in range(x+1, max_x-1):
        if cell > g['n'][a, y]:
            d_rt += 1
            # print('r', end='')
        elif cell <= g['n'][a, y]:
            d_rt += 1
            # print('R', end='')
            break

    # print("\t [%d,%d](%d) = [U:%d, D:%d, L:%d, R:%d"
    #   % (x, y, cell, d_up, d_dn, d_lf, d_rt))
    return d_up*d_dn*d_lf*d_rt


def compute(s: str) -> int:
    lines = s.splitlines()
    global max_x
    max_x = len(lines[0])
    global max_y
    max_y = len(lines)
    regex = r'([0-9])'
    grid = StringIO(''.join(lines))
    g = np.fromregex(grid, regex, dtype=[('n', int)]).reshape([max_x, max_y])
    g = np.pad(g, pad_width=1, mode='constant', constant_values=0)
    max_x += 2
    max_y += 2
    v = np.zeros([max_x, max_y], dtype=int)

    print(g['n'])

    for i in range(0, max_x):
        for j in range(0, max_y):
            v[i, j] = view(i, j, g)

    print(v)

    max_vis = np.max(v)

    return max_vis


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
