from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_crates(c: str) -> list[str]:
    cc = c.splitlines()
    regex = r'[ \[]([A-Z ])[ \]] ?'
    columns = len(re.findall(regex, cc[0]))
    verts = ['' for x in range(columns)]
    for rc in cc:
        vc = 0

        for v in re.findall(regex, rc):
            if re.match('[0-9]', v):
                break

            verts[vc] = v + verts[vc]
            # print("Vert: %d\tS: %s" % (vc, verts[vc]))
            vc += 1

    fverts = []
    for fv in verts:
        ffv = fv.lstrip().rstrip()
        fverts.append(ffv)
        # print("FV:", ffv)

    return fverts


def print_stacks(sl: list[str]) -> None:
    sc = len(sl)
    for scc in range(sc):
        print('Si: %d == %s' % (scc, sl[scc]))
    print()


def shuffle(cl: list[str], i: list[str]) -> list[str]:
    # cl = Crate list, as a List of Strings
    # i = a List of instructions, in the format:
    #  move 1 from 2 to 1
    #  move c[x] from l[a] to l[b]

    regex_shuffle = r'move ([0-9]+) from ([0-9]+) to ([0-9]+)'
    # print_stacks(cl)
    # print(i)

    for line in i:
        move = ''
        sx, sa, sb = (
            int(s) for s in re.match(
                regex_shuffle, line, re.IGNORECASE,
            ).groups()
        )

        (cl[sa-1], move) = cl[sa-1][:-sx], cl[sa-1][-sx:]
        # print("i:", sx, "m:", move)
        cl[sb-1] += move

        # print("I:", line)
        # print_stacks(cl)

    return cl


def compute(s: str) -> str:
    crates, instructions = s.split('\n\n')
    crate_list = parse_crates(crates)
    inst_list = instructions.splitlines()
    final_list = shuffle(crate_list, inst_list)

    ret = ''
    for fc in final_list:
        ret += fc[-1]
    # TODO: implement solution here!
    return ret


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'MCD'


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
