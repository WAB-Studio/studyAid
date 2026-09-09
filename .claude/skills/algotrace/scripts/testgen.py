#!/usr/bin/env python3
"""Edge-case test input generator.

Your solution passes the samples but fails a hidden test. Nine times out of
ten the hidden test is one of the shapes below. Generate them, run your
solution, find the one that breaks.

Usage:
    python testgen.py array --n 12 --lo -50 --hi 50
    python testgen.py array --n 10 --sorted --unique
    python testgen.py array --edges           # the standard nasty array cases
    python testgen.py string --n 20 --charset ab
    python testgen.py tree --n 15             # level-order with nulls, LeetCode style
    python testgen.py graph --n 6 --m 9       # edge list, may be disconnected
    python testgen.py intervals --n 8
"""

import argparse
import random


def gen_array(a):
    if a.edges:
        cases = [
            [],                                  # empty
            [1],                                 # single element
            [5, 5],                              # all duplicates, n=2
            [3] * 8,                             # all duplicates, longer
            list(range(1, 9)),                   # already sorted
            list(range(8, 0, -1)),               # reverse sorted
            [-4, -1, 0, 3, 10],                  # negatives with zero
            [2**31 - 1, 2**31 - 1],              # overflow bait for java/c++
            [-2**31, 2**31 - 1],                 # extreme spread
            [0, 0, 0, 1, 0, 0],                  # zeros with one outlier
        ]
        for c in cases:
            print(c)
        return
    vals = range(a.lo, a.hi + 1)
    if a.unique:
        arr = random.sample(list(vals), min(a.n, a.hi - a.lo + 1))
    else:
        arr = [random.randint(a.lo, a.hi) for _ in range(a.n)]
    if a.sorted:
        arr.sort()
    print(arr)


def gen_string(a):
    print("".join(random.choice(a.charset) for _ in range(a.n)))
    # worst cases for substring problems
    print(a.charset[0] * a.n)                    # one repeated char
    print((a.charset * a.n)[: a.n])              # shortest cycle


def gen_tree(a):
    # random binary tree, level-order with nulls (the LeetCode wire format)
    if a.n == 0:
        print("[]")
        return
    out = [1]
    remaining = a.n - 1
    frontier = 1
    val = 2
    while remaining > 0:
        nxt = 0
        for _ in range(frontier):
            for _ in range(2):
                if remaining > 0 and random.random() < 0.7:
                    out.append(val)
                    val += 1
                    remaining -= 1
                    nxt += 1
                else:
                    out.append(None)
        if nxt == 0:
            break
        frontier = nxt
    while out and out[-1] is None:
        out.pop()
    print([v if v is not None else None for v in out])
    # degenerate: the linked-list-shaped tree that kills naive recursion
    print("degenerate (all left):", list(range(1, a.n + 1)))


def gen_graph(a):
    m = min(a.m, a.n * (a.n - 1) // 2)
    edges = set()
    while len(edges) < m:
        u, v = random.sample(range(a.n), 2)
        edges.add((min(u, v), max(u, v)))
    print("n =", a.n)
    print(sorted(edges))
    print("watch for: disconnected components, self-contained cycles, n=1 with no edges")


def gen_intervals(a):
    out = []
    for _ in range(a.n):
        s = random.randint(0, 50)
        out.append([s, s + random.randint(0, 15)])
    out.sort()
    print(out)
    print("touching pair:", [[1, 5], [5, 9]])     # boundary equality, the classic miss


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    ar = sub.add_parser("array")
    ar.add_argument("--n", type=int, default=10)
    ar.add_argument("--lo", type=int, default=-100)
    ar.add_argument("--hi", type=int, default=100)
    ar.add_argument("--sorted", action="store_true")
    ar.add_argument("--unique", action="store_true")
    ar.add_argument("--edges", action="store_true")
    ar.set_defaults(fn=gen_array)

    st = sub.add_parser("string")
    st.add_argument("--n", type=int, default=20)
    st.add_argument("--charset", default="abc")
    st.set_defaults(fn=gen_string)

    tr = sub.add_parser("tree")
    tr.add_argument("--n", type=int, default=15)
    tr.set_defaults(fn=gen_tree)

    gr = sub.add_parser("graph")
    gr.add_argument("--n", type=int, default=6)
    gr.add_argument("--m", type=int, default=8)
    gr.set_defaults(fn=gen_graph)

    iv = sub.add_parser("intervals")
    iv.add_argument("--n", type=int, default=8)
    iv.set_defaults(fn=gen_intervals)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
