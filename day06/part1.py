from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

marker_length = 4


def find_marker(s: str, i: int) -> int:
    chars = ''
    print('I:%d S:%s' % (i, s))
    for x in range(i, len(s)):
        chars = s[x-marker_length:x]
        count = 0
        print('%d:%s\t' % (x, chars), end='')
        for c in chars:
            count = chars.count(c)
            if count > 1:
                break

        if count == 1:
            print()
            return x

    return 0


def compute(s: str) -> int:
    ret = find_marker(s, marker_length)
    return ret


INPUT_A = '''mjqjpqmgbljsphdztnvjfqwrcgsmlb'''
EXPECTED_A = 7
INPUT_B = '''bvwbjplbgvbhsrlpgdmjqwftvncz'''
EXPECTED_B = 5
INPUT_C = '''nppdvjthqldpwncqszvftbrmjlhg'''
EXPECTED_C = 6
INPUT_D = '''nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'''
EXPECTED_D = 10
INPUT_E = '''zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'''
EXPECTED_E = 11


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_A, EXPECTED_A),
        (INPUT_B, EXPECTED_B),
        (INPUT_C, EXPECTED_C),
        (INPUT_D, EXPECTED_D),
        (INPUT_E, EXPECTED_E),
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
