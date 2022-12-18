from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def in_sprite(s: int, p: int) -> bool:
    return (s >= p - 1) & (s <= p + 1)


def computeP1(s: str) -> int:
    commands = s.splitlines()

    cycle = 1
    strength = 1
    graph = [0]

    for c in commands:
        if c.startswith('noop'):
            graph.append(strength)
            cycle += 1
        if c.startswith('addx'):
            _, value = c.split(" ")
            value = int(value)

            graph.append(strength)
            cycle += 1
            graph.append(strength)
            cycle += 1
            strength += value

    final = 0
    for r in range(20, cycle, 40):
        peak = r * graph[r]
        # print(f"C:{r}\tS:{graph[r]}\tPeak:{peak}")
        final += peak

    return final


def check_pixel(s: int, c: int) -> str:
    nl = '\n' if (c == 39) else ""
    if in_sprite(s, c):
        return "#"+nl
    else:
        return "."+nl


def compute(s: str) -> str:
    commands = s.splitlines()

    cycle = 0
    strength = 1
    graph = [0]
    screen = ""

    for c in commands:
        if c.startswith('noop'):
            graph.append(strength)
            screen += check_pixel(strength, cycle)
            cycle = (cycle + 1) % 40
        elif c.startswith('addx'):
            _, value = c.split(" ")
            value = int(value)

            graph.append(strength)
            screen += check_pixel(strength, cycle)
            cycle = (cycle + 1) % 40

            graph.append(strength)
            screen += check_pixel(strength, cycle)
            cycle = (cycle + 1) % 40

            strength += value

    print(screen)
    # for r in range(20, cycle, 40):
    #     peak = r * graph[r]
    #     print(f"C:{r}\tS:{graph[r]}\tPeak:{peak}")
    #     final += peak

    return screen


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
EXPECTED_I = 13140

EXPECTED_S = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


@pytest.mark.parametrize(
    ('input_s', 'expected_s', 'expected_i'),
    (
        (INPUT_S, EXPECTED_S, EXPECTED_I),
    ),
)
def test(input_s: str, expected_s: str, expected_i: int) -> None:
    assert computeP1(input_s) == expected_i
    assert compute(input_s) == expected_s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
