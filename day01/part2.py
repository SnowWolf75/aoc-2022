from __future__ import annotations

import argparse
import os.path

import pytest

import support
# import numpy as np

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    elves = []
    c = 0
    elves.append(0)

    for i in s.splitlines():
        if i == '':
            c += 1
            elves.append(0)
            #print('')
        else:
            cal_val = int(i)
            elves[c] += cal_val
            #print(f'C: {c}  EV: {elves[c]}')

    max_cal = 0

    hungry = sorted(elves, reverse=True)
    three = hungry[0:3]
    #print(three)

    max_cal = three[0] + three[1] + three[2]

    return max_cal


INPUT_S = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
EXPECTED = 45000


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
