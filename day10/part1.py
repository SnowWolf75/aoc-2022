from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    commands = s.splitlines()
    strength = [0]
    current = 1
    cycle = 0
    for c in commands:
        if c.startswith("noop"):
            strength.append(current)
            cycle += 1
        elif c.startswith("addx"):
            strength.append(current)
            _, num = c.split(" ")
            num = int(num)
            current += num
            cycle += 2
            strength.append(current)
            print("C:%d\tS:%d" % (cycle, current))
        else:
            print("Borky bork")
            break

    print("Commands: %d" % len(commands))
    print("C:%d\tS:%d" % (cycle, current))

    first = 20
    periodic = 40

    peaks = find_peaks(strength, first, periodic)
    sum = 0
    for (x,y) in peaks:
        print("X: %d\tS: %d\tVV: %d" % (x, y, x*y))
        sum += x * y

    return sum


def find_peaks(s: list[int], f: int, p: int) -> list[(int, int)]:
    if len(s) < f:
        return [(0, 0)]

    arr = []
    i = f
    c = s[i-1]
    arr.append((i, c))

    i += p

    while i < len(s):
        arr.append((i, s[i-1]))
        i += p

    return arr


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = 13140


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
